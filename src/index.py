import json
from . import inverse_index
from . import schema
from . import ConfigService

ATOMS = {
    "atom_id": "Atom-object",
}

QUARKS = {
    "quark_id": "Quark-object",
}

IDF_TABLE = inverse_index.InverseIndex()


def save_data():
    with open(f"{ConfigService.PROJECT_ROOT}/data/ATOMS.json", "w") as f:
        json.dump(ATOMS, f, default=lambda x: x.to_json())
    with open(f"{ConfigService.PROJECT_ROOT}/data/QUARKS.json", "w") as f:
        json.dump(QUARKS, f, default=lambda x: x.to_json())
    with open(f"{ConfigService.PROJECT_ROOT}/data/IDF_TABLE.json", "w") as f:
        json.dump(IDF_TABLE.to_json(), f)

def load_data():
    global ATOMS, QUARKS, IDF_TABLE
    with open(f"{ConfigService.PROJECT_ROOT}/data/QUARKS.json", "r") as f:
        QUARKS = json.load(f)
        for k, v in QUARKS.items():
            QUARKS[k] = schema.Quark.from_json(v)
    with open(f"{ConfigService.PROJECT_ROOT}/data/ATOMS.json", "r") as f:
        ATOMS = json.load(f)
        for k, v in ATOMS.items():
            ATOMS[k] = schema.Atom.from_json(v)
    with open(f"{ConfigService.PROJECT_ROOT}/data/IDF_TABLE.json", "r") as f:
        IDF_TABLE = inverse_index.InverseIndex.from_json(json.load(f))


load_data()