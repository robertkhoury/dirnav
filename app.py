
from flask import Flask, abort, jsonify
import os
import pwd
from markupsafe import escape

app = Flask(__name__)

# Routes

@app.route('/')
def show_root():
    root_path = os.path.join(app.root_path, "user_path")
    response = format_folder(root_path, "/", with_contents=True)
    return jsonify(response)

@app.route('/<path:subpath>')
def show_subpath(subpath):
    bread_crumbs = subpath.split("/")
    updated_path = os.path.join(app.root_path, "user_path")
    for bread_crumb in bread_crumbs:
        updated_path = os.path.join(updated_path, bread_crumb)
    if not os.path.exists(updated_path):
        abort(400)
    response = format_object(updated_path, object_name=bread_crumbs[-1], is_parent=True)
    return jsonify(response)

# Error Handlers

@app.errorhandler(400)
def page_not_found(error):
    return "No file or directory found for the given path\n", 400

# Helper Methods

def format_object(object_path, object_name, is_parent=False):
    if os.path.isfile(object_path):
        return format_file(object_path, object_name, with_text=is_parent)
    return format_folder(object_path, object_name, with_contents=is_parent)

def format_folder(path, folder_name, with_contents=False):
    response = {
        "name": folder_name,
        "object_type": "folder",
    }
    if not with_contents:
        return response
    contents = [format_object(os.path.join(path, child), child, is_parent=False) for child in os.listdir(path)]
    response["folder_contents"] = contents
    return response

def format_file(path, file_name, with_text=False):
    file_stat = os.stat(path)
    response = {
        "name": file_name,
        "object_type": "file",
        "size": "{0}B".format(file_stat.st_size),
        "owner_id": file_stat.st_uid,
        "permissions": file_stat.st_mode
    }
    if with_text:
        f = open(path, 'r')
        try:
            # Cap to first 10 MB of the file
            file_text = f.read(10**7)
        except:
            # Display message in file_text rather than throw an error. There's still useful info to be had from
            # this object (permissions, size, etc.), and I would rather display that than nullify the whole
            # thing with an error page.
            file_text = "Cannot parse file text. Make sure your file is a valid txt file."
        response["file_text"] = str(file_text)
    return response


