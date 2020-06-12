from jinja2 import Environment
from jinja2 import FileSystemLoader

opt = [
    "src/project/jinja2",
    "src/apps/index/jinja2",
    "src/apps/resume/jinja2",
    "src/apps/thoughts/jinja2",
    "src/apps/blog/jinja2",
    "src/apps/onboarding/jinja2",
]  # задать пути неявно
Environment(loader=FileSystemLoader(opt)).compile_templates("src/project/target.zip")
