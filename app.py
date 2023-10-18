from flask import Flask, render_template, request, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from boggle import Boggle

boggle_game = Boggle()
board_key = "board"


app = Flask(__name__)
app.config['SECRET_KEY'] = "timiza"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

@app.route("/")
def startGame():
    """load home page."""
    
    board = boggle_game.make_board()
    session[board_key] = board

    maxScore = session.get("maxScore", 0)
    playsCount = session.get("playsCount", 0)

    return render_template("index.html", board=board, maxScore=maxScore,playsCount=playsCount )


@app.route("/ValidateWord", methods=["POST"])
def ValidateWord():
    """checks if a word is valid."""
    board = session[board_key]
    word = request.json['word']    
    return jsonify({'result': boggle_game.check_valid_word(board,word)
})


@app.route("/Finish", methods=["POST"])
def finishGame():
    """stores max score and plays count"""

    playsCount = session.get("playsCount", 0)


    session["maxScore"] = request.json['score']
    session["playsCount"] = playsCount + 1

    return jsonify({'result': 'OK'})