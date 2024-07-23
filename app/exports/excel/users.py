import xlsxwriter
import io
from fastapi.responses import StreamingResponse
from schemas.user import User as SchemaUser
from dependencies.date_formatter import date_format_server_to_client


def export_excel_list_users(users_list: list[SchemaUser]):

    columns_keys_list = [
        "ID",
        "Name",
        "Surnames",
        "Age",
        "Email",
        "Verified email date",
        "Is active ?",
        "Role",
    ]

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Header principal
    header_merge_format = workbook.add_format(
        {
            "bg_color": "#2197ff",
            "bold": True,
            "size": 18,
            "font_color": "#ffffff",
            "font_name": "Calibri",
            "align": "center",
        }
    )
    worksheet.merge_range("A1:H1", "List of users", header_merge_format)

    # Columns keys
    columns_keys_format = workbook.add_format(
        {
            "bg_color": "#607d8b",
            "bold": True,
            "size": 11,
            "font_color": "#ffffff",
            "font_name": "Calibri",
            "align": "left",
        }
    )

    for col_num, name_column in enumerate(columns_keys_list):
        worksheet.write(
            1, col_num, name_column, columns_keys_format
        )  # Number column -1, Number row

    # Users list
    align_left = workbook.add_format({"align": "Left"})

    for row_num, row_data in enumerate(users_list):
        position_row = row_num + 2
        col_num = 0

        worksheet.write(position_row, col_num, row_data.id)
        col_num += 1
        worksheet.write(position_row, col_num, row_data.name)
        col_num += 1
        worksheet.write(position_row, col_num, row_data.surnames)
        col_num += 1
        worksheet.write(position_row, col_num, row_data.age, align_left)
        col_num += 1
        worksheet.write(position_row, col_num, row_data.email)
        col_num += 1
        worksheet.write(
            position_row,
            col_num,
            (
                date_format_server_to_client(str(row_data.email_verified_at))
                if row_data.email_verified_at is not None
                else "Unverified user"
            ),
        )
        col_num += 1
        worksheet.write(
            position_row, col_num, "True" if row_data.is_active else "False"
        )
        col_num += 1
        worksheet.write(position_row, col_num, row_data.role.name)
        col_num += 1

    worksheet.autofit()

    workbook.close()

    output.seek(0)

    headers = {"Content-Disposition": 'attachment; filename="users-list.xlsx"'}

    return StreamingResponse(output, headers=headers)
