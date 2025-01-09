from constants import DEBT_INTEREST_RATE


class Bank:
    def __init__(
        self,
        player_gold: int = 0,
        player_debt: int = 0,
        in_debt_since: int | None = None,
    ):
        self.player_gold = player_gold
        self.player_debt = player_debt
        self.in_debt_since = in_debt_since

    def deposit(self, amount: int):
        self.player_gold += amount

    def withdraw(self, amount: int):
        if self.player_gold < amount:
            raise ValueError("Not enough gold to withdraw")
        self.player_gold -= amount

    def take_loan(self, amount: int, week: int):
        self.in_debt_since = week
        self.player_debt += amount

    def pay_loan(self, amount: int):
        self.player_debt = min(self.player_debt - amount, 0)
        if self.player_debt == 0:
            self.in_debt_since = None

    def collect_interest(self, weeks: int = 1):
        if self.player_debt != 0:
            self.player_debt = int(self.player_debt * (1 + DEBT_INTEREST_RATE) ** weeks)
