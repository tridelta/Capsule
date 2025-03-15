from . import summerize_atom
from . import compute_atom_emb

from .. import index


def log(*args, **kwargs):
    print("[AOS]", *args, **kwargs)


def run():
    for aid in index.ATOMS:
        atom = index.ATOMS[aid]

        # auto tag
        if ("sum" not in atom.info) or (atom.info.get("sum-recalc", True) == True):
            sum = summerize_atom.summerize(aid)

            atom.info["sum"] = sum
            if len(atom.tags) == 0:
                atom.tags = sum["tags"]
            if atom.title == "New Atom":
                atom.title = sum["title"]

        # auto vec
        if ("vec" not in atom.info) or (atom.info.get("vec-recalc", True) == True):
            words = []
            words += [(t, 1) for t in atom.tags]
            words += [(t, 0.3) for t in atom.info["sum"]["tags"]]

            vec = compute_atom_emb.compute_emb(words)
            atom.info["vec"] = vec
            atom.info["vec-recalc"] = False

        
