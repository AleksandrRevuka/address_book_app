"""Sort garbage"""
import os
import sys
import shutil

from typing import NamedTuple, List, Dict, Tuple


PUNCTUATION = "#$%&'()*+,-/:;<=>?@[\\]^_`{|}~"  # without "."
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = [
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "y",
    "",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
]

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


def is_folder(test_path: str) -> bool:
    """Checking the path for correctness"""
    if os.path.isdir(test_path):
        return True
    return False


def parse_path() -> str:
    """Get path from input data"""
    return sys.argv[1]


def get_max_depth(path: str) -> int:
    """
    Returns the greatest folder nesting depth for the given path.
    """
    max_depth = 0
    for root, _, __ in os.walk(path):
        depth = root.count(os.sep)
        if depth > max_depth:
            max_depth = depth
    return max_depth


def normalize(name: str) -> str:
    """
    Converts Cyrillic characters in a string to their Latin equivalents, and replaces any
    other non-alphanumeric or non-underscore characters with underscores. Returns the normalized
    string.
    """

    trans = {}
    for key, value in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        trans[ord(key)] = value
        trans[ord(key.upper())] = value.upper()

    trans_name = "".join("_" if symbol in PUNCTUATION else symbol for symbol in name)

    return trans_name.translate(trans)


def check_for_repetition_of_names(file_info: InfoFile, name: str, move_files: list) -> str:
    """
    The function checks if a file with the given name already exists in the destination directory.
    If it does, the function adds a "_copy{number}" suffix to the name and returns the new name.
    If the new name is also taken, it increments the number and tries again until it finds an
    available name. If the given name is not taken, the function returns the original name.
    """

    file_extension = f"{name}{file_info.extension}"

    if file_extension in move_files:
        copy_number = 1
        while True:
            new_name = f"{name}_copy{copy_number}"
            new_name_extension = f"{new_name}{file_info.extension}"

            if new_name_extension not in move_files:
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
    except PermissionError as error:
        print(error)
    except FileNotFoundError as error:
        print(error)
    return file_new_name_extension


def extract_files_from_archive(file_info: InfoFile) -> None:
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
    except PermissionError as error:
        print(error)
    except RuntimeError:
        print(f"Archive {archive_name} is encrypted, password required for extraction")


def file_controller(data_files: Dict[int, InfoFile]) -> Dict[int, InfoFile]:
    """
    The function iterates through the given dictionary containing file information, normalizes
    the file names, and checks for name repetitions. It then moves the files to their designated
    folders and extracts any files from archives. Finally, it returns a new dictionary containing
    the updated file information.
    """

    data_files_new = {}
    move_files: list = []

    for key, file_info in data_files.items():
        file_name_normal = normalize(file_info.name)
        file_name_new = check_for_repetition_of_names(file_info, file_name_normal, move_files)

        file_info_new = InfoFile(
            file_info.name, file_info.extension, file_info.path, file_info.old_path, file_info.folder, file_name_new
        )

        if DIRECTORY["archives"] == file_info.folder:
            move_file_info: str = move_the_file(file_info_new)
            move_files.append(move_file_info)
            extract_files_from_archive(file_info_new)

        else:
            move_file_info = move_the_file(file_info_new)
            move_files.append(move_file_info)

        data_files_new[key] = file_info_new

    return data_files_new


def check_extension(extension: str) -> str | bool:
    """
    Check if the given file extension is present in the list of extensions associated
    with any folder in the FOLDERS_WITH_EXT dictionary.
    """
    for key, ext in FOLDERS_WITH_EXT.items():
        if extension.upper() in ext:
            return key
    return False


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
            file_info_new: InfoFile = InfoFile(
                file_info.name, file_info.extension, file_info.path, file_info.old_path, folder, ""
            )
            known_files[key] = file_info_new

        else:
            file_info_new: InfoFile = InfoFile(
                file_info.name, file_info.extension, file_info.path, file_info.old_path, DIRECTORY["unknown_extensions"], ""
            )
            unknown_files[key] = file_info_new

    return known_files, unknown_files


def scan_files_and_folders(path: str, root_directory: str) -> dict:
    """
    Recursively scans files and folders in the given path, creating and storing relevant file
    information in a dictionary with a hashed key. The function returns a dictionary containing
    all the file information found during the scan.
    """
    data_files = {}

    try:
        objects = os.listdir(path)

        for unk_object in objects:
            object_path = os.path.join(path, unk_object)

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

    except PermissionError:
        print(f"Permission denied: {path}")

    return data_files


def sort_files_for_print(files_info: Dict[int, InfoFile]) -> list:
    """
    Displays the names of files that have been sorted into folders.
    """
    images = []
    video = []
    documents = []
    audio = []
    archives = []

    for file_info in files_info.values():
        if file_info.folder == DIRECTORY["images"]:
            images.append(file_info.new_name + file_info.extension)

        if file_info.folder == DIRECTORY["video"]:
            video.append(file_info.new_name + file_info.extension)

        if file_info.folder == DIRECTORY["documents"]:
            documents.append(file_info.new_name + file_info.extension)

        if file_info.folder == DIRECTORY["audio"]:
            audio.append(file_info.new_name + file_info.extension)

        if file_info.folder == DIRECTORY["archives"]:
            archives.append(file_info.new_name + file_info.extension)

    folders = [images, video, documents, audio, archives]

    return folders


def print_folders(folders: list):
    """Displays the names of files"""

    images, video, documents, audio, archives = folders

    print(f"--> {DIRECTORY['images']}: {images} \n")
    print(f"--> {DIRECTORY['video']}: {video} \n")
    print(f"--> {DIRECTORY['documents']}: {documents} \n")
    print(f"--> {DIRECTORY['audio']}: {audio} \n")
    print(f"--> {DIRECTORY['archives']}: {archives} \n")


def print_extensions(extensions_data: list) -> None:
    """Print extensions"""
    unknown_extensions, known_extensions = extensions_data

    print(f"-> known_extensions: {known_extensions} \n")

    print(f"-> unknown_extensions: {unknown_extensions} \n")


def deletes_empty_folders(path_folder, root_directory) -> None:
    """
    Recursively delete empty folders in the specified path_folder directory.
    """
    try:
        for path_object in os.listdir(path_folder):
            object_full_path = os.path.join(path_folder, path_object)
            if os.path.isdir(object_full_path):
                if path_folder == root_directory:
                    if path_object.lower() not in DIRECTORY:
                        if os.listdir(object_full_path):
                            deletes_empty_folders(object_full_path, root_directory)
                        else:
                            os.rmdir(object_full_path)
                else:
                    if os.listdir(object_full_path):
                        deletes_empty_folders(object_full_path, root_directory)
                    else:
                        os.rmdir(object_full_path)

            elif os.path.isfile(object_full_path):
                continue

    except PermissionError as error:
        print(error)


def extract_the_extension_from_the_data(
    unknown_data_files: Dict[int, InfoFile], data_files_full: Dict[int, InfoFile]
) -> list[list[str]]:
    """
    This function extracts file extensions from two file information dictionaries,
     "unknown_data_files" and "data_files_full", and returns a list of unique extensions.
    """

    un_ext = list({file_info.extension for file_info in unknown_data_files.values()})

    kn_ext = list({file_info.extension for file_info in data_files_full.values()})

    data_extension = [un_ext, kn_ext]

    return data_extension


def check_folders(root_path: str):
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
            except PermissionError as error:
                print(error)


def main(folder_path):
    """Main controller"""

    if is_folder(folder_path):
        check_folders(folder_path)

        data_files = scan_files_and_folders(folder_path, folder_path)

        known_data_files, unknown_data_files = sorting_files_into_folders(data_files)

        data_files_full = file_controller(known_data_files)

        max_depth = get_max_depth(folder_path)

        while max_depth > 0:
            deletes_empty_folders(folder_path, folder_path)
            max_depth -= 1

        data_extension = extract_the_extension_from_the_data(unknown_data_files, data_files_full)

        print_extensions(data_extension)
        folders = sort_files_for_print(data_files_full)
        print_folders(folders)

    else:
        print("Something wrong, try again")


if __name__ == "__main__":
    path_in = parse_path()
    main(path_in)
