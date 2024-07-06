""" a7.py
Anigioro Daniel(doa8) Michel Adelien(mha57)
NONE
5/2/2024
# Skeleton by Prof. Bracy, AWB93, April, 2023 """

import dice

class Rules():
    """A class to store some of the basic assumptions and rules of the game."""

    NUM_DICE = 5

    # numbers for each of the 13 categories
    CHANCE = 0
    ONES = 1
    TWOS = 2
    THREES = 3
    FOURS = 4
    FIVES = 5
    SIXES = 6
    THREE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 9
    SM_STRAIGHT = 10
    LG_STRAIGHT = 11
    YAHTZEE = 12
    NUM_CATEGORIES = 13

    """
    Remember it is bad form to have `magic numbers` in your code.  Instead,
    you can create a variable whose name offers a meaningful description of
    what that number is. Here are some constants below that we want you to use.
    """
    FULL_HOUSE_PTS = 25
    SM_STRAIGHT_PTS = 30
    LG_STRAIGHT_PTS = 40
    YAHTZEE_PTS = 50

    # STUDENTS: if you want to make your own constants/variables, create
    # your new class attributes here:

    # STUDENTS: Notice that
    # CHANCE has the value 0 above, and CHANCE goes in location [0]
    names = ["Chance", "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",\
             "3 of a kind", "4 of a kind", "Full House", "Small Straight",\
             "Large Straight", "Yahtzee (5x!)"]

    # STUDENTS: Notice that
    # CHANCE has the value 0 above,   and CHANCE  goes in location [0]
    # ...
    # YAHTZEE has the value 12 above, and YAHTZEE goes in location [12]
    descriptions = [" -- sum all 5 dice ",
                    "   -- sum 1s only    ",
                    "   -- sum 2s only    ",
                    " -- sum 3s only    ",
                    "  -- sum 4s only    ",
                    "  -- sum 5s only    ",
                    "  -- sum 6s only    ",
                    " -- sum all 5 ",
                    " -- sum all 5 ",
                    "     -- "+str(FULL_HOUSE_PTS)+" pts ",
                    " -- "+str(SM_STRAIGHT_PTS)+" pts",
                    " -- "+str(LG_STRAIGHT_PTS)+" pts",
                    "  -- "+str(YAHTZEE_PTS)+" pts"]

# STUDENTS: do not modify Basic!
class Basic():
    """Basic is the simplest way to score a hand in Yahtzee.
    Any 5-dice hand meets the criteria to count for Basic.
    The score is the sum of the values of all the dice in the hand.
    """

    def __init__(self, index):
        """Creates an instance of a Basic with the following attributes:

        index:      [int] which scorecard entry this is associated with
        is_filled:  [bool] whether a hand has been assigned to this Basic
                    (this is always False in the beginning)
        points:     [int] once a hand as been associated with this category,
                    the points attribute will reflect the score
        max_points: [int] the best score one can get with this category. this
                    field will be used for the scoreboard to let users know
                    how many points they stand to earn under this category

        Precondition: 0 <= index [int] <= Rules.YAHTZEE
        """
        assert index >= 0, "index must be a positive integer"
        assert index <= Rules.YAHTZEE, \
            "index must be no larger than"+str(Rules.YAHTZEE)
        self.index = index
        self.is_filled = False
        self.points = 0
        self.max_points = Rules.NUM_DICE * dice.Die.NUM_SIDES

    def score(self, hand):
        """This method does the following:
            1. Set the `is_filled` attribute to True
            2. Set the `points` attribute to the appropriate number of points,
                given the hand and category

        Returns None (Students: don't return score. set the points attribute)

        When Basic is scored, simply sum the value of all dice in the hand.
        Also mark the category as filled. Each category can only be used once.

        Precondition: hand is a list of Die
        """
        self.points = hand.score()
        self.is_filled = True

    def __str__(self):
        """This method should be sufficient for this class and any of its
        subclasses."""
        end = "/"+str(self.max_points)+"]"
        if not self.is_filled:
            scoretext = " [ "+end
        else:
            scoretext = " ["+str(self.points)+end
        return str(self.index) + ": "+ Rules.names[self.index]+\
            Rules.descriptions[self.index] + scoretext

# STUDENTS: if you create any new classes, add them here.
class Tok_fok_fh_Yahtzees(Basic):
    def __init__(self,index):
        super().__init__(index)

    def score(self, hand):
        counts = {}
        for d in hand.mydice:
            if d.value in counts:
                counts[d.value] += 1
            else:
                counts[d.value] = 1

        if self.index == 12:
            if any(count == 5 for count in counts.values()):
                self.points = Rules.YAHTZEE_PTS
            else:
                self.points = 0

        if 3 in counts.values() and 2 in counts.values():
            self.points = Rules.FULL_HOUSE_PTS
        if self.index == 8:
            if any(count > 3 for count in counts.values()):
                self.points = hand.score()
            else:
                self.points = 0
        if self.index == 7:
            if any(count > 2 for count in counts.values()):
                self.points = hand.score()
            else:
                self.points = 0

        self.is_filled = True


class Sst_Lst(Basic):
    def __init__(self,index):
        super().__init__(index)

    def score(self, hand):
        numbers_list = []
        for d in hand.mydice:
            numbers_list.append(d.value)

        numbers_list.sort()

        max_length = 0
        current_length = 1
        for i in range(1, len(numbers_list)):
            if numbers_list[i] == numbers_list[i - 1] + 1:
                current_length += 1
        else:
            max_length = max(max_length, current_length)
            current_length = 1

        max_length = max(max_length, current_length)
        if self.index == 10:
            if max_length >= 4:
                self.points = Rules.SM_STRAIGHT_PTS
            else:
                self.points = 0
        else:
            if max_length >= 5:
                self.points = Rules.LG_STRAIGHT_PTS
            else:
                self.points = 0

        self.is_filled = True


class Upper_section(Basic):
    def __init__(self,index):
        super().__init__(index)

    def score(self, hand):
        counts = {}
        for d in hand.mydice:
            if d.value in counts:
                counts[d.value] += 1
            else:
                counts[d.value] = 1

        self.points = 0
        for i in range(1, 7):
            if self.index == i:
                self.points = i * counts.get(i, 0)
                break
        self.is_filled = True


class Scorecard():
    """The scorecard tells you what categories there are, what points can be
    earned, which ones have been filled, and what your total score is so far.
    """

    def __init__(self):
        """
        Instance attributes:
          total_score: [int] tells you how  many points have been earned
          categories: [list of Basic] there are 13 categories in the game
                  and this list keeps track of each of them
        """
        self.total_score = 0
        self.categories = [None]*Rules.NUM_CATEGORIES
        self.categories[Rules.CHANCE] = Basic(Rules.CHANCE)
        self.categories[Rules.THREE_OF_A_KIND] = Tok_fok_fh_Yahtzees(Rules.THREE_OF_A_KIND)
        self.categories[Rules.FOUR_OF_A_KIND] = Tok_fok_fh_Yahtzees(Rules.FOUR_OF_A_KIND)
        self.categories[Rules.FULL_HOUSE] = Tok_fok_fh_Yahtzees(Rules.FULL_HOUSE)
        self.categories[Rules.YAHTZEE] = Tok_fok_fh_Yahtzees(Rules.YAHTZEE)
        self.categories[Rules.SM_STRAIGHT] = Sst_Lst(Rules.SM_STRAIGHT)
        self.categories[Rules.LG_STRAIGHT] = Sst_Lst(Rules.LG_STRAIGHT)
        self.categories[Rules.ONES] = Upper_section(Rules.ONES)
        self.categories[Rules.TWOS] = Upper_section(Rules.TWOS)
        self.categories[Rules.THREES] = Upper_section(Rules.THREES)
        self.categories[Rules.FOURS] = Upper_section(Rules.FOURS)
        self.categories[Rules.FIVES] = Upper_section(Rules.FIVES)
        self.categories[Rules.SIXES] = Upper_section(Rules.SIXES)

    # --------- STUDENTS: Do not modify any of the code below ---------

    def cat_prompt(self):
        print(self)
        print("How would you like to categorize these dice?")

    def set_hand(self, hand, choice):
        """Associates a hand with one of the game categories."""
        self.categories[choice].score(hand)
        s = self.categories[choice].points
        print("You just earned "+str(s)+" points!\n")
        self.total_score += s

    def __str__(self):
        """Prints out the scorecard, one category (row) at a time."""
        result = ""
        for c in self.categories:
            result += str(c)+"\n"
        return result

    def choice_okay(self, choice):
        """
        Makes the game more usable by not letting the user select a category
        that has already been chosen or that is not valid.
        """
        if not choice.isnumeric():
            print("Please enter a number.")
            return False
        choice = int(choice)
        if (choice < 0):
            print("category index must be a positive integer.")
            return False
        if (choice > Rules.YAHTZEE):
            print("The largest category index in Yahtzee is "+str(Rules.YAHTZEE))
            return False
        if (self.categories[choice] == None):
            print("This category has not been implemented yet.")
            return False
        if (self.categories[choice].is_filled):
            print("That category has already been filled.")
            return False
        return True

    def get_choice(self):
        """Prompts the user to pick a category that they wish apply
        their current hand to.
        """
        choice = input("Your choice: ")
        while(not self.choice_okay(choice)):
            choice = input("Your choice: ")
        return int(choice)

def get_hand():
    """Rolls the dice and allows the user to re-roll up to 2 more times."""
    print("Rolling the dice...")
    hand = dice.Hand(Rules.NUM_DICE)
    if hand.initiate_reroll():
        hand.initiate_reroll()
    return hand

if __name__=='__main__':
    sc = Scorecard()
    print("Welcome to Yahtzee!")
    print(sc)
    n_turns = Rules.NUM_CATEGORIES - sc.categories.count(None)

    while (n_turns > 0):
        print("You have "+str(n_turns)+" rolls left.")
        hand = get_hand()
        sc.cat_prompt()
        choice = sc.get_choice()
        sc.set_hand(hand, choice)
        print(sc)
        print("Current score = "+str(sc.total_score))
        print("--------------------------------------------")
        n_turns -= 1

    print("FINAL SCORE = "+str(sc.total_score)+"\nThanks for playing!")
