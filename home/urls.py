from home import views

from django.conf.urls import url, include

app_name = "home"

urlpatterns = [
    url(r'^home/', views.home, name="homes"),
]
