from core.services.monopoly_bot import get_street, list_streets, parse_whatsapp_command


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
