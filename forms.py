#encoding: utf-8

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DecimalField, HiddenField
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
    habitacion = SelectField(u'Habitacion',coerce=int,choices=None, validators = [
        validators.InputRequired(message=u'Input requerido')
    ])
    fechaPedido = DateField(u'Fecha de reserva',format='%m/%d/%Y', validators = [
        validators.InputRequired(message=u'Input requerido')
    ])
    numeroDias = DecimalField(u'Numero de dias', places=0, validators = [
        validators.InputRequired(message=u'Input requerido'),
        validators.NumberRange(min=1,max=999,message=u'Numero de dias no valido')
    ])
    submit = SubmitField(u'Reservar habitacion')

class ChangeNameForm(Form):
    new_username = StringField(u'Nuevo nombre usuario', validators = [
        validators.InputRequired(message=u'Se requiere input'),
        validators.Length(message=u'Minimo 5 letras', min=5)
    ])
    submit = SubmitField(u'Cambiar nombre')

class DeleteAccountForm(Form):
    submit = SubmitField(u'Eliminar cuenta')
    user_id = HiddenField(u'userId')

class AcceptReserveForm(Form):
    submit = SubmitField(u'Aceptar reserva')
    reserva_id = HiddenField(u'reservaId')

class DeleteReserveForm(Form):
    submit = SubmitField(u'Eliminar reserva')
    reserva_id = HiddenField(u'reservaId')

class DeleteHotelForm(Form):
    submit = SubmitField(u'Eliminar hotel')
    hotel_id = HiddenField(u'hotelId')

class DeleteTipoHabitacionForm(Form):
    submit = SubmitField(u'Eliminar tipo habitacion')
    tipo_habitacion_id = HiddenField(u'tipoHabitacionId')

class DeleteHabitacionForm(Form):
    submit = SubmitField(u'Eliminar habitacion')
    habitacion_id = HiddenField(u'habitacionId')

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

class CreateTipoHabitacionForm(Form):
    nombre = StringField(u'Nombre tipo habitacion', validators = [
        validators.InputRequired(message=u'Se requiere input'),
        validators.Length(message=u'Minimo 5 letras', min=5)
    ])
    descripcion = StringField(u'Descripcion', validators = [
        validators.InputRequired(message=u'Se requiere input'),
        validators.Length(message=u'Minimo 5 letras', min=5)
    ])
    numeroPersonas = IntegerField(u'Numero de Personas', validators = [
        validators.InputRequired(message=u'Input requerido'),
        validators.NumberRange(min=1,max=999999999,message=u'Numero de Telefono no valido')
    ])
    precio = IntegerField(u'Precio', validators = [
        validators.InputRequired(message=u'Input requerido'),
        validators.NumberRange(min=1,max=999999999,message=u'Numero de Telefono no valido')
    ])
    submit = SubmitField(u'Crear Tipo Habitacion')

class CreateHabitacionForm(Form):
    numeroHabitacion = StringField(u'Numero habitacion', validators = [
        validators.InputRequired(message=u'Se requiere input')
    ])
    piso = IntegerField(u'Piso', validators = [
        validators.InputRequired(message=u'Input requerido'),
        validators.NumberRange(min=1,max=999999999,message=u'Numero de Telefono no valido')
    ])
    tipoHabitacion = SelectField(u'Tipo de Habitacion',coerce=int,choices=None, validators = [
        validators.InputRequired(message=u'Input requerido')
    ])
    hotel = SelectField(u'Hotel',coerce=int,choices=None, validators = [
        validators.InputRequired(message=u'Input requerido')
    ])
    submit = SubmitField(u'Crear Habitacion')
