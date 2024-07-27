import re
import i18n
from dependencies.date_formatter import date_format_client_to_server
import dependencies.regex as regex


def email_verified_at_format(date_verified: str):
    if not date_verified:
        return None
    elif re.match(regex.date_format_client, date_verified):
        return str(date_format_client_to_server(date_verified))
    elif re.match(regex.date_format_server, date_verified):
        return date_verified
    else:
        raise ValueError(i18n.t("the_date_has_an_incorrect_format"))
