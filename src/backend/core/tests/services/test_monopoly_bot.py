from core.services.monopoly_bot import get_street, list_streets, parse_whatsapp_command, reset_multiplayer_game


def test_list_streets_contains_22_colored_properties():
    streets = list_streets()
    assert len(streets) == 22
    assert streets[0].name == "Boulevard de Belleville"
    assert streets[-1].name == "Rue de la Paix"


def test_get_street_supports_accent_insensitive_lookup():
    street = get_street("champs elysees")
    assert street is not None
    assert street.name == "Avenue des Champs-Élysées"


def test_parse_whatsapp_command_rues_returns_board_list():
    answer = parse_whatsapp_command("RUES")
    assert "Rues Monopoly" in answer
    assert "Rue de la Paix" in answer


def test_parse_whatsapp_command_rue_returns_rent_scale():
    answer = parse_whatsapp_command("RUE paix")
    assert "Rue de la Paix" in answer
    assert "hôtel 2000" in answer


def test_multiplayer_join_status_and_next_turn():
    reset_multiplayer_game()
    assert "Joueur ajouté: Alice." == parse_whatsapp_command("MULTI JOIN Alice")
    assert "Joueur ajouté: Bob." == parse_whatsapp_command("MULTI JOIN Bob")

    status = parse_whatsapp_command("MULTI STATUS")
    assert "Tour 1" in status
    assert "Joueur actif: Alice" in status
    assert "- Bob: cash 1500M, case 0" in status

    next_turn = parse_whatsapp_command("MULTI NEXT")
    assert "Tour suivant: Bob (tour global 1)." == next_turn


def test_multiplayer_reset_and_empty_status():
    reset_multiplayer_game()
    parse_whatsapp_command("MULTI JOIN Clara")
    assert "Partie multijoueur réinitialisée." == parse_whatsapp_command("MULTI RESET")
    assert "Aucune partie multijoueur en cours." in parse_whatsapp_command("MULTI STATUS")
