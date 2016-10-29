from racing.game.game import GameLogic


class _Logic(GameLogic):

    def on_start(self):
        GameLogic.on_start(self)
        car = game.options['car'] if 'car' in game.options.dct else ''
        track = game.options['track'] if 'track' in game.options.dct else ''
        if car and track:
            self.mdt.fsm.demand('Loading', 'tracks/' + track, car)
        else:
            self.mdt.fsm.demand('Menu')