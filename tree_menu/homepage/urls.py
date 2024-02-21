from django.urls import path

from homepage import views


urlpatterns = [
    path('in_main_1/in_1_1/in_1_1_1', views.main, name='in_1_1_1'),
    path('in_main_1/in_1_1/in_1_1_2', views.main, name='in_1_1_2'),
    path('in_main_1/in_1_1', views.main, name='in_1_1'),
    path('in_main_1/in_1_2', views.main, name='in_1_2'),
    path('in_main_2/in_2_1', views.main, name='in_2_1'),
    path('in_main_2/in_2_2', views.main, name='in_2_2'),
    path('in_main_1', views.main, name='in_main_1',),
    path('in_main_2', views.main, name='in_main_2',),
    path('', views.main)
]
