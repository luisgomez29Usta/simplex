from django.urls import path
from . import views

app_name = 'web'
urlpatterns = [
    # path('', TemplateView.as_view(template_name='web/home.html'), name='home'),
    path('', views.home, name='home'),
    path('results', views.results, name='results'),

]
