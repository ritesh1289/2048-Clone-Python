

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="2048 - Enhanced Edition",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
:root {
  --page:#faf8ef;
  --text:#776e65;
  --board:#bbada0;
  --empty:#cdc1b4;
  --panel:#eee4da;
  --button:#8f7a66;
  --button-hover:#776e65;
  --shadow:0 5px 18px rgba(80,60,40,.12);
}

* { box-sizing:border-box; }

body {
  margin:0;
  padding:12px;
  background:var(--page);
  color:var(--text);
  font-family:Arial,Helvetica,sans-serif;
}

body.dark {
  --page:#171717;
  --text:#f3eee8;
  --board:#45413c;
  --empty:#625b54;
  --panel:#302d2a;
  --button:#a78b70;
  --button-hover:#c09c78;
  --shadow:0 5px 18px rgba(0,0,0,.28);
}

.game {
  width:min(100%,520px);
  margin:0 auto;
}

.header {
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:10px;
}

h1 {
  margin:0;
  font-size:clamp(2.7rem,10vw,4rem);
  line-height:1;
  letter-spacing:-3px;
}

.scores {
  display:flex;
  gap:7px;
}

.score-box {
  min-width:82px;
  padding:8px 11px;
  border-radius:7px;
  background:var(--board);
  color:white;
  text-align:center;
  font-weight:bold;
}

.score-label {
  color:#eee4da;
  text-transform:uppercase;
  font-size:.68rem;
}

.score-value {
  font-size:1.35rem;
  margin-top:2px;
}

.subrow {
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:8px;
  margin:12px 0;
}

.subtitle {
  margin:0;
  font-size:.95rem;
}

button {
  border:0;
  border-radius:7px;
  padding:10px 13px;
  color:white;
  background:var(--button);
  font-weight:700;
  cursor:pointer;
  transition:transform .12s,background .15s,box-shadow .15s;
}

button:hover {
  background:var(--button-hover);
  transform:translateY(-1px);
  box-shadow:var(--shadow);
}

button:active {
  transform:scale(.96);
}

button:disabled {
  opacity:.4;
  cursor:not-allowed;
}

.toolbar {
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:7px;
  margin:10px 0;
}

.toolbar button {
  font-size:.83rem;
  padding:10px 4px;
}

.board-wrap {
  position:relative;
}

.board {
  background:var(--board);
  border-radius:10px;
  padding:9px;
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:9px;
  width:100%;
  aspect-ratio:1/1;
  box-shadow:var(--shadow);
  touch-action:none;
  user-select:none;
}

.cell {
  background:var(--empty);
  border-radius:6px;
  display:flex;
  align-items:center;
  justify-content:center;
  min-width:0;
  min-height:0;
}

.tile {
  width:100%;
  height:100%;
  border-radius:6px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-weight:900;
  font-size:clamp(1.15rem,6vw,2.1rem);
  animation:tilePop .18s ease-out;
}

.tile.empty {
  background:transparent !important;
}

.tile.merge {
  animation:mergePulse .34s ease-in-out;
}

@keyframes tilePop {
  0% {transform:scale(.72);opacity:.55}
  70% {transform:scale(1.08)}
  100% {transform:scale(1);opacity:1}
}

@keyframes mergePulse {
  0% {transform:scale(.78)}
  45% {transform:scale(1.18);filter:brightness(1.18)}
  100% {transform:scale(1)}
}

@keyframes boardGlow {
  0%,100% {box-shadow:var(--shadow)}
  50% {
    box-shadow:0 0 0 5px rgba(237,194,46,.45),var(--shadow)
  }
}

.board.win {
  animation:boardGlow 1.1s ease-in-out 2;
}

.info {
  display:flex;
  justify-content:space-between;
  gap:8px;
  margin:10px 2px;
  font-size:.86rem;
}

.status {
  min-height:25px;
  margin:8px 0;
  font-weight:700;
  text-align:center;
}

.controls-title {
  margin:14px 0 7px;
  font-size:1rem;
}

.dpad {
  width:min(230px,75%);
  margin:0 auto;
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:7px;
}

.dpad button {
  min-height:48px;
  font-size:1.2rem;
}

.dpad .blank {
  visibility:hidden;
}

.help {
  background:var(--panel);
  padding:12px 14px;
  border-radius:8px;
  margin-top:14px;
  font-size:.86rem;
  line-height:1.5;
}

.options {
  display:flex;
  justify-content:center;
  flex-wrap:wrap;
  gap:8px;
  margin-top:12px;
}

.options button {
  font-size:.8rem;
}

.overlay {
  display:none;
  position:absolute;
  inset:0;
  border-radius:10px;
  background:rgba(250,248,239,.82);
  z-index:5;
  align-items:center;
  justify-content:center;
  text-align:center;
  padding:20px;
}

body.dark .overlay {
  background:rgba(23,23,23,.86);
}

.overlay.show {
  display:flex;
  animation:tilePop .25s ease-out;
}

.overlay-card {
  background:var(--panel);
  border-radius:12px;
  padding:22px;
  box-shadow:var(--shadow);
  width:90%;
}

.overlay-card h2 {
  margin:0 0 8px;
  font-size:1.8rem;
}

.overlay-card p {
  margin:0 0 15px;
}

@media(max-width:390px) {
  body {padding:5px}
  .board {gap:6px;padding:6px}
  .toolbar {gap:5px}
  .toolbar button {font-size:.75rem}
  .score-box {min-width:70px;padding:7px}
  .score-value {font-size:1.1rem}
}
</style>
</head>

<body>

<div class="game">

  <div class="header">
    <h1>2048</h1>

    <div class="scores">
      <div class="score-box">
        <div class="score-label">Score</div>
        <div id="score" class="score-value">0</div>
      </div>

      <div class="score-box">
        <div class="score-label">Best</div>
        <div id="best" class="score-value">0</div>
      </div>
    </div>
  </div>

  <div class="subrow">
    <p class="subtitle">
      Join the numbers and reach <b>2048!</b>
    </p>
    <button id="newGame">↻ New game</button>
  </div>

  <div class="toolbar">
    <button id="undo">↶ Undo</button>
    <button id="redo">↷ Redo</button>
    <button id="sound">🔊 Sound: On</button>
    <button id="theme">🌙 Dark mode</button>
  </div>

  <div class="board-wrap">

    <div id="board" class="board"
         role="grid" aria-label="2048 game board">
    </div>

    <div id="overlay" class="overlay">
      <div class="overlay-card">
        <h2 id="overlayTitle">You win!</h2>
        <p id="overlayText">You reached 2048.</p>

        <button id="continueBtn">
          Continue playing
        </button>

        <button id="againBtn">
          New game
        </button>
      </div>
    </div>

  </div>

  <div class="info">
    <span id="moves">Moves: 0</span>
    <span id="state">Keep going!</span>
  </div>

  <div class="status" id="status">
    Use arrow keys, WASD, buttons or swipe.
  </div>

  <div class="controls-title">
    <b>🎮 Move tiles</b>
  </div>

  <div class="dpad">
    <span class="blank"></span>
    <button data-dir="up">⬆️</button>
    <span class="blank"></span>

    <button data-dir="left">⬅️</button>
    <button data-dir="down">⬇️</button>
    <button data-dir="right">➡️</button>
  </div>

  <div class="options">
    <button id="howTo">❔ How to play</button>
    <button id="resetBest">Reset best score</button>
  </div>

  <div class="help" id="help">
    <b>How to play:</b>
    Slide all tiles in one direction. Matching numbers merge into one.
    (2 + 2 = 4). A new 2 or 4 appears after every valid move.

    <br><b>Keyboard:</b> Arrow keys or W / A / S / D.

    <br><b>Mobile:</b> Swipe in any direction.

    <br><b>Extras:</b> Undo, redo, sound and theme controls.
  </div>

</div>

<script>

(() => {

  const N = 4;
  const TARGET = 2048;

  const colors = {
    0:['#cdc1b4','#776e65'],
    2:['#eee4da','#776e65'],
    4:['#ede0c8','#776e65'],
    8:['#f2b179','#f9f6f2'],
    16:['#f59563','#f9f6f2'],
    32:['#f67c5f','#f9f6f2'],
    64:['#f65e3b','#f9f6f2'],
    128:['#edcf72','#f9f6f2'],
    256:['#edcc61','#f9f6f2'],
    512:['#edc850','#f9f6f2'],
    1024:['#edc53f','#f9f6f2'],
    2048:['#edc22e','#f9f6f2']
  };

  let board;
  let score = 0;
  let moves = 0;
  let won = false;
  let keepPlaying = false;
  let over = false;
  let soundOn = true;

  let undoStack = [];
  let redoStack = [];
  let lastMerged = new Set();

  let best = Number(
    localStorage.getItem('2048-best') || 0
  );

  const $ = id => document.getElementById(id);

  function copy(b) {
    return b.map(row => row.slice());
  }

  function snapshot() {
    return {
      board:copy(board),
      score,
      moves,
      won,
      keepPlaying,
      over
    };
  }

  function restore(s) {
    board = copy(s.board);
    score = s.score;
    moves = s.moves;
    won = s.won;
    keepPlaying = s.keepPlaying;
    over = s.over;
    lastMerged.clear();
    render();
  }

  function pushUndo() {
    undoStack.push(snapshot());

    if (undoStack.length > 100) {
      undoStack.shift();
    }

    redoStack = [];
    updateHistoryButtons();
  }

  function addTile() {

    const empty = [];

    for (let r=0; r<N; r++) {
      for (let c=0; c<N; c++) {
        if (!board[r][c]) {
          empty.push([r,c]);
        }
      }
    }

    if (!empty.length) return;

    const [r,c] =
      empty[Math.floor(Math.random()*empty.length)];

    board[r][c] =
      Math.random() < 0.9 ? 2 : 4;
  }

  function start() {

    board = Array.from(
      {length:N},
      () => Array(N).fill(0)
    );

    score = 0;
    moves = 0;
    won = false;
    keepPlaying = false;
    over = false;

    undoStack = [];
    redoStack = [];
    lastMerged.clear();

    addTile();
    addTile();

    $('status').textContent =
      'New game started. Good luck!';

    render();
  }

  function lineMove(line) {

    const values = line.filter(v => v !== 0);
    const out = [];
    const merged = [];

    for (let i=0; i<values.length; i++) {

      if (
        i < values.length-1 &&
        values[i] === values[i+1]
      ) {

        const v = values[i] * 2;

        out.push(v);
        merged.push(v);
        score += v;

        i++;

      } else {

        out.push(values[i]);

      }
    }

    while (out.length < N) {
      out.push(0);
    }

    return {line:out, merged};
  }

  function move(dir) {

    if (over || (won && !keepPlaying)) {
      return;
    }

    const before = copy(board);
    const oldScore = score;
    const mergedValues = [];

    let next = Array.from(
      {length:N},
      () => Array(N).fill(0)
    );

    for (let i=0; i<N; i++) {

      let line;

      if (dir === 'left') {
        line = board[i].slice();
      }

      if (dir === 'right') {
        line = board[i].slice().reverse();
      }

      if (dir === 'up') {
        line = board.map(row => row[i]);
      }

      if (dir === 'down') {
        line = board.map(row => row[i]).reverse();
      }

      const result = lineMove(line);

      mergedValues.push(...result.merged);

      let out = result.line;

      if (dir === 'right' || dir === 'down') {
        out = out.reverse();
      }

      if (dir === 'left' || dir === 'right') {
        next[i] = out;
      } else {
        for (let r=0; r<N; r++) {
          next[r][i] = out[r];
        }
      }
    }

    const changed =
      JSON.stringify(before) !== JSON.stringify(next);

    if (!changed) {
      score = oldScore;
      $('status').textContent =
        'No tiles can move in that direction.';
      return;
    }

    const earned = score - oldScore;

    score = oldScore;
    pushUndo();
    score = oldScore + earned;

    board = next;
    addTile();

    moves++;
    lastMerged = new Set(mergedValues);

    if (score > best) {
      best = score;
      localStorage.setItem(
        '2048-best',
        String(best)
      );
    }

    if (
      board.some(row =>
        row.some(v => v >= TARGET)
      ) && !won
    ) {

      won = true;

      playTone(660,0.18);

      showOverlay(
        '🎉 You win!',
        'You reached 2048. Keep playing or start a new game.',
        true
      );

    } else if (isGameOver()) {

      over = true;

      playTone(180,0.3);

      showOverlay(
        'Game over',
        'No more moves are possible. Try again!',
        false
      );

    } else {

      playTone(420,0.06);

      $('status').textContent = 'Nice move!';

    }

    render();
  }

  function isGameOver() {

    for (let r=0; r<N; r++) {

      for (let c=0; c<N; c++) {

        if (!board[r][c]) {
          return false;
        }

        if (
          c < 3 &&
          board[r][c] === board[r][c+1]
        ) {
          return false;
        }

        if (
          r < 3 &&
          board[r][c] === board[r+1][c]
        ) {
          return false;
        }

      }
    }

    return true;
  }

  function playTone(freq,duration) {

    if (!soundOn) return;

    try {

      const C =
        window.AudioContext ||
        window.webkitAudioContext;

      if (!C) return;

      const ctx = new C();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.frequency.value = freq;

      gain.gain.setValueAtTime(
        .07,
        ctx.currentTime
      );

      gain.gain.exponentialRampToValueAtTime(
        .001,
        ctx.currentTime + duration
      );

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + duration);

      osc.onended = () => ctx.close();

    } catch(e) {
      console.log('Audio unavailable:',e);
    }
  }

  function render() {

    const el = $('board');

    el.innerHTML = '';

    board.forEach(row => {

      row.forEach(v => {

        const cell = document.createElement('div');

        cell.className = 'cell';

        const tile = document.createElement('div');

        tile.className =
          'tile' + (v ? '' : ' empty');

        if (v) {

          const [bg,fg] =
            colors[v] || ['#3c3a32','#f9f6f2'];

          tile.style.background = bg;
          tile.style.color = fg;
          tile.textContent = v;

          if (v >= 1024) {
            tile.style.fontSize =
              'clamp(.9rem,4.5vw,1.6rem)';
          }

          if (lastMerged.has(v)) {
            tile.classList.add('merge');
          }
        }

        cell.appendChild(tile);
        el.appendChild(cell);

      });

    });

    $('score').textContent = score;
    $('best').textContent = best;
    $('moves').textContent = 'Moves: ' + moves;

    $('state').textContent =
      over ? 'Game over' :
      won ? (
        keepPlaying
        ? '2048 reached · Keep playing'
        : 'You reached 2048!'
      ) : 'Keep going!';

    $('undo').disabled = !undoStack.length;
    $('redo').disabled = !redoStack.length;

    if (won && !keepPlaying) {
      $('board').classList.add('win');
    } else {
      $('board').classList.remove('win');
    }

    if (over) {
      showOverlay(
        'Game over',
        'No more moves are possible. Try again!',
        false
      );
    } else if (won && !keepPlaying) {
      showOverlay(
        '🎉 You win!',
        'You reached 2048. Keep playing or start a new game.',
        true
      );
    } else {
      $('overlay').classList.remove('show');
    }
  }

  function showOverlay(title,message,canContinue) {

    $('overlayTitle').textContent = title;
    $('overlayText').textContent = message;

    $('continueBtn').style.display =
      canContinue ? 'inline-block' : 'none';

    $('overlay').classList.add('show');
  }

  function updateHistoryButtons() {
    $('undo').disabled = !undoStack.length;
    $('redo').disabled = !redoStack.length;
  }

  function undo() {

    if (!undoStack.length) return;

    redoStack.push(snapshot());

    const s = undoStack.pop();

    restore(s);

    $('status').textContent = 'Move undone.';

    updateHistoryButtons();
  }

  function redo() {

    if (!redoStack.length) return;

    undoStack.push(snapshot());

    const s = redoStack.pop();

    restore(s);

    $('status').textContent = 'Move restored.';

    updateHistoryButtons();
  }

  // Direction buttons
  document.querySelectorAll('[data-dir]').forEach(b => {

    b.addEventListener('click', () => {
      move(b.dataset.dir);
    });

  });

  // New game
  $('newGame').addEventListener('click',start);
  $('againBtn').addEventListener('click',start);

  // Undo and redo
  $('undo').addEventListener('click',undo);
  $('redo').addEventListener('click',redo);

  // Continue after winning
  $('continueBtn').addEventListener('click',() => {

    keepPlaying = true;

    $('overlay').classList.remove('show');

    $('status').textContent =
      'Keep playing — try for a higher tile!';

    render();

  });

  // Sound
  $('sound').addEventListener('click',() => {

    soundOn = !soundOn;

    $('sound').textContent =
      soundOn ? '🔊 Sound: On' : '🔇 Sound: Off';

  });

  // Dark mode
  $('theme').addEventListener('click',() => {

    document.body.classList.toggle('dark');

    $('theme').textContent =
      document.body.classList.contains('dark')
      ? '☀️ Light mode'
      : '🌙 Dark mode';

  });

  // Reset best score
  $('resetBest').addEventListener('click',() => {

    best = 0;

    localStorage.removeItem('2048-best');

    render();

    $('status').textContent = 'Best score reset.';

  });

  // Instructions
  $('howTo').addEventListener('click',() => {

    $('help').hidden = !$('help').hidden;

  });

  // Keyboard controls
  window.addEventListener('keydown',e => {

    const map = {

      ArrowUp:'up',
      w:'up',
      W:'up',

      ArrowDown:'down',
      s:'down',
      S:'down',

      ArrowLeft:'left',
      a:'left',
      A:'left',

      ArrowRight:'right',
      d:'right',
      D:'right'

    };

    if (map[e.key]) {

      e.preventDefault();

      move(map[e.key]);

    } else if (
      (e.ctrlKey || e.metaKey) &&
      e.key.toLowerCase() === 'z'
    ) {

      e.preventDefault();
      undo();

    } else if (
      (e.ctrlKey || e.metaKey) &&
      e.key.toLowerCase() === 'y'
    ) {

      e.preventDefault();
      redo();

    }

  });

  // Mobile swipe controls
  let touchStart = null;

  $('board').addEventListener(
    'touchstart',
    e => {

      const t = e.changedTouches[0];

      touchStart = [t.clientX,t.clientY];

    },
    {passive:true}
  );

  $('board').addEventListener(
    'touchend',
    e => {

      if (!touchStart) return;

      const t = e.changedTouches[0];

      const dx = t.clientX - touchStart[0];
      const dy = t.clientY - touchStart[1];

      if (Math.max(Math.abs(dx),Math.abs(dy)) > 25) {

        move(
          Math.abs(dx) > Math.abs(dy)
          ? (dx > 0 ? 'right' : 'left')
          : (dy > 0 ? 'down' : 'up')
        );

      }

      touchStart = null;

    },
    {passive:true}
  );

  // Start the game
  start();

  $('best').textContent = best;

})();

</script>
</body>
</html>
"""

st.markdown(
    """
    <div style="text-align:center; margin-bottom:0.5rem;">
      <h2 style="margin-bottom:0;">
        🎮 2048 Enhanced Edition
      </h2>
      <p style="margin-top:0.2rem;">
        Keyboard • Swipe • Undo/Redo • Animations
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

components.html(
    GAME_HTML,
    height=940,
    scrolling=True
)

st.caption(
    "Built with Python + Streamlit. "
    "Your best score is saved in this browser."
)
