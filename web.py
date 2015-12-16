#encoding:utf-8
from flask import Flask, render_template, request, session, url_for, redirect
from flask_login import (LoginManager, login_user,
        login_required, current_user, logout_user)
from forms import CreateUserForm,LoginUserForm,ReserveForm,DeleteReserveForm,DeleteHotelForm,CreateHotelForm
from modelos import Cliente,TipoHabitacion,Hotel,Habitacion,Reserva
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'fjfdjiofejioefijoefijofijofjioefjioefwoijefjioef00'
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    try:
        return Cliente.get(id = user_id)
    except:
        return None

login_manager.login_view = 'user_login'

login_manager.init_app(app)

Bootstrap(app)

@app.route('/user/create', methods=['GET', 'POST'])
def user_create():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    form = CreateUserForm(request.form)
    if form.validate_on_submit():
        try:
            user = Cliente.get(Cliente.nombre == form.username.data)
            if user:
                return render_template('create_user.html', form=form, error=u'nombre de usuario ya existente en sistema')
        except:
            Cliente.create(
                nombre=form.username.data,
                password=form.password.data,
                fechaInscripcion=datetime.now()
            )
            return render_template('create_user_success.html', username=form.username.data)

    return render_template('create_user.html', form=form)

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    form = LoginUserForm(request.form)
    if form.validate_on_submit():
        try:
            user = Cliente.get(Cliente.nombre == form.username.data,
                Cliente.password == form.password.data)
            login_user(user)
            session['user_id'] = user.id
            return redirect(url_for('index'))
        except:
            return render_template('login.html', form=form, error=u'Usuario o contraseña invalida')

    return render_template('login.html', form=form)

@app.route('/user/logout')
def user_logout():
    logout_user()
    return redirect(url_for('user_login'))

@app.route('/')
@login_required
def index():
    return render_template('hola.html')

@app.route('/user/reservar',methods=['GET', 'POST'])
@login_required
def reservar():
    form = ReserveForm(request.form)
    if form.validate_on_submit():
        try:
            return redirect(url_for('index'))
        except:
            return render_template('reserva.html', form=form, error=u'Error')

    return render_template('reserva.html', form=form)

@app.route('/user/ver_reservas')
@login_required
def ver_reservas():
    reserva_p = []
    for reserva in current_user.reservas:
        numeroHabitacion = reserva.habitacion.numeroHabitacion
        hotel_nombre = reserva.hotel.nombre
        fechaPedido = reserva.fechaPedido
        delta = reserva.fechaTermino - reserva.fechaPedido
        numeroDias = delta.days
        form = DeleteReserveForm(request.form)
        reserva_p.insert(len(reserva_p),{'numeroHabitacion':numeroHabitacion,
        'hotel_nombre':hotel_nombre,'fechaPedido':fechaPedido,'delta':delta,'numeroDias':numeroDias,'form':form })
    return render_template('ver_reserva.html',reservas=reserva_p)

@app.route('/admin/hoteles',methods=['GET', 'POST'])
@login_required
def admin_hoteles():
    if not current_user.is_admin():
        return redirect(url_for('index'))
    form = CreateHotelForm(request.form)
    hoteles_p = []
    for hotel in Hotel.select():
        nombre = hotel.nombre
        region = hotel.region
        ciudad = hotel.ciudad
        direccion = hotel.direccion
        formd = DeleteHotelForm(request.form)
        hoteles_p.insert(len(hoteles_p),{'nombre':nombre,
        'region':region,'ciudad':ciudad,'direccion':direccion,'form':formd })
    if form.validate_on_submit():
        try:
            hotel = Hotel.get(Hotel.nombre == form.username.data)
            if hotel:
                return render_template('admin_hoteles.html',hoteles=hoteles_p, form=form, error=u'nombre de hotel ya existente en sistema')
        except:
            Hotel.create(
                nombre=form.nombre.data,
                region=form.region.data,
                ciudad=form.ciudad.data,
                direccion=form.direccion.data,
                numeroAtencion=form.numeroAtencion.data,
                emailContacto=form.emailContacto.data
            )
        return redirect(url_for('admin_hoteles'))

    return render_template('admin_hoteles.html',hoteles=hoteles_p,form=form)

if __name__ == '__main__':
    app.run(host='localhost', port=1337, debug=True)
