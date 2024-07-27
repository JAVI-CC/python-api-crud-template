from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi import BackgroundTasks
from .conf import conf_mail
from enums.storage_path import StoragePath
from dependencies.jinja2_init import init as jinja2_init


def send_email_verify_user_background(
    background_tasks: BackgroundTasks, email_to: str, url_verify: str
):

    template_env = jinja2_init(StoragePath.TEMPLATES_HTML.value)
    template = template_env.get_template("verify_user.html")
    output_text = template.render(
        {
            "url": url_verify,
            "assets": StoragePath.get_static_images_path,
        }
    )

    message = MessageSchema(
        subject="Verify email",
        recipients=[email_to],
        body=output_text,
        subtype=MessageType.html,
    )

    fm = FastMail(conf_mail)

    background_tasks.add_task(fm.send_message, message)
