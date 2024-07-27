import io
import PIL.Image as Image
import xlsxwriter
from fastapi.responses import StreamingResponse
from dependencies.date_formatter import date_format_server_to_client
from enums.storage_path import StoragePath
from schemas.user import User as SchemaUser


def export_excel_list_users(users_list: list[SchemaUser]):

    columns_keys_list = [
        "Image profile",
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
    worksheet.merge_range("A1:I1", "List of users", header_merge_format)

    # Columns keys
    columns_keys_format = workbook.add_format(
        {
            "bg_color": "#607d8b",
            "bold": True,
            "size": 11,
            "font_color": "#ffffff",
            "font_name": "Calibri",
            "align": "center",
        }
    )

    for position_col, name_column in enumerate(columns_keys_list):
        worksheet.write(
            1, position_col, name_column, columns_keys_format
        )  # Number column -1, Number row

    # Users list
    user_list_format = workbook.add_format()
    user_list_format.set_align("center")
    user_list_format.set_align("vcenter")

    for row_num, row_data in enumerate(users_list):        
        position_row = row_num + 2
        position_col = 0

        position = (position_row, position_col)
        insert_cell_image(worksheet, position, row_data.avatar_name_file)
        position_col += 1

        worksheet.write(position_row, position_col, row_data.id, user_list_format)
        position_col += 1

        worksheet.write(position_row, position_col, row_data.name, user_list_format)
        position_col += 1

        worksheet.write(position_row, position_col, row_data.surnames, user_list_format)
        position_col += 1

        worksheet.write(position_row, position_col, row_data.age, user_list_format)
        position_col += 1

        worksheet.write(position_row, position_col, row_data.email, user_list_format)
        position_col += 1

        worksheet.write(
            position_row,
            position_col,
            (
                date_format_server_to_client(str(row_data.email_verified_at))
                if row_data.email_verified_at is not None
                else "Unverified user!"
            ),
            user_list_format,
        )
        position_col += 1

        worksheet.write(
            position_row,
            position_col,
            "Yes" if row_data.is_active else "No",
            user_list_format,
        )
        position_col += 1

        worksheet.write(
            position_row, position_col, row_data.role.name, user_list_format
        )
        position_col += 1

    worksheet.autofit()

    workbook.close()

    output.seek(0)

    headers = {"Content-Disposition": 'attachment; filename="users-list.xlsx"'}

    return StreamingResponse(output, headers=headers)


def insert_cell_image(worksheet, position: tuple, avatar_name_file: str | None):
    position_row, position_col = position

    if avatar_name_file:
        path_image = f"{StoragePath.get_avatar_path(avatar_name_file)}"
    else:
        path_image = StoragePath.AVATAR_DEFAULT.value

    img = Image.open(path_image)
    width, height = img.size

    cell_width = 70.0
    cell_height = 70.0

    x_scale = cell_width / width
    y_scale = cell_height / height

    worksheet.set_row(position_row, 70)
    worksheet.insert_image(
        position_row,
        position_col,
        path_image,
        {"x_scale": x_scale, "y_scale": y_scale},
    )
