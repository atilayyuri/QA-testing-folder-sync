# QA-testing-folder-sync

This repository is intended to create a basic one-way synchronization program **FolderSync** that is written in *Python* that synchronizes two folders: source and replica. 
The program maintains a full, identical copy of the source folder at the replica folder.

## Features

- One-way synchronization: After synchronization, the content of the replica folder exactly matches the content of the source folder.
- Periodic synchronization: Synchronization is performed periodically.
- Logging: File creation/copying/removal operations are logged to a file and to the console output.
- Command-line arguments: Folder paths, synchronization interval, and log file path have to be provided using command-line arguments.

## Prerequisites

This program has beeen developed in Windows, tested on Windows, Linux and Darwin. Hence, one should consider before running the code.

The libraries that are used in this program comes as build-in libraries. You do not need to install any additional libraries. However, ensure that you have [Python](https://www.python.org/downloads/) Version >= 3.6.

Before you get started you'll need to do following step:

- Clone this repository to your local machine using 'git clone https://github.com/atilayyuri/QA-testing-folder-sync.git'

For testing however, one should have the ```pytest``` library installed to be able to run ```test_folder_sync.py```

## Structure

```
.
├── folder_sync.py
└── create_directories_and_files.py

```

The project has two scripts where ```folder_sync.py``` is the main script for the syncronisation and contains **FolderSync**. ```create_directories_and_files.py``` is the testing script to test the functionality of the **FolderSync**. Within ```create_directories_and_files.py```, **GenerateRandom** is a class that creates random files and directories. When activated this class runs over the source and replica and directories and populates them based on the inputs *max_depth*, *max_files*, *max_dirs*.
    
```
    max_depth -- defines the maximum number of sub directory levels in a directory
    max_files -- defines the maximum number of files in a directory
    max_dirs -- defines the maximum number of directory in a directory

    To test the ability of the FolderSync class (copy detection, content detection if the filename is same)
    the random file generator has the following abilities

            Creates a file at path1 with content1
            Creates a file at path2 with content1 -- basically copies
            Creates a file at path2 with content2 -- to test the content of the file when file paths in source and
                                                     replica folder matches
```                                               

## Usage

To use **FolderSync** you can run the following command

```
python folder_sync.py [Path source <string>] [Path replica <string>] [Path log file <string>] [Sync interval <int>]
```

Warning since this is a one way synchronization script, it is advised to create a new empty folder as replica folder. Otherwise all files at the replica folder will be deleted! 

[Path source <string>] [Path replica <string>] [Path log file <string>] [Sync interval <int>] needs to be defined by the user.

If the given *source path* does not contain any directories or files, this means that the intended use case for **FolderSync** is testing. 

In this case, the class **GenerateRandom** will be activated to populate both source and replica folders. The inputs of this class can be changed from line 281 of the *folder_sync.py*

```
obj2.run(max_depth=2, max_files=4, max_dirs=3)
```
    
Alternatively, one can use ```pytest``` to test **FolderSync**
    
    
## Workflow
    
On each execution the code goes throug the following steps
    
1. Checks the command-line arguments
2. Starts the synchronization cycle
    
    * Reads the directories and files in the source folder, creates ```metadata.txt``` at replica folder that contains the information about the files and modification times.
    * Reads the directories and files in the replica folder, or reads the metadata if exists
    * Synchronizes the two folders, logs any file that is created/copied/deleted to the log file and console output
    
3. When synchronization interval is completed, starts the synchronisation cycle again

    


