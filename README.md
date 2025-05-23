<h1>Chess Game (Python + Pygame)</h1>

<p>
A simple chess game implemented in Python using Pygame.<br>
This project features a graphical chessboard, interactive piece movement, and a move log.
</p>

<h2>Features Implemented</h2>
<ol>
  <li><b>Graphical Chessboard:</b> An 8x8 chessboard is displayed using Pygame, with alternating colored squares.</li>
  <li><b>Piece Rendering:</b> Chess pieces (PNG images) are loaded and rendered on the board in their correct starting positions.</li>
  <li><b>Interactive Moves:</b> Players can select and move pieces by clicking on the board. The selected square is highlighted for clarity.</li>
  <li><b>Move Logging:</b> All moves are tracked in a move log, allowing for potential future features like undo.</li>
  <li><b>Turn Handling:</b> The game enforces alternating turns between White and Black.</li>
  <li><b>Move Validation:</b> Only allow legal chess moves for each piece.</li>
  <li><b>Undo Moves:</b> Allow players to undo move using keyboard shortcuts (Ctrl+Z) </li>
  <li><b>En Passant:</b> Implemented the special En Passant move</li>
</ol>

<h2>How to Run</h2>
<ol>
  <li>
    <b>Install requirements:</b> Make sure you have Python 3 and Pygame installed.<br>
    <code>pip install pygame</code>
  </li>
  <li>
    <b>Prepare Piece Images:</b> Place chess piece images in an <b>images/</b> folder in the project directory.
  </li>
  <li>
    <b>Run the Game:</b><br>
    <code>python Chess_main.py</code>
  </li>
</ol>

<h2>Project Structure</h2>
<ul>
  <li>Chess_engine.py &mdash; Game logic and state management</li>
  <li>Chess_main.py &mdash; Main UI and event loop</li>
  <li>images/ &mdash; Folder containing piece images (PNG)</li>
</ul>

<h2>Future updates that I'm thinking of adding</h2>
<ol>
  <li><b>Check and Checkmate Detection:</b> Notify players when their king is in check or checkmate.</li>
  <li><b>Stalemate and Draw Detection:</b> Detect and handle stalemates.</li>
  <li><b>Move History Display:</b> Show a list of previous moves on the screen.</li>
  <li><b>AI Opponent:</b> Add a simple AI to play against.</li>
  <li><b>Pawn Promotion:</b> Allow pawns to promote to another piece upon reaching the last rank.</li>
</ol>


