# Design an in-memory file system to simulate the following functions:

from copy import deepcopy

import pytest

from .main import (
    add_content_to_file,
    app,
    ls,
    mkdir,
    MOCKED_DIR_STRUCTURE,
    read_content_from_file,
    set_state,
)

ORIGINAL_DIR_L1 = [
    "empty_dir",
    "existing_file.txt",
    "unordered_dir100",
    "unordered_dir2",
]

ORIG_DIR_STRUCTURE = deepcopy(MOCKED_DIR_STRUCTURE)


# Create an auto-use fixture to reset the MOCKED_DIR_STRUCTURE
@pytest.fixture(autouse=True, scope="function")
def reset_mocked_dir_structure():
    set_state(deepcopy(ORIG_DIR_STRUCTURE))


class TestImfs:
    def test_app_runs(self):
        app()

    def test_ls_returns_top_level_objects(self):
        assert ls("/root") == ORIGINAL_DIR_L1

    def test_ls_returns_from_nested_path(self):
        assert ls("/root/empty_dir") == ["empty_dir_2"]

    def test_ls_returns_file(self):
        assert ls("/root/existing_file.txt") == ["existing_file.txt"]

    def test_mkdir_creates_new_dir(self):
        assert mkdir("/root/new_dir") == None
        expected_dir_l1 = [*ORIGINAL_DIR_L1[:2], "new_dir", *ORIGINAL_DIR_L1[2:]]
        assert ls("/root") == expected_dir_l1

    def test_mkdir_errors_on_existing_dir(self):
        with pytest.raises(FileExistsError):
            mkdir("/root/empty_dir")

        assert ls("/root") == ORIGINAL_DIR_L1

    # Read the content of the file
    def test_read_content_from_file(self):
        assert read_content_from_file("/root/existing_file.txt").strip() == "Hello, World!"

    # Create a new file if it doesn't exist
    # Append the content to the file if it exists
    def test_add_content_to_new_file(self):
        # check the file doesn't exist
        with pytest.raises(FileNotFoundError):
            read_content_from_file("/root/brand_new_file.txt")
        assert add_content_to_file("/root/brand_new_file.txt", "Hello, Universe!") == None

    def test_append_content_to_existing_file(self):
        # check the file exists and has the original content
        assert read_content_from_file("/root/existing_file.txt").strip() == "Hello, World!"
        assert add_content_to_file("/root/existing_file.txt", "\nGoodbye, Moon.") == None
        # check the content has been appended
        assert (
            read_content_from_file("/root/existing_file.txt").strip()
            == "Hello, World!\nGoodbye, Moon."
        )
