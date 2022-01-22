# TODO:
# Implement "stand" option in game() function
# Implement gui

import random as r
from os import system

suits = ("hearts", "diamonds", "spades", "clubs")

class Card:
    def __init__(self, value, suit):
        if value not in range(1, 14):
            raise TypeError("The value of the card must be between 1 and  13.")
        if suit.lower() not in suits:
            raise TypeError("The suit must be either hearts, diamonds, spades or clubs.")
        self.value = value
        self.suit = suit
        # Checks to see if it's a possible card. If not then return an error that says so

    def showCard(self):
        # This function prints the standard name of a card
        if self.value == 1:
            trueValue = "Ace"
        elif self.value == 11:
            trueValue = "Jack"
        elif self.value == 12:
            trueValue = "Queen"
        elif self.value == 13:
            trueValue = "King"
        else:
            trueValue = self.value
        print("{} of {}".format(trueValue, self.suit))


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        # This function builds the deck by looping through every possible card for each suit
        for suit in suits:
            for value in range(1, 14):
                self.cards.append(Card(value, suit))

    def showDeck(self):
        # This function goes through each card in the deck one by one and prints the standard name for each card
        for c in self.cards:
            c.showCard()

    def shuffle(self):
        # This function randomizes the order of the deck
        for i in range(0, 5):
            r.shuffle(self.cards)

    def drawCard(self):
        # This function takes the first card from the top of the deck and returns it
        return self.cards.pop()


class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def bet(self):
        # This function takes the player's wager for a hand of blackjack
        wager = int(input("How much would " + self.name + " like to bet: "))

        if wager > self.balance:
            print("Insufficient funds!")
            self.bet()
        else:
            self.balance = self.balance - wager
            print(self.name + "'s new balance is", self.balance)

        return wager

    def deposit(self, amount):
        # This function deposits money into the player's account
        self.balance = self.balance + amount


def gameOver():
    answer = input("Would you like to play again? Y/N\n")
    if answer.lower() == 'y':
        game()
    elif answer.lower() == 'n':
        print("Okay! Have a great day!")
        exit(0)
    else:
        print("Answer must be Y or N!")
        gameOver()

def clear():
    _ = system('clear')

def printHeader():
    print("__          __  _                            _______      ____  _            _        _            _")
    print("\ \        / / | |                          |__   __|    |  _ \| |          | |      | |          | |")
    print(" \ \  /\  / /__| | ___ ___  _ __ ___   ___     | | ___   | |_) | | __ _  ___| | __   | | __ _  ___| | __")
    print("  \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \    | |/ _ \  |  _ <| |/ _` |/ __| |/ /   | |/ _` |/ __| |/ /")
    print("   \  /\  /  __/ | (_| (_) | | | | | |  __/    | | (_) | | |_) | | (_| | (__|   < |__| | (_| | (__|   < ")
    print("    \/  \/ \___|_|\___\___/|_| |_| |_|\___|    |_|\___/  |____/|_|\__,_|\___|_|\_\____/ \__,_|\___|_|\_\ ")

def win(dt, pt):
    if dt == 21:
        print("You lose!")
        return 0
    elif dt > 21:
        print("You win!")
        return 1

    if pt == 21:
        print("You win!")
        return 1
    elif pt > 21:
        print("You lose!")
        return 0

def game():
    deck = Deck()
    deck.shuffle()

    clear()
    printHeader()

    player = Player("Jacob", 1000)
    playerHand = []

    Dealer = Player("Dealer", 0)
    dealerHand = []

    playerTotal = 0
    dealerTotal = 0

    print(player.name + "'s current balance is ", player.balance)

    bet = player.bet()
    endGame = False
    turn = 1

    while not endGame:
        clear()
        printHeader()

        if turn == 1:
            dealerCard = deck.drawCard()
            dealerHand.append(dealerCard)

            for i in range(2):
                playerCard = deck.drawCard()
                playerHand.append(playerCard)

            print("Dealer's hand:")
            for card in dealerHand:
                card.showCard()

                if card.value > 10:
                    dealerTotal = dealerTotal + 10
                elif card.value == 1:
                    dealerTotal = dealerTotal + 11
                else:
                    dealerTotal = dealerTotal + card.value

            print("Dealer's total is:", dealerTotal)

            print(player.name + "'s hand:")
            for card in playerHand:
                card.showCard()

                if card.value > 10:
                    playerTotal = playerTotal + 10
                elif card.value == 1:
                    playerTotal = playerTotal + 11
                else:
                    playerTotal = playerTotal + card.value

            print(player.name + "'s total is:", playerTotal)

            #win(dealerTotal, playerTotal)

            if win(dealerTotal, playerTotal) == 1:
                player.deposit(bet*2)
                endGame = True
            elif win(dealerTotal, playerTotal) == 0:
                endGame = True

            turn = turn + 1

        else:
            card = deck.drawCard()
            dealerHand.append(card)
            card.showCard()

            if card.value > 10:
                dealerTotal = dealerTotal + 10
            elif card.value == 1:
                dealerTotal = dealerTotal + 11
            else:
                dealerTotal = dealerTotal + card.value

            print("Dealer's total is:", dealerTotal)

            win(dealerTotal, playerTotal)

            if win(dealerTotal, playerTotal) == 1:
                player.deposit(bet*2)
                endGame = True
            elif win(dealerTotal, playerTotal) == 0:
                endGame = True

            card = deck.drawCard()
            playerHand.append(card)
            card.showCard()

            if card.value > 10:
                playerTotal = playerTotal + 10
            elif card.value == 1:
                playerTotal = playerTotal + 11
            else:
                playerTotal = playerTotal + card.value

            print(player.name + "'s total is:", playerTotal)

            win(dealerTotal, playerTotal)

            if win(dealerTotal, playerTotal) == 1:
                player.deposit(bet*2)
                endGame = True
            elif win(dealerTotal, playerTotal) == 0:
                endGame = True
    gameOver()


game()
