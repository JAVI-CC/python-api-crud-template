import jinja2
from dependencies.root_dir import ROOT_DIR

template_loader = jinja2.FileSystemLoader(f"{ROOT_DIR}/exports/pdf/templates/")
template_env = jinja2.Environment(loader=template_loader)

