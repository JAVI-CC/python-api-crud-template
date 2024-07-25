import pdfkit
from dependencies.jinja2_init import init as jinja2_init
from schemas.user import User as SchemaUser
from fastapi import Response
from dependencies.root_dir import ROOT_DIR
from dependencies.date_formatter import date_format_server_to_client
from enums.settings import Settings
from enums.storage_path import StoragePath


def export_pdf_list_users(users_list: list[SchemaUser]):

    template_env = jinja2_init(StoragePath.TEMPLATES_PDF.value)

    template = template_env.get_template("users.html")
    output_text = template.render(
        {"users": users_list, "date_fomat": date_format_server_to_client}
    )

    config = pdfkit.configuration(wkhtmltopdf=Settings.WKHTMLTOPDF.value)

    pdf = pdfkit.PDFKit(
        output_text,
        "string",
        configuration=config,
        css=f"{ROOT_DIR}/exports/pdf/styles/users.css",
        options={"orientation": "Landscape"},
    ).to_pdf()

    headers = {"Content-Disposition": 'attachment; filename="user-list.pdf"'}
    return Response(pdf, headers=headers, media_type="application/pdf")
