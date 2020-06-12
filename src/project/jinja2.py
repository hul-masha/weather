from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from dynaconf import settings as _settings
from jinja2 import Environment
from jinja2 import ModuleLoader


def environment(**options):
    if not _settings.PRE_COMPILE:
        env = Environment(**options)
    else:
        env = Environment(loader=ModuleLoader("src/project/target.zip"))
    env.globals.update({"static": static, "url": reverse, "debug": settings.DEBUG})
    return env
