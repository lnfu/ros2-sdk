#!/usr/bin/python3

import os
import sys
import warnings
import subprocess

VERSION = "v1.0.0"
WORK_DIR = '.devcontainer'
DOCKERFILE_NAME = 'Dockerfile'
COMPOSE_FILE_NAME = 'compose.yml'
DEV_CONTAINER_FILE_NAME = 'devcontainer.json'


def install_missing_package(package_name):
    print(f"{package_name} is not installed. Installing now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


def main():
    try:
        import docker
    except ImportError:
        install_missing_package("docker")
        import docker

    try:
        import tqdm
    except ImportError:
        install_missing_package("tqdm")
        import tqdm

    try:
        import jinja2
    except ImportError:
        install_missing_package("jinja2")
        import jinja2

    warnings.filterwarnings("ignore", category=tqdm.TqdmExperimentalWarning)

    project_name = input("Enter the project name: ")

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(WORK_DIR))
    compose_template = env.get_template(f"{COMPOSE_FILE_NAME}.j2")
    dev_container_template = env.get_template(f"{DEV_CONTAINER_FILE_NAME}.j2")

    compose = compose_template.render({
        'project_name': project_name,
        'version': VERSION
    })

    dev_container = dev_container_template.render({
        'project_name': project_name,
        'version': VERSION
    })

    with open(os.path.join(WORK_DIR, COMPOSE_FILE_NAME), "w") as f:
        f.write(compose)

    with open(os.path.join(WORK_DIR, DEV_CONTAINER_FILE_NAME), "w") as f:
        f.write(dev_container)

    docker_client = docker.APIClient()
    logs = docker_client.build(
        path=WORK_DIR,
        dockerfile=DOCKERFILE_NAME,
        tag=f"{project_name}:{VERSION}",
        rm=True,
        decode=True
    )

    progress_bar = tqdm.tqdm(total=3751, unit="step")
    for log in logs:
        progress_bar.update(1)
        if 'aux' in log:
            image_id = log['aux']['ID']
    if progress_bar:
        progress_bar.close()
    docker_client.prune_builds()

    print(f"\n{'-'*70}")
    if image_id.startswith("sha256:"):
        image_id = image_id[len("sha256:"):]
    print("Image Information")
    print(f" - Repository: {project_name}")
    print(f" - Tag: {VERSION}")
    print(f" - ID: {image_id}")
    print(f"{'-'*70}")


if __name__ == "__main__":
    main()
