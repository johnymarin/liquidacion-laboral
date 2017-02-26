from django.contrib import messages
from django.shortcuts import render
from django.core.cache import cache
from django.core import serializers
from django.views.decorators.cache import cache_control
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import  Liquidacion
from .forms import LiquidacionForm, TerminoFijoForm, ObraLaborForm, IndefinidoForm
# Create your views here.

TIPOS_DE_FORMULARIO = {
    'f_normal': LiquidacionForm,
    'f_fijo': TerminoFijoForm,
    'f_obra': ObraLaborForm,
    'f_servicios': 'Servicios',
    'f_indefinido': IndefinidoForm
}

#TODO write views for the new home page
def home(request):
    return render(request, 'liquidacion/home.html')


@cache_control(private=True)
def full_form(request, p_tipo = 'f_normal'):
    p_form = TIPOS_DE_FORMULARIO[p_tipo]
    #If this is a POST request we need to process data
    if request.method=='POST':
        #we create a form instance an populate with data form request:
        form = p_form(request.POST)
        #check wheter it's valid:
        if form.is_valid():
            #process the data in form.cleaned_data as required
            #...do stuff
            #instance a Liquidacion object from From
            instanceLiquidacion = Liquidacion(**form.cleaned_data)
            instanceLiquidacion.save()
            request.session['liquidacion_calculada'] = instanceLiquidacion.id
            #redirect to a new page with the results
            return HttpResponseRedirect('resultados')
        #if not valid form add error messages and render the form
        else:
            form = p_form()
            #FIXME delete this 'hola mundo'
            messages.error(request,'hola mundo.')
            return render(request,'liquidacion/full_form.html', {'form':form})
    # if is a get or any other method we create a new form
    else:
        form = p_form()
        return render(request,'liquidacion/full_form.html',{'form':form})

#TODO write a view for a simplified form termino fijo



#TODO write a view for simplified form construccion

#TODO write a view for simplified form servicio

#TODO write a view for simplified form indefinido

@cache_control(private=True)
def results(request):
    try:
        instanceLiquidacion2 = Liquidacion.objects.get(id=request.session['liquidacion_calculada'])
        return render(request,'liquidacion/results.html',{'liquidacion':instanceLiquidacion2})
    except KeyError:
        return render(request,'liquidacion/results.html',)