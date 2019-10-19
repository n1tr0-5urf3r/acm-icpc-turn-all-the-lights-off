# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt


class Board:
    def __init__(self, row, solving_path="", matrix=None):
        self.row = row
        self.col = row
        self.solving_path = solving_path

        if matrix is not None:
            self.matrix = matrix
        else:
            self.matrix = np.zeros((self.row, self.col))

    def __deepcopy__(self):
        """Creates a new object as deepcopy"""
        new_mat = np.copy(self.matrix)
        b = Board(self.row, self.solving_path, new_mat)
        return b

    def plot(self):
        """Plots a given matrix as grid"""
        plt.figure(1, figsize=(self.row, self.col))
        tb = plt.table(cellText=self.matrix, loc=(0, 0), cellLoc='center')

        tc = tb.properties()['child_artists']
        for cell in tc:
            cell.set_height(1.0 / self.row)
            cell.set_width(1.0 / self.col)
        ax = plt.gca()
        ax.set_xticks([])
        ax.set_yticks([])
        plt.show()

    def invert(self, row_index, col_index):
        """Inverts state of a given room"""
        if self.matrix[row_index, col_index]:
            self.matrix[row_index, col_index] = False
        else:
            self.matrix[row_index, col_index] = True

    def push_button(self, row_index, col_index):
        """Pushes a button and invertes state of the room and all adjacent rooms"""
        self.invert(row_index, col_index)
        self.invert(row_index - 1, col_index)
        self.invert(row_index, col_index - 1)
        if row_index + 1 == self.row:
            self.invert(0, col_index)
        else:
            self.invert(row_index + 1, col_index)
        if col_index + 1 == self.col:
            self.invert(row_index, 0)
        else:
            self.invert(row_index, col_index + 1)

    def won(self):
        """Checks if all lights are turned off"""
        for i in range(self.row):
            for j in range(self.col):
                if self.matrix[i][j] != 0:
                    return False
        return True


class Solver:
    def __init__(self, board):
        self.boards = [board]
        self.known_configs = [hash(str(board.matrix))]
        self.found_solutions = []

    def solve(self):
        """
        Checks if the given Board is solvable, keeps track of possible solutions
        :return:
        """
        counter = 0
        while self.boards:
            new_boards = []
            # print("Iteration {}".format(counter))
            for b in self.boards:
                if b.won():
                    self.found_solutions.append(b.solving_path)
                    print(b.solving_path)
                    return True
                else:
                    for i in range(b.row):
                        for j in range(b.col):
                            new_board = b.__deepcopy__()
                            path = "({}|{}), ".format(i, j)
                            new_board.solving_path += path
                            new_board.push_button(i, j)
                            # print("{} {}".format(new_board.matrix, new_board.solving_path))
                            new_hash = hash(str(new_board.matrix))
                            if new_board.won():
                                self.found_solutions.append(new_board.solving_path)
                                print(new_board.solving_path)
                                return True
                            if new_hash not in self.known_configs:
                                self.known_configs.append(new_hash)
                                new_boards.append(new_board)
                self.boards = new_boards

            counter += 1
        if len(self.found_solutions) == 0:
            return False
        print("Found {} solutions!".format(len(self.found_solutions)))
        print(self.found_solutions)


def main():
    def read_input(file):
        """
        Reads from an input file and creates the boards
        :param file:
        :return:
        """
        def set_lights(ls, board):
            """
            Sets lights on a board according to a given list
            :param ls:
            :param board:
            :return:
            """
            for l in ls:
                string = l.split()
                row = int(string[0])
                col = int(string[1])
                board.matrix[row, col] = 1

        file_object = open(file, "r")
        in_string = file_object.readlines()
        in_string = [sub.replace("\n", "") for sub in in_string]
        boards = []
        counter = 0
        while counter < len(in_string):
            size = in_string[counter]
            amount_lights = in_string[counter + 1]
            lights = in_string[counter + 2:int(amount_lights) + counter + 2]
            b = Board(int(size))
            set_lights(lights, b)
            boards.append(b)
            counter += int(amount_lights) + 2
        return boards

    boards = read_input("h.in")
    for b in boards:
        print(b.matrix)
        solver = Solver(b)
        print(solver.solve())


if __name__ == '__main__':
    main()
