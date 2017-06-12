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


def handle_chat(gs, chat_obj):
    speaker_name = chat_obj['ActualNickName']
    if chat_obj['isAt'] == 'True':
        content = cu.rm_At(chat_obj['Content'])

        if content:
            return handle_targeted_chat(gs, content,
                                        speaker_name)
        else:
            return build_message(None)
    elif gs.current_speaker is not None:
        if gs.current_speaker.name == speaker_name:
            gs.append_comment(chat_obj['Content'])
            return build_message(None)
        else:
            return build_message(None)
    elif gs.director_name == speaker_name:
        return handle_director_chat(gs, chat_obj['Content'])
    else:
        return build_message(None)


def handle_director_chat(gs, content):
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


def handle_targeted_chat(gs, content, speaker_name):
    if 'help' in content:
        return build_message('discubot.com/help')
    elif '发言整理' in content:
        return build_message('discubot.com/comments')
    elif '开局' in content:
        if gs.started:
            gs.reset()
            gs.start()
        else:
            gs.start()
        gs.set_director(speaker_name)
        return build_message(vocab.acknowledge.gen())
    elif '天亮' in content:
        if speaker_name == gs.director_name:
            gs.dawn()
        return build_message(vocab.acknowledge.gen())
    elif '天黑' in content:
        if speaker_name == gs.director_name:
            gs.dusk()
        return build_message(vocab.acknowledge.gen())
    elif '发言' in content:
        return handle_comment(gs, content, speaker_name)
    else:
        tb_r = tb.get_response(content)
        rply_content = tb_r or 'echo:' + content
        return build_message(rply_content)


def handle_comment(gs, content, speaker_name):
    if '结束' in content:
        try:
            player_i = gs.current_speaker.index
            gs.set_current_speaker(None)
            link_str = 'discubot.com/comment/' + str(gs.comments[-1].id)
            _message = str(player_i) + '号的发言记录好了：' + link_str
        except:
            _message = '发言前先@我并说 x号发言， 否则我记录不到[Sweat]'
        finally:
            return build_message(_message)

    elif '号发言' in content:
        player_i = cu.get_ints(content.split('号发言')[0])[0]
        content_trimed = content.split('号发言')[1]
        try:
            player = gs.get_player(index=player_i)
        except:
            player = Player(speaker_name, player_i)
            gs.add_player(player)
        finally:
            gs.set_current_speaker(player)
            comment = Comment(player, gs.day, content_trimed)
            gs.add_comment(comment)
        return build_message(vocab.start_comment.gen())
