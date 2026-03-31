# 5. Kubernetes: Deployment, Service, Ingress
## 1. Deployment
![alt text](imgs/5/Screenshot2026-03-29at18.41.36.png)
в конфигурационный файл для контейнера записывается конфигурация

![alt text](imgs/5/Screenshot2026-03-29at18.51.35.png)
запускается служба minikube

![alt text](imgs/5/Screenshot2026-03-29at18.51.55.png)
запускается контейнер с использованием созданного конфиграционного файла

![alt text](imgs/5/Screenshot2026-03-29at18.53.07.png)
командой `kubectl get pods -w` выводится список подов, видно что созданы 3 новых

![alt text](imgs/5/Screenshot2026-03-29at18.53.30.png)
проверяется статус деплоймента. вывод в теминале показывает что приложение успешно развернуто

![alt text](imgs/5/Screenshot2026-03-29at18.53.53.png)
команда `kubectl get rs` выводит все реплики

## 2. Service + Rolling Update
![alt text](imgs/5/Screenshot2026-03-29at18.55.27.png)
новый конфиг для контейнера

![alt text](imgs/5/Screenshot2026-03-29at18.55.49.png)
запуск контейнера

![alt text](imgs/5/Screenshot2026-03-29at20.31.22.png)
тк на макос kubernetes работает не на хосте и используя виртуализацию, то по обычному ip не получится отправлять запросы. Для того что бы это сделать выполняется команда `service webapp-svc --url`, которая выводит локалхост с портом для доступа к контейнеру

![alt text](imgs/5/Screenshot2026-03-29at20.31.47.png)
выполняется команда `while true; do curl -s 127.0.0.1:65075 | grep -i "Server&nbsp;name"; sleep 0.5; done`. В выводе видно что все ответы приходят от серверов с разными именами, значит что трафик идет через разные(все) поды

![alt text](imgs/5/Screenshot2026-03-29at20.32.25.png)
командой `kubectl set image deployment/webapp webapp=nginxdemos/hello:latest` выполняется rolling update, он проходит нормально

![alt text](imgs/5/Screenshot2026-03-29at20.32.48.png)
статус обновления: все нормально

![alt text](imgs/5/Screenshot2026-03-29at20.33.40.png)
вся история контейнера, всего было 2 состояния: первоначальное и после обнолвения

![alt text](imgs/5/Screenshot2026-03-29at20.34.44.png)
откат обнолвения

![alt text](imgs/5/Screenshot2026-03-29at20.34.51.png)
статус отката, все нормально

![alt text](imgs/5/Screenshot2026-03-29at23.04.54.png)
после откта первое состояние пропало, так как оно было копией третьего и не нужно

## 3. Ingress

![alt text](imgs/5/Screenshot2026-03-29at20.38.44.png)
создается новый контейнер на основе образа, которое возвращает указанный текст по api

![alt text](imgs/5/Screenshot2026-03-29at20.38.56.png)
создается служба для перенаправления трафика по названию пода на его ip, так как при перезапуске пода у него меняется ip адрес, для решения этой проблемы можно использовать такой способ

![alt text](imgs/5/Screenshot2026-03-29at20.39.31.png)
новый конфиг


![alt text](imgs/5/Screenshot2026-03-29at20.40.31.png)
запуск контейнера с помощью конфига

![alt text](imgs/5/Screenshot2026-03-29at20.40.35.png)
список ingress правил, описанных в конфиге

![alt text](imgs/5/Screenshot2026-03-29at20.44.26.png)
тк на макос оно работает через виртуализацию сначала создается тунель

![alt text](imgs/5/Screenshot2026-03-29at20.44.55.png)
далее в `/etc/hosts` записывается 127.0.0.1 webapp.local для перенаправления трафика на контейнер

![alt text](imgs/5/Screenshot2026-03-29at20.46.57.png)
выполняются запросы к домену, обращение к просто домену возвращает информацию о сервере, обращение к апи – то что должно возвращать апи

![alt text](imgs/5/Screenshot2026-03-29at20.47.27.png)
список ingress-controller подов

## 4. Сравнение типов Service

![alt text](imgs/5/Screenshot2026-03-29at20.47.46.png)
создается новый сервис, но уже с ip доступным только внутри кластера

![alt text](imgs/5/Screenshot2026-03-29at20.48.37.png)
видно, что внешнего ip нет

![alt text](imgs/5/Screenshot2026-03-29at20.52.24.png)
внутри кластера ip адрес есть

![alt text](imgs/5/Screenshot2026-03-29at20.54.27.png)
работает с nodeport и порте 30080