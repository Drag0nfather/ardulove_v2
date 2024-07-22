from django.urls import path
from . import views

urlpatterns = [
    path('', views.instruction_main, name='instruction_list'),
    path('instruction/<int:instruction_id>/', views.instruction_detail, name='instruction_detail'),
]
