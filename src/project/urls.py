from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path

# from apps.thoughts.views import view

STATIC_DIR = settings.PROJECT_DIR / "static"
# CSS_PATH_BOOTS = STATIC_DIR / "css" / "bootstrap.min.css"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.index.urls")),
    # path('re/', view, name="re"),
    # path('tho/', view, name="tho"),
    # path('index.html', include("apps.index.urls")), #view),
    # path('css/bootstrap.min.css', bootstrap),
    # path('css/hero-slider-style.css', hero),
    # path('css/magnific-popup.css', magn),
    # path('css/tooplate-style.css', toop),
    # path('css/font-awesome.min.css', awesome),
    # path('assets/gBAs.jpg',img),
    # path('favicon.ico',ico),
    # path('fonts/fontawesome-webfont.woff2', woff2),
    # path('fonts/fontawesome-webfont.woff', woff),
    # path('fonts/fontawesome-webfont.ttf', ttf),
    # path('js/bootstrap.min.js', jsbootstrap),
    # path('js/hero-slider-main.js',jshero),
    # path('js/jquery.magnific-popup.min.js',jsmag),
    # path('js/jquery-1.11.3.min.js',jsjquery),
    # path('fontawesome-webfont.svg',svg),
    # path('fonts/fontawesome-webfont.eot',eot),
    # path('fonts/FontAwesome.otf',otf),
]

if settings.DEBUG and settings.PROFILING:  # pragma: no cover
    urlpatterns.append(re_path(r"^silk/", include("silk.urls", namespace="silk")))


# def view(r, f=static_re):
#   return f(file="index.html")#так код работает быстрее тут не тратиться время на поиск имени функ при ее вызове
# но эт все равно копейки (связь с именем установ при синтак дереве поэтому не тратиться время на  ее поиск )
# render(r,"index.html")
