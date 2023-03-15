import os
import sys
import string
import argparse
import platform
os.system('color')
import fileinput
from pathlib import PureWindowsPath


class InputTest:
    """
    # Test-driven-development
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
    #   b) All the inputs need to be checked i.e multiple lines, blank spaces, os specific characters
    #   c) Inputs need to follow upper-lower case consistency
    #   d)
    """

    def __init__(self):
        self.path_source = None
        self.path_replica = None
        self.sync_interval = None
        self.log_file_path = None
        self.log_file_mode = None

    # def __init__(self,path_source,path_replica,sync_interval,log_file_path,log_file_mode):
    #     self.path_source = path_source
    #     self.path_replica = path_replica
    #     self.sync_interval = sync_interval
    #     self.log_file_path = log_file_path
    #     self.log_file_mode = log_file_mode

    @staticmethod
    def capitalize_string(s):
        if s[0] == s[0].lower():
            return string.capwords(s)
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
            input_file = log_file_directory + '\logfile.txt'
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
            except:
                print(f'Synchronization interval must be a positive integer\n')

    def _check_path_identical(self, path1, path2):
        while True:
            if path1 == path2:
                print(f'The path for source and replica folder can not be identical\n')
                path_replica = input(f'Please enter the path for the replica folder:').strip()
                if path1 == path_replica:
                    self._check_path_identical(path1, path_replica)
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

    def __init__(self, path_source, path_replica, sync_interval, path_log_file):
        self.path_source = path_source
        self.path_replica = path_replica
        self.sync_interval = sync_interval
        self.path_log_file = path_log_file

    # @property
    # def set_inputs(self):
    #
    #     return self._path_source, self._path_replica, self._sync_inteval, self. self._log_file_path
    #
    # @set_inputs.setter
    # def set_inputs(self, path_source, path_replica, sync_interval, log_file_path):
    #
    #     self._path_source = path_source
    #     self._path_replica = path_replica
    #     self._sync_interval = sync_interval
    #     self._log_file_path = log_file_path

    def check_paths(self, path):
        new_path=''
        sep = os.sep
        splitted = path.split(sep)
        #print('splitted',splitted[1:])

        if platform.system() == 'Windows':
            special_characters = sep+'/:*?<>|'
            # check every character of splitted except if it is empty strong
            if any(c in special_characters for c in splitted[1:] if c != ''):
                raise AttributeError(f'{bcolors.FAIL}{self.path_source} has special characters{bcolors.ENDC}')
        elif platform.system() == 'Linux':
            raise AttributeError(f'{bcolors.FAIL}Linux specifications needs to be implemented to safely run this code{bcolors.ENDC}')

        for directory in splitted:
            if directory == '':
                continue
            new_path = new_path+directory+sep
        #print('new_path',new_path)
        return new_path

    def check_sys_args(self):

        paths = [self.path_source, self.path_replica, self.path_log_file]


        for path in paths:
            new_path = self.check_paths(path)
            print('path',path)
            print('npath',new_path)
            setattr(self,path, new_path)

        if not os.path.isdir(self.path_source):
            print(f'{bcolors.FAIL}Error: Path for source directory {self.path_source} does not exist{bcolors.ENDC}')
            return False
        if not os.path.isdir(self.path_replica):
            print(f'{bcolors.FAIL}Error: Path for replica directory {self.path_replica} does not exist{bcolors.ENDC}')
            return False
        if self.path_source == self.path_replica:
            print(f'{bcolors.FAIL}Error: Path for source and replica directory can not be identical{bcolors.ENDC}')
        if not os.path.isdir(self.path_log_file):
            print(f'{bcolors.FAIL}Error: Folder path for the log file {self.path_log_file} does not exist{bcolors.ENDC}')
            return False
        if self.sync_interval < 0:
            print(f"{bcolors.FAIL}Error: Synchronisation interval {self.sync_interval} must be positive integer{bcolors.ENDC}")
            return False

        return True


class bcolors:
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
        parser = argparse.ArgumentParser(prog='SyncFolder ',
                                         description='A simple program to one-way sync source folder to replica folder')
        parser.add_argument('path_source', metavar='[Path source <string>]', type=str, help='Path for the source folder')
        parser.add_argument('path_replica', metavar='[Path replica <string>]', type=str, help='Path for the replica folder')
        parser.add_argument('log_file_path', metavar='[Path log file <string>]', type=str, help='Folder path of the log file')
        parser.add_argument('sync_interval', metavar='[Sync interval <int>]', type=int, help='Synchronization interval')
        #parser.add_argument('--sum', dest='accumulate', action='store_const',
        #                     const=sum, default=max,
        #                     help='sum the integers (default: find the max)')

        args = parser.parse_args()


        obj1 = FolderSync(args.path_source,args.path_replica, args.sync_interval, args.log_file_path)
        print(obj1.__dir__())

        if obj1.check_sys_args():
            break
        else:
            exit(-1)
        #print(args.path_source, args.path_replica, args.log_file_path, args.sync_interval)
    #print(args.accumulate(args.integers))
    print(f"{bcolors.OKGREEN}INFO: System arguments passed the test{bcolors.ENDC}")

    args = sys.argv
    print(args)

    # for line in fileinput.input():
    #     f_line = line[0]
    #     break
    # print(f_line)
    #
    #
    # # py
    # #try123 = input('try1_')
    # #check_input(try123)
    # #print('return',try123)
    #
    #
    # #check_input(input(f'Please enter the path for the source folder:'))
    #
    #
    # path_source = check_path_directory(check_input(input(f'Please enter the path for the source folder:').strip()), 'source')
    # path_replica = input(f'Please enter the path for the replica folder:').strip()
    #
    # path_replica = check_path_identical(path_source,path_replica)
    #
    # sync_interval = check_sync_interval()
    #
    # [log_file_path, log_file_mode] = check_path_file(input(f'Please enter the path for the log file:').strip())
    # print(log_file_mode, log_file_path)

    #test = InputTest()
    #test.check_user_input()


if __name__ == '__main__':
    main()
