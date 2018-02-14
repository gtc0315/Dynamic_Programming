import numpy as np
import argparse
from TicTacToe import TicTacToe

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tic Tac Toe')
    parser.add_argument('input_file', type=str, default=None, help='name for the input file.')
    parser.add_argument('output_file', type=str, default=None, help='name for the output file.')
    args = parser.parse_args()
    output_file = args.output_file

    # train TTT with dynamic programming (don't care lose, I first)
    game1 = TicTacToe(cost_win=-1, cost_lose=0, cost_tie=0, i_first=True)
    game1.dynamic_programming()

    # train TTT with dynamic programming (care lose, I first)
    game2 = TicTacToe(cost_win=-1, cost_lose=1, cost_tie=0, i_first=True)
    game2.dynamic_programming()

    # train TTT with dynamic programming (don't care lose, opponent first)
    game3 = TicTacToe(cost_win=-1, cost_lose=0, cost_tie=0, i_first=False)
    game3.dynamic_programming()

    # train TTT with dynamic programming (care lose, opponent first)
    game4 = TicTacToe(cost_win=-1, cost_lose=1, cost_tie=0, i_first=False)
    game4.dynamic_programming()

    games = [game1, game2, game3, game4]

    x0 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])

    # probability of winning
    print 'Calculating probability of winning...'
    prob = []
    for i in range(4):
        statistics = games[i].probability_win(x0, 0)  # [win, lose, tie]
        # print statistics[0] / np.sum(statistics), statistics
        if i % 2 == 0:
            prob.append(statistics[0] / np.sum(statistics))  # maximum probability of winning
        else:
            prob.append(
                (statistics[0] - statistics[1]) / np.sum(statistics))  # maximum probability of winning minus losing

    # simulation
    print 'Simulating...'
    simu = []
    iter = 10000
    for i in range(4):
        statistics = np.array([0, 0, 0], dtype=np.float32)
        for _ in range(iter):
            statistics += games[i].simulation(visual=False)  # [win, lose, tie]
        # print statistics[0] / np.sum(statistics), statistics
        if i % 2 == 0:
            simu.append(statistics[0] / np.sum(statistics))
        else:
            simu.append((statistics[0] - statistics[1]) / np.sum(statistics))

    # write output file
    print 'Writing to output file...'
    with open(output_file, "w") as ot:
        for i in range(4):
            ot.write("{:.5f} {:.5f}\n".format(prob[i], simu[i]))

    # visualize my first move
    if True:
        print 'Visualizing...'
        for i in range(2):
            print 'game' + str(i)
            state = games[i].my_turn(x0, games[i].policy[0][str(x0.tolist())])
            games[i].visualize(state)
        for i in range(2, 4):
            print 'game' + str(i)
            for w in range(9):
                state = games[i].opponent_turn(x0, w)
                state = games[i].my_turn(state, games[i].policy[1][str(state.tolist())])
                games[i].visualize(state)
