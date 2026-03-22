# SiriusK8s — Практика по Kubernetes и контейнеризации

Учебная практика по технологиям виртуализации: от Linux namespaces и Docker до Kubernetes.

## Структура репозитория

```
.
├── README.md                  # Этот файл — обзор практики
├── PRACTIC/                   # Материалы для практических занятий (7 пар)
│   ├── README.md              # Расписание и сводка по парам
│   ├── 1_Linux/               # Пара 1: Linux — namespaces, cgroups, chroot
│   ├── 2_Docker_run/          # Пара 2: Docker — образы, Dockerfile, контейнеры
│   ├── 3_Docker_net_vol/      # Пара 3: Docker — сети, volumes, docker-compose
│   ├── 4_Kub_init/            # Пара 4: Kubernetes — установка, первые поды
│   ├── 5_Kub_deploy/          # Пара 5: Deployment, Service, Ingress
│   ├── 6_Kub_config/          # Пара 6: ConfigMap, Secret, PV/PVC
│   └── 7_kub_security/        # Пара 7: RBAC, NetworkPolicy, Falco
├── Students/                  # Списки групп и приём работ
│   ├── README.md              # Инструкция по сдаче работ
│   ├── K0109-23/              # Группа K0109-23
│   ├── K0409-24-1/            # Группа K0409-24-1
│   ├── K0409-24-2/            # Группа K0409-24-2
│   └── K0609-23/              # Группа K0609-23
├── docker/                    # Дополнительная практика: безопасность Docker
│   └── README.md              # Взлом и защита контейнеров
├── PRACTICAL_ASSIGNMENTS.md   # Подробные задания с критериями оценки
├── CHEATSHEET.md              # Краткий справочник по kubectl
└── RESOURCES.md               # Ссылки на документацию и подготовку к CKA/CKAD
```

---

## 7 пар практики

| Пара | Тема |
|------|------|
| 1 | Linux: namespaces, cgroups, chroot — основы контейнеризации |
| 2 | Docker: образы, Dockerfile, запуск контейнеров |
| 3 | Docker: сети, volumes, docker-compose |
| 4 | Kubernetes: установка кластера, первые поды |
| 5 | Kubernetes: Deployment, Service, Ingress |
| 6 | Kubernetes: ConfigMap, Secret, PV/PVC |
| 7 | Безопасность: RBAC, NetworkPolicy, Falco |

---

## Группы

| Группа | Расписание (23–27 марта 2026) |
|--------|------------------------------|
| K0409-24-1 | пн 5-я, ср 4-я, чт 3-я |
| K0409-24-2 | вт 5-я, ср 5-я, чт 5-я |
| K0609-23 | пт 3-я |
| K0109-23 | чт 4-я |

Списки студентов и отметки о сдаче — в папках [`Students/K0109-23`](Students/K0109-23/), [`Students/K0409-24-1`](Students/K0409-24-1/), [`Students/K0409-24-2`](Students/K0409-24-2/), [`Students/K0609-23`](Students/K0609-23/).

---

## Сдача работ

Формат ветки и папок: **`<номер_группы>/Фамилия`**  
Пример: `K0109-23/ivanov`

- **Practic/** — основные задания по парам (`1_kub_intro`, `2_kub_deployment`, …)
- **Extra/** — дополнительные задания

Подробная инструкция: [Students/README.md](Students/README.md)

Сдача через **pull request** в ветку `main`.

---

## Дополнительные материалы

| Файл | Описание |
|------|----------|
| [PRACTICAL_ASSIGNMENTS.md](PRACTICAL_ASSIGNMENTS.md) | Подробные задания с критериями оценки |
| [CHEATSHEET.md](CHEATSHEET.md) | Справочник по kubectl и Kubernetes |
| [RESOURCES.md](RESOURCES.md) | Документация, CKA/CKAD, инструменты |
| [docker/README.md](docker/README.md) | Практика по безопасности Docker-контейнеров |
