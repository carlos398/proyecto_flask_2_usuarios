from flask import Flask, request, render_template,make_response, session,flash,g
from flask import url_for
from flask_mysqldb import MySQL
from flask_wtf import CsrfProtect
from flask import redirect
from config import DevelopmentConfig
from models import db, User, Comment
import forms 
from helper import date_format

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
    if 'username' not in session and request.endpoint in ['index', 'comment']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login', 'create_user']:
        return redirect(url_for('index'))


@app.route('/')
def index():
    print(g.test) #si fuese una nueva conexion a una bd podemos pasarle un .close() para que se cierre la consulta
    tittle = 'index'
    username = session['username']
    print(username)
    return render_template('index1.html', title = tittle, username = username)


@app.route('/register', methods = ['GET', 'POST'])
def create_user():
    register_form = forms.register_form(request.form)
    if request.method == 'POST' and register_form.validate():

        user = User(
            register_form.username.data,
            register_form.email.data,
            register_form.password.data
            )

        db.session.add(user)
        db.session.commit()

        succes_message = 'The user is create in the database congrats'
        flash(succes_message)

    return render_template('register.html', register = register_form)


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
        password = login_form.password.data

        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            success_message = 'bienvenido {}'.format(username)
            flash(success_message)
            session['username'] = username
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            error_message = ' usuario o contraseña no validos'
            flash(error_message)
        
    return render_template('index.html', form = login_form) #el response es el return de las funciones 


@app.route('/comment', methods = ['GET', 'POST'])
def comment():
    comment_form = forms.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():

        user_id = session['user_id']
        comentario = Comment(
            user_id = user_id , 
            text = comment_form.comment.data)
        db.session.add(comentario)
        db.session.commit()

        succes_message = 'nuevo comentario creadp'
        print(succes_message)
        flash(succes_message)
        
        return render_template('index1.html')

    return render_template('comment.html', form = comment_form)


@app.route('/reviews/', methods = ['GET'])
@app.route('/reviews/<int:page>', methods = ['GET'])
def reviews(page = 1):
    per_page = 3
    comment_list = Comment.query.join(User).add_columns(
        User.username, 
        Comment.text,
        Comment.created_date).paginate(page,per_page,False)
    return render_template(
        'review.html', 
        comments = comment_list, 
        date_format = date_format)


@app.route('/<username>/reviews/', methods = ['GET'])
@app.route('/<username>/reviews/<int:page>', methods = ['GET'])
def profile(username, page = 1):
    per_page = 3
    comment_list = Comment.query.join(User).add_columns(
        User.username, 
        Comment.text,
        Comment.created_date).filter_by(username = username).paginate(page,per_page,False)
    return render_template(
        'review.html', 
        comments = comment_list, 
        date_format = date_format)


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