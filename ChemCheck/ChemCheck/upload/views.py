from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import Chemkinupload
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'
    #pass


def upload(request):
    if request.method == 'POST':
        form = Chemkinupload(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = Chemkinupload()
    return render(request, 'upload.html', {
        'form': form
    })


    #class FileFieldView(FormView): 
    #form_class = FileFieldForm
    #template_name = 'upload.html'  # Replace with your template.
    #success_url = '...'  # Replace with your URL or reverse().

    #def post(self, request, *args, **kwargs):
     #   form_class = self.get_form_class()
      #  form = self.get_form(form_class)
       # files = request.FILES.getlist('file_field')
        #if form.is_valid():
         #   for f in files:
          #      ...  # Do something with each file.
           # return self.form_valid(form)
        #else:
         #   return self.form_invalid(form)