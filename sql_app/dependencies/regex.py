from pydantic import (
    Field,
    TypeAdapter,
    ConfigDict,
)
from typing import Annotated, Final
import re

# FORMAT YYYY-mm-dd hh:mm:ss
date_format_server = r"[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9]"

# Format dd-mm-YYYY hh:mm:ss
date_format_client = r"^(0[1-9]|1\d|2[0-8]|29(?=-\d\d-(?!1[01345789]00|2[1235679]00)\d\d(?:[02468][048]|[13579][26]))|30(?!-02)|31(?=-0[13578]|-1[02]))-(0[1-9]|1[0-2])-([12]\d{3}) ([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$"


password_format = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


pydantic_password_format: Final[re.Pattern] = re.compile(password_format)
ConfigStr = Annotated[str, Field(..., pattern=pydantic_password_format)]
ConfigStrTA = TypeAdapter(ConfigStr, config=ConfigDict(regex_engine="python-re"))
