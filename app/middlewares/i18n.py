from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
import i18n
from dependencies.root_dir import ROOT_DIR

i18n.load_path.append(f"{ROOT_DIR}/i18n")
i18n.set('file_format', 'json')
i18n.set('filename_format', '{locale}.{format}')
i18n.set('locale', 'en-US')
i18n.set('fallback', 'en-US')

class I18nMiddleware(BaseHTTPMiddleware):
    languages_list = ["en-US", "es-ES"]


    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):

        locale = request.headers.get("Accept-Language", "en-US")

        if locale not in self.languages_list:
            locale = "en-US"

        i18n.set('locale', locale)
        i18n.set('fallback', locale)
        #print(i18n.t("email_or_password_incorrect"))

        return await call_next(request)
