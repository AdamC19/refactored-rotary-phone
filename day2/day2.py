import os



#------------------------------------------------------------------------------
def decode_score(round: str) -> int:
    """ shape + outcome 

    shape:      A/X : 1
                B/Y : 2
                C/Z : 3

    outcome:    LOSE: 0
                DRAW: 3
                WIN:  6
    """
    moves = round.strip().split(' ')
    opp_move = moves[0]
    
    my_move = moves[1]
    my_move_std = 'A'
    shape_score = 0
    if my_move == 'X':
        shape_score = 1
        my_move_std = 'A'
    elif my_move == 'Y':
        shape_score = 2
        my_move_std = 'B'
    elif my_move == 'Z':
        shape_score = 3
        my_move_std = 'C'
    
    outcome_score = 0 # default to lose, only change if need be

    if opp_move == my_move_std:
        outcome_score = 3
    else:
        if opp_move == 'A' and my_move_std == 'B':
            outcome_score = 6
        elif opp_move == 'B' and my_move_std == 'C':
            outcome_score = 6
        elif opp_move == 'C' and my_move_std == 'A':
            outcome_score = 6
    
    return shape_score + outcome_score
#------------------------------------------------------------------------------
def win_rps(opp_play) -> str:
    if opp_play == 'A':
        return 'B'
    elif opp_play == 'B':
        return 'C'
    elif opp_play == 'C':
        return 'A'
#------------------------------------------------------------------------------
def lose_rps(opp_play) -> str:
    if opp_play == 'A':
        return 'C'
    elif opp_play == 'B':
        return 'A'
    elif opp_play == 'C':
        return 'B'
#------------------------------------------------------------------------------
def draw_rps(opp_play) -> str:
    return opp_play

#------------------------------------------------------------------------------



file_list = os.listdir()
for i in range(0, len(file_list)):
    print("{}\t{}".format(i, file_list[i]))

try:
    fname = file_list[int(input("Line Number: "))]
except IndexError or ValueError:
    fname = "game.txt"

f = open(fname, 'r')

scores = []
for line in f:
    scores.append(decode_score(line))

total_score = sum(scores)
print("My total score should be {}.".format(total_score))

f.close()

f = open(fname, 'r')

scores = []
for line in f:
    move_outcome = line.strip().split(' ')

    our_play_std = ''

    if move_outcome[1] == 'X':
        # we must LOSE
        our_play_std = lose_rps(move_outcome[0])
    elif move_outcome[1] == 'Y':
        # we  must DRAW
        our_play_std = draw_rps(move_outcome[0])
    elif move_outcome[1] == 'Z':
        # we must WIN
        our_play_std = win_rps(move_outcome[0])
    
    if our_play_std == 'A':
        our_play = 'X'
    elif our_play_std == 'B':
        our_play = 'Y'
    else:
        our_play = 'Z'
    
    actual_round = "{} {}".format(move_outcome[0], our_play)
    
    scores.append(decode_score(actual_round))

total_score = sum(scores)
print("Using the CORRECT method, my total score will be {}.".format(total_score))

f.close()
