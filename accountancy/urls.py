from django.urls import path

from . import views

app_name = 'accountancy'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.Upload.as_view(), name='upload'),
    path('list', views.list, name='list'),
    path('list/<int:file_id>/', views.presentation_file, name='presentation'),  # через этот путь передается id файла, который следует отобразить
    path('exist', views.exist, name='exist'),
    path('success', views.success, name='success')
]
