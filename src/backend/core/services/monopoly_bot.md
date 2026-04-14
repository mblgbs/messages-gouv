# MonopolyBot (WhatsApp)

Ce document décrit les commandes texte gérées par `parse_whatsapp_command` pour piloter le bot Monopoly via WhatsApp.

## Commandes disponibles

### `ACHAT cash prix risque proprietes_groupe total_groupe`
Retourne une décision d'achat de propriété.

Exemple :

```text
ACHAT 500 180 50 1 3
```

### `PRISON cash risque tours_restants carte(0|1)`
Retourne une stratégie en prison (`wait`, `use_card`, `pay_or_roll`).

Exemple :

```text
PRISON 600 70 2 1
```

### `RUES`
Retourne la liste des 22 rues colorées du Monopoly (ordre du plateau français).

Exemple :

```text
RUES
```

### `RUE <nom>`
Retourne le détail d'une rue (groupe, prix, loyers) avec recherche tolérante aux accents.

Exemples :

```text
RUE paix
RUE Champs Elysees
```

## Structure des données

Le module expose aussi :

- `MonopolyStreet` : nom, groupe, prix, loyers (nu -> hôtel)
- `list_streets()` : copie de la liste des rues
- `get_street(name)` : recherche partielle accent-insensible

## Note sur les loyers

Les loyers sont initialisés depuis la table issue du fichier `monopoly_loyers-1.xlsx` fourni dans ce projet.
