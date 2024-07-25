import jinja2
from dependencies.root_dir import ROOT_DIR


def init(path: str):
    template_loader = jinja2.FileSystemLoader(path)
    template_env = jinja2.Environment(loader=template_loader)

    return template_env
