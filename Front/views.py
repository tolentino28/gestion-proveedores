from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# Importar Q para realizar búsquedas OR
from django.db.models import Q  

# Importa los modelos necesarios
from .models import Producto
from .models import Proveedor
from .models import Compra, Cuota, Pago

# Create your views here.
def Inicio(request):
    return render(request, 'Inicio.html')

def Información(request):
    return render(request, 'Información.html')

def Contacto(request):
    return render(request, 'Contacto.html')

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado')
            return render(request, 'Registro')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuario ya registrado')
            return render(request, 'Registro')
        
        nuevo_usuario = User(
            username=username,
            email=email,
            password=make_password(password)
        )
        nuevo_usuario.save()
        return redirect('IniciarSesión' )
    return render(request, 'Registro.html') 

def IniciarSesión(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if Producto.objects.filter(id_usuario=user).exists():
                return redirect('Proveedores') 
            return redirect('RegistroProductoBienvenida') 

        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'Iniciar-Sesión.html')

def CerrarSesion(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('Inicio')

@login_required
def RegistroProductoBienvenida(request):
    return render(request, 'Registro-Producto-Bienvenida.html', {'tituloHead': "Registrar Producto"})

@login_required
def RegistroProducto(request):
    # Intentar obtener el producto del usuario logueado
    producto = Producto.objects.filter(id_usuario=request.user).first()

    if request.method == 'POST':
        nombre = request.POST.get('producto')
        descripcion = request.POST.get('descripcion')
        unidad_de_medida = request.POST.get('unidad')
        imagen = request.FILES.get('imagen') 

        # Si el usuario ya tiene un producto, lo actualizamos
        if producto:
            producto.nombre = nombre
            producto.descripcion = descripcion
            producto.unidad_de_medida = unidad_de_medida
            if imagen:
                producto.imagen = imagen
            # Actualizar la fecha_registro si quieres reflejar modificación
            producto.fecha_registro = timezone.now()
            producto.save()
        else:
            # Crear un nuevo producto
            producto = Producto(
                id_usuario=request.user, 
                nombre=nombre,
                descripcion=descripcion,
                unidad_de_medida=unidad_de_medida,
                imagen=imagen,
                fecha_registro=timezone.now()
            )
            producto.save()

        return redirect('Proveedores') 

    # Pasamos el producto al template, puede ser None
    if producto:
        titulo_head = "Actualizar Producto"
    else:
        titulo_head = "Registrar Producto"

    return render(request, 'Registro-Producto.html', {
        'tituloHead': titulo_head,
        'producto': producto
    })

@login_required
def RegistrarOEditarProveedor(request, id_proveedor=None):
    proveedor = None
    # Si estamos editando, obtenemos el proveedor
    if id_proveedor:
        try:
            proveedor = Proveedor.objects.get(id_proveedor=id_proveedor, id_usuario=request.user)
        except Proveedor.DoesNotExist:
            messages.error(request, 'Proveedor no encontrado o no tienes permiso para editarlo.')
            return redirect('Proveedores')

    # Si es un POST, procesamos el formulario
    if request.method == 'POST':
        dni_pasaporte = request.POST.get('dni_pasaporte')
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        telefono = request.POST.get('telefono')
        ubicacion = request.POST.get('ubicacion')
        correo_electronico = request.POST.get('correo_electronico')

        # Verificar si el correo electrónico ya está registrado para este usuario
        if Proveedor.objects.filter(id_usuario=request.user, correo_electronico=correo_electronico).exclude(id_proveedor=id_proveedor).exists():
            messages.error(request, 'Correo electrónico ya registrado para otro proveedor.')
            return render(request, 'Registro-Proveedor.html', {'tituloHead': "Registrar Proveedor" if not proveedor else "Editar Proveedor", 'proveedor': proveedor})

        # Verificar si el DNI/Pasaporte ya está registrado para este usuario
        if Proveedor.objects.filter(id_usuario=request.user, dni_pasaporte=dni_pasaporte).exclude(id_proveedor=id_proveedor).exists():
            messages.error(request, 'DNI/Pasaporte ya registrado para otro proveedor.')
            return render(request, 'Registro-Proveedor.html', {'tituloHead': "Registrar Proveedor" if not proveedor else "Editar Proveedor", 'proveedor': proveedor})

        # Si estamos editando, actualizamos el proveedor
        if proveedor:
            proveedor.dni_pasaporte = dni_pasaporte
            proveedor.nombre = nombre
            proveedor.apellidos = apellidos
            proveedor.telefono = telefono
            proveedor.ubicacion = ubicacion
            proveedor.correo_electronico = correo_electronico
            proveedor.save()

        else:
            # Si estamos creando un nuevo proveedor
            proveedor = Proveedor(
                id_usuario=request.user, 
                dni_pasaporte=dni_pasaporte,
                nombre=nombre,
                apellidos=apellidos,
                telefono=telefono,
                ubicacion=ubicacion,
                correo_electronico=correo_electronico,
                fecha_hora_registro=timezone.now()
            )
            proveedor.save()

        return redirect('Proveedores')

    # Si es un GET, mostramos el formulario con los datos del proveedor (si es edición)
    return render(request, 'Registro-Proveedor.html', {
        'tituloHead': "Editar Proveedor" if proveedor else "Registrar Proveedor",
        'proveedor': proveedor  # Pasamos el objeto proveedor para prellenar los campos
    })

@login_required
def Proveedores(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda desde la URL

    # Si hay un término de búsqueda, filtramos los proveedores
    if query:
        proveedores = Proveedor.objects.filter(
            id_usuario=request.user
        ).filter(
            # Usamos Q para combinar los filtros de forma OR
            Q(nombre__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(telefono__icontains=query) |
            Q(dni_pasaporte__icontains=query) |
            Q(ubicacion__icontains=query)
        )
    else:
        # Si no hay búsqueda, mostramos todos los proveedores del usuario autenticado
        proveedores = Proveedor.objects.filter(id_usuario=request.user)

    return render(request, 'Proveedores.html', {'proveedores': proveedores, 'query': query})

def EliminarProveedor(request, id_proveedor):
    proveedor = Proveedor.objects.get(id_proveedor=id_proveedor)
    proveedor.delete()
    messages.success(request, 'Proveedor eliminado correctamente.')
    return redirect('Proveedores')

@login_required
def Compras(request):
    query = request.GET.get('q', '')  # Recupera el término de búsqueda

    if query:
        # Si hay un término de búsqueda, filtramos las compras
        compras = Compra.objects.filter(
            id_proveedor__id_usuario=request.user  # Filtramos las compras asociadas al usuario
        ).filter(
            Q(cantidad__icontains=query) |  # Buscar en la cantidad
            Q(precio__icontains=query) |  # Buscar en el precio
            Q(monto_total__icontains=query) |  # Buscar en el monto total
            Q(nivel_calidad__icontains=query) |  # Buscar en el nivel de calidad
            Q(observacion__icontains=query) |  # Buscar en las observaciones
            Q(tipo_pago__icontains=query) |  # Buscar en el tipo de pago
            Q(fecha_compra__icontains=query)  # Buscar en la fecha de compra
        )
    else:
        # Si no hay búsqueda, mostramos todas las compras del usuario autenticado
        compras = Compra.objects.filter(id_proveedor__id_usuario=request.user)

    # Pasamos las compras y el término de búsqueda al contexto
    return render(request, 'Compras.html', {'compras': compras, 'query': query})

@login_required
def FormularioCompra(request):
    proveedores = Proveedor.objects.filter(id_usuario=request.user)
    context = {'proveedores': proveedores, 'tituloHead': "Registrar Compra"}

    if request.method == 'POST':
        try:
            # Recoger datos del formulario
            proveedor = Proveedor.objects.get(id_proveedor=request.POST.get('proveedor'))
            producto = Producto.objects.get(id_usuario=request.user)
            cantidad = int(request.POST['cantidad'])
            precio = float(request.POST['precio'])
            nivel_calidad = request.POST['calidad']
            tipo_pago = request.POST['tipo_pago']
            observaciones = request.POST.get('observaciones', '')

            monto_total = cantidad * precio

            # Crear la compra
            compra = Compra.objects.create(
                id_producto=producto,
                id_proveedor=proveedor,
                cantidad=cantidad,
                precio=precio,
                monto_total=monto_total,
                nivel_calidad=nivel_calidad,
                tipo_pago=tipo_pago,
                observacion=observaciones,
                fecha_compra=timezone.now()
            )

            # Manejo del tipo de pago
            if tipo_pago == 'cuotas':
                num_cuotas = int(request.POST.get('num_cuotas', 0))
                fecha_pago = request.POST.get('fecha_pago')
                if num_cuotas > 0 and fecha_pago:
                    # Calcular el monto por cuota (sin afectar cantidad_cuotas)
                    monto_por_cuota = monto_total / num_cuotas if num_cuotas != 0 else 0
                    
                    # Crear una sola cuota asociada a la compra
                    Cuota.objects.create(
                        id_compra=compra,
                        cantidad_cuotas=num_cuotas,  # Asignar directamente num_cuotas
                        monto=monto_por_cuota,
                        fecha_vencimiento=fecha_pago,
                        estado_pago='Pendiente',
                        cuotas_pagadas=0
                    )
                else:
                    messages.error(request, 'Faltan datos para el pago en cuotas.')
                    return render(request, 'Registro-Compra.html', context)


            elif tipo_pago == 'contado':
                # Verificar que los datos del modal de contado estén presentes
                metodo_pago = request.POST.get('metodo_pago_contado')
                evidencia_pago = request.FILES.get('evidencia_pago_contado')
                if metodo_pago:
                    Pago.objects.create(
                        id_compra=compra,
                        metodo_pago=metodo_pago,
                        evidencia_pago=evidencia_pago,
                        fecha_pago=timezone.now()
                    )
                else:
                    messages.error(request, 'Faltan datos para el pago contado.')
                    return render(request, 'Registro-Compra.html', context)

            # Redirigir con mensaje de éxito
            messages.success(request, 'Compra registrada exitosamente.')
            return redirect('Compras')

        except Proveedor.DoesNotExist:
            messages.error(request, 'Proveedor no válido.')
        except Producto.DoesNotExist:
            messages.error(request, 'Producto no encontrado.')
        except Exception as e:
            messages.error(request, f'Error al registrar la compra: {str(e)}')

    return render(request, 'Registro-Compra.html', context)

def EliminarCompra(request, id_compra):
    compra = Compra.objects.get(id_compra=id_compra)
    compra.delete()
    messages.success(request, 'Compra eliminada correctamente.')
    return redirect('Compras')

def Pagos(request):
    return render(request, 'Pagos.html')

@login_required
def Perfil(request):
    return render(request, 'Perfil.html', {'user': request.user})

def obtener_cuotas(request, compra_id):
    try:
        # Obtener la compra usando el campo correcto
        compra = Compra.objects.get(id_compra=compra_id)
        
        # Obtener la única cuota asociada a la compra
        cuota = Cuota.objects.get(id_compra=compra)
        
        # Crear un diccionario con los datos de la cuota
        cuota_data = {
            'id_cuota': cuota.id_cuota,
            'estado': cuota.estado_pago,
            'total_cuotas': cuota.cantidad_cuotas,
            'monto_por_cuota': float(cuota.monto),
            'cuotas_pagadas': cuota.cuotas_pagadas or 0,
            'vencimiento': cuota.fecha_vencimiento.strftime('%Y-%m-%d'),
            'total': float(compra.monto_total)
        }

        return JsonResponse(cuota_data)

    except Compra.DoesNotExist:
        return JsonResponse({'error': 'Compra no encontrada'}, status=404)
    except Cuota.DoesNotExist:
        return JsonResponse({'error': 'Cuota no encontrada para esta compra'}, status=404)

@csrf_exempt
def registrar_pago(request, cuota_id):
    if request.method == "POST":
        try:
            cuota = Cuota.objects.get(pk=cuota_id)  # Buscar la cuota por ID
            compra = cuota.id_compra  # Obtener la compra relacionada con la cuota

            # Verificar si la cuota ya está pagada
            if cuota.estado_pago == "pagada":
                return JsonResponse({"success": False, "message": "La cuota ya está pagada"}, status=400)

            # Manejar datos del formulario
            metodo_pago = request.POST.get('metodo_pago')
            fecha_pago = request.POST.get('fecha_pago')

            # Manejar archivo de evidencia de pago
            evidencia_pago = request.FILES.get('evidencia_pago')

            # Validar datos necesarios
            if not metodo_pago or not fecha_pago:
                return JsonResponse({"success": False, "message": "Faltan datos requeridos"}, status=400)

            # Registrar el pago
            pago = Pago.objects.create(
                id_cuota=cuota,
                id_compra=compra,
                fecha_pago=fecha_pago,
                metodo_pago=metodo_pago,
                evidencia_pago=evidencia_pago
            )

            # Incrementar el campo cuotas_pagadas de la cuota
            cuota.cuotas_pagadas = (cuota.cuotas_pagadas or 0) + 1  # Manejar None
            cuota.save()

            # Verificar el estado de la cuota
            if cuota.cuotas_pagadas >= cuota.cantidad_cuotas:
                cuota.estado_pago = "pagada"
            elif cuota.fecha_vencimiento < timezone.now().date():
                cuota.estado_pago = "vencida"
            else:
                cuota.estado_pago = "pendiente"

            cuota.save()  # Guardar la actualización del estado de la cuota

            return JsonResponse({"success": True, "message": "Pago registrado exitosamente"})
        except Cuota.DoesNotExist:
            return JsonResponse({"success": False, "message": "Cuota no encontrada"}, status=404)
        except Compra.DoesNotExist:
            return JsonResponse({"success": False, "message": "Compra no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)

