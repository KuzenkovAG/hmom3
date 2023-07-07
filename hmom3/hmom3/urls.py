from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('apps.users.urls', namespace='users')),
    path('town/', include('apps.towns.urls', namespace='towns')),
    path('statics/', include('apps.stats.urls', namespace='stats')),
    path('about/', include('apps.about.urls', namespace='about')),
    path('market/', include('apps.market.urls', namespace='market')),
    path('hooks/', include('apps.webhooks.urls', namespace='webhooks')),
    path('management/', admin.site.urls),
    path(
        'yandex_ab06da8ab2a9aead.html',
        TemplateView.as_view(
            template_name='search_system/yandex_ab06da8ab2a9aead.html'
        )
    ),
    path(
        'robots.txt',
        TemplateView.as_view(
            template_name='search_system/robots.txt',
            content_type='text/plain'
        )
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
