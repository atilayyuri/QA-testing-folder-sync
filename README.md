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

Before you get started you'll need to do following step:

- Clone this repository to your local machine using 'git clone https://github.com/atilayyuri/QA-testing-folder-sync.git'

## Structure

```
.
├── folder_sync/
└── create_directories_and_files/

```

The project has two scripts where ```folder_sync.py``` is the main code for the syncronisation, ```create_directories_and_files.py``` is the testing script to test the functionality of the **FolderSync**

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













