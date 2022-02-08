from info import INFO_LICENSE, INFO
from os import system
from art import tprint
from terminal import Terminal
from commands import get_commands_as_table
from setting import setting


class Menu:

    MENU = """1. License.\n2. About it.\n3. Start server.\n4. View Commands.\n5. Exit"""

    def __init__(self) -> None:
        self.__menu_action = {
            "1": self.__show_license,
            "2": self.__show_use,
            "3": self.__start_backdoor,
            "4": self.__view_commands,
            "5": self.__exit
        }
        self.__running = True

    def show_menu(self):
        print(self.MENU)

    def execute(self):
        system("cls")
        while self.__running:
            tprint(f"{setting['title']}\n")
            print(self.MENU)
            option = self.execute_menu_item()
            input("\n\nPress Enter key to continue...")
            system("cls")

    def execute_menu_item(self)->int:
        print()
        option = input("Enter option >> ")
        print()
        action = self.__menu_action.get(option)
        if action:
            action()
        else:
            option = -1
            print("Incorrect Option")
        return int(option)

    def __show_license(self):
        print(INFO_LICENSE)

    def __show_use(self):
        print(INFO)
    
    def __start_backdoor(self):
        terminal = Terminal()
        terminal.run()        

    def __view_commands(self):
        print(get_commands_as_table())

    def __exit(self):
        system("cls")
        self.__running = False

        