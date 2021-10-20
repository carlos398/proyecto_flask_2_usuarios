from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from flask_wtf import CsrfProtect
import forms 

app = Flask(__name__)
app.secret_key = 'my_secret_key'
csrf = CsrfProtect(app)


@app.route('/', methods = ['GET', 'POST'])
def index():
    login_form = forms.login(request.form)
    if request.method == 'POST' and login_form.validate():
        print(login_form.username.data)
        print(login_form.password.data)
    else:
        print("error en el formulario")
    return render_template('index.html', form = login_form)


@app.route('/params')
def params():
    return 'params'


def pagina_no_encontrada(error):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(port = 3000, debug = True)