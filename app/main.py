from flask import Flask, request
from model import Game, Player
import display
import pickle
import os
import controller as c

app = Flask(__name__)


@app.route('/')
def hello():
    msg = "Laugh all you want, they are not for sale"
    return display.message("Not for sale",
                           msg)


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


@app.route('/players', methods=['GET'])
def display_players():
    return display.players(game)


@app.route('/shreff/assign/<shreff_index_str>', methods=['GET'])
def assign_shreff(shreff_index_str):
    game.shreff = game.get_player(index=int(shreff_index_str))
    msg = 'Shreff has assigned to player ' + shreff_index_str
    return display.message(msg, ''), 202


@app.route('/player/add/<name>/<index_str>', methods=['GET'])
def add_player(name, index_str):
    if index_str:
        player = Player(name, int(index_str))
        game.add_player(player)
        msg = f'Player {name} has been added with index {index_str}'
    else:
        player = Player(name)
        game.add_player(player)
        msg = f'Player {name} has been added'
    return display.message(msg, ''), 202


@app.route('/player/kill/<index_str>', methods=['GET'])
def kill_player(index_str):
    player = game.get_player(index=int(index_str))
    player.is_dead = True
    msg = f'Player {index_str} has been killed'
    return display.message(msg, ''), 202


@app.route('/game/state/all', methods=['GET'])
def print_game_state():
    return str(game).replace(',', '<br>')


@app.route('/game/state', methods=['GET'])
def display_game_state():
    return display.game_state(game)


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
