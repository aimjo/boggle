from boggle import Boggle
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

boggle_game = Boggle()

app.config["SECRET_KEY"] = 'Applecore'
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def display_board():
    if 'board' not in session:
        session['board'] = boggle_game.make_board()

    board = session['board']
    return render_template('board.html', board=board)

@app.route('/check_guess', methods=['POST'])
def check_guess():
    guess = request.json.get('guess')
    board = session['board']

    # Check if the guess is a valid word and exists on the board
    result = boggle_game.check_valid_word(board, guess)

    # Create a response dictionary with a message based on the result
    response = {'result': result}

    if result == "ok":
        response['message'] = 'Valid word on the board!'
    elif result == "not-on-board":
        response['message'] = 'Valid word, but not on the board.'
    else:
        response['message'] = 'Not a valid word.'

    # Return a JSON response with the result and message
    return jsonify(response)

@app.route('/reset_board', methods=['GET'])
def reset_board():
    session['board'] = boggle_game.make_board()  # Generate a new board and store it in the session
    board = session['board']
    return jsonify({'board': board})

# Initialize game count and highest score
game_count = 0
high_score = 0

@app.route('/update_score', methods=['POST'])
def update_score():
    global game_count, high_score

    # Get the score sent from the front-end
    score = request.json['score']

    # Update game count and highest score
    game_count += 1
    if score > high_score:
        high_score = score

    # Return updated game count and highest score as JSON
    return jsonify({'game_count': game_count, 'high_score': high_score})