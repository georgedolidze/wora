import os
import sys
import getpass
try:
    import keyring
    _HAVE_KEYRING = True
except ImportError:
    _HAVE_KEYRING = False

def get_auth(appid, force=False):
    """
    Prompt for a user or password if necessary, or if force is True

    Kwargs:
    force -- always ask the user for their password
    """
    user = os.getenv('LOGIN_' + appid + '_USER')
    password = os.getenv('LOGIN_' + appid + '_PASSWORD')
    if _HAVE_KEYRING:
        if user is None or user == '':
            user = keyring.get_password(appid, appid + '.user')
        if password is None or password == '':
            password = keyring.get_password(appid, user)
    if user is None or user == '' or force:
        sys.stderr.write("Username ({}): ".format(appid))
        user = input()
    if password is None or password == '' or force:
        password = getpass.getpass()
    return (user, password)

def save_auth(appid, auth):
    """Save the credentials in the keyring, if the module is available"""
    if _HAVE_KEYRING and auth is not None:
        keyring.set_password(appid, appid + '.user', auth[0])
        keyring.set_password(appid, auth[0], auth[1])
