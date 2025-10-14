### Docker presentation

https://docs.google.com/presentation/d/1TClOq3s__IAEwI7xQbVTJ1nMv9UNQ1OcoQ6-OKSy3Ko/edit?usp=sharing

### Podman pull

```bash
podman pull docker.io/library/nginx:stable-alpine3.21
```

### create a network

```bash
podman network create demo-network

podman network inspect demo-network
```

### To run a container 

```bash
podman run -d --name nginx1 -p 28080:80 --network demo-network nginx:stable-alpine3.21 
```

### To check running containers 

```bash
podman ps
```

### To run contaier and interactive tty 

```bash
podman run -i -t --network=demo-network --name ub1 ubuntu bash
```


### Run a stopped container

```bash
podman start ub1
podman exec -it ub1 bash
```

### podman commands 

```bash
podman stop ub1 
# to delete the container
podman rm -f ub1
```

### building an image

```bash
docker  build . -f Dockerfile -t jpalaparthi/ubuntu-curl:v01
```

### Run postgres db

```bash
podman run -d --name pg -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=appdb postgres:16
```

### Run the admin UI

```bash
podman -d --name dbui -p 18080:8080 adminer
```