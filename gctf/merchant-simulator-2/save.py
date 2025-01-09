from __future__ import annotations

import hmac
import pickle
import pickletools
from dataclasses import dataclass
from hashlib import sha256
from io import BytesIO
from typing import TYPE_CHECKING
from zlib import compress, decompress

if TYPE_CHECKING:
    from main import Game
    from models import Player, Town


with open("SECRET_KEY", "rb") as f:
    SECRET_KEY = f.read()


@dataclass
class SaveState:
    # Game state
    week: int
    prices: dict[str, int]
    current_town_index: int

    # Player state
    player: Player

    # Towns
    towns: list[Town]

    # Bank state
    player_gold: int
    player_debt: int
    in_debt_since: int | None


class SaveUnpickler(pickle.Unpickler):
    def find_class(self, module: str, name: str):
        if (
            module == "models"
            and not name.count(".")
            and name.lower() in "playertown"
            and len(name) % 2 == len(module) % 2
            and len(name) <= 10
            or module == "save"
            and name.count(".") <= 1
            and "save" in name.lower()
            and len(name) <= 19
        ):
            return super().find_class(module, name)

        raise pickle.UnpicklingError("Dangerous pickle detected")


def save_game(game: Game):
    state = SaveState(
        week=game.week,
        prices=game.prices,
        current_town_index=game.current_town_index,
        player=game.player,
        towns=game.towns,
        player_gold=game.bank.player_gold,
        player_debt=game.bank.player_debt,
        in_debt_since=game.bank.in_debt_since,
    )
    state_bytes = pickle.dumps(state)
    state_bytes = compress(state_bytes)
    state_signature = hmac.new(SECRET_KEY, state_bytes, sha256).digest()
    return f"{state_bytes.hex()}.{state_signature.hex()}"


def load_game(state_signed: str):
    if state_signed.count(".") != 1:
        return "Invalid save format detected"

    state_bytes, state_signature = state_signed.split(".")

    print(state_bytes, state_signature)

    state_bytes = bytes.fromhex(state_bytes)
    state_signature = bytes.fromhex(state_signature)
    loaded_signature = hmac.new(SECRET_KEY, state_bytes, sha256).digest()

    state_bytes = decompress(state_bytes)

    for op, _, _ in pickletools.genops(state_bytes):
        if op.code == "R":
            return "Disallowed opcode in save!"

    try:
        save_state = SaveUnpickler(BytesIO(state_bytes)).load()
    except pickle.UnpicklingError:
        return "Dangerous pickle detected!"

    if hmac.compare_digest(state_signature, loaded_signature):
        return save_state
    else:
        return "Invalid save signature!"
