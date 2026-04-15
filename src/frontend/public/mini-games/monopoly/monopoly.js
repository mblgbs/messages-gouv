const MAX_PLAYERS = 6;
const BOARD_SIZE = 20;
const TOKENS = ["🚗", "🎩", "🐶", "🚀", "🛳️", "🧸"];

const boardEl = document.getElementById("board");
const playersListEl = document.getElementById("players-list");
const currentPlayerEl = document.getElementById("current-player");
const diceResultEl = document.getElementById("dice-result");
const actionLogEl = document.getElementById("action-log");
const cardsEl = document.getElementById("cards");

const playerForm = document.getElementById("player-form");
const playerNameInput = document.getElementById("player-name");
const rollDiceButton = document.getElementById("roll-dice");
const nextTurnButton = document.getElementById("next-turn");
const generateCardButton = document.getElementById("generate-card");

const state = {
  players: [],
  currentPlayerIndex: 0,
};

function drawBoard() {
  boardEl.innerHTML = "";

  for (let i = 0; i < BOARD_SIZE; i += 1) {
    const cell = document.createElement("div");
    cell.className = "cell";

    const playersHere = state.players.filter((player) => player.position === i);

    cell.innerHTML = `
      <strong>Case ${i + 1}</strong>
      <div class="tokens">${playersHere.map((player) => player.token).join(" ") || "·"}</div>
    `;

    boardEl.appendChild(cell);
  }
}

function drawPlayers() {
  playersListEl.innerHTML = "";

  state.players.forEach((player, index) => {
    const li = document.createElement("li");
    const activeMark = index === state.currentPlayerIndex ? "👉 " : "";
    li.textContent = `${activeMark}${player.token} ${player.name} — $${player.balance}`;
    playersListEl.appendChild(li);
  });
}

function getCurrentPlayer() {
  return state.players[state.currentPlayerIndex] || null;
}

function refreshTurnPanel() {
  const player = getCurrentPlayer();

  if (!player) {
    currentPlayerEl.textContent = "Aucun joueur";
    return;
  }

  currentPlayerEl.textContent = `${player.token} ${player.name} (case ${player.position + 1})`;
}

function render() {
  drawBoard();
  drawPlayers();
  refreshTurnPanel();
}

function randomDice() {
  return Math.floor(Math.random() * 6) + 1;
}

function randomDigits(length) {
  return Array.from({ length }, () => Math.floor(Math.random() * 10)).join("");
}

function generateFakeCard() {
  return {
    number: `${randomDigits(4)} ${randomDigits(4)} ${randomDigits(4)} ${randomDigits(4)}`,
    holder: `JOUEUR ${randomDigits(2)}`,
    expires: `${String(Math.floor(Math.random() * 12) + 1).padStart(2, "0")}/${Math.floor(Math.random() * 5) + 26}`,
    cvv: randomDigits(3),
  };
}

function appendCard(card) {
  const cardEl = document.createElement("article");
  cardEl.className = "card";
  cardEl.innerHTML = `
    <div>MONOPOLY BANK</div>
    <strong>${card.number}</strong>
    <div>${card.holder}</div>
    <div>EXP ${card.expires} · CVV ${card.cvv}</div>
  `;

  cardsEl.prepend(cardEl);
}

playerForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const name = playerNameInput.value.trim();
  if (!name || state.players.length >= MAX_PLAYERS) {
    return;
  }

  state.players.push({
    name,
    token: TOKENS[state.players.length],
    position: 0,
    balance: 1500,
  });

  actionLogEl.textContent = `${name} rejoint la partie.`;
  playerNameInput.value = "";
  render();
});

rollDiceButton.addEventListener("click", () => {
  const player = getCurrentPlayer();

  if (!player) {
    actionLogEl.textContent = "Ajoutez des joueurs avant de lancer les dés.";
    return;
  }

  const d1 = randomDice();
  const d2 = randomDice();
  const total = d1 + d2;

  player.position = (player.position + total) % BOARD_SIZE;
  diceResultEl.textContent = `${d1} + ${d2} = ${total}`;

  if (player.position === 0) {
    player.balance += 200;
    actionLogEl.textContent = `${player.name} passe par la case départ et gagne $200.`;
  } else {
    actionLogEl.textContent = `${player.name} avance de ${total} cases.`;
  }

  render();
});

nextTurnButton.addEventListener("click", () => {
  if (state.players.length === 0) {
    return;
  }

  state.currentPlayerIndex = (state.currentPlayerIndex + 1) % state.players.length;
  actionLogEl.textContent = `Tour de ${state.players[state.currentPlayerIndex].name}.`;
  render();
});

generateCardButton.addEventListener("click", () => {
  appendCard(generateFakeCard());
});

render();
