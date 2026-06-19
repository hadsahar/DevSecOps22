# Compose application

### Python/Flask application with Nginx proxy and a Mongo database

Project structure:
```bash
├── flask
   ├── Dockerfile
   ├── requirements.txt
   └── server.py

```
# frontend
ngnix image runs on port 80
no need to install anything 
environment variables : 
- FLASK_SERVER_ADDR=((flask service name)):((flaskport))
the application depnds on the backend 

# backend 
### flask app runs in this prot : 9091
### env  FLASK_SERVER_PORT=9091
### the application depnds on the mongo db  


you need to add volume to the db at - vol name :/data/db

#
your task is to create a docker-compose file that will run the application
- flask 
- mongo 

attach the backend and the mongo to the same network

