import re
from dependencies.regex import date_format_client, date_format_server
from dependencies.date_formatter import date_format_client_to_server


def email_verified_at_format(date_verified: str):
    if not date_verified:
        return None
    elif re.match(date_format_client, date_verified):
        return str(date_format_client_to_server(date_verified))
    elif re.match(date_format_server, date_verified):
        return date_verified
    else:
        raise ValueError("The date has an incorrect format.")
