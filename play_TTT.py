from TicTacToe import TicTacToe
import pickle
import numpy as np


if __name__ == '__main__':
    with open('TicTacToe', 'rb') as TTT:
        games = pickle.load(TTT)
    x = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
    player_first = input("Do you want to play first? you->X, computer->O\n(True/False)")
    if player_first: # computer second
        game = games[3]
        odd_even = 1
    else: # computer first
        game = games[1]
        odd_even = 0
    game.visualize(x)
    for t in range(game.T):
        if t % 2 == odd_even:
            x = game.my_turn(x, game.policy[t][str(x)])
            game.visualize(x)
        else:
            w = input("your move (1-9)")
            x = game.opponent_turn(x, w-1)
        check_point = game.game_over(x)

        if not np.array_equal(check_point, np.array([0, 0, 0], dtype=np.float32)):
            game.visualize(x)
            if np.array_equal(check_point, np.array([1,0,0], dtype=np.float32)):
                print 'you lose'
            elif np.array_equal(check_point, np.array([0,1,0], dtype=np.float32)):
                print 'you win'
            elif np.array_equal(check_point, np.array([0, 0, 1], dtype=np.float32)):
                print 'you tie'
            break
