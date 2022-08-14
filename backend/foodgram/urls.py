from django.conf import settings
from django.contrib import admin
from django.urls import include, path

api = [
    path('', include('users.urls', namespace='users')),
    path('', include('recipes.urls', namespace='recipes')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls), name='debug_toolbar')
    ] + urlpatterns
