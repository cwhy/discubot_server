class VerboseObj:
    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(key=key,
                                               value=self.__dict__[key]))
        return '{' + ', '.join(sb) + '}'

    def __repr__(self):
        return self.__str__()


class Player:
    def __init__(self, name, index=None):
        self.name = name
        self.index = index
        self.is_dead = False
        self.profile_pic = f'/assets/images/profile_pics/{name}.jpg'
        self.is_shreff_cadidate = False
        # TODO
        # self.id = 0

    def __str__(self):
        return f'\'{self.name}, index={self.index}\''

    def __repr__(self):
        return self.__str__()


class Comment(VerboseObj):
    def __init__(self, player, day, content, is_suicide=False):
        self.player = player
        self.day = day
        self.is_shreff_run = False
        self.is_suicide = is_suicide
        self.paragraphs = []
        self.id = None
        if content.strip():
            self.paragraphs.append(content)

    def append(self, content):
        self.paragraphs.append(content.strip())


class Game(VerboseObj):
    def __init__(self):
        self.reset()

    def start(self):
        self.started = True

    def simulate_start(self):
        self.reset()
        self.started = True
        player = Player('test', 23)
        self.add_player(player)
        self.set_current_speaker(player)
        comment = Comment(player, self.day, "kasdfa asdfkl")
        comment.append('asdf')
        self.add_comment(comment)

    def set_director(self, name):
        self.director_name = name

    def reset(self):
        self.comments = []
        self.day = 0
        self.isNight = False
        self.started = False
        self.players = []
        self.n_players = 0
        self.director_name = ''
        self.current_speaker = None
        self.started = False
        self.shreff = None

    def dawn(self):
        self.isNight = False
        self.day += 1

    def dusk(self):
        self.isNight = True

    def add_player(self, player):
        self.players.append(player)
        self.n_players += 1

    def get_player(self, name=None, index=None):
        for player in self.players:
            if player.index == index:
                return player
            elif player.name == name:
                return player
        if name:
            raise Exception(f'Player {name} not found!')
        elif index:
            raise Exception(f'Player {index} not found!')
        else:
            raise Exception('Bad player request')

    def init_player(self, name, index):
        try:
            player = self.get_player(name=name, index=index)
        except:
            player = Player(name, index)
            self.add_player(player)
        finally:
            return player

    def add_comment(self, comment):
        comment.id = len(self.comments)
        self.comments.append(comment)

    def set_current_speaker(self, player):
        self.current_speaker = player

    def append_comment(self, content):
        self.comments[-1].append(content)

    def get_comments_by_player(self, player):
        cs = []
        for c in self.comments:
            if c.player == player:
                cs.append(c)
        return cs

    def get_comments_by_day(self, day):
        cs = []
        for c in self.comments:
            if c.day == day:
                cs.append(c)
        return cs
