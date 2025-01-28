import random
from hashlib import sha256
import time

ATOMS = {}
QUARKS = {}
CONNECTIONS = {}


def _sha256(text) -> str:
    return sha256(text.encode()).hexdigest()


def _get_random_id() -> str:
    """
    Generates a random ID.
    Atom's ID is generated by this function.

    @return str: A SHA-256 hash string representing the random ID.
    """
    return _sha256(random.random())


def _get_hash_id(content: str | bytes) -> str:
    """
    Generates a hash ID from the given text/binary.
    Quark's ID is generated by this function.

    @param content str|bytes: The content to be hashed.
    """
    if isinstance(content, str):
        return _sha256(content)
    return sha256(content).hexdigest()


""" ATOM """


def add_atom(atom):
    atom_id = "A_" + _get_random_id()

    ATOMS[atom_id] = {
        "id": atom_id,
        "title": atom["title"],
        "contents": atom["contents"],
        "last_modified": time.time(),
    }

    return atom_id


def get_atom(atom_id):
    return ATOMS.get(atom_id)


""" CONNECTION """


# TODO: 既然我们说这个东西像一个图，那么就需要决定边的表示方式。比如说是用邻接表还是邻接矩阵。
def add_connection(connection):
    pass


def get_connection(connection_id):
    pass


""" QUARK """


def add_quark(quark):
    quark_hash = _get_hash_id(quark["content"])
    quark_id = "Q_" + quark_hash

    ATOMS[quark_id] = {
        "id": quark_id,
        "sha256": quark_hash,
        "type": quark["type"],
        "content": quark["content"],
        "last_modified": time.time(),
    }

    return quark_id

def get_quark(quark_id):
    return QUARKS.get(quark_id)
