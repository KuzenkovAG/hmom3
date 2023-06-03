from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('apps.users.urls', namespace='users')),
    path('town/', include('apps.towns.urls', namespace='towns')),
    path('statics/', include('apps.stats.urls', namespace='stats')),
    path('about/', include('apps.about.urls', namespace='about')),
    path('market/', include('apps.market.urls', namespace='market')),
    path('management/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
