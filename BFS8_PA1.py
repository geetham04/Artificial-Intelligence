# GEETHA MADHURI CHITTULURI
# ARTIFICIAL INTELLIGENCE PA#1

import random
import math

max_moves = 10000

goal_state = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, 0]]


class EightPuzzle:
    def __init__(self):
        # heuristic value
        self.hscore = 0
        # no. of nodes traversed from start node to get to the current node in search path
        self.gscore = 0
        # parent node
        self._parent = None
        self.adjacent_matrix = []
        for i in range(3):
            self.adjacent_matrix.append(goal_state[i][:])

    def _duplicate(self):
        puz = EightPuzzle()
        for i in range(3):
            puz.adjacent_matrix[i] = self.adjacent_matrix[i][:]
        return puz

    def get_possible_moves(self):
        # generates and return a list
        # get row and column of the empty block
        row, col = self.find(0)
        freespace = []

        # find which block can move there
        if row > 0:
            freespace.append((row - 1, col))
        if col > 0:
            freespace.append((row, col - 1))
        if row < 2:
            freespace.append((row + 1, col))
        if col < 2:
            freespace.append((row, col + 1))

        return freespace

    def set(self, other) :
        i = 0
        for row in range(3):
            for col in range(3):
                self.adjacent_matrix[row][col] = int(other[i])
                i = i+1

    def generate_moves(self):
        freespace = self.get_possible_moves()
        zero = self.find(0)

        def swap_and_duplicate(a, b):
            p = self._duplicate()
            p.swap(a,b)
            p.gscore = self.gscore + 1
            p._parent = self
            return p

        return map(lambda pair: swap_and_duplicate(zero, pair), freespace)

    def generate_solution_path(self, path):
        if self._parent == None:
            return path
        else:
            path.append(self)
            return self._parent.generate_solution_path(path)

    def stepcount_to_solve(self, h):
        def is_solved(puzzle):
            return puzzle.adjacent_matrix == goal_state

        openList = [self]
        closedList = []
        move_count = 0
        while len(openList) > 0:
            m = openList.pop(0)
            move_count += 1
            if((move_count > max_moves) & (~(is_solved(m)))):
                return [], move_count

            if (is_solved(m)):
                if len(closedList) > 0:
                    return m.generate_solution_path([]), move_count
                else:
                    return [m]

            succsr = m.generate_moves()
            idm_open = idm_closed = -1
            for move in succsr:
                idm_open = index(move, openList)
                idm_closed = index(move, closedList)
                hval = h(move)
                fscore = hval

                if idm_closed == -1 and idm_open == -1:
                    move.hscore = hval
                    openList.append(move)
                elif idm_open > -1:
                    copy = openList[idm_open]
                    if fscore < copy.hscore:
                        copy.hscore = hval
                        copy._parent = move._parent
                elif idm_closed > -1:
                    copy = closedList[idm_closed]
                    if fscore < copy.hscore:
                        move.hscore = hval
                        closedList.remove(copy)
                        openList.append(move)

            closedList.append(m)
            openList = sorted(openList, key=lambda p: p.hscore)
            
        return [], 0

    def randomshuffle(self, step_count):
        #shuffles the goal state using random.choice
        for i in range(step_count):
            row, col = self.find(0)
            freespace = self.get_possible_moves()
            target = random.choice(freespace)
            self.swap((row, col), target)
            row, col = target

    def find(self, value):
        #find and return the row, column coordinates
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.adjacent_matrix[row][col] == value:
                    return row, col

    def get_value(self, row, col):
        return self.adjacent_matrix[row][col]

    def set_value(self, row, col, value):
        self.adjacent_matrix[row][col] = value

    def swap(self, pos_a, pos_b):
        temp = self.get_value(*pos_a)
        self.set_value(pos_a[0], pos_a[1], self.get_value(*pos_b))
        self.set_value(pos_b[0], pos_b[1], temp)

def index(item, seq):
    try:
        return seq.index(item)
    except:
        return -1

def heur_value(puzzle, item_total, total_calc):

    #value of the heuristic function
    #item_total - with 4 parameters: current row, target row, current column, target column.
    #total_calc - with 1 parameter, the sum of item_total over all entries.

    tar = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.get_value(row, col) - 1
            target_col = val % 3
            target_row = val / 3

            if target_row < 0:
                target_row = 2

            tar += item_total(row, target_row, col, target_col)

    return total_calc(tar)

def manhattan_distance(puzzle):
    return heur_value(puzzle,
                lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t : t)

def euclidean_distance(puzzle):
    return heur_value(puzzle,
                lambda r, tr, c, tc: math.sqrt(math.sqrt((tr - r)**2 + (tc - c)**2)),
                lambda t: t)

def misplaced_tiles(puzzle):
    count=0
    for row in range(3):
        for col in range(3):
            if puzzle.get_value(row,col) != goal_state[row][col]:
                count+=1
                if puzzle.get_value(row,col)==0:
                    if goal_state[row][col]!=0:
                        count-=1

    return count


def main():
    total_steps_count = 0
    # writes to misplaced_tiles_bfs.txt
    with open('misplaced_tiles_bfs8.txt','w') as out_file:
        out_file.write("Best First Search\n")
        out_file.write("Misplaced tiles\n\n")
        for i in range(5):
            p = EightPuzzle()
            p.randomshuffle(15)
            out_file.write(str(i+1) + "Iteration")
            out_file.write(" Eight Puzzle: \n")
            for row in range(3):
                for col in range(3):
                    out_file.write(str(p.get_value(row,col)) + " ")
                out_file.write("\n")
            out_file.write("-------------\n")
            path, count = p.stepcount_to_solve(misplaced_tiles)
            path.reverse()
            for mat in path:
                for row in range(3):
                    for col in range(3):
                        out_file.write(str(mat.get_value(row,col)) + " ")
                    out_file.write("\n")
                out_file.write("\n")
            total_steps_count = total_steps_count + count
            out_file.write("For " + str(i+1) + " Iteration " + "steps count to solve puzzle: " + str(count) + "\n\n")
            if ((count > max_moves) & (path == [])):
                out_file.write("Puzzle is not solved in 10000 steps\n\n")
            print("total count",total_steps_count)
        out_file.write("Average number of steps for 5 iterations:" + str(total_steps_count/5)+"\n\n")

if __name__ == "__main__":
    main()
