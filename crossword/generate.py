import sys

from crossword import *



class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            length = variable.length
            for i in self.domains[variable].copy():
                if len(i) != length:
                    self.domains[variable].remove(i)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revise = False
        overlap = self.crossword.overlaps[x, y]
        if overlap != None:
            for i in self.domains[x].copy(): 
                satisfied = False
                for j in self.domains[y].copy():
                    if i[overlap[0]] == j[overlap[1]]:
                        satisfied = True
                if satisfied == False:
                    self.domains[x].remove(i)
                    revise = True
        return revise

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # creates a queue of arcs to process
        queue = list()
        if arcs == None:
            for i in self.domains:
                for j in self.crossword.neighbors(i):
                    if (i, j) not in queue and i != j:
                        queue.append((i, j))
        else:
            for arc in arcs:
                queue.append(arc)

        # actual ac3 stuff
        while len(queue) != 0:
            (x, y) = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if x != y:
                        queue.append((z, x))


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.domains:
            if variable not in assignment.keys():
                return False
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # list of values to check for uniqueness
        values = list()

        # iterates of assignment
        for variable in assignment:

            # checks that value is distinct
            if assignment[variable] in values:
                return False
            values.append(assignment[variable])

            # checks that value is correct length
            length = variable.length
            if len(assignment[variable]) != length:
                return False

            # checks for conflicts between neighboring variables
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[variable, neighbor]
                    i = assignment[variable]
                    j = assignment[neighbor]
                    if i[overlap[0]] != j[overlap[1]]:
                        return False

        return True
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = list(self.domains[var].copy())
        values.sort(key = lambda value: self.num_values(value, var, assignment))
        return values
        
    def num_values(self, value, var, assignment):
        """
        Returns the number of times a value is present in neighboring
        variables; returns the number of neighboring values a value would rule 
        out. 
        Helper function for order_domain_values.
        """
        counter = 0
        for neighbor in self.crossword.neighbors(var):
            if neighbor not in assignment:
                overlap = self.crossword.overlaps[var, neighbor]
                if overlap != None:
                    for v in self.domains[neighbor]:
                        if value[overlap[0]] != v[overlap[1]]:
                            counter += 1
        return counter


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = list(self.domains - assignment.keys())
        unassigned.sort(key = lambda variable: len(self.domains[variable]))
        least = len(self.domains[unassigned[0]])
        
        # finds variables with least remaining values
        minimum = list()
        for x in unassigned:
            if len(self.domains[x]) == least:
                minimum.append(x)

        # if theres a tie, sort by degree
        if len(minimum) != 1:
            highest = 0
            placeholder = None
            for value in minimum:
                neighbors = self.crossword.neighbors(value)
                if len(neighbors) > highest:
                    highest = len(self.crossword.neighbors(value))
                    placeholder = value
            return placeholder
        else:
            return minimum[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        values = self.order_domain_values(var, assignment)
        for value in values:
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
            assignment.pop(var)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
