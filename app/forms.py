from wtforms import Form, StringField, TextField, validators, HiddenField, PasswordField
from wtforms.fields.html5 import EmailField
from models import User

class CommentForm(Form):

    def length_honeypot(form, field):
        if len(field.data) > 0:
            raise validators.ValidationError('El campo debe estar vacio')


    username = StringField('username', [
        validators.Required(message = 'es necesario un username'),
        validators.length(min=4, 
        max=25, 
        message='ingrese un username valido')])

    email = EmailField('email', [
        validators.Required(message = 'es requerido un email'),
        validators.length(min=8, 
        max=25, 
        message='ingrese uncorreo valida')])

    comment = TextField('comentario', [
        validators.length(min=4, 
        max=255, 
        message='ingrese un comentario valido')])

    honeypot = HiddenField('',[length_honeypot] ) #honey pot metodo de proteccion contra ataque de datos


class login(Form):

    def length_honeypot(form, field):
        if len(field.data) > 0:
            raise validators.ValidationError('El campo debe estar vacio')


    username = StringField('Username', [
        validators.Required(message = 'El ingreso de un usario es necesario'),
        validators.length(min=4, max=25, message = 'El usuario no es valido')
       ])

    password = PasswordField('Password', [
        validators.Required(message = 'El password es requerido')
        ])

    honeypot = HiddenField('',[length_honeypot] ) 


class register_form(Form):

    username = StringField('Username', [
        validators.Required(message = 'The username is required'),
        validators.length(
            min=4, 
            max=50, 
            message='the user is invalid')
    ])

    email = EmailField('Email', [
        validators.Required(message = 'The email is required'),
        validators.length(
            min=8, 
            max=40, 
            message='The email is invalid')
    ])

    password = PasswordField('Password', [
        validators.Required(message = 'The password is required'),
        validators.length(
            min=4, 
            max=66, 
            message='The password is invalid')
    ]) 

    def validate_username(form, field):
        username = field.data 
        user = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('el username ya se encuentra registrado')
