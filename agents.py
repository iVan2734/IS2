import random
import time


class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_action(self, state, max_depth):
        pass


class RandomAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        return actions[random.randint(0, len(actions) - 1)]


class GreedyAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = None, None
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = new_state.get_score(state.get_on_move_chr())
            if (best_score is None and best_action is None) or score > best_score:
                best_action = action
                best_score = score
        return best_action


def is_terminal_node(state, depth):
    return depth == 0 or len(state.get_legal_actions()) == 0

class MaxNAgent(Agent):
    @staticmethod
    def maxN(state, depth):
        if is_terminal_node(state, depth):
            return state.get_scores()
        player = state.get_on_move_chr()
        best_scores = None
        for action in state.get_legal_actions():
            child = state.generate_successor_state(action)
            scores = MaxNAgent.maxN(child, depth - 1)
            if best_scores is None or scores[player] > best_scores[player]:
                best_scores = scores
        return best_scores

    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        player = state.get_on_move_chr()
        best_action = None
        best_value = -float("inf")
        for action in state.get_legal_actions():
            child = state.generate_successor_state(action)
            scores = MaxNAgent.maxN(child, max_depth - 1)
            if scores[player] > best_value:
                best_value = scores[player]
                best_action = action
        return best_action


class MiniMaxAgent(Agent):
    @staticmethod
    def miniMax(state, depth, maxPlayer):
        if is_terminal_node(state, depth):
            return state.get_score('a')-state.get_score('b')

        if maxPlayer:
            score = -float("inf")
            for action in state.get_legal_actions():
                child = state.generate_successor_state(action)
                score = max(score, MiniMaxAgent.miniMax(child, depth - 1, False))
            return score
        else:
            score = float("inf")
            for action in state.get_legal_actions():
                child = state.generate_successor_state(action)
                score = min(score, MiniMaxAgent.miniMax(child, depth - 1, True))
            return score

    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        player = state.get_on_move_chr()
        maxPlayer = (player == 'A')
        best_action = None

        if maxPlayer:
            best_value = -float("inf")
            for action in state.get_legal_actions():
                child = state.generate_successor_state(action)
                score = MiniMaxAgent.miniMax(child, max_depth - 1, False)
                if score > best_value:
                    best_value = score
                    best_action = action
        else:
            best_value = float("inf")
            for action in state.get_legal_actions():
                child = state.generate_successor_state(action)
                score = MiniMaxAgent.miniMax(child, max_depth - 1, True)
                if score < best_value:
                    best_value = score
                    best_action = action
        return best_action


class MiniMaxAlphaBetaAgent(Agent):
    @staticmethod
    def miniMaxAlphaBeta(state, depth, maxPlayer,alpha,beta):
        if is_terminal_node(state, depth):
            #print(state.get_score('a'))
            #print(state.get_score('b'))
            return state.get_score('a')-state.get_score('b')

        if maxPlayer:
            score = -float("inf")
            for action in state.get_legal_actions():
                child = state.generate_successor_state(action)
                score = max(score, MiniMaxAlphaBetaAgent.miniMaxAlphaBeta(child, depth - 1, False,alpha,beta))
                alpha = max(score, alpha)
                if alpha >= beta: break
            return score
        else:
            score = float("inf")
            for action in state.get_legal_actions():
                child = state.generate_successor_state(action)
                score = min(score, MiniMaxAlphaBetaAgent.miniMaxAlphaBeta(child, depth - 1, True,alpha,beta))
                beta = min(score, beta)
                if alpha >= beta: break
            return score

    def get_chosen_action(self, state, max_depth):
        #time.sleep(0.5)
        player = state.get_on_move_chr()
        maxPlayer = (player=="A")
        best_action = None

        alpha = -float("inf")
        beta = float("inf")

        if maxPlayer:
            bestScore = -float("inf")
            for action in state.get_legal_actions():
                newState = state.generate_successor_state(action)
                score = MiniMaxAlphaBetaAgent.miniMaxAlphaBeta(newState, max_depth - 1, False,alpha,beta)
                if score > bestScore:
                    bestScore = score
                    best_action = action
                    alpha=score
                    if alpha>=beta: break
        else:
            bestScore = float("inf")
            for action in state.get_legal_actions():
                newState = state.generate_successor_state(action)
                score = MiniMaxAlphaBetaAgent.miniMaxAlphaBeta(newState, max_depth - 1, True,alpha,beta)
                if score < bestScore:
                    bestScore = score
                    best_action = action
                    beta=score
                    if alpha>=beta: break
        return best_action