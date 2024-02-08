from app import app
from flask import request, send_from_directory
from app.config import hashing_algorithm
from .classes import File
from json import dumps


@app.route('/upload', methods=['POST'])
def upload():
    if request.authorization is None:
        return dumps({'result': 'error', 'error': 'no auth'})

    username = request.authorization.username
    if 'file' not in request.files:
        return dumps({'result': 'error', 'error': 'no file'})
    file = request.files['file']
    if file.filename == '' or not file:
        return dumps({'result': 'error', 'error': 'no file'})

    filename = hashing_algorithm(file.read()).hexdigest()
    f = File(filename)
    f.save(file, username)
    return dumps({'result': 'ok', 'hash': filename})


@app.route('/delete', methods=['GET'])
def delete():
    if request.authorization is None:
        return dumps({'result': 'error', 'error': 'no auth'})

    username = request.authorization.username
    file = request.args.get('file')

    if not file:
        return dumps({'result': 'error', 'error': 'empty name'})

    f = File(file)
    if f.exists:
        f.delete(username)
        return dumps({'result': 'ok'})  # вернет ок даже если не владелец (и не yдалит)
    return dumps({'result': 'error', 'error': 'file do not exists'})


@app.route('/download', methods=['GET'])
def download():
    file = request.args.get('file')

    if not file:
        return dumps({'result': 'error', 'error': 'empty name'})

    f = File(file)
    if f.exists:
        return send_from_directory(f.dir_path, file)
    return dumps({'result': 'error', 'error': 'file do not exists'})

