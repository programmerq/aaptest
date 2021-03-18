from bottle import route, run, template, redirect
import socket, signal


@route('/')
def index():
    return str(socket.gethostname()) + '\n'


@route('/temp')
def index():
    redirect("http://localhost/foo/bar", 302)


@route('/temp2')
def index():
    redirect("http://localhost:8000/foo/bar", 302)


@route('/foo/bar')
def index():
    return 'successfully redirected\n'


run(host='0.0.0.0', port=8000)
