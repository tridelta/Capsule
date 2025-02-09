import fastapi
import base64
from .. import index
from .. import schema

app = fastapi.FastAPI()

@app.get("/atom/{atom_id}")
def get_atom(atom_id: str):
    if atom_id in index.ATOMS:
        return {
            "code": 0,
            "message": "Atom found",
            "atom": index.ATOMS.get(atom_id).to_json()
        }
    else:
        return {
            "code": 1,
            "message": "Atom not found"
        }
    
@app.get("/atom/{atom_id}/tags")
def get_atom_tags(atom_id: str):
    if atom_id in index.ATOMS:
        return {
            "code": 0,
            "message": "Atom tags found",
            "tags": index.ATOMS.get(atom_id).tags
        }
    else:
        return {
            "code": 1,
            "message": "Atom not found"
        }

@app.post("/atom")
def create_atom():
    title = fastapi.requests.json().get("title")
    contents_id = fastapi.requests.json().get("contents")
    contents = [index.QUARKS.get(qid) for qid in contents_id]

    atom = schema.Atom(title, contents)

    return {
        "code": 0,
        "message": "Atom created",
        "atom_id": atom.id
    }

@app.get("/quark/{quark_id}")
def get_quark(quark_id: str):
    if quark_id in index.QUARKS:
        return {
            "code": 0,
            "message": "Quark found",
            "quark": index.QUARKS.get(quark_id).to_json()
        }
    else:
        return {
            "code": 1,
            "message": "Quark not found"
        }
    
@app.post("/quark")
def create_quark():
    type = fastapi.requests.json().get("type")
    content = fastapi.requests.json().get("content")
    trans = fastapi.requests.json().get("transcripts")

    if type != "text":
        content = base64.b64decode(content)

    quark = schema.Quark(content, type, trans)

    return {
        "code": 0,
        "message": "Quark created",
        "quark_id": quark.id
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
