import os
import random
import string
from shutil import copy2


class GenerateRandom:

    def __init__(self, path_source, path_replica):

        self.path_source = path_source
        self.path_replica = path_replica

    @staticmethod
    def log(path, filename, key):
        """ This method simply logs out the created files based on whether they have identical or different content"""
        with open(os.path.join(path, 'FILES_INFO.txt'), 'a') as f:
            if key == 'another':
                f.write(f' DIFFERENT CONTENT --- {filename}\n')
            else:
                f.write(f' IDENTICAL CONTENT --- {filename}\n')

    @staticmethod
    def count_files_dirs(path, num_files, num_dirs):
        files = 0
        dirs = 0
        for dirpath, dirnames, filenames in os.walk(path):
            dirs += len(dirnames)
            files += len(filenames)
            break

        # if files >= num_files:
        #     print('exit max files')
        #     return 'file'
        # elif dirs >= num_dirs:
        #     print('exit max dir')
        #     return 'dir'
        # else:
        #     print('continue')
        #     return 'continue'
        return [files, dirs]

    def _generate_random_files(self, target_path, target_path_2, num_files, max_dirs):
        """This method generates random files with all same filename

        Possible outcomes can be following

            Creates a file at path1 with content1
            Creates a file at path2 with content1
            Creates a file at path2 with content2 -- to test the content of the file when file paths in source and
                                                     replica folder matches
        """
        # Check all the files in given paths and break if the max files is reached
        if self.count_files_dirs(target_path, num_files, max_dirs)[0] >= num_files:
            print(f'Maximum file number is by generate_random reached at {target_path}')
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
            print(f'The file {os.path.join(target_path, filename)} has been created')

            # Write another file with different content but with same filename at path2 based on probability
            dice_roll = random.randint(10, 100)
            if dice_roll > 40:
                # Check the path2 exists
                if not os.path.isdir(os.path.join(target_path_2)):
                    os.makedirs(target_path_2)
                    with open(os.path.abspath(os.path.join(target_path_2, filename)), 'w') as f:
                        f.write(content_2)
                print(
                    f'The file with another content but same path {os.path.join(target_path_2, filename)} has been created')

                self.log(self.path_source, os.path.abspath(os.path.join(target_path, filename)), 'another')

            # Write another file with same content and filename at path2 based on probabality
            dice_roll_2 = random.randint(10, 100)
            if dice_roll_2 > 10:
                if not os.path.isdir(os.path.join(target_path_2)):
                    os.makedirs(target_path_2)
                    copy2(os.path.join(target_path, filename), os.path.join(target_path_2, filename))
                    print(
                        f'The file {os.path.join(target_path, filename)} has been copied to {os.path.join(target_path_2, filename)} ')

                    self.log(self.path_source, os.path.abspath(os.path.join(target_path, filename)), 'same')

    def generate_random_directories(self, max_depth, max_files, max_dirs):
        """This method generates random directories and sub-directories in source and replica folders.
        It also populates those directories with random files in a probabilistic fashion.
        TODO:Although max depth functionality works, max file needs improvement
        """
        paths = [self.path_source, self.path_replica]

        if max_depth == 0:
            # Base case, generate random files to destination
            if self.count_files_dirs(self.path_source, max_files, max_dirs)[0] < max_files:
                # Max file number is not reached, continue
                print(f'Continue creating file via folder at {self.path_source}')
                self._generate_random_files(self.path_source, self.path_replica, random.randint(0, max_files),max_dirs)
            else:
                print(f'Maximum file number is reached at {self.path_source}')
                # Max file number is reached, swap paths to create files path2
                if self.count_files_dirs(self.path_replica, max_files, max_dirs)[0] < max_files:
                    print(f'Continue creating file via folder at {self.path_replica}')
                    self._generate_random_files(self.path_replica, self.path_replica, random.randint(0, max_files), max_dirs)

        else:
            # Iterate over paths to give chance the probabilistic file creation
            for path in paths:
                print((self.count_files_dirs(path, max_files, max_dirs)))
                print((self.count_files_dirs(path, max_files, max_dirs))[1])
                copy_path = paths[(len(paths) - (paths.index(path)) - 1)]
                # Generate subdirectories and recurse
                for i in range(random.randint(1, max_dirs)):
                    dir_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
                    dir_path = os.path.join(path, dir_name)
                    # If max dir is not reached at source path, continue
                    if self.count_files_dirs(path, max_files, max_dirs)[1] < max_dirs:
                        print(f'dir creation continue at {path}')
                        os.makedirs(dir_path)
                        print(f'The directory {dir_path} has been crated')
                        #self.path_source = dir_path
                        self.generate_random_directories(max_depth - 1, max_files, max_dirs)
                        # Generate random files under sub directories as well
                        self._generate_random_files(dir_path, os.path.join(copy_path, dir_name),
                                                    random.randint(0, max_files), max_dirs)
                    # If max dir is reached at source path
                    else:
                        print(f'Maximum dir number is reached at {path}')
                        dir_path_2 = os.path.join(copy_path, dir_name)
                        # If max dir is not reached at replica path, continue
                        if self.count_files_dirs(copy_path, max_files, max_dirs)[1] < max_dirs:

                        #self.path_source = copy_path
                        #self.path_replica = path
                            print(f'dir creation continue at {copy_path}')
                            os.makedirs(dir_path_2)
                            print(f'The directory {dir_path_2} has been crated')
                            self.generate_random_directories(max_depth - 1, max_files, max_dirs)
                            self._generate_random_files(dir_path_2, dir_path,
                                                    random.randint(0, max_files), max_dirs)
                        # If max dir is reached at replica path, check whether the max file is reached
                        else:
                            if self.count_files_dirs(copy_path, max_files, max_dirs)[0] < max_files:
                                self._generate_random_files(dir_path_2, dir_path,
                                                            random.randint(0, max_files), max_dirs)
                        # If max file is not reached at replica+dir_name path, stop directory creation
                        #if self.count_files_dirs(dir_path_2, max_files, max_dirs)[0] < max_files:
                        #    self._generate_random_files(dir_path_2, dir_path,
                        #                                random.randint(0, max_files), max_dirs)
                        #    return


