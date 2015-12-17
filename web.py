#encoding:utf-8
import pprint
from flask import Flask, render_template, request, session, url_for, redirect
from flask_login import (LoginManager, login_user,
        login_required, current_user, logout_user)
from forms import ChangeNameForm,CreateUserForm,LoginUserForm,ReserveForm,AcceptReserveForm,DeleteReserveForm,DeleteHotelForm,DeleteTipoHabitacionForm,DeleteHabitacionForm,CreateHotelForm,CreateTipoHabitacionForm,CreateHabitacionForm,DeleteAccountForm
from modelos import Cliente,TipoHabitacion,Hotel,Habitacion,Reserva
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta

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

@app.route('/',methods=['GET', 'POST'])
@login_required
def index():
    form_delete = DeleteAccountForm(request.form,user_id=str(current_user.id))
    form = ChangeNameForm(request.form)
    if form.validate_on_submit():
        try:
            current_user.nombre = form.new_username.data
            current_user.save()
        except:
            None
    return render_template('hola.html',form=form,form_delete=form_delete)

@app.route('/user/delete',methods=['POST'])
@login_required
def user_delete():
    form_delete = DeleteAccountForm(request.form,user_id=str(current_user.id))
    if form_delete.validate_on_submit():
        try:
            for reserva in current_user.reservas:
                reserva.delete_instance()
            current_user.delete_instance()
            logout_user()
        except:
            None
    return redirect(url_for('index'))

@app.route('/user/reservar',methods=['GET', 'POST'])
@login_required
def reservar():
    form = ReserveForm(request.form)
    choices = []
    for habitacion in Habitacion.select():
        valor = u'Habitacion: {}, Hotel: {}, Precioxdia: {}'.format(habitacion.numeroHabitacion,habitacion.hotel.nombre,habitacion.tipoHabitacion.precio)
        choices.insert(len(choices),(habitacion.id,valor))
    form.habitacion.choices = choices
    if form.validate_on_submit():
        try:
            reserva = Reserva.get(Reserva.fechaPedido == form.fechaPedido.data,Reserva.habitacion == form.habitacion.data)
            if reserva:
                return render_template('reserva.html', form=form, error=u'reserva ya existente en sistema')
        except:
            fechaTermino = form.fechaPedido.data + timedelta(days=int(form.numeroDias.data))
            Reserva.create(
                fechaPedido=form.fechaPedido.data,
                fechaTermino=fechaTermino,
                cliente=current_user.id,
                habitacion=form.habitacion.data
            )
            return redirect(url_for('index'))
        try:
            return redirect(url_for('index'))
        except:
            return render_template('reserva.html', form=form, error=u'Error')

    return render_template('reserva.html', form=form)

@app.route('/user/reservas')
@login_required
def ver_reservas():
    reserva_p = []
    for reserva in current_user.reservas:
        numeroHabitacion = reserva.habitacion.numeroHabitacion
        hotel_nombre = reserva.habitacion.hotel.nombre
        fechaPedido = reserva.fechaPedido
        delta = reserva.fechaTermino - reserva.fechaPedido
        numeroDias = delta.days
        cancelado = reserva.cancelado
        form = DeleteReserveForm(request.form,reserva_id=str(reserva.id))
        reserva_p.insert(len(reserva_p),{'numeroHabitacion':numeroHabitacion,
        'hotel_nombre':hotel_nombre,'fechaPedido':fechaPedido,'delta':delta,'numeroDias':numeroDias,'cancelado':cancelado,
        'form':form })
    return render_template('ver_reserva.html',reservas=reserva_p)

@app.route('/user/reservas/delete',methods=['POST'])
@login_required
def reserva_delete():
    form = DeleteReserveForm(request.form)
    if form.validate_on_submit():
        try:
            reserva = Reserva.get(Reserva.id == form.reserva_id.data,Reserva.cliente == current_user.id,Reserva.cancelado == False)
            reserva.delete_instance()
        except:
            None
    return redirect(url_for('ver_reservas'))

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
            hotel = Hotel.get(Hotel.nombre == form.nombre.data)
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

@app.route('/admin/tipos_habitacion',methods=['GET', 'POST'])
@login_required
def admin_tipos_habitacion():
    if not current_user.is_admin():
        return redirect(url_for('index'))
    form = CreateTipoHabitacionForm(request.form)
    tipos_habitacion_p = []
    for tipoHabitacion in TipoHabitacion.select():
        nombre = tipoHabitacion.nombre
        descripcion = tipoHabitacion.descripcion
        numeroPersonas = tipoHabitacion.numeroPersonas
        precio = tipoHabitacion.precio
        formd = DeleteTipoHabitacionForm(request.form)
        tipos_habitacion_p.insert(len(tipos_habitacion_p),{'nombre':nombre,
        'descripcion':descripcion,'numeroPersonas':numeroPersonas,'precio':precio,'form':formd })
    if form.validate_on_submit():
        try:
            tipoHabitacion = TipoHabitacion.get(TipoHabitacion.nombre == form.nombre.data)
            if tipoHabitacion:
                return render_template('admin_tipos_habitacion.html',tipos_habitacion=tipos_habitacion_p, form=form, error=u'nombre de tipo habitacion ya existente en sistema')
        except:
            TipoHabitacion.create(
                nombre=form.nombre.data,
                descripcion=form.descripcion.data,
                numeroPersonas=form.numeroPersonas.data,
                precio=form.precio.data
            )
        return redirect(url_for('admin_tipos_habitacion'))

    return render_template('admin_tipos_habitacion.html',tipos_habitacion=tipos_habitacion_p,form=form)

@app.route('/admin/habitaciones',methods=['GET', 'POST'])
@login_required
def admin_habitaciones():
    if not current_user.is_admin():
        return redirect(url_for('index'))
    form = CreateHabitacionForm(request.form)
    tipos_habitacion_choices = []
    for tipo_habitacion in TipoHabitacion.select():
        valor = u'Tipo: {},Numero Personas: {},Precio: {}'.format(tipo_habitacion.nombre,tipo_habitacion.numeroPersonas,tipo_habitacion.precio)
        tipos_habitacion_choices.insert(len(tipos_habitacion_choices),(tipo_habitacion.id,valor))
    form.tipoHabitacion.choices = tipos_habitacion_choices
    hoteles_choices = []
    for hotel in Hotel.select():
        valor = u'Hotel: {}'.format(hotel.nombre)
        hoteles_choices.insert(len(hoteles_choices),(hotel.id,valor))
    form.hotel.choices = hoteles_choices
    habitaciones_p = []
    for habitacion in Habitacion.select():
        numeroHabitacion = habitacion.numeroHabitacion
        piso = habitacion.piso
        tipoHabitacion = habitacion.tipoHabitacion.nombre
        hotel = habitacion.hotel.nombre
        formd = DeleteHabitacionForm(request.form)
        habitaciones_p.insert(len(habitaciones_p),{'numeroHabitacion':numeroHabitacion,
        'piso':piso,'tipoHabitacion':tipoHabitacion,'hotel':hotel,'form':formd })
    if form.validate_on_submit():
        try:
            tipoHabitacion = TipoHabitacion.get(TipoHabitacion.numeroHabitacion == form.numeroHabitacion.data)
            if tipoHabitacion:
                return render_template('admin_habitaciones.html',habitaciones=habitaciones_p, form=form, error=u'habitacion ya existente en sistema')
        except:
            Habitacion.create(
                numeroHabitacion=form.numeroHabitacion.data,
                piso=form.piso.data,
                tipoHabitacion=form.tipoHabitacion.data,
                hotel=form.hotel.data
            )
        return redirect(url_for('admin_habitaciones'))

    return render_template('admin_habitaciones.html',habitaciones=habitaciones_p,form=form)

@app.route('/admin/reservas')
@login_required
def admin_reservas():
    if not current_user.is_admin():
        return redirect(url_for('index'))
    reserva_p = []
    for reserva in Reserva.select().where(Reserva.cancelado == False):
        fechaPedido = reserva.fechaPedido
        delta = reserva.fechaTermino - reserva.fechaPedido
        numeroDias = delta.days
        nombreCliente = reserva.cliente.nombre
        nombreHotel = reserva.habitacion.hotel.nombre
        numeroHabitacion = reserva.habitacion.numeroHabitacion
        forma = AcceptReserveForm(request.form,reserva_id=str(reserva.id))
        formd = DeleteReserveForm(request.form,reserva_id=str(reserva.id))
        reserva_p.insert(len(reserva_p),{'id':reserva.id,'fechaPedido':fechaPedido,
        'numeroDias':numeroDias,'nombreCliente':nombreCliente,'nombreHotel':nombreHotel,'numeroHabitacion':numeroHabitacion,
        'forma':forma,'formd':formd })

    return render_template('admin_reservas.html',reservas=reserva_p)

@app.route('/admin/reservas/accept',methods=['POST'])
@login_required
def admin_reservas_accept():
    if not current_user.is_admin():
        return redirect(url_for('index'))
    form = AcceptReserveForm(request.form)
    if form.validate_on_submit():
        try:
            print vars(form.reserva_id)
            reserva = Reserva.get(Reserva.id == form.reserva_id.data)
            reserva.cancelado = True
            reserva.save()
        except:
            None
    return redirect(url_for('admin_reservas'))

@app.route('/admin/reservas/delete',methods=['POST'])
@login_required
def admin_reservas_delete():
    if not current_user.is_admin():
        return redirect(url_for('index'))
    form = DeleteReserveForm(request.form)
    if form.validate_on_submit():
        try:
            reserva = Reserva.get(Reserva.id == form.reserva_id.data)
            reserva.delete_instance()
        except:
            None
    return redirect(url_for('admin_reservas'))

if __name__ == '__main__':
    app.run(host='localhost', port=1337, debug=True)
