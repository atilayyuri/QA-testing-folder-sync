import os
from argparse import ArgumentParser
from platform import system
from hashlib import md5
from create_directories_and_files import GenerateRandom
from datetime import datetime
from time import sleep
from shutil import copy2
from enum import Enum

if system() == 'Windows':
    os.system('color')


class FolderSync:
    """ This class performs the following operations

    1) Check command line arguments

    2) Scan both source and replica, find the difference, copy the difference from source to replica,
    remove the non existent ones from the replica, remove first and then copy the file name matchers but not identical.

    Complexity of os.walk(), since it is a generator it depends on how far you walk the three, however when
    f:= total number of files within path, s:= total number of directories within path
     --> O(f+s) --> O(n)

    s : total number of files + total number of directories in source
    r : total number of files + total number of directories in replica

    worst case non-meta run :  O(s) + O(r) + O(s) + O(r-s) + O(s-r)- os.walk(s), os.walk(r), meta_write(s), delete, copy
    worst case metarun run :  O(s) + O(s) + O(r-s) + O(s-r) -- os.walk(s), meta_read(s) , delete, copy

    metarun is   O(r) is faster

    """

    def __init__(self, path_source, path_replica, sync_interval, log_file_path):
        self.path_source = path_source
        self.path_replica = path_replica
        self.sync_interval = sync_interval
        self.log_file_path = log_file_path
        self.count_file_copied = 0
        self.count_file_removed = 0

    @staticmethod
    def log(log_string, filename, key):
        """ This method simply logs out a string to log file path by appending and also console output"""
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open(filename, 'a') as f:
            f.write(f'[ {current_time} ] {log_string} \n')
        if key == 'red':
            print(f'{Colors.FAIL.value} {current_time} ERROR:{log_string} {Colors.ENDC.value}')
        elif key == 'green':
            print(f'{Colors.OKGREEN.value} {current_time} INFO:{log_string} {Colors.ENDC.value}')
        elif key == 'blue':
            print(f'{Colors.OKBLUE.value} {current_time} INFO:{log_string} {Colors.ENDC.value}')
        elif key == 'cyan':
            print(f'{Colors.OKCYAN.value} {current_time} INFO:{log_string} {Colors.ENDC.value}')
        elif key == 'orange':
            print(f'{Colors.WARNING.value} {current_time} WARNING:{log_string} {Colors.ENDC.value}')
        elif key == 'bold':
            print(f'{Colors.BOLD.value} {current_time} INFO:{log_string} {Colors.ENDC.value}')

    @staticmethod
    def _log_metadata(path, data, filename):
        """ This method simply writes out the metadata"""
        with open(filename, 'a') as f:
            f.write(f'{path} , {data}\n')

    @staticmethod
    def _read_metadata(filename):
        """ This method simply reads the metadata and deletes it"""
        metadata = {}
        with open(filename, 'r') as f:
            for line in f:
                stripped_line = line.strip()
                path, time = stripped_line.split(',')
                metadata[path.strip()] = float(time)

        return metadata

    def _copy_file(self, path1, path2):
        """This method handles error if for any reason shutil.copy2 fails, logs out to the logfile and console"""
        path2_directories = ''
        if system() == 'Windows':
            path2_directories = 'C:\\' + (os.path.join(*path2.split('\\')[1:-1]))
        elif (system() == 'Linux') or (system() == 'Darwin') :
            path2_directories = os.path.join(*path2.split('/')[:-1])

        try:
            if not os.path.exists(path2_directories):
                os.makedirs(path2_directories)
            copy2(os.path.abspath(path1), os.path.abspath(path2))
            self.log(f' ---- Copy ---- The file {path1} has been copied to replica', self.log_file_path, 'green')
            self.count_file_copied += 1
        except OSError as e:
            self.log(f' Error copying {path1} to {path2}: {e}', self.log_file_path, 'red')
        except Exception as e:
            self.log(f' Error copying {path1} to {path2}: {e}', self.log_file_path, 'red')

    def _remove_file(self, path):
        """This method handles error if for any reason os.remove fails, logs out to the logfile and console"""
        try:
            os.remove(path)
            self.count_file_removed += 1
            self.log(f' ---- Remove ---- The file {path} has been deleted from replica', self.log_file_path, 'orange')
        except OSError as e:
            self.log(f' Error removing file {path}: {e} ', self.log_file_path, 'red')

    def check_sys_args(self):
        """This method check system arguments

        After checking the paths using check_paths method it checks

        1) If given source and replica directories exist
        2) If given source and replica directories identical
        3) If the given directory path for logfile exists
        4) If the given synchronization interval is positive integer

        """

        if not os.path.isdir(self.path_source):
            raise ValueError(f"Source directory {self.path_source} does not exist")
        if not os.path.isdir(self.path_replica):
            raise ValueError(f"Replica directory {self.path_replica} does not exist")
        if self.path_source == self.path_replica:
            raise ValueError("Path for source and directory directories are identical")
        if os.path.isdir(self.log_file_path):
            raise ValueError(f"Given input {self.log_file_path} is a directory, please provide full path for log file")
        else:
            if os.path.exists(self.log_file_path):
                self.log(f' Logfile path {self.log_file_path} exists new log will be append to existing file', self.log_file_path, 'orange')

        if self.sync_interval < 0:
            raise ValueError(f"Synchronisation interval {self.sync_interval} must be positive integer")

    def compare_and_match(self):
        """This method compares source and replica paths, finds
        1) Files that have not identical filename, that are needs to be removed from replica path,
        and needs to be copied from source path to replica path
        2) Files that have identical filename -- for this case it checks file content
        3) Prints out the metadata of source path in replica directory, once script is run once the source path
        information will be printed to replica, when this is available there is no need to scan the replica
        again.This is implemented in order to reduce the order of complexity
         """
        source_files_dir = set()
        target_files_dir = set()

        target_metadata_info = {}

        diff_to_copy = set()
        diff_to_remove_to_append = set()

        # Check metadata exists
        meta_exists = os.path.isfile(os.path.join(self.path_replica, 'metadata.txt'))
        if meta_exists:
            # Idea is to read the metadata in each cycle and delete it, so it will be refreshed each cycle
            target_metadata_info = self._read_metadata(os.path.join(self.path_replica, 'metadata.txt'))
            os.remove(os.path.join(self.path_replica, 'metadata.txt'))

        # Check the source and replica paths and add dirnames+filenames to relevant sets
        for source_dirpath, dirnames, filenames in os.walk(self.path_source):
            for source_filename in filenames:
                # In case the log file defined in source path, we do not want to involve it into loop
                if os.path.join(self.path_source, source_filename) == self.log_file_path:
                    continue
                relative_dir_source = os.path.relpath(source_dirpath, self.path_source)
                # Define the dirname+filename to add to the set
                relative_path_source = os.path.normpath(os.path.join(relative_dir_source, source_filename))
                source_files_dir.add(relative_path_source)
                if meta_exists:
                    # Check if the source file is already at replica directory
                    if relative_path_source in set(target_metadata_info.keys()):
                        # Check if modification times does not match,
                        # that means it is changed in source directory, so copy it
                        if not float(target_metadata_info[relative_path_source]) == float(
                                os.path.getmtime(os.path.join(source_dirpath, source_filename))):
                            diff_to_copy.add(relative_path_source)
                    # If the source path does not exist in replica directory
                    else:
                        self.log(
                            f' ---- Create ---- A new file has been created at source directory '
                            f'{os.path.join(self.path_source,relative_path_source)}',
                            self.log_file_path, 'bold')

                        diff_to_copy.add(relative_path_source)
                else:
                    # Create metadata for source folder at replica directory
                    data = os.path.getmtime(os.path.join(source_dirpath, source_filename))
                    self._log_metadata(relative_path_source, data, os.path.join(self.path_replica, 'metadata.txt'))

        if not meta_exists:
            # If metadata does not exist/missing we dont need any information about history
            # program needs to start from scratch
            for target_dirpath, dirnames, target_filenames in os.walk(self.path_replica):
                for target_filename in target_filenames:
                    # In case logfile defined into target path, we do not want to involve it into loop
                    if os.path.join(self.path_replica, target_filename) == self.log_file_path:
                        continue
                    relative_dir_target = os.path.relpath(target_dirpath, self.path_replica)
                    # Define the dirname+filename, add it to set
                    relative_path_target = os.path.normpath(os.path.join(relative_dir_target, target_filename))
                    target_files_dir.add(relative_path_target)
                    # Check if the target path exist in source dir
                    if relative_path_target in source_files_dir:
                        if not self._check_files_matching(os.path.join(self.path_source, relative_path_target),
                                                          os.path.join(self.path_replica, relative_path_target)):
                            # If the content is not matching remove
                            diff_to_remove_to_append.add(relative_path_target)
                            pass
                        pass

            # Find the files that only exist in the source path, does not exist in source path
            diff_to_copy = source_files_dir.difference(target_files_dir)
            diff_to_remove = (target_files_dir.difference(source_files_dir))
            diff_to_remove.union(diff_to_remove_to_append)
            # Metadata should be remove at the beginning of the cycle not the end
            diff_to_remove.remove('metadata.txt')
        else:
            diff_to_remove = set(target_metadata_info.keys()).difference(source_files_dir)

        for file_to_copy in diff_to_copy:
            if (os.path.join(self.path_source, file_to_copy) == self.log_file_path) or \
                    (os.path.join(self.path_replica, file_to_copy) == self.log_file_path):
                continue
            self._copy_file(os.path.join(self.path_source, file_to_copy), os.path.join(self.path_replica, file_to_copy))

        for file_to_remove in diff_to_remove:
            self._remove_file(os.path.join(self.path_replica, file_to_remove))

        return diff_to_copy, diff_to_remove

    @staticmethod
    def _check_files_matching(file_1, file_2):
        # First, to open the file only-read mode with encoding='utf-8' has been tried but failed
        # Due to that rb action is chosen
        with open(file_1, 'rb') as f1:
            with open(file_2, 'rb') as f2:
                if md5(f1.read()).hexdigest() == md5(f2.read()).hexdigest():
                    return True
                else:
                    return False


class Colors(Enum):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    while True:
        parser = ArgumentParser(prog='SyncFolder',
                                description='A simple program to one-way sync source folder to replica folder')
        parser.add_argument('path_source', metavar='[Path source <string>]', type=str,
                            help='Path for the source folder')
        parser.add_argument('path_replica', metavar='[Path replica <string>]', type=str,
                            help='Path for the replica folder')
        parser.add_argument('log_file_path', metavar='[Path log file <string>]', type=str,
                            help='Folder path of the log file')
        parser.add_argument('sync_interval', metavar='[Sync interval <int>]', type=int,
                            help='Synchronization interval')

        args = parser.parse_args()
        obj1 = FolderSync(args.path_source, args.path_replica, args.sync_interval, args.log_file_path)
        obj1.check_sys_args()
        break


    obj1.log(f' System arguments passed the test successfully', obj1.log_file_path, 'green')

    obj2 = GenerateRandom(obj1.path_source, obj1.path_replica)
    if (obj2.count_files_dirs_recurs(obj1.path_source)[0] == 0) \
            or (obj2.count_files_dirs_recurs(obj1.path_source)[0]) == 0:
        # max_depth define the length of subdirectories in path, max_files defines the possible max number of
        # files in path , max_dirs defines possible max number of directories in path
        obj2.run(max_depth=2, max_files=4, max_dirs=3)

    obj1.log(f' ---- Start of synchronization ---- ', obj1.log_file_path, 'cyan')

    while True:

        if not os.path.isdir(obj1.path_source):
            obj1.log(f' The source path {obj1.path_source} does not exist anymore', obj1.log_file_path, 'red')
            break

        elif not os.path.isdir(obj1.path_replica):
            obj1.log(f' The source path {obj1.path_replica} does not exist anymore', obj1.log_file_path, 'red')
            break

        obj1.log(f' ---- Start of cycle --- ', obj1.log_file_path, 'blue')

        copy_results, remove_results = obj1.compare_and_match()

        obj1.log(f' ---- End of cycle, for this cycle number of files copied: {len(copy_results)}, '
                 f'number of files deleted: {len(remove_results)}\n', obj1.log_file_path, 'blue')

        sleep(obj1.sync_interval)

    obj1.log(f' ---- End of synchronization, total number of files copied: {obj1.count_file_copied}, '
             f'total number of files deleted: {obj1.count_file_removed}', obj1.log_file_path, 'cyan')


if __name__ == '__main__':
    main()
