import i18n


def is_match_password(self, password: str, password_confirmation: str):
    if password == password_confirmation:
        return self
    else:
        raise ValueError(i18n.t("the_passwords_not_match"))
