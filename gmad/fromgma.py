"""Extract .gmas to folders."""
from os.path import exists as path_exists
from os.path import dirname as path_get_directory
from os.path import join as path_join
from os.path import splitext as path_ext
from os import makedirs as path_make_directories
from binascii import crc32
from shutil import rmtree
from json import loads as json_decode
import chardet

if __name__ == "__main__":
    import utils
else:
    import gmad.utils as utils

def get_header(in_path):
    """Extracts the gma header from the input file."""
    if not path_exists(in_path):
        raise IOError("in_path " + in_path + " does not exist.")

    file = open(in_path, 'rb')
    data = {}

    data['identifier'] = utils.read_length_string(file, 4)
    if data['identifier'] != "GMAD":
        raise IOError("in_path `" + in_path + "` does not contain .gma file.")

    data['gmadversion'] = utils.read_int(file, 1)
    data['steamid'] = utils.read_int(file, 8)
    data['timestamp'] = utils.read_int(file, 8)
    data['required'] = utils.read_int(file, 1)
    data['title'] = utils.read_null_string(file)
    data['info'] = utils.read_null_string(file)
    data['author'] = utils.read_null_string(file)
    data['version'] = utils.read_int(file)

    return data, file

def extract_header(in_path):
    """Extracts the gma header, closing the file and returning the information."""
    header, file = get_header(in_path)
    file.close()

    header['in_json'] = json_decode(header['info'])
    return header

def extract_gma(in_path, out_path):
    if path_exists(out_path):
        rmtree(out_path)
    if not path_exists(out_path):
        path_make_directories(out_path)

    """Takes an input path, and output path, and creates a directory from the gma input."""
    data, file = get_header(in_path) # Call the function. Might as well, keep it dry.

    file_num = 0
    files = []

    while utils.read_int(file) != 0:
        file_data = {}
        file_num += 1
        file_data['name'] = utils.read_null_string(file)
        file_data['size'] = utils.read_int(file, 8)
        file_data['crc'] = utils.read_int(file)
        files.append(file_data)

    for key in range(file_num):
        content = file.read(files[key]["size"])

        if crc32(content) != files[key]['crc']:
            raise IOError("CRC of data from " + files[key]['name'] + " failed to pass CRC.")

        tmp_out_path = path_join(out_path, files[key]['name'])
        if not path_exists(path_get_directory(tmp_out_path)):
            path_make_directories(path_get_directory(tmp_out_path))
        with open(tmp_out_path, 'wb') as new_file:
            new_file.write(content)
        _, ext = path_ext(tmp_out_path)
        if ext == ".lua":
            with open(tmp_out_path, 'rb') as new_file:
                cnt = new_file.read()
                cset = chardet.detect(cnt)['encoding']
                if cset is None:
                    cset = "ascii"
                # print(tmp_out_path, cset)
                cnt = cnt.decode(cset, errors = "ignore")
                cnt = cnt.replace("//", "--")
                cnt = cnt.replace("/*", "--[[")
                cnt = cnt.replace("*/", "--]]")
            with open(tmp_out_path, 'w', encoding="utf8") as new_file:
                new_file.write(cnt)

    with open(path_join(out_path, "addon.json"), 'w', encoding="utf8") as new_file:
        new_file.write(data['info'])

    file.close()
    return data

if __name__ == "__main__":
    import sys
    try:
        PATH = sys.argv[1]
        if len(sys.argv) > 2:
            OUT = sys.argv[2]
        else:
            OUT = ""
        extract_gma(PATH, OUT)
    except IndexError:
        print("Usage: fromgma.py <input_path> [<output_directory>]")
        print("Created and populate the output directory.")
        print("Data is sourced from the gma passed as input path.")
