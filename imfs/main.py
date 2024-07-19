from pathlib import Path

MOCKED_DIR_STRUCTURE = {
    "/": {
        "__type": "dir",
        "root": {
            "__type": "dir",
            "unordered_dir2": {
                "__type": "dir",
            },
            "unordered_dir100": {
                "__type": "dir",
            },
            "empty_dir": {
                "__type": "dir",
                "empty_dir_2": {
                    "__type": "dir",
                },
            },
            "existing_file.txt": {"__type": "file", "__content": "Hello, World!"},
        },
    }
}


def set_state(state):
    # Python imports are cached, so we need to expose
    # a way for the tests to reset the state
    global MOCKED_DIR_STRUCTURE
    MOCKED_DIR_STRUCTURE = state


def _get_path(path: str | Path) -> Path:
    path = Path(path)
    curr_dict = MOCKED_DIR_STRUCTURE
    for p in Path(path).parts:
        if p not in curr_dict:
            raise KeyError("Path not found")
        curr_dict = curr_dict[p]
    return curr_dict


def ls(path: str | Path) -> list[str]:
    path = Path(path)

    try:
        # return the lexicographically sorted list
        path_dict = _get_path(path)
        if path_dict["__type"] == "file":
            return [path.parts[-1]]
        return sorted([k for k in path_dict.keys() if not k.startswith("__")])
    except KeyError:
        raise FileNotFoundError("ls: Path not found")


def mkdir(path: str | Path, exists_ok: bool = False) -> None:
    path = Path(path)
    try:
        # if the path is not found, it'll raise a FileNotFoundError
        # so if ls(path) succeeds, we should raise on mkdir
        # (it's a bit backwards, but it works!)
        _get_path(path)
        if not exists_ok:
            raise FileExistsError("mkdir: Path already exists")
    except KeyError:
        curr_dict = MOCKED_DIR_STRUCTURE  # do not copy here
        for p in Path(path).parts:
            # if the current p doesn't exist, create it
            if p not in curr_dict:
                curr_dict[p] = {"__type": "dir"}
            curr_dict = curr_dict[p]


def touch(path: str | Path) -> None:
    path = Path(path)

    # if the path already exists, raise an error
    try:
        _get_path(path)
        raise FileExistsError("touch: Path already exists")
    except KeyError:
        pass

    # If the path is not found, create the parents using mkdir and then create the file
    mkdir(path.parent, exists_ok=True)

    curr_dict = MOCKED_DIR_STRUCTURE
    for p in path.parts[:-1]:
        if p not in curr_dict:
            curr_dict[p] = {"__type": "dir"}
        curr_dict = curr_dict[p]
    curr_dict[path.parts[-1]] = {"__type": "file"}


def read_content_from_file(path: str | Path) -> str:
    path = Path(path)
    try:
        curr_dict = _get_path(path)
        # If it's not a file, raise an error
        if not curr_dict["__type"] == "file":
            raise FileNotFoundError("read_content_from_file: Path is not a file")
    except KeyError:
        # If the path is not found, raise an error
        raise FileNotFoundError(f"read_content_from_file: {path} does not exist")

    # Otherwise, return the content of the file or an empty string
    return curr_dict.get("__content", "")


def add_content_to_file(path: str | Path, content: str) -> None:
    path = Path(path)

    try:
        # Create the file if it doesn't exist
        touch(path)
    except FileExistsError:
        pass

    curr_dict = _get_path(path)
    curr_dict["__content"] = curr_dict.get("__content", "") + content


def app():
    print(MOCKED_DIR_STRUCTURE)
