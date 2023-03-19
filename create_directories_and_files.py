import os
import random
import string
from shutil import copy2
from datetime import datetime
from platform import system


class GenerateRandom:
    """This class runs over the source and replica and populates them based on max_depth, max_files, max_dirs
    if those directories empty

    max_depth -- defines the maximum number of sub directory levels in a directory
    max_files -- defines the maximum number of files in a directory
    max_dirs -- defines the maximum number of directory in a directory

    To test the ability of the FolderSync class (copy detection, content detection if the filename is same)
    the random file generator has the following abilities

            Creates a file at path1 with content1
            Creates a file at path2 with content1 -- basically copies
            Creates a file at path2 with content2 -- to test the content of the file when file paths in source and
                                                     replica folder matches
    """

    def __init__(self, path_source, path_replica):

        self.path_source = path_source
        self.path_replica = path_replica
        self.intersection_list = []

    @staticmethod
    def log(path, filename, key):
        """ This method simply logs out the created files based on whether they have identical or different content"""
        current_time = datetime.now().strftime("%H:%M:%S")
        with open(os.path.join(path, 'FILES_INFO.txt'), 'a') as f:
            if key == 'another':
                f.write(f'[ {current_time} ] DIFFERENT CONTENT --- {filename}\n')
            elif key == 'same':
                f.write(f'[ {current_time} ] IDENTICAL CONTENT --- {filename}\n')

    def run(self, max_depth, max_files, max_dirs):
        """This method runs the other methods"""
        path_1 = self.path_source
        path_2 = self.path_replica


        self.generate_random_directories(path_1, path_2, max_depth, max_files, max_dirs)

        return self.count_files_dirs_recurs(path_1), self.count_files_dirs_recurs(path_2), self.intersection_list

    @staticmethod
    def count_files_dirs(path):
        """This method counts the directories and files in a given path"""
        files = 0
        dirs = 0
        for dirpath, dirnames, filenames in os.walk(path):
            dirs += len(dirnames)
            files += len(filenames)
            break

        return [files, dirs]

    @staticmethod
    def count_files_dirs_recurs(path):
        """This method counts the directories and files in a given path"""
        files = 0
        dirs = 0
        for dirpath, dirnames, filenames in os.walk(path):
            dirs += len(dirnames)
            files += len(filenames)


        return [files, dirs]

    @staticmethod
    def create_directory(dir_path):
        """This method handles error if for any reason directory creation using os.makedirs fails"""
        try:
            os.makedirs(dir_path)
        except OSError as e:
            print(f"Error creating directory {dir_path}: {e}")


    def _generate_random_files(self, target_path, target_path_2, num_files):
        """This method generates random files with all same filename

        Possible outcomes can be following

            Creates a file at path1 with content1
            Creates a file at path2 with content1
            Creates a file at path2 with content2 -- to test the content of the file when file paths in source and
                                                     replica folder matches
        """
        # Check all the files in given paths and break if the max files is reached
        if self.count_files_dirs(target_path)[0] >= num_files:
            return

        for i in range(num_files):
            # Generate random filename
            filename = ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + '.txt'
            # Generate random content for file
            content = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(10, 100)))
            content_2 = ''.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(10, 100)))

            # Write file to path1
            with open(os.path.abspath(os.path.join(target_path, filename)), 'w') as f:
                f.write(content)

            if target_path == target_path_2:
                continue

            # Write another file with different content but with same filename at path2 based on probability
            dice_roll = random.randint(10, 100)
            if dice_roll > 40:
                # Check if max file is reached
                if self.count_files_dirs(target_path_2)[0] < num_files:
                    # Check if the path exists
                    if not os.path.isdir(os.path.join(target_path_2)):
                        self.create_directory(target_path_2)
                        with open(os.path.abspath(os.path.join(target_path_2, filename)), 'w') as f:
                            f.write(content_2)

                        self.log(self.path_source, os.path.abspath(os.path.join(target_path, filename)), 'another')

                        # It is observed that os.path.relpath(target_path,self.path_source) command returns
                        # a path that is either relative directory path or a path starts with ../ due to target_path
                        # shifting between self.path_source and self.path_replica i.e.
                        # for C:\Users\user.FBTSB1\OneDrive\Desktop\test_sync_folder\replica_folder\krnvnipivh\fxhnmslvyv\zgbjoxuygw\qnmvtsbdob.txt
                        # ..\replica_folder\krnvnipivh\fxhnmslvyv\zgbjoxuygw\qnmvtsbdob.txt
                        # or
                        # for C:\Users\user.fbtsb1\onedrive\Desktop\test_sync_folder\src_folder\krnvnipivh\pswqloakqm\gipvrelcnr\rivoqxmvgj.txt
                        # krnvnipivh\pswqloakqm\gipvrelcnr\rivoqxmvgj.txt
                        dirnames_and_file = os.path.join(os.path.relpath(target_path, self.path_source), filename)
                        if dirnames_and_file[0:2] == '..':
                            if system == 'Windows':
                                dirnames_and_file = os.path.join(*dirnames_and_file.split(os.sep)[2:])
                            elif (system == 'Linux') or (system == 'Darwin'):
                                dirnames_and_file = os.path.join(*dirnames_and_file.split(os.sep)[2:])

                        self.intersection_list.append(dirnames_and_file)

                continue

            # Write another file with same content and filename at path2 based on probability
            dice_roll_2 = random.randint(10, 100)
            if dice_roll_2 > 40:
                # Check if max file is reached
                if self.count_files_dirs(target_path_2)[0] < num_files:
                    # Check if the path exists
                    if not os.path.isdir(os.path.join(target_path_2)):
                        self.create_directory(target_path_2)
                        copy2(os.path.join(target_path, filename), os.path.join(target_path_2, filename))

                        self.log(self.path_source, os.path.abspath(os.path.join(target_path, filename)), 'same')

                        dirnames_and_file = os.path.join(os.path.relpath(target_path, self.path_source), filename)
                        if dirnames_and_file[0:2] == '..':
                            if system == 'Windows':
                                dirnames_and_file = os.path.join(*dirnames_and_file.split(os.sep)[2:])
                            elif (system == 'Linux') or (system == 'Darwin'):
                                dirnames_and_file = os.path.join(*dirnames_and_file.split(os.sep)[2:])

                        self.intersection_list.append(dirnames_and_file)


    def generate_random_directories(self, path_1, path_2, max_depth, max_files, max_dirs):
        """This method generates random directories and sub-directories in source and replica folders.
        It also populates those directories with random files in a probabilistic fashion.
        """
        paths = [path_1, path_2]

        if (max_depth == 0) or max_dirs == 0:
            # Write random files at source or replica path
            # Check if max file is reached at source
            if self.count_files_dirs(self.path_source, )[0] < max_files:
                self._generate_random_files(self.path_source, self.path_replica, random.randint(0, max_files))
            elif path_1 != path_2:
                # Check if max file is reached at replica path
                if self.count_files_dirs(self.path_replica, )[0] < max_files:
                    self._generate_random_files(self.path_replica, self.path_replica, random.randint(0, max_files))

        else:
            # Generate directories and sub directories as well as random files (in random numbers) in recursive fashion
            # both at source and replica folder
            for path in paths:
                copy_path = paths[(len(paths) - (paths.index(path)) - 1)]

                for i in range(random.randint(1, max_dirs)):
                    dir_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
                    dir_path = os.path.join(path, dir_name)
                    dir_path_2 = os.path.join(copy_path, dir_name)
                    # Create directory if max directory number is not reached at path1
                    if self.count_files_dirs(path)[1] < max_dirs:
                        self.create_directory(dir_path)
                        # Populate the directory with random amount of files (0 -- max_files)
                        self._generate_random_files(dir_path, dir_path_2,
                                                    random.randint(0, max_files))
                        # Proceed with the subdirectories
                        self.generate_random_directories(dir_path, dir_path_2, max_depth - 1,
                                                         max_files, max_dirs)

                    else:
                        # Create directory if max directory number is not reached at path2
                        if self.count_files_dirs(copy_path)[1] < max_dirs:
                            self.create_directory(dir_path_2)
                            # Populate the directory with random amount of files (0 -- max_files)
                            self._generate_random_files(dir_path_2, dir_path,
                                                        random.randint(0, max_files))
                            # Proceed with the subdirectories
                            self.generate_random_directories(dir_path_2, dir_path,
                                                             max_depth - 1, max_files, max_dirs)

                        # If max dir is reached at replica path, check whether the max file is reached
                        if self.count_files_dirs(copy_path)[0] < max_files:
                            self._generate_random_files(copy_path, copy_path,
                                                        random.randint(0, max_files))


