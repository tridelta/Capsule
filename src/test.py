import flask
from flask import request
import base64
import index
import schema

app = flask.Flask(__name__)

@app.route("/atom/<atom_id>")
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
    
@app.route("/atom/<atom_id>/tags")
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

@app.route("/atom", methods=["POST"])
def create_atom():
    title = request.json.get("title")
    contents_id = request.json.get("contents")
    contents = [index.QUARKS.get(qid) for qid in contents_id]

    atom = schema.Atom(title, contents)
    index.ATOMS[atom.id] = atom

    return {
        "code": 0,
        "message": "Atom created",
        "atom_id": atom.id
    }

@app.route("/quark/<quark_id>")
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
    
@app.route("/quark", methods=["POST"])
def create_quark():
    type = request.json.get("type")
    content = request.json.get("content")
    trans = request.json.get("transcripts")
    trans = request.json.get("transcripts")

    if type != "text":
        content = base64.b64decode(content)

    quark = schema.Quark(content, type, trans)
    index.QUARKS[quark.id] = quark

    return {
        "code": 0,
        "message": "Quark created",
        "quark_id": quark.id
    }


if __name__ == "__main__":
    app.run(port=8000, debug=True)
