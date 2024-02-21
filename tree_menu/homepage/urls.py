from django.urls import path

from homepage import views


urlpatterns = [
    path('main1/1page1/1sub1/', views.main),
    path('main1/1page1/1sub2/', views.main),
    path('main1/1page1/', views.main),
    path('main1/1page2/2sub1/', views.main),
    path('main1/1page2/2sub2/', views.main),
    path('main1/1page2/', views.main),
    path('main1/', views.main),
    path('main2/2page1/', views.main),
    path('main2/2page2/', views.main),
    path('main2/', views.main),
    path('main3/', views.main),
    path('side1/', views.main),
    path('side2/', views.main),
    path('', views.main)
]
