import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If number of cells equals count, all cells are mines
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If number of cells equals 0, all cells are safe
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Check if cell is in the sentence
        if cell in self.cells:
            # Since cell is a mine, remove it from the set and decrease the count of mines by 1
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Check if cell is in the sentence
        if cell in self.cells:
            # Since cell is a mine, remove it from the set and decrease the count of mines by 1
            # Since cell is not a mine, remove it from the set and DO NOT decrease the count of mines by 1
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # Mark cell as move that has been made
        self.moves_made.add(cell)

        # Mark cell as safe
        self.safes.add(cell)

        # Add new sentence to knowledge base
        # Get all neighbors of cell
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # If cell is in bounds
                if i >= 0 and j >= 0 and i < self.height and j < self.width:
                    # If cell is not already a move that has been made or a mine, add it to neighbors
                    if (i, j) not in self.moves_made and (i, j) not in self.mines:
                        neighbors.add((i, j))
                    # If cell is a mine, decrease count by 1
                    if (i, j) in self.mines:
                        count -= 1

        # Add new sentence to knowledge base
        self.knowledge.append(Sentence(neighbors, count))

        # Mark additional cells as safe or mines
        # Iterate through sentences
        for sentence in self.knowledge:
            # For each safe cell in the sentence, mark it as safe
            if not sentence.known_safes() is None:
                for safe_cell in list(sentence.known_safes()):
                    self.mark_safe(safe_cell)
            # For each mine in the sentence, mark it as a mine
            if not sentence.known_mines() is None:
                for mine_cell in list(sentence.known_mines()):
                    self.mark_mine(mine_cell)

        # Add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge based on subset method

        # Create list to hold new sentences
        new_sentences = []

        # Iterate through sentences
        for super_sentence in self.knowledge:
            # Iterate through sentences again
            for sub_sentence in self.knowledge:
                # Check if sub_sentence is a subset of super_sentence
                if sub_sentence.cells.issubset(super_sentence.cells):
                    # Create a new sentence with the difference of the two sentences
                    new_sentence = Sentence(
                        super_sentence.cells - sub_sentence.cells,
                        super_sentence.count - sub_sentence.count,
                    )
                    # Check if new sentence is not already in knowledge base
                    if new_sentence not in self.knowledge:
                        # Add new sentence to knowledge base
                        new_sentences.append(new_sentence)

        # Add new sentences to knowledge base
        self.knowledge.extend(new_sentences)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Create a copy of list of safe cells
        safe_list = list(self.safes)

        # Iterate through list of safe cells
        for i in range(len(safe_list)):
            # If cell is not already a move that has been made, return it
            safe_cell = list(safe_list)[i]
            if safe_cell not in self.moves_made:
                return safe_cell

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        possible_moves = set()
        # Iterate through all cells
        for i in range(self.height):
            for j in range(self.width):
                # If cell is not already a move that has been made or a known mine, add it to possible moves
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves.add((i, j))

        # If there are no possible moves, return None
        if len(possible_moves) == 0:
            return None
        else:
            # Otherwise, return a random move
            return random.choice(list(possible_moves))
