from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('<str:message>/', views.predict),
]

urlpatterns = format_suffix_patterns(urlpatterns)