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
#   b) All the inputs need to be checked i.e multiple lines, blank spaces
#   c) Inputs need to follow upper-lower case consistency
#   d)


import os
import sys
import string
import fileinput
from pathlib import PureWindowsPath

class InputTest:
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
        #input_path = input_path.strip()
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

    def _check_path_identical(self,path1,path2):
        while True:
            if path1 == path2:
                print(f'The path for source and replica folder can not be identical\n')
                path_replica = input(f'Please enter the path for the replica folder:').strip()
                if path1 == path_replica:
                    self._check_path_identical(path1,path_replica)
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

    def __init__(self, path_source, path_replica, sync_interval, log_file_path):
        self.path_source = path_source
        self.path_replica = path_replica
        self.sync_interval = sync_interval
        self.log_file_path = log_file_path

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

    pass


# To appear visually nice
def capitalize_string(str):
    if str[0] == str[0].lower():
        return string.capwords(str)
    else:
        return str



def check_input(input_text):
    #print('text',input_text.strip())
    input_lines = [input_text.strip('')]
    while input_text :

            #break
        #print(input_text)
        # Read in the next line of input
        input_text = input().strip()

        # If the line is empty, stop reading in input
        if len(input_lines)>100:
            break

        # Add the line to the list of lines
        input_lines.append(input_text)


    print('input_lines',input_lines)
    return input_lines[0]


def check_path_directory(input_path, folder_key):
    input_path = input_path.strip()
    if os.path.isdir(input_path):
        print(f'{capitalize_string(folder_key)} path is defined\n')
        return input_path

    elif not os.path.isdir(input_path):
        print(f'The given path "{input_path}" does not exist\n')
        while True:
            respond = check_input(input(f'To create a new {folder_key} folder at given path please type "y", to define a new {folder_key} folder please type "n":').strip())
            print('respondis', respond)
            if respond.lower() == 'y':
                os.mkdir(input_path)
                print(f'The {folder_key} folder is created\n')
                return input_path
            elif respond.lower() == 'n':
                terminate = check_path_directory(input(f'Please enter a new path for {folder_key} directory:'), folder_key)
                if isinstance(terminate, str):
                    break
            else:
                print(f'Input is not recognized, please input only "y" or "n"\n')


def check_path_file(input_file):
    #input_file = input_file.strip()
    if os.path.isdir(input_file):
        log_file_directory = check_path_directory(input_file, 'log file')
        input_file = log_file_directory + '\logfile.txt'
        print(f'Synchronization will be logged to {input_file}\n')

    if os.path.exists(input_file):
        while True:
            file_mode = input(
                f'The path "{input_file}" already exists, please type "w" to overwrite or type "a" to append:')
            if file_mode.lower() == 'a' or file_mode.lower() == 'w':
                print(f'Synchronization will be logged to {input_file}\n')
                break
            else:
                print(f'Input is not recognized, please input only "w" or "a"\n')
    else:
        file_mode = 'w'

    return [input_file, file_mode.lower()]


def check_path_identical(path1,path2):
    print('p12',path1,path2)
    while True:
        if path1 == path2:
            if path2 == "":
                check_path_directory(path2, 'replica')
            else:
                print(f'The path for source and replica folder can not be identical\n')
                path_replica = input(f'Please enter the path for the replica folder:').strip(' ')
                print('pp23',path_replica)
                check_path_identical(path1, path_replica)
        else:
            non_identical_replica = check_path_directory(path2, 'replica')
            return non_identical_replica

def check_sync_interval():
    while True:
        try:
            sync_interval = int(input(f'Please enter the synchronization interval in seconds:'))
            if sync_interval > 0:
                print(f'Synchronization interval is defined\n')
                return sync_interval
            else:
                print(f'Synchronization interval must be a positive integer\n')
        except:
            print(f'Synchronization interval must be a positive integer\n')




def main():


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

    test = InputTest()
    test.check_user_input()


if __name__ == '__main__':
    main()
