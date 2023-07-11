"""
Evaluation functions
"""


def dummy_evaluation_func(state):
    return 0.0


def distance_evaluation_func(state):
    player = state.get_current_player()
    info = state.get_info()
    score = 0.0
    for p, info_p in info.items():
        if p == player:
            score -= info_p["max_distance"]
        else:
            score += info_p["max_distance"]
    return score


def detailed_evaluation_func(state):
    player = state.get_current_player()
    info = state.get_info()
    score = 0.0
    for p, info_p in info.items():
        if p == player:
            if info_p["live_four"] > 0 or info_p["four"] > 0:
                score += 10000
            if info_p["live_three"] > 0: 
                score += 100
            score += info_p["live_two"] * 0.02 + info_p["three"] * 0.02
            score -= info_p["max_distance"]
        else:
            if info_p["live_four"] > 0:
                score -= 1000
            score -= info_p["live_two"] * 0.02 + info_p["three"] * 0.02 + info_p["four"] * 0.05 + info_p["live_three"] * 0.05
            score += info_p["max_distance"]
    if score > 1:
        score = 0.99
    elif score < -1:
        score = -0.99
    return score


def get_evaluation_func(func_name):
    if func_name == "dummy_evaluation_func":
        return dummy_evaluation_func
    elif func_name == "distance_evaluation_func":
        return distance_evaluation_func
    elif func_name == "detailed_evaluation_func":
        return detailed_evaluation_func
    else:
        raise KeyError(func_name)
