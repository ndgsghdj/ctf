"""
   __  ___            __             __    _____            __     __
  /  |/  /__ ________/ /  ___ ____  / /_  / __(_)_ _  __ __/ /__ _/ /____  ____
 / /|_/ / -_) __/ __/ _ \/ _ `/ _ \/ __/ _\ \/ /  ' \/ // / / _ `/ __/ _ \/ __/
/_/  /_/\__/_/  \__/_//_/\_,_/_//_/\__/ /___/_/_/_/_/\_,_/_/\_,_/\__/\___/_/
"""

import random

from bank import Bank
from constants import (
    BASE_MIN_LOAN,
    GAME_END_WEEK,
    ITEMS,
    MAX_DEBT_WEEKS,
    STARTING_GOLD,
    TARGET_GOLD,
    TOWN_NAMES,
)
from interface import Interface
from models import Item, Player, Town
from save import SaveState, load_game, save_game


class Game:
    week: int
    prices: dict[str, int]

    def __init__(self):
        self.interface = Interface()
        self.items = [Item(name, price) for name, price in ITEMS]

        self.is_running = False

        self.alerts: list[str] = []

    @property
    def current_town(self) -> Town:
        return self.towns[self.current_town_index]

    def from_save_state(self, state: SaveState):
        self.week = state.week
        self.prices = state.prices
        self.current_town_index = state.current_town_index
        self.player = state.player
        self.towns = state.towns
        self.bank = Bank(
            player_gold=state.player_gold,
            player_debt=state.player_debt,
            in_debt_since=state.in_debt_since,
        )

    def load_save(self):
        state = self.interface.ask("Enter your magic save string")
        try:
            save_state = load_game(state)
        except Exception:
            self.interface.flash("Invalid save string!")
            return

        if isinstance(save_state, str):
            self.interface.flash(save_state)
            return

        self.from_save_state(save_state)

    def save_game(self):
        save_string = save_game(self)
        self.interface.ask(
            f"Save your game with this magic string: {save_string}\nPress enter to continue."
        )

    def generate_towns(self) -> list[Town]:
        COORDS = [
            (0, 0),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        ]
        towns = []
        for name, (x, y) in zip(TOWN_NAMES, COORDS):
            towns.append(
                Town(
                    name=name,
                    x=random.randrange(x * 100, x * 100 + 100),
                    y=random.randrange(y * 100, y * 100 + 100),
                    is_main_city=name == "Ravenwood",
                    price_weights={
                        item.name: random.randint(-5, 5) for item in self.items
                    },
                )
            )
        return towns

    def generate_price_weights(self) -> dict[str, int]:
        local_weights = self.current_town.price_weights
        weights = {
            item.name: random.randint(-15, 15) + local_weights[item.name]
            for item in self.items
        }

        if random.random() < 0.4:
            item = random.choice(self.items)
            weights[item.name] *= 2.5

            if weights[item.name] > 25:
                self.alerts.append(
                    f"{item.name.capitalize()} is more expensive than usual!"
                )
            elif weights[item.name] < -25:
                self.alerts.append(
                    f"{item.name.capitalize()} is more cheaper than usual!"
                )

        return weights

    def generate_prices(self):
        weights = self.generate_price_weights()
        self.prices = {
            item.name: int(item.base_price * (1 + (weights[item.name] / 100)))
            for item in self.items
        }

    def check_debt_status(self):
        if self.bank.in_debt_since is not None:
            in_debt_for = self.week - self.bank.in_debt_since
            if in_debt_for >= MAX_DEBT_WEEKS:
                self.end_game(debt=True)
            else:
                self.alerts.insert(
                    0,
                    f"You have been in debt for {in_debt_for} weeks. If you don't pay it off in {50 - in_debt_for} weeks, you will be forced to retire!",
                )

    def get_travel_time(self, town: Town) -> int:
        return self.current_town.distance_from(town) // 50

    @property
    def net_worth(self) -> int:
        return (
            self.player.gold
            + self.bank.player_gold
            - self.bank.player_debt
            + sum(
                self.player.inventory[item.name] * item.base_price
                for item in self.items
            )
        )

    def get_status(self) -> str:
        return (
            f"Welcome, {self.player.name}! You are currently in {self.current_town.name}.\n"
            f"Gold: {self.player.gold}\n"
            f"Bank: {self.bank.player_gold}\n"
            f"Week: {self.week}\n"
            f"Debt: {self.bank.player_debt}\n"
            f"Inventory:\n"
            f"  Tools: {self.player.inventory['tools']}\n"
            f"  Silk: {self.player.inventory['silk']}\n"
            f"  Books: {self.player.inventory['books']}\n"
            f"  Weapons: {self.player.inventory['weapons']}\n"
            f"  Jewelry: {self.player.inventory['jewellery']}"
        )

    def display_prices(self):
        return "Current prices:\n" + "\n".join(
            f"  {item.name.capitalize()}: {self.prices[item.name]}"
            for item in self.items
        )

    def pass_weeks(self, weeks: int):
        self.week += weeks
        self.bank.collect_interest(weeks)
        self.check_debt_status()
        self.generate_prices()

        for alert in self.alerts:
            self.interface.flash(alert, duration=2)

        self.alerts = []

    def start_game(self):
        self.interface.clear()

        choice = self.interface.choice(
            __doc__,
            ["New game", "Load save", "Exit"],
        )

        if choice == 0:
            self.interface.clear()
            self.bank = Bank()
            self.towns = self.generate_towns()
            self.current_town_index = 0
            self.week: int = 1
            self.generate_prices()
            name = self.interface.ask("What is your name?")
            self.player = Player(
                name,
                STARTING_GOLD,
                {"tools": 0, "silk": 0, "books": 0, "weapons": 0, "jewellery": 0},
            )
        elif choice == 1:
            self.load_save()
        else:
            return

        self.interface.clear()

        self.is_running = True
        self.main_loop()

    def end_game(
        self, debt: bool = False, retire: bool = False, save_and_exit: bool = False
    ):
        self.is_running = False
        self.interface.clear()

        if debt:
            self.interface.output(
                "You have been forced to retire due to excessive debt!"
            )
            self.interface.output(f"Your final net worth was {self.net_worth} gold.")
        elif retire:
            self.interface.output("Congratulations! You have retired!")
            self.interface.output(f"Your final net worth was {self.net_worth} gold.")
            with open("flag.txt", "r") as f:
                self.interface.output(f.read())
        elif save_and_exit:
            self.interface.output("Game saved. Goodbye!")
        else:
            self.interface.output("You have ran out of time, you lose!")
            self.interface.output(f"Your final net worth was {self.net_worth} gold.")

    def bank_loop(self):
        while True:
            choice = self.interface.choice(
                "Welcome to the bank!\nWhat would you like to do?",
                ["Deposit", "Withdraw", "Take out a loan", "Pay off loan", "Exit"],
            )

            match choice:
                case 0:
                    amount = self.interface.ask_amount(
                        "How much would you like to deposit? ('a' for all)",
                        self.player.gold,
                    )
                    try:
                        self.player.pay(amount)
                    except ValueError:
                        self.interface.flash("You don't have enough gold!")
                        continue
                    self.bank.deposit(amount)
                    self.interface.flash(f"You have deposited {amount} gold.")
                case 1:
                    amount = self.interface.ask_amount(
                        "How much would you like to withdraw? ('a' for all)",
                        self.bank.player_gold,
                    )
                    try:
                        self.bank.withdraw(amount)
                    except ValueError:
                        self.interface.flash("You don't have enough gold!")
                        continue
                    self.player.receive(amount)
                    self.interface.flash(f"You have withdrawn {amount} gold.")
                case 2:
                    if self.bank.player_debt > 0:
                        self.interface.flash("You already have a loan!")
                        continue
                    max_loan = max(
                        BASE_MIN_LOAN, self.net_worth * 2 - self.bank.player_debt
                    )
                    amount = self.interface.ask_amount(
                        "How much would you like to borrow? ('a' for all)", max_loan
                    )
                    if amount > max_loan:
                        self.interface.flash("You can't borrow that much!")
                        continue
                    self.bank.take_loan(amount, self.week)
                    self.player.receive(amount)
                    self.interface.flash(f"You have taken out a loan of {amount} gold.")
                case 3:
                    if self.bank.player_debt == 0:
                        self.interface.flash("You don't have a loan!")
                        continue
                    amount = self.interface.ask_amount(
                        "How much would you like to pay off? ('a' for all)",
                        min(self.bank.player_debt, self.player.gold),
                    )
                    if amount > self.bank.player_debt:
                        self.interface.flash("You can't pay off that much!")
                        continue
                    if amount > self.player.gold:
                        self.interface.flash("You don't have enough gold!")
                        continue
                    self.bank.pay_loan(amount)
                    self.player.pay(amount)
                    self.interface.flash(f"You have paid off {amount} gold.")
                case 4:
                    break

    def shop_loop(self):
        self.interface.append_header(self.display_prices)

        while True:
            choice = self.interface.choice(
                "Welcome to the shop!\nWhat would you like to do?",
                [
                    "Buy items",
                    "Sell items",
                    "Go back",
                ],
            )

            match choice:
                case 0:
                    item = self.interface.choice(
                        "What would you like to buy?",
                        [
                            "Tools",
                            "Silk",
                            "Books",
                            "Weapons",
                            "Jewelry",
                        ],
                    )
                    amount = self.interface.ask_amount(
                        "How many would you like to buy? ('a' for all)",
                        self.player.gold // self.prices[self.items[item].name],
                    )

                    try:
                        self.player.pay(amount * self.prices[self.items[item].name])
                    except ValueError:
                        self.interface.flash("You don't have enough gold!")
                        continue

                    self.player.inventory[self.items[item].name] += amount
                    self.interface.flash(
                        f"You have bought {amount} {self.items[item].name}!"
                    )
                case 1:
                    item = self.interface.choice(
                        "What would you like to sell?",
                        [
                            "Tools",
                            "Silk",
                            "Books",
                            "Weapons",
                            "Jewelry",
                        ],
                    )
                    amount = self.interface.ask_amount(
                        "How many would you like to sell? ('a' for all)",
                        self.player.inventory[self.items[item].name],
                    )

                    if amount > self.player.inventory[self.items[item].name]:
                        self.interface.flash("You don't have that many!")
                        continue

                    self.player.receive(amount * self.prices[self.items[item].name])
                    self.player.inventory[self.items[item].name] -= amount
                    self.interface.flash(
                        f"You have sold {amount} {self.items[item].name}!"
                    )
                case 2:
                    self.interface.pop_header(animate=False)
                    break

    def travel_loop(self):
        travel_times = {town.name: self.get_travel_time(town) for town in self.towns}

        choices = [f"{town} ({time} weeks)" for town, time in travel_times.items()]
        choices.append("Go back")

        choice = self.interface.choice(
            "Where would you like to travel?",
            choices,
        )
        if choice == len(choices) - 1:
            return

        if self.current_town.name == self.towns[choice].name:
            self.interface.flash("You are already in that town!")
            return

        self.interface.flash(f"You are traveling to {self.towns[choice].name}!")

        travel_time = travel_times[self.towns[choice].name]
        self.current_town_index = choice

        self.interface.flash("Traveling...", duration=travel_time)

        self.interface.flash(f"You have arrived in {self.current_town.name}!")

        self.pass_weeks(travel_time)

    def save_loop(self):
        choice = self.interface.choice(
            "What would you like to do?",
            [
                "Save",
                "Save and exit",
                "Load",
                "Cancel",
            ],
        )

        match choice:
            case 0:
                self.save_game()
            case 1:
                self.save_game()
                self.end_game(save_and_exit=True)
            case 2:
                self.load_save()
                self.interface.flash("Game loaded successfully!")
            case 3:
                return

    def main_loop(self):
        self.interface.append_header(self.get_status, animate=False)

        while self.is_running:
            if self.week >= GAME_END_WEEK:
                self.end_game()
                break

            choices = [
                "Shop",
                "Travel",
                "Rest for a week",
                "Save Menu",
            ]
            if self.current_town.is_main_city:
                choices.append("Go to the bank")
            if self.net_worth >= TARGET_GOLD:
                choices.append("Retire")

            choice = self.interface.choice("What would you like to do?", choices)

            match choice:
                case 0:
                    self.shop_loop()
                case 1:
                    self.travel_loop()
                case 2:
                    self.interface.flash("You rest for a week.", duration=1)
                    self.pass_weeks(1)
                case 3:
                    self.save_loop()
                case _:
                    if choices[choice] == "Go to the bank":
                        self.bank_loop()
                    elif choices[choice] == "Retire":
                        self.end_game(retire=True)
                        break


if __name__ == "__main__":
    try:
        Game().start_game()
    except KeyboardInterrupt:
        pass
