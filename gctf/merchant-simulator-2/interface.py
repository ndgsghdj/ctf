import os
import time
from typing import Callable


class Interface:
    def __init__(self):
        self.header_factories: list[Callable[[], str]] = []
        self.header_visible = False

    def output(self, message: str, animate: bool = True):
        for line in message.splitlines():
            print(line)
            if animate:
                time.sleep(0.01)

    def clear(self, keep_header: bool = False):
        os.system("cls" if os.name == "nt" else "clear")
        if keep_header:
            self.show_header(animate=not self.header_visible)
        else:
            self.header_visible = False

    def show_header(self, animate: bool = True):
        self.header_visible = True
        for factory in self.header_factories:
            self.output(factory(), animate=animate)

    def append_header(
        self,
        factory: Callable[[], str],
        update: bool = True,
        clear: bool = False,
        animate: bool = True,
    ):
        self.header_factories.append(factory)
        if clear:
            self.clear()
            if update:
                self.show_header(animate=animate)
        else:
            if update:
                self.output(factory(), animate=animate)

    def pop_header(self, update: bool = True, animate: bool = True):
        self.header_factories.pop()
        self.clear()
        if update:
            self.show_header(animate=animate)

    def ask(self, message: str) -> str:
        self.output(message)
        return input("> ")

    def choice(
        self,
        message: str,
        options: list[str],
        with_header: bool = True,
    ) -> int:
        self.clear(keep_header=with_header)
        self.output(message)

        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")

        choice = input("> ")
        while not choice.isdigit() or not (1 <= int(choice) <= len(options)):
            self.output("Invalid choice.")
            choice = input("> ")

        return int(choice) - 1

    def ask_amount(
        self,
        message: str,
        max_amount: int,
        with_header: bool = True,
    ) -> int:
        self.clear(keep_header=with_header)

        choice = self.ask(message)
        while not (choice.isdigit() or choice.upper() == "A"):
            choice = self.ask("Invalid choice.")

        if choice.upper() == "A":
            return max_amount
        return int(choice)

    def flash(self, message: str, duration: int = 1):
        self.clear()
        self.output(message)
        time.sleep(duration)
