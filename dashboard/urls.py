from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'login/',
        views.login_page,
        name='login'
    ),

    path(
        'logout/',
        views.logout_page,
        name='logout'
    ),

    path(
        'export/',
        views.export_csv,
        name='export_csv'
    ),
]