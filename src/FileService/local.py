"""
This module provides functions to save and retrieve quark content from local disk storage.

Functions:
- save_quark_content(quark_id, content): Save quark content to local disk.
- get_quark_content(quark_id): Get quark content from local disk.

Config:
- PROJ_ROOT: The root directory of the project (default using cwd, in dev environment).

"""
import os

# config
PROJ_ROOT = os.getcwd()    # NOTE dev environment only
QUARK_DIR = f"{PROJ_ROOT}/data/quarks"

# init dir
if not os.path.exists(QUARK_DIR):
    os.makedirs(QUARK_DIR)

# main functions
def save_quark_content(quark_id, content):
    """
    Save quark content to local disk.

    @param quark_id str: The ID of the quark.
    @param content bytes: The content of the quark, in bytes.
    @return int: Error code.

    Error codes:
    0: Success.
    1: Quark ID conflicts.
    """
    if os.path.exists(f"{QUARK_DIR}/{quark_id}"):
        with open(f"{QUARK_DIR}/{quark_id}", "rb") as f:
            if f.read() != content:
                return 1
            else:
                return 0
    
    with open(f"{QUARK_DIR}/{quark_id}", "wb") as f:
        f.write(content)
    return 0


def get_quark_content(quark_id):
    """
    Get quark content from local disk.

    @param quark_id str: The ID of the quark.
    @return bytes: The content of the quark, in bytes.
    """
    with open(f"{QUARK_DIR}/{quark_id}", "rb") as f:
        return f.read()
