import flask
from flask import request
from flask_cors import CORS
import index
import schema
import FileService

app = flask.Flask(__name__)
CORS(app)


@app.route("/atom/<atom_id>")
def get_atom(atom_id: str):
    if atom_id in index.ATOMS:
        return {
            "code": 0,
            "message": "ok",
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
            "message": "ok",
            "tags": index.ATOMS.get(atom_id).tags
        }
    else:
        return {
            "code": 1,
            "message": "Atom not found"
        }
    
@app.route("/atom/<atom_id>/editquarks", methods=["POST"])
def edit_quarks(atom_id: str):
    if atom_id in index.ATOMS:
        quarks_id = request.json.get("quarks")
        quarks = [index.QUARKS.get(qid) for qid in quarks_id]
        index.ATOMS.get(atom_id).contents = quarks
        return {
            "code": 0,
            "message": "ok"
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
        "message": "ok",
        "atom_id": atom.id
    }

@app.route("/quark/<quark_id>")
def get_quark(quark_id: str):
    if quark_id in index.QUARKS:
        response = {
            "code": 0,
            "message": "ok",
            "quark": index.QUARKS.get(quark_id).to_json()
        }
        return flask.jsonify(response), 200, {"Cache-Control": "public, max-age=31536000"}
    else:
        return {
            "code": 1,
            "message": "Quark not found"
        }
    
@app.route("/quark", methods=["POST"])
def create_quark():
    type = request.form.get("type")

    if type == "text":
        content = request.form.get("content")
    else:
        # file was uploaded with the form
        file = request.files.get("content")
        if file is None:
            return {
                "code": 2,
                "message": "File not found"
            }
        content = file.read()

    quark = schema.Quark(content, type, [])
    index.QUARKS[quark.id] = quark

    return {
        "code": 0,
        "message": "ok",
        "quark_id": quark.id
    }


@app.route("/quarkcontent/<content_id>")
def get_quark_content(content_id: str):
    return flask.send_file(FileService.local.QUARK_DIR + "/" + content_id)

@app.route("/dev/savedata", methods=["GET"])
def save_data():
    index.save_data()
    return {
        "code": 0,
        "message": "Data saved"
    }

if __name__ == "__main__":
    app.run(port=8000, debug=True)
