from eduardo import (
    Environment,
    _Player,
    STARTING_ELO,
    K_FACTOR
)

class CustomEnvironment(Environment):
    def create_player(self, id):
        new_player = CustomPlayer(id, self)
        self.players[id] = new_player
        return new_player

class CustomPlayer(Player):
    def __init__(self, id, env):
        super().__init__(id, env)
        self._match_count = 0

    def _beat(self, opponent):
        super()._beat(opponent)
        self._match_count += 1
        opponent._match_count += 1
