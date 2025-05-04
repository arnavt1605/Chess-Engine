<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chess Game (Python + Pygame)</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 2em auto;
            max-width: 700px;
            background-color: #f8f8f8;
            color: #222;
        }
        h1, h2, h3 {
            color: #2d5aa6;
        }
        code, pre {
            background: #eee;
            padding: 2px 4px;
            border-radius: 3px;
            font-size: 1em;
        }
        pre {
            padding: 1em;
            overflow-x: auto;
        }
        ul, ol {
            margin-left: 2em;
        }
        .folder-structure {
            background: #f3f3f3;
            border-left: 4px solid #2d5aa6;
            padding: 1em;
            margin: 1em 0;
            font-family: "Courier New", Courier, monospace;
        }
    </style>
</head>
<body>
    <h1>Chess Game (Python + Pygame)</h1>
    <p>
        A simple chess game implemented in Python using Pygame.<br>
        This project features a graphical chessboard, interactive piece movement, and a move log.
    </p>

    <h2>Features Implemented</h2>
    <ul>
        <li><strong>Graphical Chessboard:</strong> An 8x8 chessboard is displayed using Pygame, with alternating colored squares.</li>
        <li><strong>Piece Rendering:</strong> Chess pieces (PNG images) are loaded and rendered on the board in their correct starting positions.</li>
        <li><strong>Interactive Moves:</strong> Players can select and move pieces by clicking on the board. The selected square is highlighted for clarity.</li>
        <li><strong>Move Logging:</strong> All moves are tracked in a move log, allowing for potential future features like undo.</li>
        <li><strong>Turn Handling:</strong> The game enforces alternating turns between White and Black.</li>
    </ul>

    <h2>How to Run</h2>
    <ol>
        <li><strong>Install requirements:</strong>
            <br>Make sure you have Python 3 and <a href="https://www.pygame.org/wiki/GettingStarted" target="_blank">Pygame</a> installed:
            <pre><code>pip install pygame</code></pre>
        </li>
        <li><strong>Prepare Piece Images:</strong>
            <br>Place chess piece images (<code>wK.png</code>, <code>bQ.png</code>, etc.) in an <code>images/</code> folder in the project directory.
        </li>
        <li><strong>Run the Game:</strong>
            <pre><code>python Chess_main.py</code></pre>
        </li>
    </ol>

    <h2>Project Structure</h2>
    <div class="folder-structure">
        Chess_engine.py   # Game logic and state management<br>
        Chess_main.py     # Main UI and event loop<br>
        images/           # Folder containing piece images (PNG)<br>
        README.html       # Project documentation<br>
    </div>

    <h2>What’s Next? (Future Updates)</h2>
    <p>Here are some features you can add to enhance your chess game:</p>
    <ul>
        <li><strong>Move Validation:</strong> Only allow legal chess moves for each piece.</li>
        <li><strong>Undo/Redo Moves:</strong> Allow players to undo or redo moves using keyboard shortcuts.</li>
        <li><strong>Check and Checkmate Detection:</strong> Notify players when their king is in check or checkmate.</li>
        <li><strong>Stalemate and Draw Detection:</strong> Detect and handle stalemates, threefold repetition, and the fifty-move rule.</li>
        <li><strong>Move History Display:</strong> Show a list of previous moves on the screen.</li>
        <li><strong>AI Opponent:</strong> Add a simple AI to play against.</li>
        <li><strong>Pawn Promotion:</strong> Allow pawns to promote to another piece upon reaching the last rank.</li>
        <li><strong>Castling and En Passant:</strong> Implement special chess moves.</li>
        <li><strong>Sound Effects:</strong> Play sounds for moves, captures, and checks.</li>
        <li><strong>Improved Graphics and Animations:</strong> Add smooth piece movement and better visuals.</li>
        <li><strong>Game Over Screen:</strong> Display a message when the game ends.</li>
    </ul>

    <p><em>Enjoy playing and developing your chess game!</em></p>
</body>
</html>
