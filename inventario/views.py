from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Producto, Venta
from .forms import ProductoForm
from django.utils import timezone
from .decorators import role_required

User = get_user_model()

# Create your views here.

#Gestion de usuarios
def home(request):
    return render(request, "home.html")

def crear_usuario(request):
    if request.method == "GET":
        return render(request, "crear_usuario.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"]
                )
                user.save()
                return redirect('pendiente')
            except Exception as e:
                print(e)
                return render(request, "crear_usuario.html", {"form": UserCreationForm, "error": "El usuario ya existe"})
        else:
            return render(request, "crear_usuario.html", {"form": UserCreationForm, "error": "Las contraseñas no coinciden"})
        
def pendiente(request):
    return render(request, "pendiente.html")

def ingresar(request):
    if request.method == "GET":
        return render(request, "ingresar.html", {"form": AuthenticationForm})
    else:
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None and user.rol != "pendiente":
            login(request, user)
            return redirect('home')
        else:
            return render(request, "ingresar.html", {"form": AuthenticationForm, "error": "Usuario o contraseña incorrectos o usuario pendiente"})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

#Gestion de productos
@login_required
def productos(request):
    productos = Producto.objects.all()
    ventas_totales = Venta.objects.all()
    return render(request, "productos.html", {
        "productos": productos,
        "totales": len(productos),
        "agotados": len(productos.filter(cantidad=0)),
        "ventas_totales": len(ventas_totales)
        })

@login_required
@role_required(["admin", "almacenista"])
def crear_producto(request):
    if request.method == "GET":
        return render(request, "crear_producto.html", {"form": ProductoForm})
    else:
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("productos")
        else:
            error = "Los datos no son válidos"
            return render(request, "crear_producto.html", {"form": ProductoForm, "error": error})
        
@login_required
@role_required(["admin", "almacenista"])
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == "GET":
        form = ProductoForm(instance=producto)
        return render(request, "editar_producto.html", {"form": form, "producto": producto})
    else:
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("productos")
        else:
            error = "Los datos no son válidos"
            return render(request, "editar_producto.html", {"form": form, "error": error, "producto": producto})

@login_required
@role_required(["admin", "almacenista"])
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if producto:
        producto.delete()
        return redirect("productos")
    

@login_required
@role_required(["admin", "vendedor"])
def vender_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == "POST":
        cantidad = int(request.POST["cantidad"])
        if cantidad > 0 and cantidad <= producto.cantidad:
            producto.cantidad -= cantidad
            producto.save()
            venta = Venta(producto=producto, cantidad=cantidad, fecha=timezone.now(), vendedor=request.user)
            venta.save()
            return redirect("productos")
        else:
            error = "Cantidad no válida"
            return render(request, "productos.html", {"producto": producto, "error": error})
    return render(request, "productos.html", {"producto": producto})

@login_required
def ventas(request):
    ventas = Venta.objects.all()
    return render(request, "ventas.html", {"ventas": ventas})