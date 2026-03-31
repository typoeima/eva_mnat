# Безопасность Kubernetes: RBAC, NetworkPolicy, Falco
## 1. RBAC

создается namespace
![Screenshot2026-03-30at02.16.22.png](imgs/7/Screenshot2026-03-30at02.16.22.png)

создается конфигурационный файл. В него записывается конфигураци для разделения прав доступа
![Screenshot2026-03-30at02.17.33.png](imgs/7/Screenshot2026-03-30at02.17.33.png)

запускается
![Screenshot2026-03-30at02.17.48.png](imgs/7/Screenshot2026-03-30at02.17.48.png)

проверка прав доступа на чтение внутри namespace
![Screenshot2026-03-30at02.18.00.png](imgs/7/Screenshot2026-03-30at02.18.00.png)

проверка прав на запись внутри namespace
![Screenshot2026-03-30at02.18.09.png](imgs/7/Screenshot2026-03-30at02.18.09.png)

проверка прав на чтение в другом namespace ( таких прав нет)
![Screenshot2026-03-30at02.18.27.png](imgs/7/Screenshot2026-03-30at02.18.27.png)

создается под, к которому будт применены созданные права
![Screenshot2026-03-30at02.19.37.png](imgs/7/Screenshot2026-03-30at02.19.37.png)

запускается
![Screenshot2026-03-30at02.19.50.png](imgs/7/Screenshot2026-03-30at02.19.50.png)

ограничения работают как надо: нельзя удалять поды и просматривать другие namespace
![Screenshot2026-03-30at02.20.27.png](imgs/7/Screenshot2026-03-30at02.20.27.png)

## 2. NetworkPolicy

создается еще один namespace
![Screenshot2026-03-30at02.20.43.png](imgs/7/Screenshot2026-03-30at02.20.43.png)

запускается контейнер на основе образа nginx:alpine с ролью фронтенд (нужно для примения политик), для него создается сервис для сетевого доступа
![Screenshot2026-03-30at02.20.54.png](imgs/7/Screenshot2026-03-30at02.20.54.png)
![Screenshot2026-03-30at02.21.03.png](imgs/7/Screenshot2026-03-30at02.21.03.png)

то же самое для бэкенда, но с другой ролью и названием
![Screenshot2026-03-30at02.21.20.png](imgs/7/Screenshot2026-03-30at02.21.20.png)

то же самое для бд
![alt text](imgs/7/Screenshot2026-03-30at02.22.29.png)

проверка что от фронтенда можно отправить запрос к бэкенду, все работает
![Screenshot2026-03-30at02.22.42.png](imgs/7/Screenshot2026-03-30at02.22.42.png)

запрос от фронтенда к бд, работает, но это плохо
![Screenshot2026-03-30at02.22.52.png](imgs/7/Screenshot2026-03-30at02.22.52.png)

конфиг для сетевой политики
![Screenshot2026-03-30at02.23.20.png](imgs/7/Screenshot2026-03-30at02.23.20.png)

применеие
![Screenshot2026-03-30at02.24.47.png](imgs/7/Screenshot2026-03-30at02.24.47.png)

запрос от фронтенда к бэкенду, все работает
![Screenshot2026-03-30at02.25.02.png](imgs/7/Screenshot2026-03-30at02.25.02.png)

от фронтенда к бд, все работает, хотя не должно. Для того что бы работало надо было запускать minikube с флагом `--cni=calico`, это плагин для применения сетевых политик, без него k8s не умеет применять их
![Screenshot2026-03-30at02.25.56.png](imgs/7/Screenshot2026-03-30at02.25.56.png)

от бэкенда до бд работает, как и должно(если бы и не должно было, все равно работало бы по той же причине)
![Screenshot2026-03-30at02.26.16.png](imgs/7/Screenshot2026-03-30at02.26.16.png)

список сетевых политик
![Screenshot2026-03-30at02.42.37.png](imgs/7/Screenshot2026-03-30at02.42.37.png)

## 3. TLS Сертификаты с OpenSSL

генерируется приватный ключ CA
![Screenshot2026-03-30at02.43.20.png](imgs/7/Screenshot2026-03-30at02.43.20.png)

создается сертификат и подаисывается созданным ключем
![Screenshot2026-03-30at02.43.26.png](imgs/7/Screenshot2026-03-30at02.43.26.png)

просмотр свойств сертификата, все как надо
![Screenshot2026-03-30at02.43.49.png](imgs/7/Screenshot2026-03-30at02.43.49.png)

создается файл для того что бы дальше подписать сертификат 
![Screenshot2026-03-30at02.44.29.png](imgs/7/Screenshot2026-03-30at02.44.29.png)

генерируется ключ сервера
![Screenshot2026-03-30at02.44.35.png](imgs/7/Screenshot2026-03-30at02.44.35.png)

создание запроса на подпись сертификата 
![Screenshot2026-03-30at02.44.42.png](imgs/7/Screenshot2026-03-30at02.44.42.png)

проверка содержимого созданного запроса
![Screenshot2026-03-30at02.44.47.png](imgs/7/Screenshot2026-03-30at02.44.47.png)

подпись сертификата с применение правил из `webapp.ext`
![Screenshot2026-03-30at02.45.29.png](imgs/7/Screenshot2026-03-30at02.45.29.png)

проверка того что сертификат подписан и для каких доменов/адресов
![Screenshot2026-03-30at02.45.36.png](imgs/7/Screenshot2026-03-30at02.45.36.png)

проверка цепочки доверия
![Screenshot2026-03-30at02.45.43.png](imgs/7/Screenshot2026-03-30at02.45.43.png)

создается secret, куда записываются ключ и сертификат
![Screenshot2026-03-30at02.45.56.png](imgs/7/Screenshot2026-03-30at02.45.56.png)

проверка создания secret
![Screenshot2026-03-30at02.46.06.png](imgs/7/Screenshot2026-03-30at02.46.06.png)

описание созданного secret
![Screenshot2026-03-30at02.46.18.png](imgs/7/Screenshot2026-03-30at02.46.18.png)

создание конфига с указанием созданного secret
![Screenshot2026-03-30at02.46.39.png](imgs/7/Screenshot2026-03-30at02.46.39.png)

запуск контейнера на основе конфига
![Screenshot2026-03-30at02.48.45.png](imgs/7/Screenshot2026-03-30at02.48.45.png)

проверка соединения с CA
![Screenshot2026-03-30at02.54.48.png](imgs/7/Screenshot2026-03-30at02.54.48.png)

проверка сертификата, все нормально
![Screenshot2026-03-30at02.55.14.png](imgs/7/Screenshot2026-03-30at02.55.14.png)


![Screenshot2026-03-30at02.55.29.png](imgs/7/Screenshot2026-03-30at02.55.29.png)
![Screenshot2026-03-30at02.55.41.png](imgs/7/Screenshot2026-03-30at02.55.41.png)
