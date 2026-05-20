
# Docker Installation
```bash
docker --version
```
# Run Your First Containers
```bash
docker run hello-world
docker run -it ubuntu
``` 

# Run Existing Applications
```bash
docker run -p 5003:5003 hothaifaz11/todos-api:latest
``` 

# Linux Namespace Isolation Demo

```bash
ps aux
ps aux | head
ps
sudo unshare --fork --pid --mount-proc bash
# in the new terminal run 
ps aux
ps aux | head
ps
# isolated bash proccess 
```

# Docker Images
```bash
docker pull ubuntu:26.04
#Wrong Image Examples (for teaching errors)
docker pull ubuntu:26.04213412421
# View Images
docker images
docker image ls
Remove Images
docker rmi ubuntu:26.04
docker rmi ubuntu
docker rmi $(docker images -q) # remove all images
```
# Naming Containers
## Wrong Example
```bash
docker run --name h ubutu:26.04
```
## Correct Example
```bash
docker run --name hothaifa ubuntu:26.04
docker run --name elad ubuntu:26.04
```
# Interactive Containers
## Run Interactive Ubuntu
```bash
docker run --name hodi -it ubuntu:26.04
```
## Start Existing Container Interactively
```bash
docker start -i hodi
```
# Detached Mode
## Run in Background
```bash
docker run --name hodi -it -d ubuntu:26.04
docker run --name hodi11 -it -d ubuntu:26.04
```
## Stop Container
```bash
docker stop hodi11
```
# Environment Variables
## Wrong Syntax
```bash
docker run --name container1 -it -e SERVER_NAME:hodi-sql ubuntu:26.04
```
## Correct Syntax
```bash
docker run --name container12 -it -e SERVER_NAME=hodi-sql ubuntu:26.04
```
# Jenkins Containers
## Run Jenkins
```bash
docker run --name jenkins jenkins/jenkins
```
## Random Port Mapping
```bash
docker run --name jenkins2 -P jenkins/jenkins
docker run --name jenkins3 -P jenkins/jenkins
```
## Specific Port Mapping
```bash
docker run --name jenkins4 -p 7000:8080 jenkins/jenkins:latest
```
## Check Used Ports
```bash
lsof -i -P -n :7000
lsof -i :7000
```
## Another Jenkins Instance
```bash
docker run --name jenkins5 -p 7005:8080 jenkins/jenkins:latest
```
# Grafana Containers
## Wrong Image Example
```bash
docker run --name grafana -p 3000:3000 grafana/grafnaa
```
## Correct Image
```bash
docker run --name grafana -p 3000:3000 grafana/grafana
docker run --name grafana1 -p 3000:3000 grafana/grafana
```
# Inspect Containers & Networks
## List Running Containers
```bash
docker ps
docker ps -a
docker ps -aq
```
## Inspect Containers
```bash
docker inspect db92aca7431d
docker inspect b621fdf82806
docker inspect 25ec1b4c58a1
```
## List Networks
```bash
docker network ls
```
# Cleanup Commands
## Remove Specific Container
```bash
docker rm da5b93e53895
```
## Remove All Containers
```bash
docker rm $(docker ps -qa)
```
## Useful Commands Throughout Lesson
```bash
clear
exit
docker rm --help
ls
```
# Random Port Mapping
```bash
docker run --name jenkins2 -P jenkins/jenkins
docker run --name jenkins3 -P jenkins/jenkins
```
# Specific Port Mapping
```bash
docker run --name jenkins4 -p 7000:8080 jenkins/jenkins:latest
```
# Check Used Ports
```bash
lsof -i -P -n :7000
lsof -i :7000
