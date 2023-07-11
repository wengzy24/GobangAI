import copy
from game import State, Player
from mcts import MCTS
from copy import deepcopy
import random

inf = 10000

class AlphaZero(MCTS):
    """
    A modification based on pure MCTS, replacing randomly playout with using an evaluation function.
    """
    def __init__(self, start_state: State, evaluation_func, c=5, n_playout=2000):
        """
        Parameters:
            evaluation_func: a function taking a state as input and
                outputs the value in the current player's perspective.
        """
        super().__init__(start_state, c, n_playout)
        self.evaluation_func = evaluation_func


    def get_leaf_value(self, state: State):
        if state.game_end()[0]:
            if state.game_end()[1] == -1:
                return 0
            if state.game_end()[1] == state.get_current_player():
                return -1
            return 1
        return -self.evaluation_func(state)


class AlphaZeroPlayer(Player):
    """AI player based on MCTS"""
    def __init__(self, evaluation_func, c=0.1, n_playout=2000):
        super().__init__()
        self.evaluation_func = evaluation_func
        self.c = c
        self.n_playout = n_playout

    def get_action(self, state: State):
        mcts = AlphaZero(state, self.evaluation_func, self.c, self.n_playout)
        for n in range(self.n_playout):
            state_copy = copy.deepcopy(state)
            mcts.playout(state_copy)

        '''
        for i in mcts.root.actions:
            print(i, mcts.root.children[i].n_visits, mcts.root.children[i].get_ucb(self.c))
        '''

        return max(mcts.root.children.items(),
                   key=lambda act_node: act_node[1].n_visits)[0]
