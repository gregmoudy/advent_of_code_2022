# --- Day 2: Rock Paper Scissors ---
# The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already in progress.

# Rock Paper Scissors is a game between two players. 
# Each game contains many rounds; in each round, the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape. 
# Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape, the round instead ends in a draw.

# Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. 
# "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

# The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. 
# Winning every time would be suspicious, so the responses must have been carefully chosen.

# The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. 
# The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) 
# plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

# Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

# For example, suppose you were given the following strategy guide:

# A Y
# B X
# C Z
# This strategy guide predicts and recommends the following:

# In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
# In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
# The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
# In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

# What would your total score be if everything goes exactly according to your strategy guide?

# --- Part Two ---
# The Elf finishes helping with the tent and sneaks back over to you. 
# "Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

# The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated. The example above now goes like this:

# In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
# In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
# In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.
# Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

# Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?


import timeit

MOVE_P1_ROCK = 'A'
MOVE_P1_PAPER = 'B'
MOVE_P1_SCISSORS = 'C'

MOVE_P2_ROCK = 'X'
MOVE_P2_PAPER = 'Y'
MOVE_P2_SCISSORS = 'Z'

SCORE_ROCK = 1
SCORE_PAPER = 2
SCORE_SCISSORS = 3

SCORE_RANKINGS = [SCORE_ROCK, SCORE_PAPER, SCORE_SCISSORS]

SCORE_PER_MOVE = {
    MOVE_P1_ROCK : SCORE_ROCK, MOVE_P1_PAPER : SCORE_PAPER, MOVE_P1_SCISSORS : SCORE_SCISSORS,
    MOVE_P2_ROCK : SCORE_ROCK, MOVE_P2_PAPER : SCORE_PAPER, MOVE_P2_SCISSORS : SCORE_SCISSORS,
}

SCORE_DRAW = 3
SCORE_WIN = 6

GUIDE_P2_OUTCOME_LOSE = 1
GUIDE_P2_OUTCOME_DRAW = 2
GUIDE_P2_OUTCOME_WIN = 3



def read_input():
    with open('./day_02_input.txt', 'r') as file:
        lines = file.read().splitlines()
    
    moves = [tuple(x.split(' ')) for x in lines]

    return moves



def get_scores_per_moves(moves):
    # I convert all the ABC/XYZ characters in the move/guide list to their int score values and can still infer what they mean.
    # This simplifies things from the get go instead of having to do this conversion later.
    scores_per_moves = list()
    for p1_move, p2_move in moves:
        scores_per_move = (SCORE_PER_MOVE.get(p1_move), SCORE_PER_MOVE.get(p2_move))
        scores_per_moves.append(scores_per_move)

    return scores_per_moves



def get_complete_game_scores(scores_per_move, use_game_guide=False):
    p1_score_total = 0
    p2_score_total = 0

    for p1_move_score, p2_move_score in scores_per_move:
        # Use the game guide guidelines for Part 2.
        if use_game_guide:
            if p2_move_score == GUIDE_P2_OUTCOME_LOSE:
                # Look at the previous score value in the rankings to see what P2 would lose against.
                p2_move_score = SCORE_RANKINGS[p1_move_score - 1 - 1]

            elif p2_move_score == GUIDE_P2_OUTCOME_WIN:
                # Look at the next score value in the rankings to see what P2 would win against.
                p2_move_score = SCORE_RANKINGS[(p1_move_score - 1 + 1) % len(SCORE_RANKINGS)] # The % here allows us to wrap around moving forward through the list without causing an index error.

            elif p2_move_score == GUIDE_P2_OUTCOME_DRAW:
                # Copy P1's move to result in a draw.
                p2_move_score = p1_move_score

        # Each player gets the point value for their move.
        p1_score_total += p1_move_score
        p2_score_total += p2_move_score

        # DRAW
        if p1_move_score == p2_move_score:
            p1_score_total += SCORE_DRAW
            p2_score_total += SCORE_DRAW

        else:
            # Look at the previous score value in the rankings to see what P1 would win against.
            move_score_win_against = SCORE_RANKINGS[p1_move_score - 1 - 1]

            # WIN
            if p2_move_score == move_score_win_against:
                p1_score_total += SCORE_WIN

            # LOSS
            else:
                p2_score_total += SCORE_WIN

    return p1_score_total, p2_score_total



def run():
    moves = read_input()
    scores_per_move = get_scores_per_moves(moves)

    print('DAY 02')

    # Part 1 Answer
    _p1_score_total, p2_score_total = get_complete_game_scores(scores_per_move) # 10933, 14297
    print(f'What would your total score be if everything goes exactly according to your strategy guide? : {p2_score_total}') # 14297

    # Part 2 Answer
    _p1_score_total, p2_score_total = get_complete_game_scores(scores_per_move, use_game_guide=True) # 15022, 10498
    print(f"Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide? : {p2_score_total}") # 10498



if __name__ == '__main__':
    start_time = timeit.default_timer()
    run()
    print('Runtime: {} seconds.'.format(round(timeit.default_timer() - start_time, 5)))
