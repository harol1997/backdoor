from winreg import HKEY_LOCAL_MACHINE, KEY_WRITE, REG_SZ, HKEY_CURRENT_USER
from win32.win32api import RegOpenKeyEx, RegSetValueEx, RegCloseKey, RegDeleteValue


SUBKEY = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
SUBKEY_64 = "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run"

def run_at_startup_set(appname, path):
    key = RegOpenKeyEx(HKEY_CURRENT_USER, SUBKEY, 0, KEY_WRITE)
    RegSetValueEx(key, appname, 0, REG_SZ, path)
    RegCloseKey(key)


def run_at_startup_remove(appname):
    key = RegOpenKeyEx(HKEY_LOCAL_MACHINE, SUBKEY, 0, KEY_WRITE)
    RegDeleteValue(key, appname)
    RegCloseKey(key)
