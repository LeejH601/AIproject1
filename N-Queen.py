import queue
import copy


class State:
    def __init__(self, board, pairs, count, moves=0):
        self.board = board
        self.pairs = pairs
        self.count = count
        self.moves = moves

    def get_new_Board(self, x, y, moves):
        board = copy.deepcopy(self.board)
        board[x][y] = 1
        pairs = copy.deepcopy(self.pairs)
        pairs.append([x,y])
        return State(board, pairs, self.count-1, moves)

    def expand(self, moves):
        result = []
        impossible_line = []
        impossible_low = []
        for i in range(len(self.board)):
            if 1 in self.board[i]:
                impossible_line.append(i)
                impossible_low.append(self.board[i].index(1))
                continue
        for i in range(len(self.board)):
            if i in impossible_line:
                continue
            for j in range(len(self.board)):
                if j in impossible_low:
                    continue
                loopflag = True
                for pair in self.pairs:
                    if abs(i - pair[0]) == abs(j - pair[1]):
                        loopflag = False
                if loopflag:
                    result.append(self.get_new_Board(i,j,moves))
        return result

    def f(self):
        return self.h() + self.g()

    def h(self):
        # for i in range(len(self.pairs)):
        #     for j in range(len(self.pairs[i:])):
        #         sub = [self.pairs[i][0] - self.pairs[i+j][0],self.pairs[i][1] - self.pairs[i+j][1]]
        #         if sub[0] != sub[1]:
        #             return float('inf')
        # for pair1 in self.pairs:
        #     for pair2 in self.pairs:
        #         if pair1 != pair2:
        #             if abs(pair1[0] - pair2[0]) == abs(pair1[1] - pair2[1]):
        #                 return float('inf')
        return self.count

    def g(self):
        return self.moves

    def __lt__(self, other):
        return self.f() < other.f()

    def __str__(self):
        text = "------------------ f(n)=" + str(self.f()) +"\n"+\
                "------------------ h(n)=" + str(self.h()) +"\n"+\
                "------------------ g(n)=" + str(self.g()) +"\n"

        for line in self.board:
            text = text + str(line) + '\n'

        text = text + "-----------------------"

        return text




count = int( input())
moves = 0

open_queue = queue.PriorityQueue()
open_queue.put(State([[0 for _ in range(int(count))] for _ in range(int(count))], [], int(count)))

closed_queue = []

while open_queue:
    current = open_queue.get()
    # print(current)
    if (current.count == 0):
        print(current)
        print("탐색성공")
        break
    moves = current.moves + 1
    for state in current.expand(moves):
        for state2 in closed_queue:
            if state2.board == state.board:
                continue
        open_queue.put(state)
    closed_queue.append(current)
    board = copy.deepcopy(current.board)
    for _ in range(3):
        new_board = [[0 for _ in range(count)] for _ in range(count)]
        pairs = []
        for pair in current.pairs:
            new_board[(count-1) - pair[1]][pair[0]] = 1
            pairs.append([(count-1) - pair[1], pair[0]])
        closed_queue.append(State(new_board,pairs,current.count,moves))
