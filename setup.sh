#!/usr/bin/sh

VERSION="v1.0.0"
WORK_DIR=".devcontainer"
DOCKERFILE_NAME="Dockerfile"
COMPOSE_FILE_NAME="compose.yml"
DEV_CONTAINER_FILE_NAME="devcontainer.json"

echo "Enter the project name:"
read -r project_name

echo "\nRendering templates..."

export project_name
export version=$VERSION

envsubst < "$WORK_DIR/$COMPOSE_FILE_NAME.template" > "$WORK_DIR/$COMPOSE_FILE_NAME"
envsubst < "$WORK_DIR/$DEV_CONTAINER_FILE_NAME.template" > "$WORK_DIR/$DEV_CONTAINER_FILE_NAME"

echo "compose.yml and devcontainer.json files created."

docker_image_tag="$project_name:$VERSION"

echo "\nBuilding Docker image for $project_name:$VERSION..."
docker build -f "$WORK_DIR/$DOCKERFILE_NAME" -t "$docker_image_tag" .
docker builder prune -f > /dev/null
image_id=$(docker images -q "$docker_image_tag")

echo "\n$(printf '%0.s-' $(seq 1 70))"
echo "Docker Image Information"
echo " - Repository: $project_name"
echo " - Tag: $VERSION"
echo " - ID: $image_id"

echo "\nTo start the Docker container, run the following command:"
echo "docker compose --file $WORK_DIR/$COMPOSE_FILE_NAME up -d"

echo "\nOnce the container is up and running, you can access it using:"
echo "docker exec -it $project_name bash"

echo "$(printf '%0.s-' $(seq 1 70))"
