# Пара 2 - Docker: образы, Dockerfile, запуск

## Блок 1 - Первый Dockerfile
Создается директория для работы:
```bash
mkdir ~/docker-lab && cd ~/docker-lab
```

Приложение `app.py`, `requirements.txt` и `Dockerfile`, который мы для начало напишем криво косо
```bash
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

Запускаем с помощью `docker build -t myapp:bad .`, проверяем с помощью curl и проверяем вес(видим, что он почти 2 Гига)
<img width="900" height="62" alt="image" src="https://github.com/user-attachments/assets/86f95874-aafc-4259-9e58-bd7a9434a86f" />

<img width="931" height="78" alt="image" src="https://github.com/user-attachments/assets/9a28974d-1949-45a3-869b-68de25d831db" />


**Контрольный вопрос:** Почему образ такой большой?

**Ответ:** Во-первых образ основан на Debian, то есть мы буквально берем системные утилиты, пакетный менеджер, множество дополнителых библиотек. Копируем абсолютно все файлы: временные файлы, папки типа `__pycache__`, служебные директории, логи, бэкапы и прочие данные, не нужные для приложения.

## Блок 2 - Multistage build
Теперь "Хороший Dockerfile" с установкой только нужных пакетов, отключение хэширования(без архивов не нужных для финальной сборки контейнера), с установкой пакетов в каталог пользователя, с использованием Alpine заместо Ubuntu/Debian. С добавление `.dockerignore`, чтобы не собирать в контейнере не нужные файлы + запуск с ограниченными ресурсами

Сравним размеры `myapp:bad` и `myapp:good`
<img width="936" height="102" alt="image" src="https://github.com/user-attachments/assets/1ca81f5e-d7f5-404d-94f3-b9519adf2e59" />


## Блок 3 - Исследование образа
Можно посмотреть слои контейнеров
<img width="938" height="805" alt="image" src="https://github.com/user-attachments/assets/35b50a6c-a920-48a8-8899-da858b815a77" />

<img width="936" height="688" alt="image" src="https://github.com/user-attachments/assets/0ee70f22-24b2-4b14-b4a6-adf210c1cc0b" />


Детальную информацию по `myapp:good`
<img width="731" height="279" alt="image" src="https://github.com/user-attachments/assets/53adf453-b7a6-4f4c-99d2-09c7ff33ca2d" />


## Блок 4 - Docker Hub
Для этого нужно залогинеться `docker login` и опубликовать на docker hub
<img width="919" height="313" alt="image" src="https://github.com/user-attachments/assets/5030d6f4-367f-405e-8709-9db53a050ae6" />

Теперь скачаем образы и запустим
<img width="903" height="254" alt="image" src="https://github.com/user-attachments/assets/ebce0b4c-a68e-448a-8e12-47fbe4095bc8" />


