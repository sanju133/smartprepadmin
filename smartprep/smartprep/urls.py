from django.urls import path, include

urlpatterns = [
    path('materials/', include('materials.urls')),
    path('admins/', include('admins.urls')),
    path('', include('accounts.urls')),
    path('lecturer/', include('lecturer.urls'))

]
