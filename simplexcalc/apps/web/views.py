from django.http import JsonResponse
from django.shortcuts import render
from .simplexClass import Simplex
import json


def home(request):
    if request.POST:
        data = json.loads(request.body)
        cv = data['cantidad_variables']
        cc = data['cantidad_constrains']
        cval = data['col_values']
        z = data['ecuacion_Z']
        obj = Simplex(cv, cc, cval, z)
        obj.display()
        obj.calculate()
        return JsonResponse({'status': 'Información a gráficar'})
    else:
        return render(request, 'web/home.html')


def results(request):
    return None
