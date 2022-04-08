import os
import re
from typing import Union
### for not getting error pip install git+https://github.com/maxcountryman/flask-uploads.git@f66d7dc
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """
    Make our filename related functions generic, able to deal with FileStorage object as well as filename str.
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


def get_extension(file: Union[str, FileStorage]) -> str:
    """
    Return file's extension, for example
    get_extension('image.jpg') returns '.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
