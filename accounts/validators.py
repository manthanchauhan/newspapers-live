from django.core.validators import ValidationError


def validate_username(username):
    if len(username) < 4:
        raise ValidationError("Username should contain at least 4 characters")

    chars = list(username)
    for char in chars:
        if (
            not ("a" <= char <= "z")
            and not ("A" <= char <= "Z")
            and not ("0" <= char <= "9")
        ):
            raise ValidationError("Username should contain only alphabets and digits")

    contains_alphabet = False
    for char in chars:
        if "a" <= char <= "z" or "A" <= char <= "Z":
            contains_alphabet = True
            break

    if not contains_alphabet:
        raise ValidationError("Username should contain at least 1 alphabet")
