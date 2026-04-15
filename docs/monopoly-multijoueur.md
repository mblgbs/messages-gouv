# Mini app web : Monopoly multijoueur

Cette mini application web est disponible dans :

- `src/frontend/public/mini-games/monopoly/index.html`

## Fonctionnalités

- Mode multijoueur local (2 à 6 joueurs sur le même navigateur)
- Ajout de joueurs avec pion dédié
- Lancer de dés (2 dés)
- Avancement sur un plateau simplifié de 20 cases
- Gestion d'un solde de départ ($1500)
- Bonus de case départ (+$200)
- Générateur de **fausses cartes bancaires (CB)** pour le jeu

> ⚠️ Les cartes générées sont fictives et uniquement destinées à un usage ludique / test.

## Lancer l'application

1. Démarrer le frontend (depuis `src/frontend`) :

```bash
npm run dev
```

2. Ouvrir ensuite :

```text
http://localhost:3000/mini-games/monopoly/index.html
```

## Idées d'amélioration

- Ajouter des propriétés achetables
- Gérer des loyers entre joueurs
- Sauvegarder l'état de partie (localStorage)
- Ajouter un vrai mode multijoueur réseau (WebSocket)
