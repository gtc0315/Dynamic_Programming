import numpy as np


class TicTacToe:
    def __init__(self, cost_win=-1, cost_lose=1, cost_tie=0, i_first=True):
        self.player_value = np.array([0, 1, 2])  # [free, i, opponent]
        self.win_states = np.array(
            [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]])
        self.state_space = self.__create_state_space()
        self.state_space_size = np.shape(self.state_space)[0]
        self.T = 9
        self.value = [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
        self.policy = [{}, {}, {}, {}, {}, {}, {}, {}, {}]
        self.cost_win = cost_win
        self.cost_lose = cost_lose
        self.cost_tie = cost_tie
        self.cost_invalid_state = 999
        self.cost_each_move = 0.001
        self.i_first = i_first

    def __create_state_space(self):
        x_space = []
        for x0 in self.player_value:
            for x1 in self.player_value:
                for x2 in self.player_value:
                    for x3 in self.player_value:
                        for x4 in self.player_value:
                            for x5 in self.player_value:
                                for x6 in self.player_value:
                                    for x7 in self.player_value:
                                        for x8 in self.player_value:
                                            x_space.append([x0, x1, x2, x3, x4, x5, x6, x7, x8])
        return np.array(x_space)

    def cost(self, state, move=-1):
        # unbalanced moves (invalid)
        if np.abs(len(np.where(state == 1)[0]) - len(np.where(state == 2)[0])) > 1:
            return self.cost_invalid_state

        i_win = 0
        opponent_win = 0
        for states in self.win_states:
            if state[states[0]] == self.player_value[1] and state[states[1]] == self.player_value[1] and \
                            state[states[2]] == self.player_value[1]:
                i_win += 1  # I win
            if state[states[0]] == self.player_value[2] and state[states[1]] == self.player_value[2] and \
                            state[states[2]] == self.player_value[2]:
                opponent_win += 1  # opponent wins

        if i_win + opponent_win > 1:  # invalid state (more than one win)
            return self.cost_invalid_state
        else:  # zero/one win
            if i_win == 1:  # I win
                return self.cost_win
            elif opponent_win == 1:  # opponent win
                return self.cost_lose
            else:  # no one win
                if 0 not in state:  # horizon
                    return self.cost_tie  # tie
                else:
                    if move >= 0 and state[move] != 0:  # play on occupied cell
                        return self.cost_invalid_state
                    else:
                        return self.cost_each_move

    def my_turn(self, state, u):
        new_state = [i for i in state]
        new_state[u] = 1
        return np.array(new_state)

    def opponent_turn(self, state, w=-1):
        if w == -1:  # random move on a free cell
            available_state = np.where(state == 0)[0]
            w = available_state[np.random.randint(0, len(available_state))]
        new_state = [i for i in state]
        new_state[w] = 2
        return np.array(new_state)

    def __dp_helper(self, x, u, t):
        # calculate the expected loss
        if self.i_first:
            x_next = self.my_turn(x, u)  # my turn
            available_state = np.where(x_next == 0)[0]
            n = len(available_state)
            expectation = 0.0
            for w in available_state:
                expectation += 1.0 / n * self.value[t][str(self.opponent_turn(x_next, w).tolist())]  # opponent turn
            return expectation
        else:
            available_state = np.where(x == 0)[0]
            n = len(available_state)
            expectation = 0.0
            for w in available_state:
                expectation += 1.0 / n * self.value[t][
                    str(self.my_turn(self.opponent_turn(x, w), u).tolist())]  # opponent turn then my turn
            return expectation

    def dynamic_programming(self):
        print 'dynamic programming...'
        for i in range(self.state_space_size):
            self.value[self.T][str(self.state_space[i].tolist())] = self.cost(self.state_space[i])
        for t in range(self.T - 1, -1, -1):
            print 't=' + str(t)
            Q = np.zeros((self.state_space_size, 9))
            for i in range(self.state_space_size):  # for all x in X
                for u in range(9):  # for all u in U
                    Q[i, u] = self.cost(self.state_space[i], u) + self.__dp_helper(self.state_space[i], u, t + 1)
            for i in range(self.state_space_size):
                self.value[t][str(self.state_space[i].tolist())] = np.amin(Q[i, :])
                self.policy[t][str(self.state_space[i].tolist())] = np.argmin(Q[i, :])

    def game_over(self, state):
        # check if the game is over
        score = self.cost(state)
        if score == self.cost_win:
            return np.array([1, 0, 0], dtype=np.float32)  # i win
        elif score == self.cost_lose:
            return np.array([0, 1, 0], dtype=np.float32)  # i lose
        elif score == self.cost_tie:
            return np.array([0, 0, 1], dtype=np.float32)  # tie
        else:
            return np.array([0, 0, 0], dtype=np.float32)  # game is not over yet

    def visualize(self, state):
        # visualize in 3x3 grid
        state_str = []
        for i in range(9):
            if state[i] == self.player_value[0]:
                state_str.append(' ')
            elif state[i] == self.player_value[1]:
                state_str.append('O')
            else:
                state_str.append('X')
        print '|'.join(state_str[0:3])
        print '|'.join(state_str[3:6])
        print '|'.join(state_str[6:9])
        print '\n'

    def probability_win(self, x, t):
        # find the count of all win, lose, tie using recursion
        check = self.game_over(x)
        if not np.array_equal(check, np.array([0, 0, 0], dtype=np.float32)):
            return check  # game ends
        else:
            if self.i_first:
                odd_even = 0
            else:
                odd_even = 1

            if t % 2 == odd_even:  # my turn
                return self.probability_win(self.my_turn(x, self.policy[t][str(x.tolist())]), t + 1)
            else:
                cnt = np.array([0, 0, 0], dtype=np.float32)
                available_state = np.where(x == 0)[0]
                for w in available_state:
                    cnt += 1.0 / len(available_state) * self.probability_win(self.opponent_turn(x, w), t + 1)
                return cnt

    def simulation(self, visual=False):
        x = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        if self.i_first:
            odd_even = 0
        else:
            odd_even = 1

        for t in range(self.T):
            if t % 2 == odd_even:
                x = self.my_turn(x, self.policy[t][str(x.tolist())])  # optimal policy
            else:
                x = self.opponent_turn(x)  # random pick
            check_point = self.game_over(x)
            if visual:
                self.visualize(x)
            if not np.array_equal(check_point, np.array([0, 0, 0], dtype=np.float32)):
                return check_point
