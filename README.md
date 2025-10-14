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