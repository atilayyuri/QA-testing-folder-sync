import os
from string import capwords
from argparse import ArgumentParser
from platform import system
from hashlib import md5
from create_directories_and_files import GenerateRandom
from datetime import datetime
from time import sleep
from shutil import copy2, rmtree, Error

os.system('color')


class InputTest:
    """
    # Test-driven-development
    # This class test the user inputs for FolderSync class to make sure the user defined paths are aligned
    #
    # Best case scenarios
    #
    # 1) Directory paths: user defines directory path which exists
    # 2) Log file: user defines a path in the form of directory+filename which does not exist
    # 3) Interval: user defines a positive integer
    #
    # Possible scenarios and test cases for faulty user input regarding
    #
    # 1) Directory paths
    #   a) Test: Does defined directory exists (a.1) or not (a.2)?
    #       └── (a.1) --> define directory paths (ideal, except they source and replica paths are same, see --> (4.a))
    #
    #                            Does user wants to create a directory?
    #                          /
    #       └── (a.2) --> ────
    #                          \ Does user wants to redefine the directory?
    #                                                                                       Overwrite?
    # 2) Log file                                                                          /
    #   a) Test: Does defined path is directory path (a.1) or file path (a.2)?     yes ────
    #       └── (a.1) --> add the file name       ╗                               /        \
    #                                             ╠═ does that path exists?   ────          Append?
    #       └── (a.2)                             ╝                               \
    #                                                                              no --> define log file path (ideal)
    #
    #
    # 3) Interval
    #   a) Test: Does the nature of the input is non-integer (a.1) or integer (a.2)?
    #       └── (a.1) --> user needs to redefine input
    #
    #                       Positive? --> define synchronisation interval (ideal)
    #                     /
    #       └── (a.2) ────
    #                     \
    #                       Negative? --> user needs to redefine input
    #
    # 4) Additional caution points
    #   a) Paths for source and replica can not be identical
    #   b) All the inputs need to be checked i.e multiple lines(!!), blank spaces, or specific characters
    #   c) Line seperator should be consistent
    #   d)
    """

    def __init__(self):
        self.path_source = None
        self.path_replica = None
        self.sync_interval = None
        self.log_file_path = None
        self.log_file_mode = None

    @staticmethod
    def capitalize_string(s):
        if s[0] == s[0].lower():
            return capwords(s)
        else:
            return s

    def _check_path_directory(self, input_path, folder_key):
        # input_path = input_path.strip()
        if os.path.isdir(input_path):
            print(f'{self.capitalize_string(folder_key)} path is defined as {input_path}\n')
            return input_path

        elif not os.path.isdir(input_path):
            print(f'The given path "{input_path}" does not exist\n')
            while True:
                respond = input(
                    f'To create a new {folder_key} folder at given path please type "y", to define a new {folder_key} folder please type "n":').strip()
                if respond.lower() == 'y':
                    os.mkdir(input_path)
                    print(f'The {folder_key} folder is created\n')
                    return input_path
                elif respond.lower() == 'n':
                    self._check_path_directory(input(f'Please enter a new path for {folder_key} directory:').strip(),
                                               folder_key)
                    break
                else:
                    print(f'Input is not recognized, please input only "y" or "n"\n')

    def _check_path_file(self, input_file):
        input_file = input_file.strip()
        if os.path.isdir(input_file):
            log_file_directory = self._check_path_directory(input_file, 'log file')
            input_file = log_file_directory + os.sep + 'logfile.txt'
            print(f'Synchronization will be logged to {input_file}\n')

        if os.path.exists(input_file):
            while True:
                file_mode = input(
                    f'The path "{input_file}" already exists, please type "w" to overwrite or type "a" to append:').strip()
                if file_mode.lower() == 'a' or file_mode.lower() == 'w':
                    print(f'Synchronization will be logged to {input_file}\n')
                    break
                else:
                    print(f'Input is not recognized, please input only "w" or "a"\n')
        else:
            file_mode = 'w'

        return [input_file, file_mode.lower()]

    def _check_sync_interval(self):

        while True:
            try:
                self.sync_interval = int(input(f'Please enter the synchronization interval in seconds:'))
                if self.sync_interval > 0:
                    print(f'Synchronization interval is defined\n')
                    break
                else:
                    print(f'Synchronization interval must be a positive integer\n')
            except ValueError:
                print(f'Synchronization interval must be a positive integer\n')

    def _check_path_identical(self, path_1, path_2):
        while True:
            if path_1 == path_2:
                print(f'The path for source and replica folder can not be identical\n')
                path_replica = input(f'Please enter the path for the replica folder:').strip()
                if path_1 == path_replica:
                    self._check_path_identical(path_1, path_replica)
                else:
                    self.path_replica = path_replica

            break

    def check_user_input(self):
        self.path_source = self._check_path_directory(input(f'Please enter the path for the source folder:').strip(),
                                                      'source')
        self.path_replica = input(f'Please enter the path for the replica folder:').strip()

        self.path_replica = self._check_path_identical(self.path_source, self.path_replica)

        self._check_sync_interval()

        [self.log_file_path, self.log_file_mode] = self._check_path_file(
            input(f'Please enter the path for the log file:'))


class FolderSync:
    """Possible algorithm structures

    1) scan both source and replica, find the difference, copy the diff from source to replica, remove the non existent
    ones from the replica, remove first and then copy the file name matchers but not identicals.

    first time run : O(n_source)

    2)

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
            print(f'{Colors.FAIL} {current_time} {log_string} {Colors.ENDC}')
        elif key == 'green':
            print(f'{Colors.OKGREEN} {current_time} {log_string} {Colors.ENDC}')
        elif key == 'blue':
            print(f'{Colors.OKBLUE} {current_time} {log_string} {Colors.ENDC}')
        elif key == 'cyan':
            print(f'{Colors.OKCYAN} {current_time} {log_string} {Colors.ENDC}')
        elif key == 'orange':
            print(f'{Colors.WARNING} {current_time} {log_string} {Colors.ENDC}')
        elif key == 'bold':
            print(f'{Colors.BOLD} {current_time} {log_string} {Colors.ENDC}')

    @staticmethod
    def _log_metadata(path, data, filename):
        """ This method simply writes out the metadata"""
        # current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open(filename, 'a') as f:
            f.write(f'{path} , {data}\n')

    def _read_metadata(self, filename):
        """ This method simply reads the metadata and deletes it"""
        metadata = {}
        # current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open(filename, 'r') as f:
            for line in f:
                stripped_line = line.strip()
                path, time = stripped_line.split(',')
                metadata[path.strip()] = float(time)

        os.remove(filename)
        return metadata

    @staticmethod
    def _check_paths(path):
        """This method checks whether the given path has special characters"""
        new_path = ''
        # Define operation system specific line seperator
        sep = os.sep
        splitted = path.split(sep)


        if system() == 'Windows':
            special_characters = sep + '/:*?<>|'
            # If it is windows it starts with C: D: etc, which has ":" in it but it is not special character
            for directory in splitted[1:]:
                # Check if any string element has special character in it
                if any(c in special_characters for c in directory):
                    raise AttributeError(f'{Colors.FAIL}{path} has special characters{Colors.ENDC}')
        # TODO Define Linux specific character later to run the program on environment
        elif system() == 'Linux':
            raise AttributeError(
                f'{Colors.FAIL}Linux specifications needs to be implemented to safely run this code{Colors.ENDC}')

        # After checking every string element, it builds the string
        for directory_1 in splitted:
            # os.normpath and os.abspath already applied to string but just to be on the safe side
            if directory_1 == '':
                continue
            new_path = new_path + directory_1 + sep
        return new_path

    def _copy_file(self, path1, path2):
        """This method handles error if for any reason shutil.copy2 fails, logs out to the logfile and console"""
        # print('path2 original', path2)
        path2_directories = 'C:\\'+(os.path.join(*path2.split('\\')[1:-1]))

        try:
            # print('path1',path1)
            # print('path2',split_path2[:-1])
            if not os.path.exists(path2_directories):
                print('yok')
            #print(os.path.exists(path2_directories))
                os.makedirs(path2_directories)
            copy2(os.path.abspath(path1), os.path.abspath(path2))
            self.log(f' -- Copy -- The file {path1} has been copied to {path2}', self.log_file_path, 'green')
            self.count_file_copied += 1
        except OSError as e:
            self.log(f' Error copying {path1} to {path2}: {e}', self.log_file_path, 'red')
        # except Error as e:
        #    self.log(f' Error copying {path1} to {path2}: {e}', self.log_file_path, 'red')
        except Exception as e:
            self.log(f' Error copying {path1} to {path2}: {e}', self.log_file_path, 'red')

    def _remove_file(self, path):
        """This method handles error if for any reason os.remove fails, logs out to the logfile and console"""
        try:
            os.remove(path)
            #if path is os.path.join(self.path_replica,'metadata.txt'):
            #    return
            self.count_file_removed += 1
            self.log(f' -- Remove -- The file {path} has been deleted', self.log_file_path, 'orange')
        except OSError as e:
            # print(f'{Colors.FAIL} Error removing file {path}: {e} {Colors.ENDC}')
            self.log(f' Error removing file {path}: {e} ', self.log_file_path, 'red')

    def check_sys_args(self):
        # TODO Define point 3) later when you handle logfile question (What if the path_log_file_dir is a path? What should be the correct way to handle this?)
        """This method check system arguments

        After checking the paths using check_paths method it checks

        1) If given source and replica directories exist
        2) If given source and replica directories identical
        3) If the given directory path for logfile exists
        4) If the given synchronization interval is positive integer

        """

        paths = [self.path_source, self.path_replica, self.log_file_path]
        attrs = ['path_source', 'path_replica', 'path_log_file_dir']

        for path, attr in zip(paths, attrs):
            new_path = self._check_paths(os.path.normpath(os.path.abspath(path)))
            setattr(self, attr, new_path)

        #error = False

        if not os.path.isdir(self.path_source):
            #print(f'{Colors.FAIL}Error: Path for source directory {self.path_source} does not exist{Colors.ENDC}')
            raise ValueError(f"Source directory {self.path_source} does not exist")
            #error = True
        if not os.path.isdir(self.path_replica):
            #print(f'{Colors.FAIL}Error: Path for replica directory {self.path_replica} does not exist{Colors.ENDC}')
            raise ValueError(f"Replica directory {self.path_replica} does not exist")
            #error = True
        if self.path_source == self.path_replica:
            #print(f'{Colors.FAIL}Error: Path for source and replica directory can not be identical{Colors.ENDC}')
            raise ValueError("Path for source and directory directories are identical")
            #error = True

        if os.path.isdir(self.log_file_path):
            #print(f'{Colors.FAIL}Error: Given input {self.log_file_path} is a directory, please provide full path for log file {Colors.ENDC}')
            raise ValueError(f"Given input {self.log_file_path} is a directory, please provide full path for log file")
            #error = True
        else:
            # TODO ?? What if the path_log_file_dir is a path? What should be the correct way to handle this?
            if os.path.exists(self.log_file_path):
                print(f'{Colors.WARNING}WARNING: Logfile path {self.log_file_path} exists new log will be append to existing file{Colors.ENDC}')

        if self.sync_interval < 0:
            #print(f"{Colors.FAIL}Error: Synchronisation interval {self.sync_interval} must be positive integer{Colors.ENDC}")
            raise ValueError(f"Synchronisation interval {self.sync_interval} must be positive integer")

            #error = True

#        if error:
#            return True
#        else:
#            return False

    def compare_and_match(self):
        """This method compares source and replica paths, finds
        1) Files that are not matching, that are needs to be removed from replica path, and needs to be copied
        from source path to replica path
        2) Finds the files that have identical filename --intersection-- and checks their content
        3) Find


         """
        # print('source', path_source)
        # print('target', path_target)
        # source_files_dir_path = []
        # target_files_dir_path = []
        # source_files_dir = os.listdir(path_source)
        # target_files_dir = os.listdir(path_target)

        # Create an empty set to add dirnames+filename after
        source_files_dir = set()
        target_files_dir = set()

        source_metadata_info = {}
        target_metadata_info = {}

        diff_to_copy = set()

        # Check metadata exists
        meta = os.path.isfile(os.path.join(self.path_replica, 'metadata.txt'))

        if meta:
            target_metadata_info = self._read_metadata(os.path.join(self.path_replica, 'metadata.txt'))
            print('the metadata from previous run', target_metadata_info)
            print('META VAR META VARRRRRRR')

        # Check the source and replica paths and add dirnames+filenames to relevant sets
        for source_dirpath, dirnames, filenames in os.walk(self.path_source):
            for source_filename in filenames:
                # In case the log file defined in source path, we do not want to involve it into loop
                if os.path.join(self.path_source,source_filename) == self.log_file_path:
                    continue
                # Define the dirname
                relative_dir_source = os.path.relpath(source_dirpath, self.path_source)
                # Define the dirname+filename, add it to set
                relative_path_source = os.path.normpath(os.path.join(relative_dir_source, source_filename))
                source_files_dir.add(relative_path_source)
                if meta:
                    # If the source path does exist in meta
                    # print(f'relative_path_source {relative_path_source}')
                    # print(f'relative_path_type {type(relative_path_source)}')
                    # print(f'metadata_path_keys {target_metadata_info.keys()}')
                    # If the source path does exist in meta that means it is in target directory
                    if relative_path_source in set(target_metadata_info.keys()):
                        # If modification times does not match, that means it is changed in source directory, so copy it
                        print(f' modify info {target_metadata_info[relative_path_source]} {os.path.getmtime(os.path.join(source_dirpath, source_filename))}' )
                        if not float(target_metadata_info[relative_path_source]) == float(
                                os.path.getmtime(os.path.join(source_dirpath, source_filename))):
                            diff_to_copy.add(relative_path_source)
                            print(f'META modification --- {relative_path_source} will be copied')
                    # If the source path does not exist in meta
                    else:
                        # Check if the content is the same, might be that they did not modified
                        # but still content is the same
                        if not self._check_files_matching(os.path.join(self.path_source, relative_path_source),
                                                          os.path.join(self.path_replica, relative_path_source)):
                            diff_to_copy.add(relative_path_source)
                            print(f'META --- {relative_path_source} will be copied')
                # If meta does not exist, create meta
                else:
                    source_metadata_info[relative_path_source] = os.path.getmtime(
                        os.path.join(source_dirpath, source_filename))

        if not meta:
            # If metadata does not exist/missing we dont need any information about history
            # program needs to start from scratch
            for target_dirpath, dirnames, target_filenames in os.walk(self.path_replica):
                for target_filename in target_filenames:
                    # In case logfile defined into target path, we do not want to involve it into loop
                    if os.path.join(self.path_replica, target_filename) == self.log_file_path:
                        continue
                    # Define the dirname
                    relative_dir_target = os.path.relpath(target_dirpath, self.path_replica)
                    # Define the dirname+filename, add it to set
                    relative_path_target = os.path.normpath(os.path.join(relative_dir_target, target_filename))
                    target_files_dir.add(relative_path_target)
                    # target_metadata_info[relative_path_target] = os.path.getmtime(
                    #    os.path.join(target_dirpath, target_filename))

            # TODO metadata for the copied files
            # If metadata does not exist/missing we dont need any information about history
            # program needs to start from scratch

            # Find the files that only exist in the source path, does not exist in source path, and exist both of them
            diff_to_copy = source_files_dir.difference(target_files_dir)
            diff_to_remove = target_files_dir.difference(source_files_dir)
            intersection = source_files_dir.intersection(target_files_dir)

            # This section checks whether the files that have the same filename have the same context
            for file in intersection:
                # In case user have the logfile in source path, we might not want to copy that
                #if os.path.join(self.path_source, file) == self.log_file_path:
                #    continue
                # Check whether files are matching
                if not self._check_files_matching(os.path.join(self.path_source, file),
                                                  os.path.join(self.path_replica, file)):
                    # A file has been found to copy
                    diff_to_copy.add(file)
        else:
            # if len(target_metadata_info) > len(source_files_dir):
            print(f'META var REMOVEEE')
            print(source_files_dir)
            diff_to_remove = set(target_metadata_info.keys()).difference(source_files_dir)


        print('diff_to_copy', diff_to_copy, len(diff_to_copy))
        print('diff_to_remove', diff_to_remove, len(diff_to_remove))
        print()
        print('source_metadata_when_there is no metadata', source_metadata_info, len(source_metadata_info))
        for file_to_copy in diff_to_copy:
            if (os.path.join(self.path_source,file_to_copy) == self.log_file_path) or (os.path.join(self.path_replica,file_to_copy) == self.log_file_path):
                continue
            #if os.path.join(self.)
            # If there is no metadata, that means we can assume replica folder is empty.
            # Everything that is copied from source to replica will be to content of source file
            print('file to copy', file_to_copy)
            # TODO metadata olmadigi zaman ne yapacaksin?
            if file_to_copy in source_metadata_info.keys():
                data = source_metadata_info[file_to_copy]
                self._log_metadata(file_to_copy, data, os.path.join(self.path_replica, 'metadata.txt'))
            self._copy_file(os.path.join(self.path_source, file_to_copy), os.path.join(self.path_replica, file_to_copy))
            # self._log(f'The file {os.path.join(path_source, file_to_copy)}',self.log_file_path)

        for file_to_remove in diff_to_remove:
            self._remove_file(os.path.join(self.path_replica, file_to_remove))

        return diff_to_copy, diff_to_remove
        # for intersection remove from the replica first, then copy from the source
        #

    @staticmethod
    def _check_files_matching(file_1, file_2):
        # print('file1', file_1)
        # print('file2', file_2)
        # To open the file only-read mode with encoding='utf-8' has been tried but failed
        with open(file_1, 'rb') as f1:
            with open(file_2, 'rb') as f2:
                if md5(f1.read()).hexdigest() == md5(f2.read()).hexdigest():
                    print(f'{Colors.OKBLUE} The file {file_1} and {file_2} are identical {Colors.ENDC}')
                    return True
                else:
                    print(f'{Colors.OKCYAN} The file {file_1} and {file_2} are not identical {Colors.ENDC}')
                    return False


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def remove_all_dir_and_subdir(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)
        except Error as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
        except OSError as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


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
        #if not obj1.check_sys_args():
        #    break
        #else:
        #    exit(-1)

    print(f"{Colors.OKGREEN}INFO: System arguments passed the test successfully{Colors.ENDC}")
    # exit()
    print(obj1.__dict__)

    print('\n')

    obj2 = GenerateRandom(obj1.path_source, obj1.path_replica)
    #[count_source_files, count_source_dire],[count_target_files, count_target_dirs],intersection_list_generate_random = obj2.run(max_depth=3, max_files=4, max_dirs=3)
    #print(f'count_source_files {count_source_files}  count_source_dire {count_source_dire} count_target_files {count_target_files} count_target_dirs {count_target_dirs}')
    #exit()

    # print(f'source_files {count_source_files} count_source_dirs {count_source_dire} count_target_files {count_target_files}, count_target_dirs {count_target_dirs}' )

    # TODO in the while main loop check that folders are still exist
    # TODO to control the metafile os.stat('path')#
    # TODO metafile routine check metafile at replica, read the timestamp, check the files that are modified at source
    # TODO that are modified after metafile timestamp, for each file, check whether they exist at replica, if does compare
    # TODO the content, delete any file that is in replica which is not exist at source

    # at
    while True:

        if not os.path.isdir(obj1.path_source):
            obj1.log(f' The source path {obj1.path_source} does not exist anymore', obj1.log_file_path, 'red')
            break

        elif not os.path.isdir(obj1.path_replica):
            obj1.log(f' The source path {obj1.path_replica} does not exist anymore', obj1.log_file_path, 'red')
            break  # TODO change this to continue later

        copy_results, remove_results = obj1.compare_and_match()
        if remove_results is not None:
            print('copy in main loop', copy_results, len(copy_results), '\n')
            print('remove in main loop', remove_results, len(remove_results), '\n')
            print()

        obj1.log(f' ---- End of cycle, number of files copied: {obj1.count_file_copied}, '
                 f'number of files deleted: {obj1.count_file_removed}', obj1.log_file_path, 'blue')

        sleep(obj1.sync_interval)

    obj1.log(f' ---- END OF SYNC, number of files copied: {obj1.count_file_copied}, '
             f'number of files deleted: {obj1.count_file_removed}', obj1.log_file_path, 'cyan')

    #
    # if len(intersection_set_folder_sync) == len(intersection_list_generate_random):
    #     pass

    # ------------------------------- REMOVE ALL DIR AND SUBDIR ------------------------#
    ask = input('Delete or not')
    if ask == 'y':
        remove_all_dir_and_subdir(obj1.path_source)
        remove_all_dir_and_subdir(obj1.path_replica)

    # ------------------------------- REMOVE ALL DIR AND SUBDIR ------------------------#


if __name__ == '__main__':
    main()
