from model import Comment
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


def build_message_multimsgs(msgs):
    return jsonify(
        command='msgs',
        msgs=msgs
    )


def handle_chat(game, chat_obj):
    speaker_name = chat_obj['name']
    if cu.is_self(speaker_name):
        pass
    elif chat_obj['isAt'] == 'True':
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
    base_url_sheet = 'https://docs.google.com/spreadsheets/d/'
    base_url_doc = 'https://docs.google.com/document/d/'
    params = '/edit?usp=sharing'
    if '行程' in content:
        return build_message(base_url_doc +
                             '14gxFL5sz5VrVPJQC3HdT7DuBYm3XkG-HTTMHAxDoiB4' +
                             params)
    elif '账单' in content:
        return build_message(base_url_sheet +
                             '1g9BnJHIdUvwHl-OOB6meMDJKOWq0aE-57Ktl5SeGFBM' +
                             params)
    elif game.recruiting:
        if '1' in content:
            game.init_player(speaker_name, '?')
        elif '0' in content:
            game.remove_player(name=speaker_name)
        return build_message('报名表已更新：discubot.com/players')
    elif 'help' in content:
        return build_message('discubot.com/help')
    elif 'players' in content:
        return build_message('discubot.com/players')
    elif '发言整理' in content or '整理发言' in content:
        return build_message('discubot.com/comments')
    elif '开始报名' in content or '报名开始' in content:
        if game.started:
            game.reset()
        game.recruiting = True
        game.set_director(speaker_name)
        _msg_contents = [vocab.recruit_start.gen(),
                         '你已被钦定为导演[Sly]',
                         '管理界面在discubot.com/director/players']
        _users = [None, speaker_name, speaker_name]
        _msgs = [{'user': u, 'contents': c} for u, c in zip(_users, _msg_contents)]
        return build_message_multimsgs(_msgs)
    elif '开局' in content:
        if game.recruiting:
            game.recruiting = False
        else:
            game.reset()
            game.set_director(speaker_name)
        game.start()
        return build_message(vocab.game_start.gen())
    elif '天亮' in content:
        if speaker_name == game.director_name:
            game.dawn()
            game.set_current_speaker(None)
        return build_message(vocab.dawn.gen())
    elif '天黑' in content:
        if speaker_name == game.director_name:
            game.dusk()
            game.set_current_speaker(None)
        return build_message(vocab.dusk.gen())
    elif '号发言' in content and not ("结束" in content):
        return init_comment(game, content, speaker_name)
    elif '号自爆' in content:
        if not game.isNight:
            game.set_current_speaker(None)
            player_i = cu.get_ints(content.split('号自爆')[0])[0]
            content_trimed = content.split('号自爆')[1]
            player = game.init_player(speaker_name, player_i)
            player_i.is_dead = True
            comment = Comment(player, game.day, content_trimed, is_suicide=True)
            game.add_comment(comment)
            game.set_current_speaker(None)
            game.dusk()
            _message = f'{player_i}号自爆了，夜幕又降临在这个诡异的微信群🌚'
            return build_message(_message)
        else:
            _message = f'如果我没有记错的话，现在是晚上不能自爆...'
            return build_message(_message)
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
    player = game.init_player(speaker_name, player_i)
    game.set_current_speaker(player)
    comment = Comment(player, game.day, content_trimed)
    if game.day <= 1:
        if not game.shreff:
            player.is_shreff_cadidate = True
            comment.is_shreff_run = True
    game.add_comment(comment)
    return build_message(vocab.start_comment.gen())
