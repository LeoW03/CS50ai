from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(

    # Structure
    Or(AKnight, AKnave), # A is a Knight or a Knave
    Not(And(AKnight, AKnave)), # But not both

    # Puzzle
    Biconditional(AKnight, And(AKnave, AKnight)) # A is a Knight if A is both Knave and Knight
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    # Structure
    Or(AKnight, AKnave), # A is a Knight or a Knave
    Implication(AKnight, Not(AKnave)), # If A is a Knight, A is not a Knave
    Or(BKnight, BKnave), # B is a Knight or a Knave
    Implication(BKnave, Not(BKnight)), # If B is a Knave, B is not a Knight

    # Puzzle
    Biconditional(AKnight, And(AKnave, BKnave)) # A is a Knight if A and B are both Knaves
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    # Structure
    Or(AKnight, AKnave), # A is a Knight or a Knave
    Implication(AKnight, Not(AKnave)), # If A is a Knight, A is not a Knave
    Or(BKnight, BKnave), # B is a Knight or a Knave
    Implication(BKnight, Not(BKnave)), # If B is a Knight, B is not a Knave

    # Puzzle
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), # A is Knight if A and B are both Knights or Knaves
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))) # B is a Knight if A and B are different characters
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    # Structure
    Or(AKnight, AKnave), # A is a Knight or a Knave
    Implication(AKnight, Not(AKnave)), # If A is a Knight, A is not a Knave
    Or(BKnight, BKnave), # B is a Knight or a Knave
    Implication(BKnight, Not(BKnave)), # If B is a Knight, B is not a Knave
    Or(CKnight, CKnave), # C is a Knight or a Knave
    Implication(CKnight, Not(CKnave)), # If C is a Knight, C is not a Knave

    # Puzzle
    Biconditional(AKnight, Or(AKnight, AKnave)), # A is a Knight if A says "I am a knight." or "I am a knave."
    Biconditional(BKnight, And(CKnave, Biconditional(AKnight, AKnave))), # B is a Knight if C is a Knave and A says A is a Knave
    Biconditional(CKnight, AKnight) # C is a Knight if A is a Knight
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
