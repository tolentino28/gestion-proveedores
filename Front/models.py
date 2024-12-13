from django.db import models
from django.contrib.auth.models import User

class Proveedor(models.Model):
    id_proveedor = models.AutoField(db_column='ID_Proveedor', primary_key=True)
    id_usuario = models.ForeignKey(User, models.CASCADE, db_column='ID_Usuario')  
    dni_pasaporte = models.CharField(db_column='DNI_Pasaporte', max_length=50)
    nombre = models.CharField(db_column='Nombre', max_length=255)
    apellidos = models.CharField(db_column='Apellido_Paterno', max_length=255, null=True)
    telefono = models.CharField(db_column='Telefono', max_length=15, blank=True, null=True)
    correo_electronico = models.EmailField(db_column='Correo_Electronico', max_length=255)
    ubicacion = models.CharField(db_column='Ubicacion', max_length=255, blank=True, null=True)
    fecha_hora_registro = models.DateTimeField(db_column='Fecha_Hora_Registro', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    class Meta:
        db_table = 'proveedor'

class Producto(models.Model):
    id_producto = models.AutoField(db_column='ID_Producto', primary_key=True)
    id_usuario = models.ForeignKey(User, models.CASCADE, db_column='ID_Usuario') 
    nombre = models.CharField(db_column='Nombre', max_length=255)
    descripcion = models.CharField(db_column='Descripcion', max_length=255, blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    fecha_registro = models.DateField(db_column='Fecha_Registro', blank=True, null=True)
    unidad_de_medida = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'producto'

class Compra(models.Model):
    id_compra = models.AutoField(db_column='ID_Compra', primary_key=True)
    id_producto = models.ForeignKey('Producto', models.CASCADE, db_column='ID_Producto')  
    id_proveedor = models.ForeignKey('Proveedor', models.CASCADE, db_column='ID_Proveedor') 
    fecha_compra = models.DateField(db_column='Fecha_Compra', blank=True, null=True)
    cantidad = models.IntegerField(db_column='Cantidad')
    precio = models.DecimalField(db_column='Precio', max_digits=10, decimal_places=2)
    monto_total = models.DecimalField(db_column='Monto_Total', max_digits=10, decimal_places=2)
    nivel_calidad = models.CharField(db_column='Nivel_Calidad', max_length=5)
    observacion = models.TextField(db_column='Observacion', blank=True, null=True)
    tipo_pago = models.CharField(db_column='Tipo_Pago', max_length=7)

    class Meta:
        db_table = 'compra'

    def __str__(self):
        return f"Compra {self.id_proveedor.nombre} - {self.id_compra}"

class Cuota(models.Model):
    id_cuota = models.AutoField(db_column='ID_Cuota', primary_key=True)
    id_compra = models.OneToOneField(Compra, models.CASCADE, db_column='ID_Compra') 
    cantidad_cuotas = models.IntegerField(db_column='Cantidad_Cuotas') 
    monto = models.DecimalField(db_column='Monto', max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField(db_column='Fecha_Vencimiento')
    estado_pago = models.CharField(db_column='Estado_Pago', max_length=10, blank=True, null=True)
    cuotas_pagadas = models.IntegerField(db_column='Cuotas_Pagadas', blank=True, null=True)

    def __str__(self):
        return f"Cuota {self.cantidad_cuotas} de Compra {self.id_compra.id_compra}"

    class Meta:
        db_table = 'cuota'

class Pago(models.Model):
    id_pago = models.AutoField(db_column='ID_Pago', primary_key=True)
    id_cuota = models.ForeignKey(Cuota, models.CASCADE, db_column='ID_Cuota', null=True, blank=True)  
    id_compra = models.ForeignKey(Compra, models.CASCADE, db_column='ID_Compra') 
    fecha_pago = models.DateField(db_column='Fecha_Pago', blank=True, null=True)
    metodo_pago = models.CharField(db_column='Metodo_Pago', max_length=13)
    evidencia_pago = models.ImageField(upload_to='Evidencia_Pagos/', blank=True, null=True)

    def __str__(self):
        return f"Pago {self.id_pago} - {self.id_cuota}"

    class Meta:
        db_table = 'pago'