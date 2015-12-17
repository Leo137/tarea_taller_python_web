import peewee
from datetime import datetime

db = peewee.SqliteDatabase('base.sqlite')

class BaseModel(peewee.Model):
	class Meta:
		database = db

class Cliente(BaseModel):
    nombre = peewee.CharField()
    password = peewee.CharField()
    fechaInscripcion = peewee.DateTimeField(default=datetime.now())
    baneado = peewee.BooleanField(default=False)
    administrador = peewee.BooleanField(default=False)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return self.baneado

    @property
    def is_authenticated(self):
        return self.nombre != ''

    def is_admin(self):
        return self.administrador

    def get_id(self):
        return unicode(self.id)

class TipoHabitacion(BaseModel):
    nombre = peewee.CharField()
    descripcion = peewee.TextField()
    numeroPersonas = peewee.IntegerField()
    precio = peewee.FloatField()

class Hotel(BaseModel):
    nombre = peewee.CharField()
    region = peewee.CharField()
    ciudad = peewee.CharField()
    direccion = peewee.CharField()
    numeroAtencion = peewee.IntegerField()
    emailContacto = peewee.CharField()

class Habitacion(BaseModel):
    numeroHabitacion = peewee.CharField()
    piso = peewee.IntegerField()
    tipoHabitacion = peewee.ForeignKeyField(TipoHabitacion)
    hotel = peewee.ForeignKeyField(Hotel)

class Reserva(BaseModel):
    fechaPedido = peewee.DateTimeField(default=datetime.now())
    fechaTermino = peewee.DateTimeField(default=datetime.now())
    cliente = peewee.ForeignKeyField(Cliente, related_name='reservas')
    habitacion = peewee.ForeignKeyField(Habitacion, related_name='reservas')
    cancelado = peewee.BooleanField(default=False)
    class Meta:
        database = db

if __name__ == '__main__':
    db.create_tables([Cliente, TipoHabitacion, Hotel, Habitacion, Reserva])
