from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)


@app.route('/')
def index():
    return 'holap'

#validador de rutas
@app.route('/params')
@app.route('/params/<name>')
def params(name = 'nombre por defecto'):
    return "el parametro es {}".format(name) 


def pagina_no_encontrada(error):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(port = 3000, debug = True)