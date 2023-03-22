import os
import tempfile
import pytest

from folder_sync import FolderSync


# arrange, act, assert, cleanup
# fixtures are certain prerequisite/setup that you can achieve prior to running
# (prior to doing an act for particular test case)

# the steps that are needed prior to executing the test case as a predifined steps so that they will be executed
# prior to every test case


@pytest.fixture
def two_dirs():
    # Use tempfile.mkdtemp to create two separate temporary directories
    path1 = tempfile.mkdtemp()
    path2 = tempfile.mkdtemp()
    # Return both paths as a tuple
    yield path1, path2
    # Clean up the temporary directories after the test
    for path in [path1, path2]:
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
    os.rmdir(path)


def test_log(two_dirs):
    # create a temporary log file and test the log method
    dir1, dir2 = two_dirs
    filename = os.path.join(dir1, 'test.log')
    log_string = 'Test log string'
    key = 'green'
    FolderSync.log(log_string, filename, key)
    with open(filename, 'r') as f:
        assert log_string in f.read()

def test_compare_and_match(two_dirs):
    # Create temporary directories and files for testing
    dir1, dir2 = two_dirs

    with open(os.path.join(dir1, 'file1.txt'), 'w') as f:
        f.write('This is file 1')
    with open(os.path.join(dir1, 'file2.txt'), 'w') as f:
        f.write('This is file 2')
    with open(os.path.join(dir2, 'file2.txt'), 'w') as f:
        f.write('This is file 2 in replica with diff context')

    with open(os.path.join(dir2, 'file3.txt'), 'w') as f:
        f.write('This is file 3')

    # Call the compare_and_match function
    instance = FolderSync(dir1, dir2, 4, 'test.log')
    diff_to_copy, diff_to_remove, file_content_not_matching = instance.compare_and_match()

    # A file simply does not exist in replica
    assert 'file1.txt' in diff_to_copy
    # A file exist in replica but content is not matching
    assert 'file2.txt' in file_content_not_matching
    assert 'file2.txt' in diff_to_copy
    # A file does not exist in replica
    assert 'file3.txt' in diff_to_remove



def test_copy_file(two_dirs):
    dir1, dir2 = two_dirs
    # create a file and test the _copy_file method
    file1 = os.path.join(dir1, 'file1.txt')
    file2 = os.path.join(dir2, 'file2.txt')
    with open(file1, 'w') as f:
        f.write('Test file 1')
    sync = FolderSync(dir1, dir2, 1, 'test.log')
    sync._copy_file(file1, file2)
    assert os.path.exists(file2)
    with open(file2, 'r') as f:
        assert f.read() == 'Test file 1'


def test_remove_file(two_dirs):
    dir1, dir2 = two_dirs
    file1 = os.path.join(dir1, 'file1.txt')
    with open(file1, 'w') as f:
        f.write('Test file 1')
    sync = FolderSync(dir1, dir1, 1, 'test.log')
    sync._remove_file(file1)
    assert not os.path.exists(file1)


def test_check_sys_args_valid(two_dirs):
    # test the check_sys_args method with valid arguments
    dir1, dir2 = two_dirs
    sync = FolderSync(dir1, dir2, 1, 'test.log')
    assert sync.check_sys_args() is None


def test_check_sys_args_invalid_source(two_dirs):
    # test the check_sys_args method with invalid paths
    dir1, dir2 = two_dirs
    sync = FolderSync('/invalid/path', dir2, 1, 'test.log')
    with pytest.raises(ValueError):
        sync.check_sys_args()


def test_check_sys_args_invalid_replica(two_dirs):
    # test the check_sys_args method with invalid paths
    dir1, dir2 = two_dirs
    sync = FolderSync(dir1, '/invalid/path', 1, 'test.log')
    with pytest.raises(ValueError):
        sync.check_sys_args()


def test_check_sys_args_identical(two_dirs):
    # test the check_sys_args method with identical paths
    dir1, dir2 = two_dirs
    sync2 = FolderSync(dir1, dir1, 1, 'test.log')
    with pytest.raises(ValueError):
        sync2.check_sys_args()


def test_check_sys_args_log_is_dir(two_dirs):
    # test the check_sys_args method with invalid log file path
    dir1, dir2 = two_dirs
    sync3 = FolderSync(dir1, dir2, 1, dir2)
    with pytest.raises(ValueError):
        sync3.check_sys_args()


def test_check_sys_args_invalid_sync(two_dirs):
    # test the check_sys_args method with invalid sync interval
    dir1, dir2 = two_dirs
    sync4 = FolderSync(dir1, dir2, -1, 'logfile.log')
    with pytest.raises(ValueError):
        sync4.check_sys_args()
    print('Passed bla bla')
