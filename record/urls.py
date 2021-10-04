from django.urls import path

from record import views

urlpatterns = [
    path('search', views.search, name="search"),
    path('download/<slug:meeting_id>/',views.download,name="download")
]
