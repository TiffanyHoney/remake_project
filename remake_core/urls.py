from django.contrib import admin
from django.urls import path, include

# 반드시 추가
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔽 로그인/로그아웃 등 인증 관련 URL 추가
    path('accounts/', include('django.contrib.auth.urls')),

    # 게시판 앱
    path('', include('board.urls')),
]

# 개발 모드일 때만 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
