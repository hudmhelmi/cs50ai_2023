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
    # A can be either a knight or a knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # A says "I am both a knight and a knave."
    # If A is a knight, then A is both a knight and a knave, and vice versa
    Biconditional(AKnight, And(AKnight, AKnave)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A and B can be either knights or knaves but not both
    And(
        And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
        And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    ),
    # A says "We are both knaves."
    # If A is a knight, then A and B are both knaves, and vice versa
    Biconditional(AKnight, And(AKnave, BKnave)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A and B can be either knights or knaves but not both
    And(
        And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
        And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    ),
    # If A is a knight, then A and B are the same kind
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # If B is a knight, then A and B are different kinds
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A, B, and C can be either knights or knaves but not both
    And(
        And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
        And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
        And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
    ),
    # B says "A said 'I am a knave'."
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    # B says "C is a knave."
    Biconditional(BKnight, CKnave),
    # C says "A is a knight."
    Biconditional(CKnight, AKnight),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
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
