import queue
import copy


class State:
    def __init__(self, board, pairs, count, moves=0):
        self.board = board
        self.pairs = pairs
        self.count = count
        self.moves = moves

    def get_new_Board(self, x, y, moves):
        board = copy.copy(self.board)
        board[x][y] = 1
        pairs = self.pairs.copy()
        pairs.append([x,y])
        return State(board, pairs, self.count-1, moves)

    def expand(self, moves):
        result = []
        impossible_line = []
        impossible_low = []
        for i in range(8):
            if 1 in self.board[i]:
                impossible_line.append(i)
                impossible_low.append(self.board[i].index(1))
                continue
        for i in range(8):
            if i in impossible_line:
                continue
            for j in range(8):
                if j in impossible_low:
                    continue
                result.append(self.get_new_Board(i,j,moves))
        return result

    def f(self):
        return self.h() + self.g()

    def h(self):
        for i in range(len(self.pairs)):
            for j in range(len(self.pairs[i:])):
                sub = [self.pairs[i][0] - self.pairs[i+j][0],self.pairs[i][1] - self.pairs[i+j][1]]
                if abs(sub[0]) != abs(sub[1]):
                    return float("inf")
        return self.count

    def g(self):
        return self.moves

    def __lt__(self, other):
        return self.f() < other.f()

    def __str__(self):
        return "------------------ f(n)=" + str(self.f()) +"\n"+\
                "------------------ h(n)=" + str(self.h()) +"\n"+\
                "------------------ g(n)=" + str(self.g()) +"\n"+\
            str(self.board[0]) +"\n"+\
            str(self.board[1]) +"\n"+\
            str(self.board[2]) +"\n"+\
            str(self.board[3]) +"\n"+\
            str(self.board[4]) +"\n"+\
            str(self.board[5]) +"\n"+\
            str(self.board[6]) +"\n"+\
            str(self.board[7]) +"\n"+\
            "-----------------------"

count = 8
moves = 0
open_queue = queue.PriorityQueue()
open_queue.put(State([[0 for _ in range(8)] for _ in range(8)], [], count))

closed_queue = []

while open_queue:
    current = open_queue.get()
    print(current)
    if (current.count == 0):
        print("탐색성공")
        break
    moves = current.moves + 1
    for state in current.expand(moves):
        if state not in closed_queue:
            open_queue.put(state)
        closed_queue.append(current)
