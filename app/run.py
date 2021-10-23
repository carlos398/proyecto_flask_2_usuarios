from flask import Flask, request, render_template,make_response, session,flash,g
from flask import url_for
from flask_mysqldb import MySQL
from flask_wtf import CsrfProtect
from flask import redirect
from config import DevelopmentConfig
from models import db, User
import forms 

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CsrfProtect(app)

@app.before_request
def befor_request():
    #esto es lo que se ejecutara antes de enviar la funcion siguiente, cosas como permisos etc
    # if 'username' not in session and request.endpoint not in ['login']:
    #     return redirect(url_for("login"))
    g.test = 'test 1' #manejo de variables globales mediante g de flask
    print(g.test)


@app.route('/')
def index():
    print(g.test) #si fuese una nueva conexion a una bd podemos pasarle un .close() para que se cierre la consulta
    if 'username' in session:
        username = session['username']
        print(username)
    tittle = 'index'
    return render_template('index1.html', title = tittle)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = forms.login(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        success_message = 'bienvenido {}'.format(username)
        flash(success_message)
        session['username'] = login_form.username.data
    return render_template('index.html', form = login_form) #el response es el return de las funciones 


# @app.after_request()
# def after_request(response): #las funciones after request del metodo after reciben como parametro el response
#     return response


@app.route('/cookies')
def params():
    response = make_response(render_template('cookies.html'))
    response.set_cookie('custome_cokie', 'eduardo')
    return response


def pagina_no_encontrada(error):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    csrf.init_app(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    app.run(port = 3000)