from typing import Optional

import jinja2

from isu_info_bot import config


def render_template(template_name: str, data: Optional[dict] = None) -> str:
    if data is None:
        data = {}
    template = _get_template_env().get_template(template_name)
    rendered = template.render(**data)
    return rendered


def _get_template_env():
    if not getattr(_get_template_env, "template_env", None):
        template_loader = jinja2.FileSystemLoader(searchpath=config.TEMPLATES_DIR)
        env = jinja2.Environment(
            loader=template_loader,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )

        _get_template_env.template_env = env

    return _get_template_env.template_env
