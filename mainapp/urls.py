from django.urls import path
from django.views.generic import TemplateView

app_name = 'mainapp'

urlpatterns = [
    path('', TemplateView.as_view(template_name='mainapp/main.html'), name='main'),

]
