import os
import random
import string
from shutil import copy2
from datetime import datetime

class GenerateRandom:

    def __init__(self, path_source, path_replica):

        self.path_source = path_source
        self.path_replica = path_replica

    @staticmethod
    def log(path, filename, key):
        """ This method simply logs out the created files based on whether they have identical or different content"""
        current_time = datetime.now().strftime("%H:%M:%S")
        with open(os.path.join(path, 'FILES_INFO.txt'), 'a') as f:
            if key == 'another':
                f.write(f'[ {current_time} ] DIFFERENT CONTENT --- {filename}\n')
            else:
                f.write(f'[ {current_time} ] IDENTICAL CONTENT --- {filename}\n')

    def run(self, max_depth, max_files, max_dirs):
        """This method runs the other methods"""
        path_1 = self.path_source
        path_2 = self.path_replica

        self.generate_random_directories(path_1, path_2, max_depth, max_files, max_dirs)

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

            # Write another file with different content but with same filename at path2 based on probability
            dice_roll = random.randint(10, 100)
            if dice_roll > 40:
                # Check if max file is reached
                if self.count_files_dirs(target_path_2)[0] < num_files:
                    # Check if the path exists
                    if not os.path.isdir(os.path.join(target_path_2)):
                        os.makedirs(target_path_2)
                        with open(os.path.abspath(os.path.join(target_path_2, filename)), 'w') as f:
                            f.write(content_2)

                    self.log(self.path_source, os.path.abspath(os.path.join(target_path, filename)), 'another')

            # Write another file with same content and filename at path2 based on probability
            dice_roll_2 = random.randint(10, 100)
            if dice_roll_2 > 10:
                # Check if max file is reached
                if self.count_files_dirs(target_path_2)[0] < num_files:
                    # Check if the path exists
                    if not os.path.isdir(os.path.join(target_path_2)):
                        os.makedirs(target_path_2)
                        copy2(os.path.join(target_path, filename), os.path.join(target_path_2, filename))

                    self.log(self.path_source, os.path.abspath(os.path.join(target_path, filename)), 'same')

    def generate_random_directories(self, path_1, path_2, max_depth, max_files, max_dirs):
        """This method generates random directories and sub-directories in source and replica folders.
        It also populates those directories with random files in a probabilistic fashion.
        TODO:Although max depth functionality works, max file needs improvement
        """
        paths = [path_1, path_2]

        if max_depth == 0:
            # Write random files at source or replica path
            # Check if max file is reached at source
            if self.count_files_dirs(self.path_source, )[0] < max_files:
                self._generate_random_files(self.path_source, self.path_replica, random.randint(0, max_files))
            else:
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
                        os.makedirs(dir_path)
                        # Populate the directory with random amount of files (0 -- max_files)
                        self._generate_random_files(dir_path, dir_path_2,
                                                    random.randint(0, max_files))
                        # Proceed with the subdirectories
                        self.generate_random_directories(dir_path, dir_path_2, max_depth - 1,
                                                         max_files, max_dirs)

                    else:
                        # Create directory if max directory number is not reached at path2
                        if self.count_files_dirs(copy_path)[1] < max_dirs:
                            os.makedirs(dir_path_2)
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
