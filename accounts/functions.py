import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from passlib.context import CryptContext


def generate_key(pass_phrase):
    password = pass_phrase.encode()
    salt = b"\xa2K\x8f\x1b\xb5\xd6\x0f\x91\x8eT1\xfd\x95B\x19_"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def encode_data(pass_phrase, data):
    """
    This function encodes data into a string.
    :rtype: str
    :param pass_phrase: a random string to be used for decoding.
    :param data: string (you'll receive the same string using "decode_data()").
    :return: string, list data in encoded form
    """
    # create a fernet key
    key = generate_key(pass_phrase)
    encoded_data = ""
    f = Fernet(key)

    # encode data
    data_value = data.encode()
    encoded_form = f.encrypt(data_value)
    encoded_data += encoded_form.decode("utf-8")

    return encoded_data


def encrypt_data(password) -> str:
    """
    Hashes the password
    :param password: password provided by user, as str.
    :return: Hash of the password, str.
    """
    # define a context for hashing
    # we can later hide this in some .env file
    context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=32752,
    )
    return context.encrypt(password)


def check_data(user_provided, encrypted) -> bool:
    """
    Checks if user provided password & encrypted hash correspond to same password.
    :param user_provided: password provided by user during login.
    :param encrypted: password hash stored in db during signup.
    :return: True/False
    """
    context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=32752,
    )
    try:
        ans = context.verify(user_provided, encrypted)
    except ValueError:
        ans = False

    return ans


def decode_data(pass_phrase, encoded_data):
    key = generate_key(pass_phrase)

    from cryptography.fernet import Fernet

    f = Fernet(key)

    decoded_form = f.decrypt(str.encode(encoded_data))
    return decoded_form
