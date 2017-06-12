from flask import Flask, request
from model import Game
import display
import pickle
import os
import controller as c

app = Flask(__name__)


@app.route('/')
def hello():
    return "Laugh all you want, they are not for sale"


@app.route('/help')
def help():
    return display.static_page('help.html')


@app.route('/comment/<c_id>')
def display_comment(c_id):
    return display.comment(game, int(c_id))


@app.route('/comments/player/<p_idx>')
def display_comments_by_player(p_idx):
    return display.comments(game,
                            player_index=int(p_idx))


@app.route('/comments')
def display_all_comments():
    return display.comments(game)


@app.route('/comments/day/<day>')
def display_comments_by_day(day):
    return display.comments(game,
                            day=int(day))


# @app.route('/comment/add', methods=['POST'])
# def add_comment():
#     game_state['comment_N'] += 1
#     return 'Request Success', 202


@app.route('/chats/add', methods=['POST'])
def log_chat():
    raw_chats.append(request.form)
    message = c.handle_chat(game, request.form)
    return message, 202


@app.route('/chats/list_all', methods=['GET'])
def list_chat():
    content = '<br>'.join([str(c) for c in raw_chats])
    return content


@app.route('/game/state', methods=['GET'])
def print_game_state():
    return str(game).replace(',', '<br>')


@app.route('/game/save', methods=['GET'])
def save_game():
    with open('data/current.pkl', 'wb') as f_:
        pickle.dump(game, f_)
    response = display.message('Game state saved', '')
    return response, 202


@app.route('/game/reset', methods=['GET'])
def reset_game():
    game.reset()
    if os.path.isfile('data/current.pkl'):
        os.remove('data/current.pkl')
    response = display.message('Game reinitialized', '')
    return response, 202


@app.route('/game/simulate', methods=['GET'])
def simulate_game():
    game.simulate_start()
    response = display.message('Game simulated', '')
    return response, 202


@app.errorhandler(404)
def page_not_found(e):
    return display.page_404(), 404


raw_chats = []
print('Try loading old record')
try:
    with open('data/current.pkl', 'rb') as f_:
        game = pickle.load(f_)
        print('Loading success~')
except IOError:
    print('No records found, fresh state initialted')
    game = Game()

if __name__ == '__main__':
    app.run()
