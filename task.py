# variant 8(23) - json
import functools
import json
import logging
import os
from typing import Any, Callable, Type


class FileOperationError(Exception):
    """Base exception for file operations."""


class FileNotFound(FileOperationError):
    """Exception raised when the target file does not exist."""

    def __init__(self, file_path: str, message: str | None = None) -> None:
        self.file_path = file_path
        super().__init__(message or f"File not found at path: '{file_path}'")


class FileCorrupted(FileOperationError):
    """Exception raised when a file is corrupted or cannot be read/written."""

    def __init__(self, file_path: str, message: str | None = None) -> None:
        self.file_path = file_path
        super().__init__(
            message or f"File is corrupted or inaccessible for reading/writing: '{file_path}'"
        )


def logged(
    exception: Type[Exception] | tuple[Type[Exception], ...],
    mode: str = "console",
    log_file: str = "file_operations.txt",
) -> Callable:
    """
    Parameterized decorator for logging file operations and catching specified exceptions.

    :param exception: Exception class (or tuple of exception classes) to log when raised.
    :param mode: Logging mode — either "console" or "file".
    :param log_file: Path to the text file used for logging when mode is "file".
    """
    if mode not in ("console", "file"):
        raise ValueError("Unsupported logging mode. Use 'console' or 'file'.")

    logger_name = f"json_file_logger.{mode}.{log_file}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        if mode == "console":
            handler: logging.Handler = logging.StreamHandler()
        else:
            handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            operation_name = func.__name__
            logger.info("Executing operation '%s'...", operation_name)
            try:
                result = func(*args, **kwargs)
                logger.info("Operation '%s' completed successfully.", operation_name)
                return result
            except exception as exc:
                logger.error(
                    "Exception in method '%s' [%s]: %s",
                    operation_name,
                    type(exc).__name__,
                    exc,
                )
                raise

        return wrapper

    return decorator


class JsonFileManager:
    """Class for safely reading, writing, and appending data to a JSON file."""

    @logged((FileNotFound, FileCorrupted), mode="file", log_file="file_operations.txt")
    def __init__(self, directory_path: str, file_name: str) -> None:
        self.directory_path = directory_path
        self.file_name = file_name
        self.full_path = os.path.join(directory_path, file_name)

        if not os.path.isfile(self.full_path):
            raise FileNotFound(self.full_path)

        if not os.access(self.full_path, os.R_OK):
            raise FileCorrupted(
                self.full_path,
                f"No read permissions for file: '{self.full_path}'",
            )

    @logged((FileNotFound, FileCorrupted), mode="console")
    def read(self) -> Any:
        """Reads and returns data from the JSON file."""
        if not os.path.isfile(self.full_path):
            raise FileNotFound(self.full_path)

        try:
            with open(self.full_path, mode="r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError, PermissionError, OSError) as exc:
            raise FileCorrupted(
                self.full_path,
                f"Read error or corrupted JSON structure in '{self.full_path}': {exc}",
            ) from exc

    @logged((FileNotFound, FileCorrupted), mode="file", log_file="file_operations.txt")
    def write(self, data: Any) -> None:
        """Overwrites the JSON file with new data."""
        if not os.path.isfile(self.full_path):
            raise FileNotFound(self.full_path)

        try:
            serialized_data = json.dumps(data, ensure_ascii=False, indent=4)
        except (TypeError, ValueError) as exc:
            raise FileCorrupted(
                self.full_path,
                f"Provided data cannot be serialized to JSON: {exc}",
            ) from exc

        try:
            with open(self.full_path, mode="w", encoding="utf-8") as file:
                file.write(serialized_data)
        except (PermissionError, OSError) as exc:
            raise FileCorrupted(
                self.full_path,
                f"Unable to write to file '{self.full_path}': {exc}",
            ) from exc

    @logged((FileNotFound, FileCorrupted), mode="file", log_file="file_operations.txt")
    def append(self, data: Any) -> None:
        """
        Appends data to the JSON file while preserving existing content and valid JSON structure:
        - if the root element is a list, appends an item or extends the list;
        - if the root element is a dict and new data is also a dict, updates the dictionary.
        """
        existing_data = self.read()

        if isinstance(existing_data, list):
            if isinstance(data, list):
                existing_data.extend(data)
            else:
                existing_data.append(data)
        elif isinstance(existing_data, dict) and isinstance(data, dict):
            existing_data.update(data)
        else:
            raise FileCorrupted(
                self.full_path,
                "Cannot append data: root JSON type in the file is incompatible with the new data.",
            )

        self.write(existing_data)


if __name__ == "__main__":
    work_dir = "."
    valid_file = "users.json"
    full_file_path = os.path.join(work_dir, valid_file)

    with open(full_file_path, "w", encoding="utf-8") as f:
        json.dump([{"id": 1, "name": "Olena"}], f, ensure_ascii=False, indent=4)

    manager = JsonFileManager(work_dir, valid_file)
    print("Initial content:", manager.read())

    manager.append({"id": 2, "name": "Andrii"})
    print("After append:", manager.read())

    manager.write([{"id": 10, "name": "Maria"}])
    print("After write:", manager.read())

    try:
        JsonFileManager(work_dir, "non_existent.json")
    except FileNotFound as e:
        print("Caught expected exception:", e)

    with open(full_file_path, "w", encoding="utf-8") as f:
        f.write("{broken_json: [1, 2,")

    try:
        manager.read()
    except FileCorrupted as e:
        print("Caught expected exception:", e)