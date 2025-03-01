import inverse_index
import json
import schema

ATOMS = {
    "atom_id": "Atom-object",
}

QUARKS = {
    "quark_id": "Quark-object",
}

IDF_TABLE = inverse_index.InverseIndex()


def save_data():
    with open("data/ATOMS.json", "w") as f:
        json.dump(ATOMS, f, default=lambda x: x.to_json())
    with open("data/QUARKS.json", "w") as f:
        json.dump(QUARKS, f, default=lambda x: x.to_json())
    with open("data/IDF_TABLE.json", "w") as f:
        json.dump(IDF_TABLE.to_json(), f)

def load_data():
    global ATOMS, QUARKS, IDF_TABLE
    with open("data/QUARKS.json", "r") as f:
        QUARKS = json.load(f)
        for k, v in QUARKS.items():
            QUARKS[k] = schema.Quark.from_json(v)
    with open("data/ATOMS.json", "r") as f:
        ATOMS = json.load(f)
        for k, v in ATOMS.items():
            ATOMS[k] = schema.Atom.from_json(v)
    with open("data/IDF_TABLE.json", "r") as f:
        IDF_TABLE = inverse_index.InverseIndex.from_json(json.load(f))


load_data()