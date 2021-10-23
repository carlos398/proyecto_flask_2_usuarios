from flask import Flask, request, render_template,make_response, session,flash
from flask import url_for
from flask_mysqldb import MySQL
from flask_wtf import CsrfProtect
from flask import redirect
import forms 

app = Flask(__name__)
app.secret_key = 'my_secret_key'
csrf = CsrfProtect(app)

@app.route('/')
def index():
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
    return render_template('index.html', form = login_form)


@app.route('/cookies')
def params():
    response = make_response(render_template('cookies.html'))
    response.set_cookie('custome_cokie', 'eduardo')
    return response


def pagina_no_encontrada(error):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(port = 3000, debug = True)