from flask import render_template
import vocab


def message(_title, _message):
    return render_template('message.html',
                           title=_title,
                           messages=_message.split('\n'))


def page_404():
    broken_message = vocab.broken.gen()
    return message('404',
                   broken_message)


def static_page(name):
    return render_template(name)


def comment(game, c_id):
    try:
        comment = game.comments[c_id]
    except IndexError:
        return page_404()
    else:
        return render_template('single_comment.html',
                               player_index=comment.player.index,
                               day=comment.day,
                               paragraphs=comment.paragraphs)


def comments(game, player_index=None, day=None):
    if player_index is not None:
        _title = f'{player_index}号玩家的所有发言'
        try:
            _player = game.get_player(index=player_index)
        except:
            return message('玩家不存在', '')
        else:
            _comments = game.get_comments_by_player(_player)
            return render_template('comments.html',
                                   title=_title,
                                   show_day=True,
                                   comments=_comments)
    elif day is not None:
        if day == 0:
            _title = f'警上所有的发言'
        else:
            _title = f'第{day}天的发言'
        _comments = game.get_comments_by_day(day)
        if not _comments:
            return message('这一天还没有发言', '')
        else:
            return render_template('comments.html',
                                   title=_title,
                                   show_player=True,
                                   comments=_comments)
    else:
        _title = '到目前为止的所有发言'
        return render_template('comments.html',
                               title=_title,
                               show_player=True,
                               show_day=True,
                               comments=game.comments)
