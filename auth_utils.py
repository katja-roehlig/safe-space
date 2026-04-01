from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# im Mixer wird die Methode gespeichert, mit der das password verschlüsselt wird
pwd_mixer = PasswordHasher()


# Hier wirds verschlüsselt
def hash_password(password: str):
    return pwd_mixer.hash(password)


# Prüft ob beim Login das Passwort und die Verschlüsselung zusammenpassen
def login_check(
    hashed_password: str,
    plain_password: str,
):
    try:
        return pwd_mixer.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False
