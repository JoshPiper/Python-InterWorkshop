import chardet

"""Various utilities for stuff."""
def read_until_null(file):
    """Read a file pointer until it reaches a null byte, returning an array of byte objects."""
    return_data = b""
    next_byte = file.read(1)
    while next_byte != b"\x00":
        return_data += next_byte
        next_byte = file.read(1)
    return return_data

def read_null_string(file):
    """Read a null terminated string from a filer pointer, returning the read string."""
    raw = read_until_null(file)
    cset = chardet.detect(raw)['encoding']
    if cset is None:
        cset = "ascii"
    return raw.decode(cset)


def read_length_string(file, length=0):
    """Return a string of given length pulled from the file."""
    raw = file.read(length)
    cset = chardet.detect(raw)['encoding']
    if cset is None:
        cset = "ascii"
    return raw.decode(cset)

def read_int(file, length=4, edian='little'):
    """Read integer from file, returning an int of byte length and edian encoding."""
    return int.from_bytes(file.read(length), edian)

def list_has_item(in_list, item):
    """Return if the list has a given item."""
    try:
        in_list.index(item)
        return True
    except ValueError:
        return False
