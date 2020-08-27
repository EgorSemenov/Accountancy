from django.shortcuts import render
from django.shortcuts import reverse
from accountancy.controllers.handlers import handle_uploaded_file
from accountancy.forms import FileUploadForm
from accountancy.models import File
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from accountancy.utility.export_module import export_file
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect


# Create your views here.
def index(request):
    return render(request, 'accountancy/welcome_page.html')


class upload(CreateView):
    model = File
    template_name = 'accountancy/upload.html'
    form_class = FileUploadForm

    def get_success_url(self):
        return reverse('success')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = FileUploadForm(request.POST, request.FILES)
            name = request.FILES['file'].name
            if form.is_valid():
                if handle_uploaded_file(request.FILES['file'], request.FILES['file'].temporary_file_path(),
                                        name) == -1:
                    return HttpResponseRedirect('exist')
                else:
                    return HttpResponseRedirect('success')
        else:
            form = FileUploadForm()
        return render(request, 'accountancy/upload.html', {'form': form})


def list(request):
    names_of_files = File.objects.all()
    return render(request, 'accountancy/list.html', {'names_of_files': names_of_files})


def presentation_file(request, file_id):
    name = File.objects.get(id=file_id).name
    export_list = export_file(file_id)
    return render(request, 'accountancy/presentation.html', {'data': export_list, 'name': name})


def success(request):
    return render(request, 'accountancy/success.html')


def exist(request):
    return render(request, 'accountancy/err_exist.html')
