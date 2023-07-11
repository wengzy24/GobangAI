from typing import Tuple
from copy import deepcopy
from game import State, Player
import copy


inf = 10000


class MinimaxSearchPlayer(Player):
    """
    Player based on minimax search.
    """

    def get_action(self, state: State):
        """
        An interface for recursively searching.
        """
        assert state.get_current_player() == self.player
        
        def minimax_search(s: State) -> Tuple:
            """
            Recursively search values of all succeeding nodes, taking maximum of children
            when current player is the agent (self.player) and minimum for opponent.

            Parameters:
                s: the current state

            Return:
                Tuple(value, action): the node value and the best action (if exists)
            
            Note: before you perform an action, you might need to copy the original state for in-place update.
            """
            end, winner = s.game_end()
            value, action = None, None
            if end:
                if winner == -1:
                    value = 0
                else:
                    value = (1 if winner == self.player else -1)
            else:
                if s.get_current_player() == self.player:
                    value = -inf
                    for i in s.get_all_actions():
                        ss = copy.deepcopy(s)
                        ss.perform_action(i)
                        v, a = minimax_search(ss)
                        if value < v:
                            value = v
                            action = i
                else:
                    value = inf
                    for i in s.get_all_actions():
                        ss = copy.deepcopy(s)
                        ss.perform_action(i)
                        v, a = minimax_search(ss)
                        if value > v:
                            value = v
                            action = i
            return value, action

        return minimax_search(state)[1]


class AlphaBetaSearchPlayer(Player):
    """
    Player based on alpha-beta search.
    """

    def get_action(self, state: State):
        """
        An interface for recursively searching.
        """
        assert state.get_current_player() == self.player

        def alpha_beta_search(s: State, alpha, beta):
            """
            Based on minimax search, record current maximum value of the max player (alpha)
            and current minimum value of the min player (beta), use alpha and beta to prune.

            Parameters:
                s: the current state
                alpha: the current maximum value of the max player
                beta: the current minimum value of the min player

            Return:
                Tuple(value, action): the node value and the best action (if exists)
            
            Note: before you perform an action, you might need to copy the original state for in-place update.
            """
            end, winner = s.game_end()
            value, action = None, None
            max_value = alpha
            min_value = beta
            if end:
                if winner == -1:
                    value = 0
                else:
                    value = (1 if winner == self.player else -1)
            else:
                if s.get_current_player() == self.player:
                    value = -inf
                    for i in s.get_all_actions():
                        ss = copy.deepcopy(s)
                        ss.perform_action(i)
                        v, a = alpha_beta_search(ss, max_value, min_value)
                        if value < v:
                            value = v
                            action = i
                        if value > max_value:
                            max_value = value
                        if max_value >= min_value:
                            return value, action
                else:
                    value = inf
                    for i in s.get_all_actions():
                        ss = copy.deepcopy(s)
                        ss.perform_action(i)
                        v, a = alpha_beta_search(ss, max_value, min_value)
                        if value > v:
                            value = v
                            action = i
                        if value < min_value:
                            min_value = value
                        if max_value >= min_value:
                            return value, action
            return value, action

        return alpha_beta_search(state, -inf, inf)[1]


class CuttingOffAlphaBetaSearchPlayer(Player):

    def __init__(self, max_depth, evaluation_func=None):
        """
        Player based on cutting off alpha-beta search.
        Parameters:
            max_depth: maximum searching depth. The search will stop when the depth exists max_depth.
            evaluation_func: a function taking a state as input and
                outputs the value in the current player's perspective.
        """
        super().__init__()
        self.max_depth = max_depth
        self.evaluation_func = (lambda s: 0) if evaluation_func is None else evaluation_func

    def evaluation(self, state: State):
        """
        Calculate the evaluation value relative to the agent player (rather than state's current player),
        i.e., take negation if the current player is opponent or do nothing else wise.
        """
        value = self.evaluation_func(state)
        if self.player != state.get_current_player():
            value = -value
        return value

    def get_action(self, state: State):
        """
        An interface for recursively searching.
        """
        assert state.get_current_player() == self.player

        def cutting_off_alpha_beta_search(s: State, d, alpha, beta):
            """
            Search for several depth and use evaluation value as cutting off.

            Parameters:
                s: the current state
                d: the remaining search depth, the search will stop when d=0
                alpha: the current maximum value of the max player
                beta: the current minimum value of the min player

            Return:
                Tuple(value, action): the node value and the best action (if exists)
            
            Note: before you perform an action, you might need to copy the original state for in-place update.
            """
            end, winner = s.game_end()
            value, action = None, None
            if end:
                if winner == -1:
                    value = 0
                else:
                    value = (1 if winner == self.player else -1)
            else:
                if d == 0:
                    value = self.evaluation(s)
                    return value, action
                if s.get_current_player() == self.player:
                    max_value = -inf
                    min_value = inf
                    for i in s.get_all_actions():
                        ss = copy.deepcopy(s)
                        ss.perform_action(i)
                        v, a = cutting_off_alpha_beta_search(ss, d - 1, max_value, min_value)
                        if max_value < v:
                            max_value = v
                            value = v
                            action = i
                            if max_value > beta:
                                return value, action
                        if min_value > v:
                            min_value = v
                else:
                    max_value = -inf
                    min_value = inf
                    for i in s.get_all_actions():
                        ss = copy.deepcopy(s)
                        ss.perform_action(i)
                        v, a = cutting_off_alpha_beta_search(ss, d - 1, max_value, min_value)
                        if min_value > v:
                            min_value = v
                            value = v
                            action = i
                            if min_value < alpha:
                                return value, action
                        if max_value < v:
                            max_value = v
            return value, action

        return cutting_off_alpha_beta_search(state, self.max_depth, -inf, inf)[1]
