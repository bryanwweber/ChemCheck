from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView, View
from .forms import ChemkinUpload
from .models import Mechanism
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import os
from django.core.files.base import File
from django.urls import reverse_lazy


# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'
   

def upload(request):
    if request.method == 'POST':
        form = ChemkinUpload(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/list/')
    else:
        form = ChemkinUpload()
    return render(request, 'upload.html', {
        'form': form
    })

def ck2yaml(request, pk):
    mechanism = get_object_or_404(Mechanism, pk=pk)

    conversion_log = "Going to try this..."

    from .ck2yaml import Parser
    import traceback
    import logging

    parser = Parser()
    input_file = mechanism.ck_mechanism_file.path
    thermo_file =  mechanism.ck_thermo_file.path if mechanism.ck_thermo_file else None
    transport_file = mechanism.ck_transport_file.path if mechanism.ck_transport_file else None
    surface_file = mechanism.ck_surface_file.path if mechanism.ck_surface_file else None
    phase_name = None # will default to 'gas'
    out_name = os.path.join(os.path.split(input_file)[0], 'cantera.txt')


    try:
        parser.convert_mech(input_file, 
                        thermo_file, 
                        transport_file,
                        surface_file,
                        phase_name,
                        out_name = out_name,
                        quiet = False,
                        permissive = True,
                        )
    except Exception as e:
        conversion_log += str(e)                      
        error_message = traceback.format_exc()
        conversion_log += error_message
        mechanism.ct_conversion_errors = error_message
        mechanism.ct_mechanism_file = None
        mechanism.save()
    else:
        mechanism.ct_mechanism_file = out_name
        mechanism.save()
        conversion_log += f"\nConversion successful!\nCantera yaml file saved to {out_name}"
    return render(request, 'ck2yaml.html', {
       'mech': mechanism,
       'conversion_log': conversion_log,
    })

    
class MechanismDetailView(DetailView):
    model = Mechanism
    
def ace_mech(request, pk):
    mechanism = get_object_or_404(Mechanism, pk=pk)
    f = mechanism.ck_mechanism_file.path
    content = open(f, "r").read()
    return render(request, 'ace.html', {
        'content': content,
        'mechanism': mechanism
        })
def ace_therm(request, pk):
    mechanism = get_object_or_404(Mechanism, pk=pk)
    f = mechanism.ck_thermo_file.path
    content = open(f, "r").read()
    return render(request, 'ace.html', {
        'content': content,
        'mechanism': mechanism
        })
def ace_trans(request, pk):
    mechanism = get_object_or_404(Mechanism, pk=pk)
    f = mechanism.ck_transport_file.path
    content = open(f, "r").read()
    return render(request, 'ace.html', {
        'content': content,
        'mechanism': mechanism
        })
def ace_surf(request, pk):
    mechanism = get_object_or_404(Mechanism, pk=pk)
    f = mechanism.ck_surface_file.path
    content = open(f, "r").read()
    return render(request, 'ace.html', {
        'content': content,
        'mechanism': mechanism
        })

def mechanisms_list(request):
    mechanisms = Mechanism.objects.all()
    return render(request, 'list.html', {
       'mechanisms': mechanisms
    })
    
class MechanismObjectMixin(object):
    model = Mechanism
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = None
        if pk is not None:
            obj = get_object_or_404(self.model, pk=pk)
        return obj

class MechanismDeleteView(MechanismObjectMixin, View):
    template_name="file_delete_mechanism.html"
    def get(self, request, id=id, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object().ck_mechanism_file
        if obj is not None:
            obj.delete()
            context['object'] = None
            return HttpResponseRedirect('/list/')
        return render(request, self.template_name, context)

class MechanismthermoDeleteView(MechanismObjectMixin, View):
    template_name="file_delete_thermo.html"
    def get(self, request, id=id, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object().ck_thermo_file
        if obj is not None:
            obj.delete()
            context['object'] = None
            return HttpResponseRedirect('/list/')
        return render(request, self.template_name, context)


class MechanismtransportDeleteView(MechanismObjectMixin, View):
    template_name="file_delete_transport.html"
    def get(self, request, id=id, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object().ck_transport_file
        if obj is not None:
            obj.delete()
            context['object'] = None
            return HttpResponseRedirect('/list/')
        return render(request, self.template_name, context)

class MechanismsurfaceDeleteView(MechanismObjectMixin, View):
    template_name="file_delete_surface.html"
    def get(self, request, id=id, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        obj = self.get_object().ck_surface_file
        if obj is not None:
            obj.delete()
            context['object'] = None
            return HttpResponseRedirect('/list/')
        return render(request, self.template_name, context)


class MechanismUpdateView(MechanismObjectMixin, View):
    template_name="file_update.html"
    def get(self, request, id=id, *args, **kwargs):
        context = {}
        obj = self.get_object()
        if obj is not None:
            form = ChemkinUpload(instance=obj)
            context['object'] = obj
            context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()

        form = ChemkinUpload(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            url = reverse_lazy('mechanism-detail', args=[obj.pk])
            return HttpResponseRedirect(url)
    