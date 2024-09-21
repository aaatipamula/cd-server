#!/bin/sh

exit_if_error() {
  if [ $? -ne 0 ]
  then
    echo "Error: $1 went wrong"
    exit $?
  fi
}

USERNAME=$(whoami)

if [ -z $1 ]
then
  echo 'Please enter a name for the Docker image/container!'
  exit 1
fi

if [ -f ./Dockerfile ]
then 
  echo "Stopping container $1"
  docker rm -f -v $1
  # exit_if_error "Stopping container $1 failed"

  echo "Removing image $USERNAME/$1:latest"
  docker rmi $USERNAME/$1:latest
  # exit_if_error "Removing image $USERNAME/$1:latest"

  echo "Building $USERNAME/$1:latest"
  DOCKER_BUILDKIT=1 docker build -t $USERNAME/$1:latest . 
  exit_if_error "Building $USERNAME/$1:latest"

  # Make this more robust
  echo "Starting container $1"
  if [ -d ./src/data ]
  then
    docker run -d \
      -it \
      --restart unless-stopped \
      --name $1 \
      --mount type=bind,source=$(pwd)/src/data,target=/home/bot/src/data \
      $USERNAME/$1:latest
    exit_if_error "Starting container $1"
  else
    docker run -it -d --name $1 $USERNAME/$1:latest
    exit_if_error "Starting container $1"
  fi
else
  echo 'No Dockerfile found.'
  exit 1 
fi
