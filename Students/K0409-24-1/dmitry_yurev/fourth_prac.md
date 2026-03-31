# Kub init
## 1. Состояние кластера
Для прросмотра всех нод выполняется команда `kubectl get nodes -o wide`
![alt text](imgs/4/Screenshot2026-03-26at12.36.10.png)

Для просмотра информации об конкретной ноде выполняется команда `kubectl describe node <имя-ноды> | head -50`
![alt text](imgs/4/Screenshot2026-03-26at12.36.22.png)

Команда `kubectl get pods -n kube-system` выводящая список и статус подов (минимальных единиц kubernetes)
![alt text](imgs/4/Screenshot2026-03-26at12.36.45.png)

`kubectl get componentstatuses` выводит список и статус компонентов управления
![alt text](imgs/4/Screenshot2026-03-26at12.37.01.png)

Внутри контейнера выполняется команда `ls /etc/kubernetes/manifests/`. Она выводит основные конфигурационные файлы kubernetes
![alt text](imgs/4/Screenshot2026-03-26at12.39.51.png)

`cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep -A5 -e "- --"`  выводит содержание конфигурационного файла `kube-apiserver.yaml`, в нем содержится конфигурация статического пода, используемого для запуска API сервера
![alt text](imgs/4/Screenshot2026-03-26at12.42.40.png)

`kubectl api-resources | head -20` выводит первые 20 доступных api
![alt text](imgs/4/Screenshot2026-03-26at12.44.11.png)

команда `kubectl version` выводит версию kubectl и сервера kubernetes
![Screenshot2026-03-26at12.45.39.png](imgs/4/Screenshot2026-03-26at12.45.39.png)

## 2. Первый Pod
Команда `kubectl run nginx --image=nginx:alpine --port=80` запускает контейнер с образом nginx:alpine и портом 80
![Screenshot2026-03-26at12.46.49.png](imgs/4/Screenshot2026-03-26at12.46.49.png)

Команда `kubectl get pods -o wide` выводит список подов, запущенный под работает на ноде minikube
![Screenshot2026-03-26at12.47.30.png](imgs/4/Screenshot2026-03-26at12.47.30.png)

Для отслеживания в реальном времени используется команда `kubectl get pods -w`
![Screenshot2026-03-26at12.48.03.png](imgs/4/Screenshot2026-03-26at12.48.03.png)

Для откртия терминла запущенного контейнера используется команда `kubectl exec -it nginx -- sh`. Внутри контейнера команда `hostname` выводит имя ноды, `cat /etc/hosts` ip пода и dns, `env | grep KUBE` выводит переменные окружения содержащие в названии KUBE, `ps aux` выводит процессы внутри контейнера
![Screenshot2026-03-26at13.02.15.png](imgs/4/Screenshot2026-03-26at13.02.15.png)

`kubectl logs nginx -f` выводит логи указанного контейнера в реальном времени
![Screenshot2026-03-26at13.04.35.png](imgs/4/Screenshot2026-03-26at13.04.35.png)

`kubectl describe pod nginx` выводит описание пода
![Screenshot2026-03-26at13.05.05.png](imgs/4/Screenshot2026-03-26at13.05.05.png)

## 3. Pod через YAML

В файл `pod.yaml` записывается конфигурация
![Screenshot2026-03-26at13.07.22.png](imgs/4/Screenshot2026-03-26at13.07.22.png)

`kubectl apply -f pod.yaml` создает и запускает под используя созданную конфигурацию, команда `kubectl get pods -w` проверяет, запустился он или нет(он запустился)
![Screenshot2026-03-26at13.08.03.png](imgs/4/Screenshot2026-03-26at13.08.03.png)

``
![Screenshot2026-03-26at13.09.19.png](imgs/4/Screenshot2026-03-26at13.09.19.png)

Для просмотра логов из конкретного контейнера используется команда `kubectl logs my-webserver -c log-sidecar`, для входа в конкретный контейнер используется команда `kubectl exec -it my-webserver -c nginx -- sh`
![Screenshot2026-03-26at13.14.29.png](imgs/4/Screenshot2026-03-26at13.14.29.png)

`kubectl get pod my-webserver -o yaml | head -60` используется для вывода yaml для конкретного контейнера
![Screenshot2026-03-26at13.15.22.png](imgs/4/Screenshot2026-03-26at13.15.22.png)

## 4. Самовосстановление
Командой `kubectl exec my-webserver -c nginx -- kill 1` убивается процесс,  kubernetes его сам перезапускает, это проверяется командами `kubectl get pods -w` и `kubectl get pod my-webserver`
![Screenshot2026-03-26at13.16.52.png](imgs/4/Screenshot2026-03-26at13.16.52.png)
