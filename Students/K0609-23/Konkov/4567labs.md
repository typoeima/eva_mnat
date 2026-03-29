# 4 Лабораторная:

1. Чему научился:

В ходе выполнения лабораторной работы был получен базовый практический опыт работы с Kubernetes-кластером.
Понял как подключаться к контейнеру, и что там можно увидеть. Понял, что кубернетис при принудительном завершении процесса - перезагружается. И в целом, понял зачем Pod нужен.

2. Возникшие проблемы и способы их решения

Основная проблема с тем, что я делал с ks3, а много команд написаны под minikube. и переодически я просто не понимал почему у меня не запускается что-то.

<img width="1173" height="532" alt="image" src="https://github.com/user-attachments/assets/840627db-894d-47dd-8c69-b22eba18231e" />
<img width="1280" height="738" alt="image" src="https://github.com/user-attachments/assets/fee1149d-215c-4ab7-9b66-3fb50b20e049" />
<img width="964" height="389" alt="image" src="https://github.com/user-attachments/assets/ec1317b8-d59d-4056-9c63-15cbf55545ff" />
<img width="1280" height="444" alt="image" src="https://github.com/user-attachments/assets/bb5198a1-947f-41b1-b148-0c7c0e2859b2" />
<img width="359" height="166" alt="image" src="https://github.com/user-attachments/assets/52b5a872-1595-4674-9c76-d8f7c83e03e8" />


<img width="1174" height="386" alt="image" src="https://github.com/user-attachments/assets/b261e918-57ab-4393-b634-93828d81ad7f" />
<img width="1245" height="1011" alt="image" src="https://github.com/user-attachments/assets/b18c8baa-1231-453e-b41b-ac9ebab501ea" />
<img width="1056" height="642" alt="image" src="https://github.com/user-attachments/assets/cd9434bc-b4f4-4bb4-9b62-5c5f270ca9e4" />
<img width="1280" height="980" alt="image" src="https://github.com/user-attachments/assets/aed79293-8e59-49c9-8243-68fd15514d0d" />


<img width="1280" height="980" alt="image" src="https://github.com/user-attachments/assets/09a2ba42-6328-4290-ba6a-8e81ba33ff21" />
<img width="910" height="483" alt="image" src="https://github.com/user-attachments/assets/08729357-77cf-4625-b68f-27cec90c27b7" />
<img width="1280" height="687" alt="image" src="https://github.com/user-attachments/assets/1d02ab7b-c60b-4e4b-aae1-3a2c7f802520" />
<img width="892" height="977" alt="image" src="https://github.com/user-attachments/assets/4cd320f0-e8f3-47a1-8876-4f3846ec77fb" />


<img width="892" height="977" alt="image" src="https://github.com/user-attachments/assets/bb304b40-f063-4eba-bb95-f8dab5c4800d" />


3. Ответы на контрольные вопросы

Вопрос 1: Какие pod-ы в kube-system должны быть всегда Running?

kube-apiserver, kube-controller-manager, kube-scheduler, etcd, coredns, kube-proxy - они обеспечивают функционирование всего Kubernetes-кластера.

Вопрос 2: Почему Pod перезапускается после завершения процесса? Кто за это отвечает?

Kubernetes постоянно отслеживает состояние Pod через kubelet. Если основной процесс контейнера завершается, система автоматически пытается восстановить его в соответствии с заданной политикой, поэтому он перезапускается.

Вопрос 3: Чем Pod отличается от контейнера?

Контейнер - это отдельный запущенный процесс с изоляцией.
Pod - более глобальная система в плане того, что он может включать в себя нескоько контейнеров, которые объеденены общей ссетью, диском, настройками.





# 5 Лабораторная:

1. Чему научился:

В ходе выполнения лабораторной работы разобрался, как в Kubernetes работает доступ к приложениям через Service. Понял, что напрямую к Pod обращаться неудобно, потому что у него может меняться IP, и для этого используется Service. Разобрался с типом NodePort и как через него можно открыть доступ к приложению.

2. Возникшие проблемы и способы их решения

Основная проблема опять была из-за того, что часть команд рассчитана на minikube, а у меня его нет.
Команда: "echo "$(minikube ip) webapp.local" | sudo tee -a /etc/hosts" - вообще не работала, потому что minikube просто отсутствует.

Решение — я взял IP ноды вручную: "kubectl get nodes -o wide" и уже его прописал в /etc/hosts.

<img width="892" height="977" alt="image" src="https://github.com/user-attachments/assets/b61e9030-5808-4cdf-a4fe-d5041918c184" />
<img width="272" height="348" alt="image" src="https://github.com/user-attachments/assets/9018ff2d-0780-414c-b3cd-91a8c9f219c4" />
<img width="826" height="367" alt="image" src="https://github.com/user-attachments/assets/a1c79b6d-a63f-449e-81ab-e0b7ddbaac97" />


<img width="931" height="99" alt="image" src="https://github.com/user-attachments/assets/9e97d63c-34fd-40f1-b850-a2c8fd8ae03d" />
<img width="931" height="99" alt="image" src="https://github.com/user-attachments/assets/96d0abc6-73bf-4e16-bf58-1dbca3b4bf85" />

<img width="934" height="78" alt="image" src="https://github.com/user-attachments/assets/beb00c32-1a8d-4295-b343-112b97b0d88f" />
<img width="803" height="766" alt="image" src="https://github.com/user-attachments/assets/676609a1-3ae2-4f4d-a455-ac419297d366" />
<img width="856" height="115" alt="image" src="https://github.com/user-attachments/assets/ad6ee0b7-6942-457d-a551-2f8d3aded911" />
<img width="931" height="184" alt="image" src="https://github.com/user-attachments/assets/dfcbf147-e443-42f2-9197-a3131029bea8" />
<img width="931" height="184" alt="image" src="https://github.com/user-attachments/assets/a7ee31c7-7575-4261-88fa-48e7fad00f2d" />
<img width="869" height="208" alt="image" src="https://github.com/user-attachments/assets/906fa283-975a-4cdc-bf82-14d947f9fc82" />


<img width="932" height="605" alt="image" src="https://github.com/user-attachments/assets/db4701b9-1c7d-4d86-b6f0-ee8a588f7fd8" />


Вопрос 1: Зачем нужен Service в Kubernetes?

Service нужен для того, чтобы дать стабильный доступ к приложению. Pod может перезапуститься и поменять IP, а Service остаётся тем же.

Вопрос 2: Что делает NodePort?

NodePort открывает порт на ноде и через него можно зайти в приложение снаружи.

Вопрос 3: Почему нельзя обращаться к Pod напрямую?

Потому что у Pod нет постоянного IP. Он может измениться при перезапуске, поэтому используют Service.





# 6 Лабораторная:

1. Чему научился:

В ходе выполнения лабораторной работы разобрался, как работает Ingress в Kubernetes.
Понял, что Ingress нужен для более удобного доступа к приложениям, чтобы не использовать NodePort, а заходить по нормальному доменному имени.

2. Возникшие проблемы и способы их решения

Была проблема с доступом через доменное имя. Я добавил запись в /etc/hosts, но сайт всё равно не открывался.

Решение:
Я понял, что не тот айпишник указал, и после проверки: правильный ли IP указан, совпадает ли домен с тем, что в Ingress.
Исправил и домен начал резолвиться.

Ещё проблема — 404 ошибка от nginx - это было из-за того, что путь в Ingress был указан неправильно.

<img width="895" height="956" alt="image" src="https://github.com/user-attachments/assets/1c48d4ca-13ba-4fab-a198-7d19e0ae28e5" />
<img width="1126" height="805" alt="image" src="https://github.com/user-attachments/assets/504c4831-5de0-4318-a3f6-b5621fa4c73e" />


<img width="932" height="747" alt="image" src="https://github.com/user-attachments/assets/12f0bfb8-b7c1-45c1-958d-88b279cba40f" />


<img width="924" height="1079" alt="image" src="https://github.com/user-attachments/assets/7de0271e-aa7e-4a72-a51a-a9bfa6d4a8a4" />
<img width="928" height="662" alt="image" src="https://github.com/user-attachments/assets/87020dc4-ae0b-41b6-b5ad-f72e47586337" />


3. Ответы на контрольные вопросы

Вопрос 1: Зачем нужен Ingress?

Ingress нужен для удобного доступа к приложениям через HTTP/HTTPS и доменные имена, без использования NodePort.

Вопрос 2: Чем Ingress отличается от Service?

Service просто даёт доступ к Pod внутри или снаружи.
Ingress получше, он управляет маршрутизацией HTTP-запросов.

Вопрос 3: Почему Ingress не работает без контроллера?

Потому что Ingress - это просто описание правил.
Контроллер - это компонент, который эти правила реально применяет (например nginx).




# 7 Лабораторная:
1. Чему научился:

В ходе выполнения лабораторной работы разобрался, как работает масштабирование и обновление приложений в Kubernetes.
Понял, что вместо обычных Pod используется Deployment, который управляет количеством реплик и следит за их состоянием.


<img width="906" height="447" alt="image" src="https://github.com/user-attachments/assets/d7c2005a-cd43-45d3-876a-7a7bea34d10c" />
<img width="929" height="566" alt="image" src="https://github.com/user-attachments/assets/85c0b3c1-10b1-429d-bae4-bf6f0c80f57f" />


<img width="1280" height="334" alt="image" src="https://github.com/user-attachments/assets/3b55fdb7-4319-4979-b92c-75a2799532f9" />
<img width="1280" height="970" alt="image" src="https://github.com/user-attachments/assets/d302b327-a329-492d-a734-06a849762fff" />
<img width="1184" height="733" alt="image" src="https://github.com/user-attachments/assets/1aa8a267-032b-48c7-95ec-7bd978efeb10" />
<img width="1280" height="794" alt="image" src="https://github.com/user-attachments/assets/d865c60a-7409-44a5-981d-044fe95a7e1b" />


<img width="1247" height="297" alt="image" src="https://github.com/user-attachments/assets/5bda68fe-c349-4938-b3ea-1c0c6a393890" />
<img width="1151" height="428" alt="image" src="https://github.com/user-attachments/assets/ff4eda0e-ebe3-4144-bf51-78391ba81843" />
<img width="1148" height="447" alt="image" src="https://github.com/user-attachments/assets/48a6e551-cdea-49fc-8f70-ff74ccf5172c" />
<img width="1157" height="441" alt="image" src="https://github.com/user-attachments/assets/3dd74ca7-75c9-4242-b051-d23c34f1f151" />
<img width="1145" height="759" alt="image" src="https://github.com/user-attachments/assets/d9d89fb7-f205-4656-b6b5-e85975d68b01" />
<img width="1179" height="323" alt="image" src="https://github.com/user-attachments/assets/7421a941-d534-4423-8c4b-b874db43a4b3" />


Вопрос 1: Зачем нужен Deployment?

Deployment нужен для управления Pod - он следит за их количеством, перезапускает их при падении и позволяет обновлять приложение.

Вопрос 2: Что такое scaling?

Scaling - это изменение количества запущенных Pod, чтобы увеличить или уменьшить нагрузку.

Вопрос 3: Что такое rolling update?

Это способ обновления приложения без остановки - Pod обновляются постепенно, а не все сразу.
