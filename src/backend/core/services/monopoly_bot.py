"""Simple Monopoly decision helper and WhatsApp-oriented command parser."""

from __future__ import annotations

from dataclasses import dataclass
import unicodedata


@dataclass
class MonopolyDecision:
    action: str
    reason: str


@dataclass
class MonopolyTurnContext:
    cash: int
    property_price: int = 0
    rent_risk_next_round: int = 0
    owned_in_color_group: int = 0
    total_in_color_group: int = 0
    in_jail: bool = False
    jail_turns_left: int = 0
    has_get_out_of_jail_card: bool = False


@dataclass(frozen=True)
class MonopolyStreet:
    name: str
    group: str
    price: int
    rent_no_house: int
    rent_1_house: int
    rent_2_houses: int
    rent_3_houses: int
    rent_4_houses: int
    rent_hotel: int


@dataclass
class MonopolyPlayerState:
    name: str
    cash: int = 1500
    position: int = 0


@dataclass
class MonopolyGameState:
    players: list[MonopolyPlayerState]
    current_player_idx: int = 0
    turn: int = 1


# French Monopoly board streets in board order (colored properties only).
_STREET_NAMES = [
    ("Boulevard de Belleville", "Marron", 60),
    ("Rue Lecourbe", "Marron", 60),
    ("Rue de Vaugirard", "Bleu clair", 100),
    ("Rue de Courcelles", "Bleu clair", 100),
    ("Avenue de la République", "Bleu clair", 120),
    ("Boulevard de la Villette", "Rose", 140),
    ("Avenue de Neuilly", "Rose", 140),
    ("Rue de Paradis", "Rose", 160),
    ("Avenue Mozart", "Orange", 180),
    ("Boulevard Saint-Michel", "Orange", 180),
    ("Place Pigalle", "Orange", 200),
    ("Avenue Matignon", "Rouge", 220),
    ("Boulevard Malesherbes", "Rouge", 220),
    ("Avenue Henri-Martin", "Rouge", 240),
    ("Faubourg Saint-Honoré", "Jaune", 260),
    ("Place de la Bourse", "Jaune", 260),
    ("Rue La Fayette", "Jaune", 280),
    ("Avenue de Breteuil", "Vert", 300),
    ("Avenue Foch", "Vert", 300),
    ("Boulevard des Capucines", "Vert", 320),
    ("Avenue des Champs-Élysées", "Bleu foncé", 350),
    ("Rue de la Paix", "Bleu foncé", 400),
]

# Rent scales from uploaded spreadsheet monopoly_loyers-1.xlsx
# [base, 1 house, 2 houses, 3 houses, 4 houses, hotel]
_RENT_SCALES = [
    (2, 10, 30, 90, 160, 250),
    (4, 20, 60, 180, 320, 450),
    (6, 30, 90, 270, 400, 550),
    (6, 30, 90, 270, 400, 550),
    (8, 40, 100, 300, 450, 600),
    (10, 50, 150, 450, 625, 750),
    (10, 50, 150, 450, 625, 750),
    (12, 60, 180, 500, 700, 900),
    (14, 70, 200, 550, 750, 950),
    (14, 70, 200, 550, 750, 950),
    (16, 80, 220, 600, 800, 1000),
    (18, 90, 250, 700, 875, 1050),
    (18, 90, 250, 700, 875, 1050),
    (20, 100, 300, 750, 925, 1100),
    (22, 110, 330, 800, 975, 1150),
    (22, 110, 330, 800, 975, 1150),
    (24, 120, 360, 850, 1025, 1200),
    (26, 130, 390, 900, 1100, 1275),
    (26, 130, 390, 900, 1100, 1275),
    (28, 150, 450, 1000, 1200, 1400),
    (35, 175, 500, 1100, 1300, 1500),
    (50, 200, 600, 1400, 1700, 2000),
]


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


MONOPOLY_STREETS = [
    MonopolyStreet(name=name, group=group, price=price, rent_no_house=rents[0], rent_1_house=rents[1], rent_2_houses=rents[2], rent_3_houses=rents[3], rent_4_houses=rents[4], rent_hotel=rents[5])
    for (name, group, price), rents in zip(_STREET_NAMES, _RENT_SCALES)
]

_MULTIPLAYER_GAME = MonopolyGameState(players=[])


class MonopolyBot:
    def decide_property_purchase(self, context: MonopolyTurnContext) -> MonopolyDecision:
        if context.property_price <= 0:
            return MonopolyDecision(action="skip", reason="Aucune propriété achetable ce tour.")

        if context.total_in_color_group > 0 and context.owned_in_color_group + 1 == context.total_in_color_group:
            return MonopolyDecision(action="buy", reason="Achat recommandé pour compléter le groupe de couleur.")

        safety_cash = context.rent_risk_next_round + 200
        if context.cash - context.property_price >= safety_cash:
            return MonopolyDecision(action="buy", reason="Trésorerie suffisante après risque locatif estimé.")

        return MonopolyDecision(action="skip", reason="Conserver du cash pour le prochain tour.")

    def decide_jail_strategy(self, context: MonopolyTurnContext) -> MonopolyDecision:
        if not context.in_jail:
            return MonopolyDecision(action="skip", reason="Le joueur n'est pas en prison.")

        if context.has_get_out_of_jail_card and context.rent_risk_next_round > 120:
            return MonopolyDecision(action="use_card", reason="Sortie via carte pour éviter un risque élevé.")

        if context.jail_turns_left > 1 and context.rent_risk_next_round < 80:
            return MonopolyDecision(action="wait", reason="Rester en prison pour limiter les déplacements risqués.")

        return MonopolyDecision(action="pay_or_roll", reason="Sortir de prison pour reprendre le développement.")


def list_streets() -> list[MonopolyStreet]:
    return MONOPOLY_STREETS.copy()


def get_street(name: str) -> MonopolyStreet | None:
    needle = _normalize(name)
    for street in MONOPOLY_STREETS:
        if needle in _normalize(street.name):
            return street
    return None


def reset_multiplayer_game() -> None:
    _MULTIPLAYER_GAME.players.clear()
    _MULTIPLAYER_GAME.current_player_idx = 0
    _MULTIPLAYER_GAME.turn = 1


def join_multiplayer_game(player_name: str) -> str:
    name = player_name.strip()
    if not name:
        return "Nom de joueur invalide."
    if any(_normalize(player.name) == _normalize(name) for player in _MULTIPLAYER_GAME.players):
        return f"Le joueur {name} est déjà dans la partie."

    _MULTIPLAYER_GAME.players.append(MonopolyPlayerState(name=name))
    if len(_MULTIPLAYER_GAME.players) == 1:
        _MULTIPLAYER_GAME.current_player_idx = 0
    return f"Joueur ajouté: {name}."


def multiplayer_status() -> str:
    if not _MULTIPLAYER_GAME.players:
        return "Aucune partie multijoueur en cours. Utilise: MULTI JOIN <nom>."

    current = _MULTIPLAYER_GAME.players[_MULTIPLAYER_GAME.current_player_idx]
    lines = [
        f"Partie multijoueur — Tour {_MULTIPLAYER_GAME.turn}",
        f"Joueur actif: {current.name}",
        "Joueurs:",
    ]
    for player in _MULTIPLAYER_GAME.players:
        lines.append(f"- {player.name}: cash {player.cash}M, case {player.position}")
    return "\n".join(lines)


def next_multiplayer_turn() -> str:
    if not _MULTIPLAYER_GAME.players:
        return "Impossible de passer le tour: aucun joueur."

    _MULTIPLAYER_GAME.current_player_idx = (_MULTIPLAYER_GAME.current_player_idx + 1) % len(_MULTIPLAYER_GAME.players)
    if _MULTIPLAYER_GAME.current_player_idx == 0:
        _MULTIPLAYER_GAME.turn += 1
    current = _MULTIPLAYER_GAME.players[_MULTIPLAYER_GAME.current_player_idx]
    return f"Tour suivant: {current.name} (tour global {_MULTIPLAYER_GAME.turn})."


def parse_whatsapp_command(text: str) -> str:
    payload = (text or "").strip()
    if not payload:
        return "Commande vide. Exemples: ACHAT..., PRISON..., RUES, RUE <nom>."

    parts = payload.split()
    command = parts[0].upper()

    if command == "ACHAT" and len(parts) == 6:
        cash, price, risk, owned, total = (int(x) for x in parts[1:])
        decision = MonopolyBot().decide_property_purchase(
            MonopolyTurnContext(
                cash=cash,
                property_price=price,
                rent_risk_next_round=risk,
                owned_in_color_group=owned,
                total_in_color_group=total,
            )
        )
        return f"[{decision.action}] {decision.reason}"

    if command == "PRISON" and len(parts) == 5:
        cash, risk, turns_left, has_card = (int(x) for x in parts[1:])
        decision = MonopolyBot().decide_jail_strategy(
            MonopolyTurnContext(
                cash=cash,
                rent_risk_next_round=risk,
                in_jail=True,
                jail_turns_left=turns_left,
                has_get_out_of_jail_card=bool(has_card),
            )
        )
        return f"[{decision.action}] {decision.reason}"

    if command == "RUES":
        lines = [f"{street.name} ({street.group})" for street in MONOPOLY_STREETS]
        return "Rues Monopoly:\n- " + "\n- ".join(lines)

    if command == "RUE" and len(parts) >= 2:
        name = " ".join(parts[1:])
        street = get_street(name)
        if street is None:
            return f"Rue introuvable: {name}."
        return (
            f"{street.name} ({street.group}) - Prix {street.price}M | "
            f"Loyers: nu {street.rent_no_house}, 1M {street.rent_1_house}, "
            f"2M {street.rent_2_houses}, 3M {street.rent_3_houses}, "
            f"4M {street.rent_4_houses}, hôtel {street.rent_hotel}."
        )

    if command == "MULTI" and len(parts) >= 2:
        subcommand = parts[1].upper()
        if subcommand == "RESET":
            reset_multiplayer_game()
            return "Partie multijoueur réinitialisée."
        if subcommand == "JOIN" and len(parts) >= 3:
            return join_multiplayer_game(" ".join(parts[2:]))
        if subcommand == "STATUS":
            return multiplayer_status()
        if subcommand == "NEXT":
            return next_multiplayer_turn()
        return "Format invalide. Utiliser: MULTI JOIN <nom> | MULTI STATUS | MULTI NEXT | MULTI RESET"

    return (
        "Format invalide. Utiliser:\n"
        "- ACHAT cash prix risque proprietes_groupe total_groupe\n"
        "- PRISON cash risque tours_restants carte(0|1)\n"
        "- RUES\n"
        "- RUE <nom>\n"
        "- MULTI JOIN <nom> | MULTI STATUS | MULTI NEXT | MULTI RESET"
    )
