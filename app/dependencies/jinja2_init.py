import jinja2

def init(path: str):
    template_loader = jinja2.FileSystemLoader(path)
    template_env = jinja2.Environment(loader=template_loader)

    return template_env
