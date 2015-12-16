#encoding: utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms import validators
from modelos import Cliente,TipoHabitacion,Hotel,Habitacion,Reserva

class CreateUserForm(Form):
    username = StringField(u'Nombre usuario', validators = [
        validators.InputRequired(message=u'Se requiere input'),
        validators.Length(message=u'Minimo 5 letras', min=5)
    ])
    password = PasswordField(u'Contraseña', validators = [
        validators.InputRequired(message=u'Input requerido'),
        validators.Length(message=u'Contraseña entre 5 y 30 letras', min=5, max=30)
    ])
    submit = SubmitField(u'Crear Usuario')

class LoginUserForm(Form):
    username = StringField(u'Nombre usuario')
    password = PasswordField(u'Contraseña')
    submit = SubmitField(u'Ingresar al sistema')

class ReserveForm(Form):
    choices = []
    for habitacion in Habitacion.select():
        valor = u'Habitacion: {}, Hotel: {}, Precioxdia: {}'.format(Habitacion.numeroHabitacion,Habitacion.hotel.nombre,Habitacion.tipoHabitacion.precio)
        choices.insert(len(choices),(Habitacion.id,valor))
    habitacion = SelectField(u'Habitacion',choices=Habitacion.select(), validators = [
        validators.InputRequired(message=u'Input requerido')
    ])
    fechaPedido = DateField(u'Fecha de reserva',format='%Y-%m-%d', validators = [
        validators.InputRequired(message=u'Input requerido')
    ])
    numeroDias = DecimalField(u'Numero de dias', places=0, validators = [
        validators.InputRequired(message=u'Input requerido'),
        validators.NumberRange(min=1,max=999,message=u'Numero de dias no valido')
    ])
    submit = SubmitField(u'Reservar habitacion')

class DeleteReserveForm(Form):
    submit = SubmitField(u'Eliminar reserva')

class DeleteHotelForm(Form):
    submit = SubmitField(u'Eliminar hotel')

class CreateHotelForm(Form):
    nombre = StringField(u'Nombre hotel', validators = [
        validators.InputRequired(message=u'Se requiere input'),
        validators.Length(message=u'Minimo 5 letras', min=5)
    ])
    region = StringField(u'Region', validators = [
        validators.InputRequired(message=u'Se requiere input')
    ])
    ciudad = StringField(u'Ciudad', validators = [
        validators.InputRequired(message=u'Se requiere input')
    ])
    direccion = StringField(u'Direccion', validators = [
        validators.InputRequired(message=u'Se requiere input')
    ])
    numeroAtencion = IntegerField(u'Telefono', validators = [
        validators.InputRequired(message=u'Input requerido'),
        validators.NumberRange(min=1,max=999999999,message=u'Numero de Telefono no valido')
    ])
    emailContacto = StringField(u'Email', validators = [
        validators.InputRequired(message=u'Se requiere input')
    ])
    submit = SubmitField(u'Crear Hotel')
