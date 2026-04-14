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

### `MULTI JOIN <nom>`
Ajoute un joueur à la partie multijoueur en mémoire.

### `MULTI STATUS`
Affiche le tour global, le joueur actif et l'état des joueurs.

### `MULTI NEXT`
Passe au joueur suivant.

### `MULTI RESET`
Réinitialise complètement la partie multijoueur.

## Structure des données

Le module expose aussi :

- `MonopolyStreet` : nom, groupe, prix, loyers (nu -> hôtel)
- `list_streets()` : copie de la liste des rues
- `get_street(name)` : recherche partielle accent-insensible
- `MonopolyGameState` / `MonopolyPlayerState` : état simplifié pour le mode multijoueur

## Note sur les loyers

Les loyers sont initialisés depuis la table issue du fichier `monopoly_loyers-1.xlsx` fourni dans ce projet.

## API HTTP

Une API dédiée est disponible pour intégrer facilement le bot depuis WhatsApp/Twilio/Meta webhook handlers :

- `POST /api/v1.0/monopoly/command/`
- Body JSON: `{ "text": "RUE paix" }`
- Réponse JSON: `{ "response": "Rue de la Paix ..." }`

Si le champ `text` est absent, l'API retourne `400` avec le détail d'erreur.
