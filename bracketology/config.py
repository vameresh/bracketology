"""
Bracketology development configuration.
"""
import pathlib, os

# Secret key for encrypting cookies
SECRET_KEY = b'p\x0f\x12\xf4\x8daY\xe6\ti\xd0\xfcj\xda\x1e\xee}Z\xe5\x88\x04\xe3\xd48'
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = './.flask_session/'

BRACKETOLOGY_ROOT = pathlib.Path(__file__).resolve().parent.parent


# Database file is var/insta485.sqlite3
DATABASE_FILENAME = BRACKETOLOGY_ROOT/'var'/'bracketology.sqlite3'
