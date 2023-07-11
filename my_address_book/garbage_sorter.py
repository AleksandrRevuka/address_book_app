"""Sort garbage"""
import os
import shutil

from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore
from queue import Queue
from typing import NamedTuple, List, Dict, Tuple, Union

from my_address_book.error import input_error

DIRECTORY = {
    "images": "images",
    "video": "video",
    "documents": "documents",
    "audio": "audio",
    "archives": "archives",
    "unknown_extensions": "unknown_extensions",
}

IMAGES_EXTENSIONS = [".JPEG", ".PNG", ".JPG", ".SVG", ".IMG"]
VIDEO_EXTENSIONS = [".AVI", ".MP4", ".MOV", ".MKV", ".FLV"]
DOCUMENTS_EXTENSIONS = [".DOC", ".DOCX", ".TXT", ".PDF", ".XLSX", ".PPTX"]
AUDIO_EXTENSIONS = [".MP3", ".OGG", ".WAV", ".AMR"]
ARCHIVES_EXTENSIONS = [".ZIP", ".GZ", ".TAR"]

folders_ext = [IMAGES_EXTENSIONS, VIDEO_EXTENSIONS, DOCUMENTS_EXTENSIONS, AUDIO_EXTENSIONS, ARCHIVES_EXTENSIONS]

FOLDERS_WITH_EXT: Dict[str, List[str]] = dict(zip(DIRECTORY.values(), folders_ext))


class InfoFile(NamedTuple):
    """File information"""

    name: str
    extension: str
    path: str
    old_path: str
    folder: str
    new_name: str


def check_for_repetition_of_names(file_info: InfoFile, move_files: Queue) -> str:
    """
    The function checks if a file with the given name already exists in the destination directory.
    If it does, the function adds a "_copy{number}" suffix to the name and returns the new name.
    If the new name is also taken, it increments the number and tries again until it finds an
    available name. If the given name is not taken, the function returns the original name.
    """
    name = file_info.name
    file_extension = f"{name}{file_info.extension}"

    if file_extension in move_files.queue:
        copy_number = 1
        while True:
            new_name = f"{name}_copy{copy_number}"
            new_name_extension = f"{new_name}{file_info.extension}"

            if new_name_extension not in move_files.queue:
                return new_name
            copy_number += 1
    else:
        return name


def move_the_file(file_info: InfoFile) -> str:
    """The function moves a file from the old location to the new location."""

    file_name_extension = f"{file_info.name}{file_info.extension}"
    file_old = os.path.join(file_info.old_path, file_name_extension)
    path_file_new = os.path.join(file_info.path, file_info.folder)

    file_new_name_extension = f"{file_info.new_name}{file_info.extension}"
    file_new = os.path.join(path_file_new, file_new_name_extension)
    try:
        shutil.move(file_old, file_new)

    except PermissionError:
        raise PermissionError(f"Error: Permission denied. Unable to move the file {file_old}.")

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File {file_old} or directory not found.")

    return file_new_name_extension


def extract_files_from_archive(file_info: InfoFile) -> bool:
    """
    This function creates a new directory with the same name as the archive file in the
    directory where the archive file is located. The files in the archive are then extracted
    into this new directory using the `shutil.unpack_archive()` function from the `shutil`
    module.
    """

    archive_name = f"{file_info.new_name}{file_info.extension}"
    archive_path = os.path.join(file_info.path, file_info.folder)
    path_to_unpack = os.path.join(archive_path, file_info.new_name)
    archive_path_full = os.path.join(archive_path, archive_name)

    try:
        os.mkdir(path_to_unpack)
        shutil.unpack_archive(archive_path_full, path_to_unpack)

    except PermissionError:
        raise PermissionError(f"Error: Permission denied. Failed to create folder {path_to_unpack}.")

    except RuntimeError:
        raise RuntimeError(f"Error: Archive {archive_name} is encrypted, password required for extraction")

    return True


def file_controller(condition, file_info: InfoFile, move_files: Queue) -> None:
    """
    The function iterates through the given dictionary containing file information, normalizes
    the file names, and checks for name repetitions. It then moves the files to their designated
    folders and extracts any files from archives. Finally, it returns a new dictionary containing
    the updated file information.
    """
    try:
        with condition:
            file_name_new = check_for_repetition_of_names(file_info, move_files)

            file_info_new = InfoFile(
                file_info.name, file_info.extension, file_info.path, file_info.old_path, file_info.folder, file_name_new
            )

            if DIRECTORY["archives"] == file_info.folder:
                move_file_info: str = move_the_file(file_info_new)
                move_files.put(move_file_info)
                message: bool = extract_files_from_archive(file_info_new)
                move_files.put(message)
            else:
                move_file_info = move_the_file(file_info_new)
                move_files.put(move_file_info)

    except Exception as error:
        move_files.put(str(error))


def check_extension(extension: str) -> str:
    """
    Check if the given file extension is present in the list of extensions associated
    with any folder in the FOLDERS_WITH_EXT dictionary.
    """
    for key, ext in FOLDERS_WITH_EXT.items():
        if extension.upper() in ext:
            return key
    return ""


def sorting_files_into_folders(data_files: Dict[int, InfoFile]) -> Tuple[Dict[int, InfoFile], Dict[int, InfoFile]]:
    """
    The function categorizes files into known and unknown file types based on their file
    extension. Files with known extensions are sorted into corresponding folders, while
    files with unknown extensions are sorted into an 'unknown' folder.
    """
    known_files = {}
    unknown_files = {}
    for key, file_info in data_files.items():
        folder = check_extension(file_info.extension)

        if folder:
            known_file_info_new: InfoFile = InfoFile(
                file_info.name, file_info.extension, file_info.path, file_info.old_path, folder, ""
            )
            known_files[key] = known_file_info_new

        else:
            folder = DIRECTORY["unknown_extensions"]
            unknown_file_info_new: InfoFile = InfoFile(
                file_info.name, file_info.extension, file_info.path, file_info.old_path, folder, ""
            )
            unknown_files[key] = unknown_file_info_new

    return known_files, unknown_files


def scan_files_and_folders(path: str, root_directory: str) -> Dict[int, InfoFile]:
    """
    The scan_files_and_folders function scans the files and folders in a given directory.
        It returns a dictionary of file information objects, where each key is the hash of
        the file's path and each value is an InfoFile object containing information about that file.

    :param path: str: Specify the path to scan
    :param root_directory: str: Compare the path of the file with it
    :return: A dictionary of objects
    """

    data_files: Dict[int, InfoFile] = {}

    def process_object(unk_object: str) -> None:
        object_path: str = os.path.join(path, unk_object)

        if os.path.isfile(object_path):
            name_file, extension = os.path.splitext(os.path.basename(object_path))
            file_info = InfoFile(name_file, extension, root_directory, path, "", "")
            data_files[hash(object_path)] = file_info

        else:
            if path == root_directory:
                if unk_object.lower() not in DIRECTORY:
                    data_files.update(scan_files_and_folders(object_path, root_directory))
            else:
                data_files.update(scan_files_and_folders(object_path, root_directory))

    objects: list[str] = os.listdir(path)

    with ThreadPoolExecutor() as executor:
        executor.map(process_object, objects)

    return data_files


def del_empty_folders(path: str) -> None:
    """
    The del_empty_folders function deletes empty folders in the directory.

    :param way: Specify the path of the directory
    """
    try:
        for address, dirs, files in os.walk(path, topdown=False):
            for dir in dirs:
                way = os.path.join(address, dir)
                if not os.listdir(way):
                    os.rmdir(way)

    except PermissionError:
        raise PermissionError(f"Error: Permission denied: {way}")


def check_folders(root_path: str) -> bool:
    """
    Checks for the existence of specific folders in a given root path, and creates
    any missing folders.
    """

    folders = list(DIRECTORY)[:-1]

    for folder in folders:
        path_folder = os.path.join(root_path, folder)
        if not os.path.exists(path_folder):
            try:
                os.mkdir(path_folder)
            except PermissionError:
                raise PermissionError(f"Error: Permission denied: {path_folder}")
    return True


@input_error
def sorter_run(folder_path) -> Union[list, bool]:
    """Main controller"""

    check_folders(folder_path)

    data_files = scan_files_and_folders(folder_path, folder_path)

    known_data_files, unknown_data_files = sorting_files_into_folders(data_files)

    move_files: Queue = Queue()
    errors: list = []
    pool = Semaphore(2)
    with ThreadPoolExecutor() as executor:
        for object_file in known_data_files.values():
            executor.submit(
                file_controller,
                pool,
                object_file,
                move_files,
            )

    while not move_files.empty():
        move_file_info = move_files.get()
        if move_file_info.startswith("Error"):
            errors.append(move_file_info)

    del_empty_folders(folder_path)

    if errors:
        return errors

    return False
