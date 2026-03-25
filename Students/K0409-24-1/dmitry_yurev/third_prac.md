# Docker, net, vol
## Docker networking
![alt text](imgs/3/Screenshot2026-03-25at14.47.14.png)\
просмотр всех всех сетей 

![alt text](imgs/3/Screenshot2026-03-25at14.47.16.png)\
просмотр конфигурации интерфейса bridge

командой `docker network create --driver bridge app-network` создается новая сеть
![alt text](imgs/3/Screenshot2026-03-25at18.59.37.png)\
запуск образа с подключением к созданной сети

запукается два образа (на скрине одного не видно), подключнные к одной сети
![alt text](imgs/3/Screenshot2026-03-25at19.01.06.png)\
из второго проверяем доступ к первому, она есть.

![alt text](imgs/3/Screenshot2026-03-25at19.09.19.png)
если запустить образ без подключения к сети, то он не будет иметь связи с другими образами

## 2. Volumes и persistent data
![alt text](imgs/3/Screenshot2026-03-25at19.14.51.png)\
создается volume, для того что бы после остановки образа данные не пропадли

![alt text](imgs/3/Screenshot2026-03-25at19.15.01.png)\
запускается образ с подключением к базе данных и volume, куда будут записываться данные в бд.

командой `docker exec -it postgres-persistent psql -U user -d mydb -c \ "CREATE TABLE items (id SERIAL, name TEXT); INSERT INTO items VALUES (1, 'test');"` данные вставляются в бд

![alt text](imgs/3/Screenshot2026-03-25at19.23.54.png)\
обрза удаляется

![alt text](imgs/3/Screenshot2026-03-25at19.24.24.png)\
образ запускается заново и проверяется доступность данных, они доступны.

![alt text](imgs/3/Screenshot2026-03-25at19.25.19.png)\
проверка, где лежит volume

## 3. docker-compose

![alt text](imgs/3/Screenshot2026-03-25at19.26.55.png)\
создается директория для работы

![alt text](imgs/3/Screenshot2026-03-25at19.27.41.png)\
создается прилоежние на питоне

![alt text](imgs/3/Screenshot2026-03-25at19.28.24.png)\
requirements.txt

![alt text](imgs/3/Screenshot2026-03-26at00.17.44.png)\
dockerfile

![alt text](imgs/3/Screenshot2026-03-26at00.19.20.png)\
nginx conf 

![alt text](imgs/3/Screenshot2026-03-26at00.22.50.png)\
docker-compose.yml

![alt text](imgs/3/Screenshot2026-03-25at19.46.38.png)\
запускается весь стек docker compose

![alt text](imgs/3/Screenshot2026-03-25at19.47.22.png)\
просмотр запущенных компонентов 

![alt text](imgs/3/Screenshot2026-03-25at19.47.32.png)\
логи

![alt text](imgs/3/Screenshot2026-03-25at19.49.48.png)\
создаются данные в бд и проверяется работа всех компонентов ( frontend > backend > db)

![alt text](imgs/3/Screenshot2026-03-25at19.51.08.png)\
запускается 3 бэкенда вместо одного

после этого завершаем стек комнадой `docker compose down`

## 4. Итог

![alt text](imgs/3/Screenshot2026-03-25at19.52.44.png)\
проверка созданнх volume

![alt text](imgs/3/Screenshot2026-03-25at19.53.33.png)\
удаление всего