# url-shortener-plus
It is an upgraded version of my URL Shortener project.
## Installation

Clone this directory in your system.(Here, Ubuntu, Docker was used)

Make a directory in your system as given command

```bash
$ sudo mkdir -p /storage/docker/mysql-data
```

Change directory to url-shortener-plus 

```bash
$ cd url-shortener-plus
```
run docker-compose up using below command

```bash
$ sudo docker-compose up 
```

Start App in Browser

```bash
  0.0.0.0:5000
```

### Information Required

if you want to connect to MySQL. Mysql user: root, Mysql Password: YasMys@1

if you want to connect to Rabbitmq. Rabbitmq user: guest, Rabbitmq password: guest
### What's New

1. Contanerised Application.

2. Async calls for signup and slink creation.

3. Celery and rabbitmq used for message queueing.

4. Redis Cache is used for fast redirection