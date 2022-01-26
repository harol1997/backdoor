from prettytable import PrettyTable

commands = {
    "screenshot": "It allows take a screenshot of client. Accept --namefile",
    "camera": "It allows take a photo of client camera if It is possible. Accept --namefile",
    "keylogger": "It allows start a keylogger in client. Accept --time",
    "show hosts": "Show  host connected list",
    "help": "Show info about command. Accept --command",
    "cmd": "execute arg in terminal. You must pass the command in --command flag",
    "close":"end connections or specific connections. Accept --host",
    "generate app": "Generate exe for client. Accept --name"
}


flags = {
    "--host": "id host",
    "--name": "namefile. You have write type file: hola.png",
    "--time": "time in seconds",
    "--command": "name command like screenshot, camera..... If you are using it with 'cmd' command can be: ipconfig, ...",
    "--flag": "flag name"
}


def get_flags(task):
    list_flags = [item.strip().lower() for item in task.split("--")]
    result = {"task":list_flags[0]}
    for item in list_flags[1:]:
        elements = item.split(" ")
        result[elements[0].strip()] = (" ".join(elements[1:])).strip()
    return result


def get_flags_as_table():
    flag_table = PrettyTable()
    flag_table.field_names = ["Flag", "Description"]
    flag_table.add_rows([[key, value] for key, value in flags.items()])

    return flag_table.get_string()

def get_flag_as_table(flag):
    flag = "--"+flag
    if flag in flags:
        flag_table = PrettyTable()
        flag_table.field_names = ["Command", "Description"]
        flag_table.add_row([flag, flags[flag]])
        return flag_table.get_string()

    return "Flag not exist"

def get_commands_as_table():
    command_table = PrettyTable()
    command_table.field_names = ["Command", "Description"]
    command_table.add_rows([[key, value] for key, value in commands.items()])

    return command_table.get_string()

def get_command_as_table(command):
    if command in commands:
        command_table = PrettyTable()
        command_table.field_names = ["Command", "Description"]
        command_table.add_row([command, commands[command]])
        return command_table.get_string()

    return "Command not exist"
    

