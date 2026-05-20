# Docker Commands Cheat Sheet

## Container Lifecycle Commands

### docker run
Creates and starts a new container from an image.
```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
docker run -d nginx                    # Run container in detached mode
docker run -it ubuntu              # Run interactively with terminal
docker run -p 8080:80 nginx            # Map port 8080 (host) to 80 (container)
docker run --name myapp nginx          # Assign custom name
docker run -e VAR=value nginx          # Set environment variable
docker run --rm nginx                  # Auto-remove container when stopped
docker run -v /host/path:/container/path  # Mount volume
```

### docker start
Starts one or more stopped containers.
```bash
docker start [OPTIONS] CONTAINER [CONTAINER...]
docker start mycontainer               # Start a stopped container
docker start -a mycontainer            # Start and attach to container
docker start -i mycontainer            # Start with interactive mode
```

### docker stop
Stops one or more running containers gracefully (sends SIGTERM).
```bash
docker stop [OPTIONS] CONTAINER [CONTAINER...]
docker stop mycontainer                # Stop a container
docker stop $(docker ps -q)            # Stop all running containers
docker stop -t 30 mycontainer          # Wait 30 seconds before force stop
```

### docker restart
Restarts one or more containers.
```bash
docker restart [OPTIONS] CONTAINER [CONTAINER...]
docker restart mycontainer             # Restart a container
```

### docker pause
Pauses all processes within a container.
```bash
docker pause CONTAINER [CONTAINER...]
docker pause mycontainer               # Pause container processes
```

### docker unpause
Unpauses all processes within a container.
```bash
docker unpause CONTAINER [CONTAINER...]
docker unpause mycontainer             # Resume paused container
```

### docker kill
Forces a container to stop immediately (sends SIGKILL).
```bash
docker kill [OPTIONS] CONTAINER [CONTAINER...]
docker kill mycontainer                # Force kill a container
docker kill -s SIGINT mycontainer      # Send specific signal
```

### docker rm
Removes one or more stopped containers.
```bash
docker rm [OPTIONS] CONTAINER [CONTAINER...]
docker rm mycontainer                  # Remove a stopped container
docker rm -f mycontainer               # Force remove running container
docker rm $(docker ps -aq)             # Remove all stopped containers
docker rm -v mycontainer               # Remove container and its volumes
```

### docker rename
Renames a container.
```bash
docker rename CONTAINER NEW_NAME
docker rename oldname newname          # Rename a container
```

## Container Information Commands

### docker ps
Lists running containers.
```bash
docker ps [OPTIONS]
docker ps                              # Show running containers
docker ps -a                           # Show all containers (running and stopped)
docker ps -q                           # Show only container IDs
docker ps -s                           # Show container sizes
docker ps --filter "status=exited"     # Filter by status
docker ps --format "table {{.Names}}\t{{.Status}}"  # Custom format
docker ps -n 5                         # Show last 5 containers
```

### docker logs
Fetches logs from a container.
```bash
docker logs [OPTIONS] CONTAINER
docker logs mycontainer                # View container logs
docker logs -f mycontainer             # Follow log output (live)
docker logs --tail 100 mycontainer     # Show last 100 lines
docker logs --since 1h mycontainer     # Show logs from last hour
docker logs -t mycontainer             # Show timestamps
```

### docker inspect
Returns detailed information about a container or image.
```bash
docker inspect [OPTIONS] CONTAINER|IMAGE
docker inspect mycontainer             # Get detailed container info (JSON)
docker inspect --format='{{.State.Running}}' mycontainer  # Get specific info
```

### docker top
Displays running processes in a container.
```bash
docker top CONTAINER [ps OPTIONS]
docker top mycontainer                 # Show processes in container
```

### docker stats
Displays live resource usage statistics.
```bash
docker stats [OPTIONS] [CONTAINER...]
docker stats                           # Show stats for all running containers
docker stats mycontainer               # Show stats for specific container
docker stats --no-stream               # Display stats once without streaming
```

### docker port
Lists port mappings for a container.
```bash
docker port CONTAINER [PRIVATE_PORT[/PROTO]]
docker port mycontainer                # Show all port mappings
docker port mycontainer 80             # Show mapping for specific port
```

## Image Commands

### docker pull
Downloads an image from a registry.
```bash
docker pull [OPTIONS] NAME[:TAG|@DIGEST]
docker pull nginx                      # Pull latest nginx image
docker pull nginx:1.21                 # Pull specific version
docker pull ubuntu:20.04               # Pull Ubuntu 20.04
```

### docker images
Lists all locally stored images.
```bash
docker images [OPTIONS]
docker images                          # List all images
docker images -a                       # Show all images (including intermediates)
docker images -q                       # Show only image IDs
docker images --filter "dangling=true" # Show untagged images
```

### docker rmi
Removes one or more images.
```bash
docker rmi [OPTIONS] IMAGE [IMAGE...]
docker rmi nginx                       # Remove an image
docker rmi -f nginx                    # Force remove an image
docker rmi $(docker images -q)         # Remove all images
```

### docker build
Builds an image from a Dockerfile.
```bash
docker build [OPTIONS] PATH | URL
docker build -t myapp:1.0 .            # Build image with tag
docker build --no-cache -t myapp .     # Build without cache
docker build -f Dockerfile.dev .       # Use specific Dockerfile
```




### docker tag
Creates a tag for an image.
```bash
docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
docker tag myapp:1.0 myapp:latest      # Tag an image
docker tag myapp myregistry.com/myapp  # Tag for registry
```

### docker push
Uploads an image to a registry.
```bash
docker push [OPTIONS] NAME[:TAG]
docker push myregistry.com/myapp:1.0   # Push image to registry
```

### docker history
Shows the history of an image.
```bash
docker history [OPTIONS] IMAGE
docker history nginx                   # Show image layer history
```

### docker save
Saves an image to a tar archive.
```bash
docker save [OPTIONS] IMAGE [IMAGE...]
docker save -o myapp.tar myapp:1.0     # Save image to file
```

### docker load
Loads an image from a tar archive.
```bash
docker load [OPTIONS]
docker load -i myapp.tar               # Load image from file
```

## Container Interaction Commands

### docker exec
Executes a command in a running container.
```bash
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
docker exec -it mycontainer bash       # Open bash shell in container
docker exec mycontainer ls /app        # Run command in container
docker exec -u root mycontainer bash   # Execute as specific user
```

### docker attach
Attaches to a running container's main process.
```bash
docker attach [OPTIONS] CONTAINER
docker attach mycontainer              # Attach to container
```

### docker cp
Copies files between container and host.
```bash
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH
docker cp [OPTIONS] SRC_PATH CONTAINER:DEST_PATH
docker cp mycontainer:/app/file.txt .  # Copy from container to host
docker cp ./file.txt mycontainer:/app  # Copy from host to container
```

### docker diff
Shows changes to container's filesystem.
```bash
docker diff CONTAINER
docker diff mycontainer                # Show filesystem changes
```

### docker commit
Creates a new image from container's changes.
```bash
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
docker commit mycontainer myapp:2.0    # Create image from container
```

### docker export
Exports container's filesystem as tar archive.
```bash
docker export [OPTIONS] CONTAINER
docker export mycontainer > backup.tar # Export container filesystem
```

### docker import
Creates image from tarball.
```bash
docker import [OPTIONS] file|URL [REPOSITORY[:TAG]]
docker import backup.tar myapp:restored # Import from tarball
```

## Network Commands

### docker network ls
Lists all networks.

### docker tag
Creates a tag for an image.
```bash
docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
docker tag myapp:1.0 myapp:latest      # Tag an image
docker tag myapp myregistry.com/myapp  # Tag for registry
```

### docker push
Uploads an image to a registry.
```bash
docker push [OPTIONS] NAME[:TAG]
docker push myregistry.com/myapp:1.0   # Push image to registry
```

### docker history
Shows the history of an image.
```bash
docker history [OPTIONS] IMAGE
docker history nginx                   # Show image layer history
```

### docker save
Saves an image to a tar archive.
```bash
docker save [OPTIONS] IMAGE [IMAGE...]
docker save -o myapp.tar myapp:1.0     # Save image to file
```

### docker load
Loads an image from a tar archive.
```bash
docker load [OPTIONS]
docker load -i myapp.tar               # Load image from file
```

## Container Interaction Commands

### docker exec
Executes a command in a running container.
```bash
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
docker exec -it mycontainer bash       # Open bash shell in container
docker exec mycontainer ls /app        # Run command in container
docker exec -u root mycontainer bash   # Execute as specific user
```

### docker attach
Attaches to a running container's main process.
```bash
docker attach [OPTIONS] CONTAINER
docker attach mycontainer              # Attach to container
```

### docker cp
Copies files between container and host.
```bash
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH
docker cp [OPTIONS] SRC_PATH CONTAINER:DEST_PATH
docker cp mycontainer:/app/file.txt .  # Copy from container to host
docker cp ./file.txt mycontainer:/app  # Copy from host to container
```

### docker diff
Shows changes to container's filesystem.
```bash
docker diff CONTAINER
docker diff mycontainer                # Show filesystem changes
```

### docker commit
Creates a new image from container's changes.
```bash
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
docker commit mycontainer myapp:2.0    # Create image from container
```

### docker export
Exports container's filesystem as tar archive.
```bash
docker export [OPTIONS] CONTAINER
docker export mycontainer > backup.tar # Export container filesystem
```

### docker import
Creates image from tarball.
```bash
docker import [OPTIONS] file|URL [REPOSITORY[:TAG]]
docker import backup.tar myapp:restored # Import from tarball
```

## Network Commands

### docker network ls
Lists all networks.

### docker tag
Creates a tag for an image.
```bash
docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
docker tag myapp:1.0 myapp:latest      # Tag an image
docker tag myapp myregistry.com/myapp  # Tag for registry
```

### docker push
Uploads an image to a registry.
```bash
docker push [OPTIONS] NAME[:TAG]
docker push myregistry.com/myapp:1.0   # Push image to registry
```

### docker history
Shows the history of an image.
```bash
docker history [OPTIONS] IMAGE
docker history nginx                   # Show image layer history
```

### docker save
Saves an image to a tar archive.
```bash
docker save [OPTIONS] IMAGE [IMAGE...]
docker save -o myapp.tar myapp:1.0     # Save image to file
```

### docker load
Loads an image from a tar archive.
```bash
docker load [OPTIONS]
docker load -i myapp.tar               # Load image from file
```

## Container Interaction Commands

### docker exec
Executes a command in a running container.
```bash
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
docker exec -it mycontainer bash       # Open bash shell in container
docker exec mycontainer ls /app        # Run command in container
docker exec -u root mycontainer bash   # Execute as specific user
```

### docker attach
Attaches to a running container's main process.
```bash
docker attach [OPTIONS] CONTAINER
docker attach mycontainer              # Attach to container
```

### docker cp
Copies files between container and host.
```bash
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH
docker cp [OPTIONS] SRC_PATH CONTAINER:DEST_PATH
docker cp mycontainer:/app/file.txt .  # Copy from container to host
docker cp ./file.txt mycontainer:/app  # Copy from host to container
```

### docker diff
Shows changes to container's filesystem.
```bash
docker diff CONTAINER
docker diff mycontainer                # Show filesystem changes
```

### docker commit
Creates a new image from container's changes.
```bash
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
docker commit mycontainer myapp:2.0    # Create image from container
```

### docker export
Exports container's filesystem as tar archive.
```bash
docker export [OPTIONS] CONTAINER
docker export mycontainer > backup.tar # Export container filesystem
```

### docker import
Creates image from tarball.
```bash
docker import [OPTIONS] file|URL [REPOSITORY[:TAG]]
docker import backup.tar myapp:restored # Import from tarball
```

## Network Commands

### docker network ls
Lists all networks.

### docker tag
Creates a tag for an image.
```bash
docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
docker tag myapp:1.0 myapp:latest      # Tag an image
docker tag myapp myregistry.com/myapp  # Tag for registry
```

### docker push
Uploads an image to a registry.
```bash
docker push [OPTIONS] NAME[:TAG]
docker push myregistry.com/myapp:1.0   # Push image to registry
```

### docker history
Shows the history of an image.
```bash
docker history [OPTIONS] IMAGE
docker history nginx                   # Show image layer history
```

### docker save
Saves an image to a tar archive.
```bash
docker save [OPTIONS] IMAGE [IMAGE...]
docker save -o myapp.tar myapp:1.0     # Save image to file
```

### docker load
Loads an image from a tar archive.
```bash
docker load [OPTIONS]
docker load -i myapp.tar               # Load image from file
```

## Container Interaction Commands

### docker exec
Executes a command in a running container.
```bash
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
docker exec -it mycontainer bash       # Open bash shell in container
docker exec mycontainer ls /app        # Run command in container
docker exec -u root mycontainer bash   # Execute as specific user
```

### docker attach
Attaches to a running container's main process.
```bash
docker attach [OPTIONS] CONTAINER
docker attach mycontainer              # Attach to container
```

### docker cp
Copies files between container and host.
```bash
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH
docker cp [OPTIONS] SRC_PATH CONTAINER:DEST_PATH
docker cp mycontainer:/app/file.txt .  # Copy from container to host
docker cp ./file.txt mycontainer:/app  # Copy from host to container
```

### docker diff
Shows changes to container's filesystem.
```bash
docker diff CONTAINER
docker diff mycontainer                # Show filesystem changes
```

### docker commit
Creates a new image from container's changes.
```bash
docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]
docker commit mycontainer myapp:2.0    # Create image from container
```

### docker export
Exports container's filesystem as tar archive.
```bash
docker export [OPTIONS] CONTAINER
docker export mycontainer > backup.tar # Export container filesystem
```

### docker import
Creates image from tarball.
```bash
docker import [OPTIONS] file|URL [REPOSITORY[:TAG]]
docker import backup.tar myapp:restored # Import from tarball
```


## Useful Docker Run Options

* -d, --detach: Run container in background
* -it: Interactive terminal
* -p, --publish: Publish container port to host
* -v, --volume: Bind mount a volume
* -e, --env: Set environment variables
* --name: Assign container name
* --rm: Automatically remove container when stopped
* --network: Connect to network
* -u, --user: Username or UID
* --restart: Restart policy (no, on-failure, always, unless-stopped)
* -w, --workdir: Working directory inside container
* --memory: Memory limit
* --cpus: Number of CPUs
* --env-file: Read environment variables from file