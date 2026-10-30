
import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Producto


@method_decorator(csrf_exempt, name='dispatch')
class ProductoView(View):

    def get(self, request):
        productos = Producto.objects.all()

        datos = [
            {
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'precio': str(producto.precio),
                'stock': producto.stock
            }
            for producto in productos
        ]

        return JsonResponse(datos, safe=False)

    def post(self, request):
        try:
            datos = json.loads(request.body)

            producto = Producto.objects.create(
                nombre=datos['nombre'],
                descripcion=datos['descripcion'],
                precio=datos['precio'],
                stock=datos['stock']
            )

            return JsonResponse({
                'mensaje': 'Producto creado correctamente',
                'id': producto.id
            }, status=201)

        except (ValueError, KeyError, TypeError):
            return JsonResponse({
                'error': 'Datos incorrectos o incompletos'
            }, status=400)

    def put(self, request):
        try:
            datos = json.loads(request.body)

            producto = Producto.objects.get(id=datos['id'])

            producto.nombre = datos['nombre']
            producto.descripcion = datos['descripcion']
            producto.precio = datos['precio']
            producto.stock = datos['stock']

            producto.save()

            return JsonResponse({
                'mensaje': 'Producto actualizado correctamente'
            })

        except Producto.DoesNotExist:
            return JsonResponse({
                'error': 'Producto no encontrado'
            }, status=404)

        except (ValueError, KeyError, TypeError):
            return JsonResponse({
                'error': 'Datos incorrectos o incompletos'
            }, status=400)

    def delete(self, request):
        try:
            datos = json.loads(request.body)

            producto = Producto.objects.get(id=datos['id'])
            producto.delete()

            return JsonResponse({
                'mensaje': 'Producto eliminado correctamente'
            })

        except Producto.DoesNotExist:
            return JsonResponse({
                'error': 'Producto no encontrado'
            }, status=404)

        except (ValueError, KeyError, TypeError):
            return JsonResponse({
                'error': 'Datos incorrectos o incompletos'
            }, status=400)
