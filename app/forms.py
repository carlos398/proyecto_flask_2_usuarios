from wtforms import Form, StringField, TextField, validators, HiddenField, PasswordField
from wtforms.fields.html5 import EmailField


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