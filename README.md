# NTP система в docker

Данный репозиторий демонстрирует проект, подготовленный в рамках выполнения курсовой работы по предмету "Системное Программное Обеспечение" студентом МФ МГТУ им. Н. Э. Баумана группы К3-56Б Зозулей Артемом

Ниже будет приведена инструкция по работе с демонстрационным проектом

---

## Пререквизиты

Необходимо иметь установленный и запущенный движок docker на хосте, а также сопутствующие пакеты, такие как docker-compose-v2, docker-buildx-plugin

> Весь набор пакетов, связанных с docker, можно установить по инструкции с [официального сайта Docker](https://docs.docker.com/engine/install/)

## Развертывание

Склонируйте данный репозиторий локально на хост, где будет проходить работа со стендом

Первым шагом необходимо запустить тестовый стенд с помощью ```docker compose```, для этого подготовлен скрипт run.sh

```bash
> ./run.sh 
Building Docker image...
[+] Building 1.6s (9/9) FINISHED                                                                                                 docker:default
 => [internal] load build definition from Dockerfile                                                                                       0.0s
 => => transferring dockerfile: 597B                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/alpine:edge                                                                             1.2s
 => [auth] library/alpine:pull token for registry-1.docker.io                                                                              0.0s
 => [internal] load .dockerignore                                                                                                          0.0s
 => => transferring context: 2B                                                                                                            0.0s
 => [1/3] FROM docker.io/library/alpine:edge@sha256:b93f4f6834d5c6849d859a4c07cc88f5a7d8ce5fb8d2e72940d8edd8be343c04                       0.0s
 => => resolve docker.io/library/alpine:edge@sha256:b93f4f6834d5c6849d859a4c07cc88f5a7d8ce5fb8d2e72940d8edd8be343c04                       0.0s
 => [internal] load build context                                                                                                          0.0s
 => => transferring context: 32B                                                                                                           0.0s
 => CACHED [2/3] RUN apk add --no-cache chrony tzdata &&     rm /etc/chrony/chrony.conf &&     rm -rf /var/cache/apk/*                     0.0s
 => CACHED [3/3] COPY ./startup.sh /bin/startup                                                                                            0.0s
 => exporting to image                                                                                                                     0.1s
 => => exporting layers                                                                                                                    0.0s
 => => exporting manifest sha256:adeeb9faedbedcb8d2f32f0f0629665ad71c123ad42cfe4b9c0cbb021bcfd122                                          0.0s
 => => exporting config sha256:0f3b3552558146eae383e4d52d0a5c23750e314695648cca3f193c9e68c84120                                            0.0s
 => => exporting attestation manifest sha256:529d4211824823f62a7a60660f0ab03a7e097ff73f1cdeabb425f2a2e3b1c136                              0.0s
 => => exporting manifest list sha256:8c28a406d34230e352a1fe5976bc4f0aa7e7e4df6ad86a71833989f6c0068900                                     0.0s
 => => naming to docker.io/custom/chrony:local                                                                                             0.0s
 => => unpacking to docker.io/custom/chrony:local                                                                                          0.0s
Running docker compose up -d...
WARN[0000] /home/user404/ntp-docker/docker-compose.yaml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
[+] Running 5/5
 ✔ Network ntp-docker_ntp_network  Created                                                                                                 0.0s 
 ✔ Container chrony-local1         Started                                                                                                 1.2s 
 ✔ Container chrony-local3         Started                                                                                                 1.2s 
 ✔ Container chrony-local2         Started                                                                                                
```

Скрипт выполняет следующие шаги:
- Проверяет наличие нужных пакетов в системе
- Собирает локальный docker-образ c ntp-сервером chrony
- запускает сервисы (набор ntp-серверов на основе собранного ранее docker-образа) из конфигурации ```docker-compose.yaml```

После успешного выполнения скрипта можно посмотреть на состояние запущенных контейнеров с помощью команды:
```bash
> docker ps
CONTAINER ID   IMAGE                 COMMAND          CREATED         STATUS                   PORTS     NAMES
90866ca3510b   custom/chrony:local   "/bin/startup"   7 minutes ago   Up 7 minutes (healthy)   123/udp   chrony-local3
06af3035df87   custom/chrony:local   "/bin/startup"   7 minutes ago   Up 7 minutes (healthy)   123/udp   chrony-local1
d8fd3be21bd3   custom/chrony:local   "/bin/startup"   7 minutes ago   Up 7 minutes (healthy)   123/udp   chrony-local2
```

## Эксплуатация

После успешного развертывания стенда предлагается изучить параметры его компонентов.

Чтобы посмотреть информацию вышестоящего стратума для каждого из трех контейнеров ```chrony-local<n>``` можно выполнить следующие команды:
```bash
> docker exec chrony-local1 chronyc sources
MS Name/IP address         Stratum Poll Reach LastRx Last sample               
===============================================================================
^* 162.159.200.123               3   6   377     9    -32ms[  -76ms] +/-   11ms
> docker exec chrony-local1 chronyc sourcestats
Name/IP Address            NP  NR  Span  Frequency  Freq Skew  Offset  Std Dev
==============================================================================
162.159.200.123             9   4   517     -3.271    573.415    -33us    59ms
>
> docker exec chrony-local1 chronyc tracking
Reference ID    : A29FC87B (162.159.200.123)
Stratum         : 4
Ref time (UTC)  : Thu Oct 31 22:52:09 2024
System time     : 0.118983239 seconds slow of NTP time
Last offset     : +0.061203212 seconds
RMS offset      : 0.137246609 seconds
Frequency       : 537.010 ppm fast
Residual freq   : +114.795 ppm
Skew            : 694.085 ppm
Root delay      : 0.025834698 seconds
Root dispersion : 0.041465286 seconds
Update interval : 65.0 seconds
Leap status     : Norma
>
> docker exec chrony-local2 chronyc sources
MS Name/IP address         Stratum Poll Reach LastRx Last sample               
===============================================================================
^* 162.159.200.123               3   6   377    49    -86ms[ -108ms] +/-   24ms
> docker exec chrony-local2 chronyc sourcestats
Name/IP Address            NP  NR  Span  Frequency  Freq Skew  Offset  Std Dev
==============================================================================
162.159.200.123             9   4   518    -15.460    604.201   -809us    45ms
>
> docker exec chrony-local2 chronyc tracking
Reference ID    : A29FC87B (162.159.200.123)
Stratum         : 4
Ref time (UTC)  : Thu Oct 31 22:52:09 2024
System time     : 0.233108655 seconds slow of NTP time
Last offset     : -0.063350037 seconds
RMS offset      : 0.137813374 seconds
Frequency       : 15.096 ppm fast
Residual freq   : +59.821 ppm
Skew            : 903.832 ppm
Root delay      : 0.022655277 seconds
Root dispersion : 0.034543112 seconds
Update interval : 64.3 seconds
Leap status     : Norma
```

Как мы видим, все 3 chrony-сервера действительно используют указанный в конфигурации сервер time.cloudflare.com и активны
```bash
> dig -x 162.159.200.123

; <<>> DiG 9.18.1-1ubuntu1.3-Ubuntu <<>> -x 162.159.200.123
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 10355
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;123.200.159.162.in-addr.arpa.  IN      PTR

;; ANSWER SECTION:
123.200.159.162.in-addr.arpa. 472 IN    PTR     time.cloudflare.com.

;; Query time: 9 msec
;; SERVER: 10.255.255.254#53(10.255.255.254) (UDP)
```

Также можно посмотреть логи одного из этих серверов командой:
```bash
> docker logs -t chrony-local1
2024-12-08T19:06:14.411818735Z 2024-12-08T19:06:14Z chronyd version 4.6.1 starting (+CMDMON +NTP +REFCLOCK +RTC +PRIVDROP +SCFILTER +SIGND +ASYNCDNS +NTS +SECHASH +IPV6 -DEBUG)
2024-12-08T19:06:14.412098220Z 2024-12-08T19:06:14Z Could not read valid frequency and skew from driftfile /var/lib/chrony/chrony.drift
2024-12-08T19:06:14.412107244Z 2024-12-08T19:06:14Z Initial frequency -29.905 ppm
2024-12-08T19:06:20.702260057Z 2024-12-08T19:06:20Z Selected source 162.159.200.123 (time.cloudflare.com)
```

## Использование стенда как ntp-сервера на хосте

Для начала убедимся, что chrony-сервера внутри контейнерлв доступны с хост-машины. Для этого нам понадобятся следующие пакеты - ```ntpdate```, ```ntp```

IP-адреса уже заранее указаны в docker-compose конфигурации

Теперь выполним команду, которая совершит запрос к каждому ntp-серверу по IP:
```bash
> for i in {2..4}; do ntpdate -q 172.20.0.$i; done
server 172.20.0.2, stratum 4, offset -0.002034, delay 0.02570
 9 Dec 02:13:14 ntpdate[4079103]: adjust time server 172.20.0.2 offset -0.002034 sec
server 172.20.0.3, stratum 4, offset +0.000014, delay 0.02571
 9 Dec 02:13:15 ntpdate[4079104]: adjust time server 172.20.0.3 offset +0.000014 sec
server 172.20.0.4, stratum 4, offset -0.002813, delay 0.02571
 9 Dec 02:13:15 ntpdate[4079105]: adjust time server 172.20.0.4 offset -0.002813 sec
```
Убедившись, что сервера в контейнерах отвечают с локальной машины, мы можем установить их для запущенного на хост-машине ntp-сервера. Чтобы узнать, запущен ли он, можно выполнить следующую команду:
```bash
> systemctl list-units --type=service | grep ntp && systemctl status ntp
  ntp.service                          loaded active running Network Time Service
● ntp.service - Network Time Service
     Loaded: loaded (/lib/systemd/system/ntp.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-10-31 23:25:38 MSK; 3h 10min ago
       Docs: man:ntpd(8)
    Process: 27714 ExecStart=/usr/lib/ntp/ntp-systemd-wrapper (code=exited, status=0/SUCCESS)
   Main PID: 27720 (ntpd)
      Tasks: 2 (limit: 4570)
     Memory: 1.3M
        CPU: 611ms
     CGroup: /system.slice/ntp.service
             └─27720 /usr/sbin/ntpd -p /var/run/ntpd.pid -g -u 115:120

Oct 31 23:25:38 ntp-test2 ntpd[27720]: Listen normally on 7 br-2b664f08e709 [fe80::42:a2ff:fe42:f7d4%15]:123
Oct 31 23:25:38 ntp-test2 ntpd[27720]: Listen normally on 8 veth1b0a614 [fe80::88d4:2dff:fe94:2109%17]:123
Oct 31 23:25:38 ntp-test2 ntpd[27720]: Listen normally on 9 veth75c4721 [fe80::4482:9bff:fe2b:4ac4%19]:123
Oct 31 23:25:38 ntp-test2 ntpd[27720]: Listen normally on 10 veth3275597 [fe80::3cd9:4eff:fe1f:919e%21]:123
Oct 31 23:25:38 ntp-test2 ntpd[27720]: Listen normally on 11 veth0f6632c [fe80::4c0:2aff:fe4d:c521%23]:123
Oct 31 23:25:38 ntp-test2 ntpd[27720]: Listening on routing socket on fd #28 for interface updates
Oct 31 23:25:38 ntp-test2 ntpd[27720]: kernel reports TIME_ERROR: 0x41: Clock Unsynchronized
Oct 31 23:25:38 ntp-test2 ntpd[27720]: kernel reports TIME_ERROR: 0x41: Clock Unsynchronized
Oct 31 23:25:38 ntp-test2 systemd[1]: Started Network Time Service.
```
Если мы получили аналогичный вывод, сообщающий, что данный сервис существует и активен, то можно переходить к изменению его конфигурации - отредактируем файл ```/etc/ntp.conf```, указав в соответствующей части IP-адрес нашего chrony-сервера в Docker вместо всех других:
```bash
...
# Specify one or more NTP servers.
server 172.20.0.2 iburst prefer
server 172.20.0.3 iburst prefer
server 172.20.0.4 iburst prefer

# Cloudflare NTP server as fallback solution
server time.cloudflare.com

...
```

После чего перезапускаем сервис и проверяем изменившиеся настройки:
```bash
> systemctl restart ntp
> ntpq -p
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*172.20.0.2      162.159.200.123  4 u  749 1024  377    0.051   +0.573   0.545
+172.20.0.3      162.159.200.123  4 u  790 1024  377    0.052   -0.054   0.807
+172.20.0.4      162.159.200.1    4 u  822 1024  377    0.051   +0.017   0.282
-time.cloudflare 10.135.8.61      3 u    3 1024  377    6.730   -0.007   2.057
> date
Mon Dec  9 02:15:58 AM MSK 2024
```

> Стоит отметить, что каждый из запущенных в контейнере NTP-серверов на базе chrony имеет стратум 4, тк использует в качестве вышестоящего сервер провайдера Cloudflare, который предоставляет CDN в многих локациях по всему миру, засчет этого его стратум равен 3, также NTP сервера Cloudflare поддерживают шифрование трафика NTS

## Использование стенда как ntp-сервера для приложений

Для демонстрации функционала использования стенда как ntp-сервера для приложений было разработано примитивное приложение на Python, которое мы запустим в контейнере внутри одной docker-bridge-сети со стендом, для этого выполним следующую команду находясь в директории склонированного репозитория:
```bash
> cd ntp-user/ && docker build -t custom/ntp-user:local . && docker run --network ntp-docker-demo_ntp_network --name ntp-time custom/ntp-user:local 172.20.0.1 --interval 5
[+] Building 0.9s (10/10) FINISHED                                                                                               docker:default
 => [internal] load build definition from Dockerfile                                                                                       0.0s
 => => transferring dockerfile: 206B                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.12.2-slim                                                                      0.6s
 => [internal] load .dockerignore                                                                                                          0.0s
 => => transferring context: 2B                                                                                                            0.0s
 => [1/5] FROM docker.io/library/python:3.12.2-slim@sha256:5dc6f84b5e97bfb0c90abfb7c55f3cacc2cb6687c8f920b64a833a2219875997                0.0s
 => => resolve docker.io/library/python:3.12.2-slim@sha256:5dc6f84b5e97bfb0c90abfb7c55f3cacc2cb6687c8f920b64a833a2219875997                0.0s
 => [internal] load build context                                                                                                          0.1s
 => => transferring context: 148.95kB                                                                                                      0.0s
 => CACHED [2/5] WORKDIR /app                                                                                                              0.0s
 => CACHED [3/5] COPY requirements.txt .                                                                                                   0.0s
 => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt                                                                        0.0s
 => CACHED [5/5] COPY . .                                                                                                                  0.0s
 => exporting to image                                                                                                                     0.1s
 => => exporting layers                                                                                                                    0.0s
 => => exporting manifest sha256:ab64f6e03f52ea0444bca6829197f60d10fd07e388e40f87dcd45e2fd4391393                                          0.0s
 => => exporting config sha256:729434fd93830c23518347c354de475b19e966e3fa218bcb30ab0e430df78b64                                            0.0s
 => => exporting attestation manifest sha256:6290375922052bf250a56a45289f25a3f6dbdc1dd19dc04ed706c66e90868020                              0.0s
 => => exporting manifest list sha256:371f372c4fd5112c98e6b4803785445366cff88d4431853a5c6776dda157337a                                     0.0s
 => => naming to docker.io/custom/ntp-user:local                                                                                           0.0s
 => => unpacking to docker.io/custom/ntp-user:local                                                                                        0.0s
2024-12-08 23:31:44,684 - INFO - Fetching time from 172.20.0.1 every 5 seconds
2024-12-08 23:31:49,688 - INFO - -----
2024-12-08 23:31:49,688 - INFO - NTP Time: 2024-12-08 23:31:49.688360
2024-12-08 23:31:49,690 - INFO - Time difference: 5.000779 seconds
2024-12-08 23:31:49,690 - INFO - Average time: 2024-12-08 23:31:47.187971
2024-12-08 23:31:49,691 - INFO - Accuracy: 5.000779 seconds
2024-12-08 23:31:54,691 - INFO - -----
2024-12-08 23:31:54,692 - INFO - NTP Time: 2024-12-08 23:31:54.691824
2024-12-08 23:31:54,693 - INFO - Time difference: 5.003464 seconds
2024-12-08 23:31:54,693 - INFO - Average time: 2024-12-08 23:31:52.190092
2024-12-08 23:31:54,694 - INFO - Accuracy: 5.003464 seconds
...
```
Приложение начнет выводить время и ряд статистических данных, полученные с NTP сервера хостовой машины с заданным интервалом (5 секунд). Тем самым демонстрируется взаимодействие приложений с ним внутри Docker-контейнеров.

Если мы посмотрим информацию об одном из наших контейнеров с chronyc используя `docker container inspect`, то получим следующую информацию о сети:
```bash
> docker container inspect chrony-local1 | jq '.[0].NetworkSettings.Networks'
{
  "ntp-docker-demo_ntp_network": {
    "IPAMConfig": {
      "IPv4Address": "172.20.0.2"
    },
    "Links": null,
    "Aliases": [
      "chrony-local1",
      "ntp-front1",
      "887d9a380068",
      "chrony.local1"
    ],
    "NetworkID": "40370636755c4a6984bfe85dc1aef9a1fc742cf1a37eb5864778e4a80bb31b00",
    "EndpointID": "d1fdf2eba62f4707cf02086106d4ce334a40570531d4743b45e97e6dc1e75df8",
    "Gateway": "172.20.0.1",
    "IPAddress": "172.20.0.2",
    "IPPrefixLen": 29,
    "IPv6Gateway": "",
    "GlobalIPv6Address": "",
    "GlobalIPv6PrefixLen": 0,
    "MacAddress": "02:42:ac:14:00:02",
    "DriverOpts": null
  }
```
Как видно, в параметре **Gateway** указан именно тот IP который мы использовали из контейнера для проверки работы локального NTP сервера хоста из контейнера с приложением.
