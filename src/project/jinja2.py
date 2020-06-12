from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse
from dynaconf import settings as _settings
from jinja2 import Environment
from jinja2 import ModuleLoader

# Compile template
# Environment(loader=FileSystemLoader('foopkg/templates'))\
#   .compile_templates("foopkg/compiled/foopkg.zip")

# Environment
# env = Environment(loader=ModuleLoader("foopkg/compiled/foopkg.zip"))


def environment(**options):
    if not _settings.PRE_COMPILE:
        env = Environment(**options)
    # раскоментить когда меняю содержимое шаблона или создаю новый
    # Environment(**options).compile_templates("src/project/target.zip")
    else:
        env = Environment(loader=ModuleLoader("src/project/target.zip"))
    env.globals.update({"static": static, "url": reverse, "debug": settings.DEBUG})
    return env
