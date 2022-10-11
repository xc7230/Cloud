from django.contrib import admin
from django.urls import path, include
import board.views
import reply.views
import accounts.views
from django.conf.urls.static import static
from config import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('board/create', board.views.create),
                  path('', board.views.list),
                  path('board/read/<int:bid>', board.views.read),
                  path('board/delete/<int:bid>', board.views.delete),
                  path('board/update/<int:bid>', board.views.update),

                  path('reply/create/<int:bid>', reply.views.create),
                  path('reply/update/<int:bid>/<int:rid>', reply.views.update),
                  path('reply/delete/<int:rid>', reply.views.delete),
                  path('like/<int:bid>', board.views.like),

                  path('accounts/', include('allauth.urls')),
                  path('accounts/profile', accounts.views.profile),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
