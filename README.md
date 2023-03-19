# QA-testing-folder-sync

This repository is intended to create a basic one-way synchronization program **FolderSync** that is written in *Python* that synchronizes two folders: source and replica. 
The program maintains a full, identical copy of the source folder at the replica folder.

## Features

- One-way synchronization: After synchronization, the content of the replica folder exactly matches the content of the source folder.
- Periodic synchronization: Synchronization is performed periodically.
- Logging: File creation/copying/removal operations are logged to a file and to the console output.
- Command-line arguments: Folder paths, synchronization interval, and log file path can be provided using command-line arguments.

## Prerequisites

The libraries that are used in this program comes as build-in libraries. You do not need to install any additional libraries. However, ensure that you have [Python](https://www.python.org/downloads/) Version >= 3.6.

## Usage

To use **FolderSync** you can run the following command

```
python folder_sync.py [Path source <string>] [Path replica <string>] [Path log file <string>] [Sync interval <int>]

```

[Path source <string>] [Path replica <string>] [Path log file <string>] [Sync interval <int>] needs to be defined by the user.

If the given *source path* does not contain any directories or files, this means that the intended use case for **FolderSync** is testing. 

In this case, the class **GenerateRandom** will be activated to populate both source and replica folders. The inputs of this class can be changed from line 281 of the *folder_sync.py*

```
obj2.run(max_depth=2, max_files=4, max_dirs=3)
```
 
max_depth define the length of subdirectories in path, max_files defines the possible max number of files in path, max_dirs defines possible max number of directories in path



Before you get started you'll need to do following steps:

- Clone this repository to your local machine using 'git clone https://github.com/atilayyuri/QA-testing-folder-sync.git'


## Workflow
On every pipeline execution, the code goes through the following steps:

1. Code is cloned from this repository, built, tested and analyzed for bugs and bad patterns.
2. A Docker Container Image is built then published to Docker Container Registry.
3. If all previous steps finished successfully, the pipeline is paused for the approval to continue to the deployment.
4. If approved, the container image is deployed in a fresh new container in related K8s namespace.

Targeted release version for the Python package and Docker image is set in the `target-version.json` file in the `app` directory.
Three tags were used as suffixes to separate the packages: dev (development), rc (release candidate), and no suffix (release).

- Any pipeline running from not main branches (a.k.a. feature/bug fix branches) builds the Python package and Docker image with the `<target-version>-dev-<uuid>` tag, then publishes the Docker image to registry and deploys it to `dev` namespace on the K8s cluster.
- Any pipeline running from the main branch builds the Python package and Docker image with the `<target-version>-rc-<uuid>` , then publishes the Docker image to registry and deploys it to `rc` namespace on the K8s cluster.
- Any pipeline running from git tag builds the Python package and Docker image with the `<target-version>` tag, then publishes the Docker image to registry and deploys it to `prod` namespace on the K8s cluster.






