from re import compile
from pydantic import AfterValidator
from typing_extensions import Annotated

PASSWORD_REGEX = compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,64}$")  # special (?=.*?[#?!@$%^&*-])


def password_validator(v: str) -> str:
    if PASSWORD_REGEX.fullmatch(v) is None:
        raise ValueError('incorrect password')
    return v


PasswordStr = Annotated[str, AfterValidator(password_validator)]
