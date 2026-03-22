# Практические задания: Kubernetes для DevOps

## Введение

**Требуемое ПО:**
- Linux хост (Ubuntu 20.04+) или WSL2
- Docker (20.10+)
- Kubernetes (1.24+) кластер или minikube/kind
- kubectl, kubeadm, kubelet
- Git, curl, vim/nano
- trivy, helm (опционально)

---

## БЛОК 1: КОНТЕЙНЕРЫ 

### Задание 1.1: Создание контейнера с нуля (без Docker) — понимание Linux namespaces и cgroups

**Цель:** Разобраться в том, как Docker работает "под капотом", создав изолированное окружение вручную с помощью Linux primitives.

**Описание задания:**

Вместо использования Docker создадим контейнер вручную, используя:
- **Namespaces** (PID, Network, Mount, UTS, IPC) для логической изоляции
- **cgroups** для ограничения ресурсов
- **chroot** для изоляции файловой системы

Контейнер — это не виртуальная машина, а процесс с ограничениями на уровне ОС.

**Пошаговые инструкции:**

1. **Подготовка базовой файловой системы:**

```bash
# Создаём директорию для контейнера
sudo mkdir -p /containers/manual-container/rootfs
cd /containers/manual-container

# Копируем минимальное окружение (busybox или alpine)
sudo apt-get install -y busybox-static

# Создаём базовую FS
sudo mkdir -p rootfs/bin rootfs/sbin rootfs/lib rootfs/etc rootfs/dev rootfs/proc rootfs/sys
sudo cp /bin/busybox rootfs/bin/
sudo cp /bin/sh rootfs/bin/

# Создаём необходимые device файлы
sudo mknod -m 666 rootfs/dev/null c 1 3
sudo mknod -m 666 rootfs/dev/zero c 1 5
sudo mknod -m 666 rootfs/dev/full c 1 7
sudo mknod -m 644 rootfs/dev/random c 1 8
sudo mknod -m 644 rootfs/dev/urandom c 1 9
sudo mknod -m 666 rootfs/dev/tty c 5 0
sudo mknod -m 666 rootfs/dev/console c 5 1
```

2. **Создание PID namespace изолированного процесса:**

```bash
# Создаём простой скрипт для запуска контейнера
cat > /tmp/run_container.sh << 'EOF'
#!/bin/bash
# Запуск процесса в новых namespaces
sudo unshare \
  --pid --uts --ipc --mount --net \
  --root=/containers/manual-container/rootfs \
  /bin/sh
EOF

chmod +x /tmp/run_container.sh
```

3. **Добавление cgroups для ограничения памяти:**

```bash
# Создаём cgroup для контейнера
sudo cgcreate -g memory:/container_group
sudo cgset -r memory.limit_in_bytes=104857600 /container_group  # 100MB

# Запуск процесса в cgroup
sudo cgexec -g memory:/container_group unshare \
  --pid --uts --ipc --mount \
  --root=/containers/manual-container/rootfs \
  /bin/sh
```

4. **Внутри контейнера проверяем изоляцию:**

```bash
# Команды для выполнения ВНУТРИ контейнера
ps aux          # Видим только процессы контейнера
hostname        # Можно изменить имя контейнера
ip addr         # Видим только сетевые интерфейсы этого namespace
df -h           # Видим файловую систему контейнера
cat /proc/meminfo
```

5. **Из хоста проверяем процессы:**

```bash
# В другом терминале на хосте:
ps aux | grep unshare
# Видим процесс контейнера с отдельным PID в host namespace
```

**Критерии оценки:**
- [ ] Успешно создана изолированная файловая система с busybox
- [ ] PID namespace работает (ps aux показывает только процессы контейнера)
- [ ] Memory cgroup применяется (можно запустить `stress` и проверить ограничение)
- [ ] Имя хоста отличается в контейнере
- [ ] Процесс контейнера виден из host namespace с другим PID

**Подсказки для troubleshooting:**

- **Ошибка "unshare: failed to execute /bin/sh"**: Проверьте, что все файлы скопированы в rootfs, включая зависимости динамических библиотек
  ```bash
  ldd /bin/sh  # Проверить зависимости
  # Скопировать необходимые .so файлы в rootfs/lib
  ```

- **Сетевой интерфейс не видно**: Network namespace создан, но виртуальные интерфейсы не соединены. Это нормально для первого упражнения.

- **cgroups не работают**: Проверьте, что cgroup2 или cgroupsv1 смонтированы:
  ```bash
  mount | grep cgroup
  cat /proc/cgroups
  ```

---

### Задание 1.2: Оптимальный Dockerfile с multistage build

**Цель:** Научиться писать эффективные Dockerfile с минимизацией размера образа и количества слоёв.

**Описание задания:**

Создадим два образа для одного приложения (Python и Go) — сначала неоптимизированный, затем с использованием multistage build.

**Пошаговые инструкции:**

1. **Python приложение (FastAPI):**

```bash
mkdir -p /tmp/docker-practice/python-app
cd /tmp/docker-practice/python-app

cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
EOF

cat > app.py << 'EOF'
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
```

2. **Неоптимальный Dockerfile (для сравнения):**

```bash
cat > Dockerfile.bad << 'EOF'
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY app.py .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0"]
EOF

# Сборка
docker build -f Dockerfile.bad -t python-app:bad .
docker images | grep python-app  # Посмотреть размер (в несколько сотен МБ)
```

3. **Оптимальный Dockerfile с multistage build:**

```bash
cat > Dockerfile << 'EOF'
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .

ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER nobody
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
EOF

# Сборка оптимального образа
docker build -t python-app:optimized .
docker images | grep python-app  # Проверить размер (должен быть меньше)
```

4. **Go приложение:**

```bash
mkdir -p /tmp/docker-practice/go-app
cd /tmp/docker-practice/go-app

cat > main.go << 'EOF'
package main

import (
    "fmt"
    "net/http"
)

func health(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, `{"status":"ok"}`)
}

func hello(w http.ResponseWriter, r *http.Request) {
    name := r.URL.Query().Get("name")
    fmt.Fprintf(w, `{"message":"Hello %s"}`, name)
}

func main() {
    http.HandleFunc("/health", health)
    http.HandleFunc("/hello", hello)
    http.ListenAndServe(":8000", nil)
}
EOF

cat > Dockerfile << 'EOF'
# Stage 1: Builder
FROM golang:1.21-alpine as builder

WORKDIR /app
COPY main.go .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o app main.go

# Stage 2: Runtime
FROM alpine:3.18

RUN adduser -D -u 65534 nobody

WORKDIR /app
COPY --from=builder /app/app .

USER nobody
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1

CMD ["./app"]
EOF

docker build -t go-app:optimized .
docker images | grep go-app
```

5. **Сравнение размеров:**

```bash
docker images | grep -E "python-app|go-app"

# Вывод должен быть примерно:
# python-app    bad          XXXMB
# python-app    optimized    ~300MB
# go-app        optimized    ~50MB
```

**Критерии оценки:**
- [ ] Неоптимальный образ Python больше, чем оптимальный
- [ ] Multistage build использует минимум 2 stage (builder и runtime)
- [ ] Промежуточные слои не включены в финальный образ (проверка через `docker history`)
- [ ] Go образ значительно меньше Python образа
- [ ] Оба образа содержат HEALTHCHECK
- [ ] Оба образа запускают процесс от непривилегированного пользователя

**Подсказки для troubleshooting:**

- **Python образ всё ещё большой**: Убедитесь, что используется `slim` или `alpine` базовый образ, не просто `python:3.11`
  ```bash
  docker image inspect python-app:optimized | grep -A5 "RootFS"
  ```

- **Go приложение не компилируется**: Проверьте версию Go и синтаксис флагов:
  ```bash
  go version
  CGO_ENABLED=0 GOOS=linux go build -help
  ```

---

### Задание 1.3: Сканирование образов на уязвимости (Trivy)

**Цель:** Научиться находить и анализировать CVE уязвимости в Docker образах.

**Описание задания:**

Установим Trivy и просканируем созданные образы на уязвимости, а затем создадим образ с исправленными версиями зависимостей.

**Пошаговые инструкции:**

1. **Установка Trivy:**

```bash
# Скачиваем и устанавливаем
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

trivy version
```

2. **Сканирование созданных образов:**

```bash
# Сканируем Python образ
trivy image python-app:optimized

# Вывод должен быть примерно:
# Total: X vulnerabilities (Y CRITICAL, Z HIGH, ...)
# Layer: sha256:...
```

3. **Детальное сканирование с форматом JSON:**

```bash
trivy image --format json --output scan-report.json python-app:optimized

# Просмотр результатов
cat scan-report.json | jq '.Results[] | select(.Severity=="CRITICAL")'
```

4. **Создание образа с обновлёнными зависимостями:**

```bash
cd /tmp/docker-practice/python-app

cat > requirements-locked.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
EOF

cat > Dockerfile.secure << 'EOF'
FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements-locked.txt .
RUN pip install --user --no-cache-dir -r requirements-locked.txt

COPY app.py .

ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

USER nobody
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
EOF

docker build -f Dockerfile.secure -t python-app:secure .
```

5. **Повторное сканирование:**

```bash
trivy image python-app:secure

# Сравнение с предыдущим результатом
trivy image --severity CRITICAL,HIGH python-app:optimized
trivy image --severity CRITICAL,HIGH python-app:secure
```

6. **Политика сканирования (опционально):**

```bash
# Игнорирование известных false-positive
cat > .trivyignore << 'EOF'
# CVE-2021-12345  # Причина: не влияет на наше приложение
EOF

trivy image --ignorefile .trivyignore python-app:optimized
```

**Критерии оценки:**
- [ ] Trivy установлен и работает
- [ ] Сканирование успешно выполняется для обоих образов
- [ ] JSON отчёт генерируется и содержит информацию о CVE
- [ ] Обновлённый образ имеет меньше или равное количество уязвимостей
- [ ] Фильтрация по severity работает
- [ ] .trivyignore файл создан и использован

**Подсказки для troubleshooting:**

- **Trivy не найден в PATH**: Убедитесь, что установка завершена:
  ```bash
  which trivy
  /usr/local/bin/trivy version
  ```

- **Сканирование занимает слишком долго**: Первый запуск загружает базу CVE. Последующие будут быстрее. Можно использовать кэш:
  ```bash
  trivy image --skip-db-update python-app:optimized
  ```

- **Много UNKNOWN уязвимостей**: Это нормально для alpine образов. Проверьте только CRITICAL и HIGH:
  ```bash
  trivy image --severity CRITICAL,HIGH python-app:optimized
  ```

---

## БЛОК 2: РАЗВЁРТЫВАНИЕ КЛАСТЕРА K8S (2 часа)

### Задание 2.1: Установка кластера Kubernetes через kubeadm

**Цель:** Развернуть production-like Kubernetes кластер с одним master и двумя worker нодами.

**Описание задания:**

Установим K8s кластер с нуля на трёх виртуальных машинах (или контейнерах) используя kubeadm. Это даст понимание архитектуры K8s и процесса инициализации.

**Требования к окружению:**

- 3 ВМ (или bare metal): master (2CPU, 2GB RAM), worker1 (2CPU, 2GB), worker2 (2CPU, 2GB)
- Ubuntu 20.04 LTS или новее
- Docker или containerd установлены
- Сетевой доступ между ВМ

**Альтернатива для локальной работы:** Используйте `kind` или `minikube` с этими же инструкциями (адаптированными).

**Пошаговые инструкции:**

1. **На всех нодах: подготовка системы:**

```bash
# Обновляем систему (на всех трёх машинах)
sudo apt-get update
sudo apt-get upgrade -y

# Отключаем swap (K8s требует это)
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab

# Включаем модули ядра для networking
cat << EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# Сетевые параметры
cat << EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
EOF

sudo sysctl --system
```

2. **Установка Docker (на всех нодах):**

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавляем текущего пользователя в группу docker
sudo usermod -aG docker $USER

# Проверяем
docker --version
docker run hello-world
```

3. **Установка kubeadm, kubelet, kubectl (на всех нодах):**

```bash
# Добавляем репозиторий K8s
sudo apt-get install -y apt-transport-https ca-certificates curl
curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Устанавливаем K8s компоненты
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl

# Зависит версия версии (например 1.27.x)
# sudo apt-get install -y kubelet=1.27.0-00 kubeadm=1.27.0-00 kubectl=1.27.0-00

sudo apt-mark hold kubelet kubeadm kubectl

# Проверяем версии
kubeadm version
kubelet --version
kubectl version --client
```

4. **Инициализация Master ноды:**

```bash
# На MASTER машине:
# Получаем IP адрес master (например 192.168.1.10)
hostname -I

# Инициализируем кластер
sudo kubeadm init \
  --apiserver-advertise-address=192.168.1.10 \
  --pod-network-cidr=10.244.0.0/16 \
  --kubernetes-version=stable-1

# Вывод будет содержать команду для join worker нод (СОХРАНИТЕ ЭТО!)
# Например: kubeadm join 192.168.1.10:6443 --token ... --discovery-token-ca-cert-hash ...
```

5. **Настройка kubeconfig (на master):**

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Проверяем
kubectl get nodes  # Должен показать master в статусе NotReady (без CNI)
```

6. **Установка CNI — Flannel:**

```bash
# На master:
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml

# Ждём пока Flannel pods запустятся
kubectl get pods -n kube-flannel --watch

# После этого master должен перейти в Ready
kubectl get nodes  # Status should be "Ready"
```

7. **Присоединение Worker нод:**

```bash
# На каждой worker машине выполняем команду из пункта 4:
sudo kubeadm join 192.168.1.10:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>

# Проверяем на master:
kubectl get nodes  # Должны показаться все 3 ноды в Ready
```

8. **Финальная проверка:**

```bash
# На master:
kubectl get nodes -o wide
kubectl get pods --all-namespaces
kubectl cluster-info

# Должны увидеть:
# - 3 ноды в статусе Ready
# - kube-system pods запущены
# - flannel pods в каждом node
```

**Критерии оценки:**
- [ ] 3 ноды в кластере с статусом Ready
- [ ] `kubectl get nodes` показывает все ноды
- [ ] Все pods в kube-system namespace Running
- [ ] kubeconfig сконфигурирован и работает без sudo
- [ ] Flannel (или другой CNI) установлен
- [ ] Можно запустить простой контейнер: `kubectl run nginx --image=nginx`

**Подсказки для troubleshooting:**

- **Master в статусе NotReady**: Ждите, пока установится CNI плагин
  ```bash
  kubectl get pods -n kube-flannel
  kubectl logs -n kube-flannel <pod-name>
  ```

- **kubeadm join не работает**: Проверьте token на master:
  ```bash
  kubeadm token list
  kubeadm token create --print-join-command
  ```

- **Сетевые проблемы между нодами**: Проверьте firewall и маршруты:
  ```bash
  sudo iptables -L -n
  ip route
  ping <other-node-ip>
  ```

---

### Задание 2.2: Установка CNI и проверка сетевого взаимодействия

**Цель:** Разобраться в том, как работает сетевое взаимодействие в K8s и конфигурировать различные CNI плагины.

**Описание задания:**

Установим несколько CNI плагинов (Flannel, Calico), поймём их различия и проверим сетевую связность.

**Пошаговые инструкции:**

1. **Если Flannel уже установлен — удалим для чистого примера:**

```bash
kubectl delete -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
kubectl get pods -n kube-flannel --watch  # Ждём удаления
```

2. **Установка Calico (альтернатива Flannel с NetworkPolicy):**

```bash
# Скачиваем манифесты Calico
curl https://raw.githubusercontent.com/projectcalico/calico/v3.26.0/manifests/tigera-operator.yaml -o tigera-operator.yaml

# Устанавливаем operator
kubectl apply -f tigera-operator.yaml

# Проверяем установку
kubectl get pods -n tigera-operator --watch

# Создаём Calico Installation манифест
cat << 'EOF' | kubectl apply -f -
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    ipPools:
    - name: default-ipv4-ippool
      blockSize: 26
      cidr: 10.244.0.0/16
      encapsulation: vxlan
      natOutgoing: Enabled
EOF

# Ждём пока ноды перейдут в Ready
kubectl get nodes --watch
```

3. **Проверка сетевых параметров:**

```bash
# На каждой ноде проверяем IP адреса
kubectl get nodes -o wide

# На worker ноде проверяем IP адреса интерфейсов
ip addr show
ip route show

# Проверяем tunl0 интерфейс (для vxlan)
ip link show
```

4. **Тестирование сетевой связности между pods:**

```bash
# Запускаем test pods в разных нодах
kubectl run test-pod-1 --image=nicolaka/netshoot -it -- bash
# (В другом терминале)
kubectl run test-pod-2 --image=nicolaka/netshoot -it -- bash

# Внутри первого pod:
kubectl exec -it test-pod-1 -- ping test-pod-2
kubectl exec -it test-pod-1 -- nslookup test-pod-2

# Должна быть связность между pods на разных нодах
```

5. **Проверка DNS разрешения:**

```bash
# Запускаем pod и проверяем DNS
kubectl run -it --rm debug --image=nicolaka/netshoot --restart=Never -- bash

# Внутри pod:
nslookup kubernetes.default
nslookup kube-dns.kube-system

# Проверяем /etc/resolv.conf
cat /etc/resolv.conf
```

6. **Сравнение CNI плагинов (таблица в конце задания):**

```bash
# Информация о установленном CNI
kubectl get daemonset -n kube-system
kubectl logs -n kube-system <cni-pod> --tail=50
```

**Таблица сравнения CNI плагинов:**

| Параметр | Flannel | Calico | Cilium |
|----------|---------|--------|--------|
| **Сложность** | Простой | Средняя | Сложная |
| **Performance** | Хороший | Отличный | Отличный |
| **NetworkPolicy** | Нет | Да | Да |
| **eBPF** | Нет | Опционально | Да (core) |
| **Encapsulation** | VXLAN/UDP | VXLAN/IPIP | Нативный |
| **Production Ready** | Да | Да | Да |

**Критерии оценки:**
- [ ] CNI плагин успешно установлен (Flannel или Calico)
- [ ] Все ноды в статусе Ready
- [ ] Pods могут коммуницировать между нодами
- [ ] DNS разрешение работает для pods
- [ ] Можно проверить logs CNI daemon set
- [ ] Понимание различий между плагинами

**Подсказки для troubleshooting:**

- **Ноды остаются в NotReady**: Проверьте лог kubelet:
  ```bash
  sudo journalctl -u kubelet -n 50
  ```

- **Pods не видят друг друга**: Проверьте сетевые политики и firewall:
  ```bash
  kubectl get networkpolicies --all-namespaces
  sudo iptables -L -n | grep FORWARD
  ```

- **Calico pods не запускаются**: Проверьте логи оператора:
  ```bash
  kubectl logs -n tigera-operator <pod-name>
  kubectl describe pod -n tigera-operator <pod-name>
  ```

---

### Задание 2.3: Диагностика и troubleshooting кластера

**Цель:** Научиться диагностировать и исправлять типичные проблемы в K8s кластере.

**Описание задания:**

Сценарии диагностики и исправления проблем, которые встречаются на production системах.

**Пошаговые инструкции:**

1. **Сценарий 1: Pod не запускается**

```bash
# Создаём pod с ошибкой
cat << 'EOF' | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: broken-pod
spec:
  containers:
  - name: app
    image: ubuntu:20.04
    command: ["sh", "-c", "sleep 1 && exit 1"]
EOF

# Диагностирование
kubectl get pods  # Статус CrashLoopBackOff
kubectl describe pod broken-pod
kubectl logs broken-pod  # Пусто или ошибка
kubectl logs broken-pod --previous  # Логи предыдущего контейнера

# Исправление
kubectl delete pod broken-pod
```

2. **Сценарий 2: Недостаточно ресурсов**

```bash
# Создаём pod с большим request
cat << 'EOF' | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: resource-hog
spec:
  containers:
  - name: app
    image: nginx
    resources:
      requests:
        memory: "10Gi"
        cpu: "100"
EOF

# Диагностирование
kubectl describe pod resource-hog  # Status: Pending
kubectl describe node worker1  # Allocated Resources

# Исправление
kubectl delete pod resource-hog

# Смотрим доступные ресурсы
kubectl top nodes
kubectl top pods --all-namespaces
```

3. **Сценарий 3: Проблемы с сетевой связностью**

```bash
# Проверяем кластерную сеть
kubectl get nodes -o wide
kubectl get pods -o wide --all-namespaces

# Диагностирование на ноде
ssh worker1

# На ноде:
docker ps  # Видим контейнеры pods
ip netns list  # Видим network namespaces
ip netns exec <namespace> ip addr  # IP адреса внутри pod

# Проверяем маршруты
ip route show
sudo iptables -t filter -L -n | head -30
```

4. **Сценарий 4: Проблемы с волюмами**

```bash
# Создаём pod с несуществующим волюмом
cat << 'EOF' | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: volume-error
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: non-existent-pvc
EOF

# Диагностирование
kubectl describe pod volume-error
kubectl get pvc  # PVC не существует

# Проверяем доступные storage classes
kubectl get storageclass
kubectl get pv

# Исправление
kubectl delete pod volume-error
```

5. **Сценарий 5: Проблемы с RBAC доступом**

```bash
# Создаём сервис аккаунт без прав
kubectl create serviceaccount limited-user
kubectl create rolebinding limited-role --clusterrole=view --serviceaccount=default:limited-user

# Проверяем права
kubectl auth can-i get pods --as=system:serviceaccount:default:limited-user
kubectl auth can-i create pods --as=system:serviceaccount:default:limited-user  # Должен быть no

# Добавляем права
kubectl create rolebinding edit-role --clusterrole=edit --serviceaccount=default:limited-user
kubectl auth can-i create pods --as=system:serviceaccount:default:limited-user  # Должен быть yes
```

6. **Сценарий 6: API Server недоступен**

```bash
# Проверяем состояние компонентов
kubectl get componentstatuses
kubectl get nodes

# Если API недоступен, смотрим логи на master
ssh master
sudo journalctl -u kubelet -n 100
docker logs <api-server-container>

# Проверяем сертификаты (часто истекают)
sudo kubeadm certs check-expiration
sudo kubeadm certs renew all  # Если нужно продлить
```

7. **Утилита для диагностики — kubectl-debug:**

```bash
# Установка (опционально)
kubectl krew install debug

# Подключение к работающему pod'у для отладки
kubectl debug -it <pod-name> --image=nicolaka/netshoot -- bash

# Это создаёт ephemeral container в pod'е
```

**Критерии оценки:**
- [ ] Успешно диагностированы все 6 сценариев
- [ ] Использованы kubectl describe, logs, top команды
- [ ] Смотрели статус компонентов кластера
- [ ] Проверили ресурсы на нодах
- [ ] Успешно исправлены все проблемы

**Подсказки для troubleshooting:**

- **Не видны логи pod'а**: Проверьте, есть ли контейнер вообще:
  ```bash
  kubectl get pod -o jsonpath='{.status.containerStatuses}' <pod-name>
  ```

- **Ноды недоступны**: Проверьте сетевую связность:
  ```bash
  ping <node-ip>
  ssh -v <node>
  sudo systemctl status kubelet
  ```

- **Неустранимые ошибки**: Пересоздайте кластер через kubeadm:
  ```bash
  sudo kubeadm reset
  # Заново инициализируем
  ```
