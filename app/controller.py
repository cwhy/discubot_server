from model import Comment, Player
from flask import jsonify
import vocab
import chat_util as cu
import turing_bot as tb


def build_message(content):
    if content:
        return jsonify(
            command='msg',
            msg_content=content
        )
    else:
        return jsonify(command=None)


def handle_chat(game, chat_obj):
    speaker_name = chat_obj['name']
    if chat_obj['isAt'] == 'True':
        content = cu.rm_At(chat_obj['Content'])

        if content:
            return handle_targeted_chat(game,
                                        content,
                                        speaker_name)
        else:
            return build_message(vocab.en.gen())
    elif game.current_speaker is not None:
        if game.current_speaker.name == speaker_name:
            game.append_comment(chat_obj['Content'])
            return build_message(None)
        else:
            return build_message(None)
    elif game.director_name == speaker_name:
        return handle_director_chat(game, chat_obj['Content'])
    else:
        return build_message(None)


def handle_director_chat(game, content):
    if '发言' in content:
        if '@' in content:
            _atu = cu.retrieve_At(content)
            _message = _atu + '记得发言格式哦\n'
            _message += 'discubot.com/help'
            return build_message(_message)
        else:
            return build_message(None)
    else:
        return build_message(None)


def handle_targeted_chat(game, content, speaker_name):
    if 'help' in content:
        return build_message('discubot.com/help')
    elif '发言整理' in content:
        return build_message('discubot.com/comments')
    elif '开局' in content:
        if game.started:
            game.reset()
            game.start()
        else:
            game.start()
        game.set_director(speaker_name)
        return build_message(vocab.acknowledge.gen())
    elif '天亮' in content:
        if speaker_name == game.director_name:
            game.dawn()
        return build_message(vocab.acknowledge.gen())
    elif '天黑' in content:
        if speaker_name == game.director_name:
            game.dusk()
        return build_message(vocab.acknowledge.gen())
    elif '号发言' in content:
        return init_comment(game, content, speaker_name)
    elif '过' == content.strip() or '发言结束' in content:
        try:
            player_i = game.current_speaker.index
            game.set_current_speaker(None)
            link_str = 'discubot.com/comment/' + str(game.comments[-1].id)
            _message = str(player_i) + '号的发言记录好了：' + link_str
        except:
            _message = '发言前先@我并说 x号发言， 否则我记录不到[Sweat]'
        finally:
            return build_message(_message)
    else:
        tb_r = tb.get_response(content)
        rply_content = tb_r or 'echo:' + content
        return build_message(rply_content)


def init_comment(game, content, speaker_name):
    player_i = cu.get_ints(content.split('号发言')[0])[0]
    content_trimed = content.split('号发言')[1]
    try:
        player = game.get_player(index=player_i)
    except:
        player = Player(speaker_name, player_i)
        game.add_player(player)
    finally:
        game.set_current_speaker(player)
        comment = Comment(player, game.day, content_trimed)
        if game.day == 1:
            if not game.shreff:
                player.is_shreff_cadidate = True
                comment.is_shreff_run = True
        game.add_comment(comment)
    return build_message(vocab.start_comment.gen())
