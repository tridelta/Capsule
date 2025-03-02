import flask
from flask import request
from flask_cors import CORS
import index
import schema
import FileService

app = flask.Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://capsule.berniehg.top", "http://capsule.berniehg.top"], "supports_credentials": True}})

def _get_quark_objects(quark_ids: list[str]) -> list[schema.Quark]:
    quarks = []
    for qid in quark_ids:
        if qid in index.QUARKS:
            quarks.append(index.QUARKS.get(qid))
        else:
            return 1, qid
    return 0, quarks

@app.route("/atom/<atom_id>")
def get_atom(atom_id: str):
    if atom_id in index.ATOMS:
        return {"code": 0, "message": "ok", "atom": index.ATOMS.get(atom_id).to_json()}
    else:
        return {"code": 1, "message": "Atom not found"}


@app.route("/atom/<atom_id>/tags")
def get_atom_tags(atom_id: str):
    if atom_id in index.ATOMS:
        return {"code": 0, "message": "ok", "tags": index.ATOMS.get(atom_id).tags}
    else:
        return {"code": 1, "message": "Atom not found"}


@app.route("/atom/<atom_id>/editquarks", methods=["POST"])
def edit_quarks(atom_id: str):
    contents_id = request.json.get("quarks")
    err, contents = _get_quark_objects(contents_id)
    if err != 0:
        return {"code": 2, "message": "Quark not found", "err_quark_id": contents}

    if atom_id in index.ATOMS:
        atom = index.ATOMS.get(atom_id)
        atom.contents = contents
        atom.last_modify = schema._get_current_timestamp()

    else:
        # Atom Not Found: create a new one
        title = "New Atom"
        atom = schema.Atom(title, contents)
        index.ATOMS[atom.id] = atom
        atom_id = atom.id
        # return {"code": 1, "message": "Atom not found"}

    return {"code": 0, "message": "ok", "atom_id": atom_id}


@app.route("/atom", methods=["POST"])
def create_atom():
    title = request.json.get("title")
    contents_id = request.json.get("contents")
    err, contents = _get_quark_objects(contents_id)
    if err != 0:
        return {"code": 2, "message": "Quark not found", "err_quark_id": contents}

    atom = schema.Atom(title, contents)
    index.ATOMS[atom.id] = atom

    return {"code": 0, "message": "ok", "atom_id": atom.id}


@app.route("/quark/<quark_id>")
def get_quark(quark_id: str):
    if quark_id in index.QUARKS:
        response = {
            "code": 0,
            "message": "ok",
            "quark": index.QUARKS.get(quark_id).to_json(),
        }
        return (
            flask.jsonify(response),
            200,
            {"Cache-Control": "public, max-age=31536000"},
        )
    else:
        return {"code": 1, "message": "Quark not found"}


@app.route("/quark", methods=["POST"])
def create_quark():
    type = request.form.get("type")

    if type == "text":
        content = request.form.get("content")
    else:
        # file was uploaded with the form
        file = request.files.get("content")
        if file is None:
            return {"code": 2, "message": "File not found"}
        content = file.read()

    quark = schema.Quark(content, type, [])
    index.QUARKS[quark.id] = quark

    return {"code": 0, "message": "ok", "quark_id": quark.id}


@app.route("/quarkcontent/<content_id>")
def get_quark_content(content_id: str):
    return flask.send_file(FileService.local.QUARK_DIR + "/" + content_id)

@app.route("/atom_list", methods=["GET"])
def get_atom_list():
    atoms = [atom.id for atom in index.ATOMS.values()]
    return {"code": 0, "message": "ok", "atom_list": atoms}

@app.route("/dev/savedata", methods=["GET"])
def save_data():
    index.save_data()
    return {"code": 0, "message": "Data saved"}


if __name__ == "__main__":
    app.run(port=5201, debug=True)
