from django.contrib import admin
from django.urls import path, include

# from ..blog


urlpatterns = [
    path('admin/', admin.site.urls),
    path('trumbowyg', include('trumbowyg.urls'))
]
