from django.shortcuts import render
from django.shortcuts import reverse
from accountancy.utility.upload import parse_file_bd
from accountancy.forms import FileUploadForm
from accountancy.models import File
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from accountancy.utility.export import export_file
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect


# Create your views here.
def index(request):
    return render(request, 'accountancy/welcome_page.html')


class Upload(CreateView):
    model = File
    template_name = 'accountancy/upload.html'
    form_class = FileUploadForm

    def get_success_url(self):
        return reverse('success')

    def post(self, request, *args, **kwargs):
        form = FileUploadForm(request.POST, request.FILES)
        name = request.FILES['file'].name
        if form.is_valid():
            if parse_file_bd(request.FILES['file'], request.FILES['file'].temporary_file_path(),
                             name) == -1:  # если файл с таким именем уже был, то переходим на соответствующий шаблон
                return HttpResponseRedirect('exist')
            else:
                return HttpResponseRedirect('success')
        return render(request, 'accountancy/upload.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = FileUploadForm()
        return render(request, 'accountancy/upload.html', {'form': form})


def list(request):
    names_of_files = File.objects.all()
    return render(request, 'accountancy/list.html', {'names_of_files': names_of_files})


def presentation_file(request, file_id):
    name = File.objects.get(id=file_id).name
    export_list = export_file(file_id)
    return render(request, 'accountancy/presentation.html',
                  {'data': export_list,
                   'name': name})  # передается список уже загруженных файлов в соответствующий шаблон.


def success(request):
    return render(request, 'accountancy/success.html')


def exist(request):
    return render(request, 'accountancy/err_exist.html')
