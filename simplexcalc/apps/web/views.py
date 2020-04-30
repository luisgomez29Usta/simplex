from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .simplex import *
import json


def home(request):
    if request.POST:
        # print(request.POST)
        # print("------------------------")
        # print(request.body)
        # print("------------------------")
        data = json.loads(request.body)
        print(data)
        cantidad_variables = data['cantidad_variables']
        cantidad_constrains = data['cantidad_constrains']
        col_values = data['col_values']
        ecuacion_Z = data['ecuacion_Z']
        # print(cantidad_variables, cantidad_constrains, col_values, ecuacion_Z)
        principal()
        return JsonResponse({'status': 'Información a gráficar'})
    else:
        return render(request, 'web/home.html')


def results(request):
    return None
