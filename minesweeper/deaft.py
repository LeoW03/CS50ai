        neighbors = []
        i, j = cell
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and i == 0: # skips itself
                    continue
                elif ((i + x), (j + y)) in self.mines or ((i + x), (j + y)) in self.safes: # checks if cell is already known
                    continue
                elif (i + x) > (self.height - 1) or (i + x) < 0 or (j + y) > (self.width - 1) or (j + y) < 0: # checks for boarder
                    continue
                else:
                    neighbors.append(((i + x), (j + y)))
        self.knowledge.append(Sentence(cells=neighbors, count=count))
