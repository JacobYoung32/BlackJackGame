# TODO:
# Reset deck and hands if player chooses to play another game
# Implement gui

import random as r
from os import system
import time

suits = ("hearts", "diamonds", "spades", "clubs")

class InsufficientFundsError(Exception):
    """A player's wager was larger than their account balance!"""
    pass

class Card:
    def __init__(self, value, suit):
        # Initializes a card object and ensures that it is a possible card
        if value not in range(1, 14):
            raise TypeError("The value of the card must be between 1 and  13.")
        if suit.lower() not in suits:
            raise TypeError("The suit must be either hearts, diamonds, spades or clubs.")
        self.value = value
        self.suit = suit
        self.shown = False

    def showCard(self):
        # Prints the standard name of a card
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
        print(f"{trueValue} of {self.suit}")
        self.shown = True


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        # Builds the deck by looping through every possible card for each suit
        for suit in suits:
            for value in range(1, 14):
                self.cards.append(Card(value, suit))

    def showDeck(self):
        # Goes through each card in the deck one by one and prints the standard name for each card
        for c in self.cards:
            c.showCard()

    def shuffle(self):
        # Randomizes the order of the deck
        for i in range(0, 5):
            r.shuffle(self.cards)

    def drawCard(self):
        # Takes the first card from the top of the deck and returns it
        return self.cards.pop()


class Player:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def bet(self):
        # Takes the player's wager for a hand of blackjack
        while True:
            try:
                wager = int(input("How much would " + self.name + " like to bet: "))
                if wager > self.balance:
                    raise InsufficientFundsError
            except ValueError:
                print("Your bet must be a number! Try again!")
                pass
            except InsufficientFundsError:
                print("Insufficient funds!")
                pass
            else:
                self.balance = self.balance - wager
                print(f"{self.name}'s new balance is ${self.balance}")
                break

        return wager

    def deposit(self, amount):
        # Deposits money into the player's account
        self.balance = self.balance + amount


class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.clear()
        self.printHeader()

        # Initializes information about the player
        playerName = input("Enter your name: ")
        self.player = Player(playerName, 1000)
        self.playerHand = []
        self.playerTotal = 0

        # Initializes information about the dealer
        self.dealer = Player("Dealer", 0)
        self.dealerHand = []
        self.dealerTotal = 0

        # Starts the game
        self.turnOne()

    def clear(self):
        # Clears system screen
        _ = system('clear')

    def printHeader(self):
        # Prints game header
        print("__          __  _                            _______      ____  _            _        _            _")
        print("\ \        / / | |                          |__   __|    |  _ \| |          | |      | |          | |")
        print(" \ \  /\  / /__| | ___ ___  _ __ ___   ___     | | ___   | |_) | | __ _  ___| | __   | | __ _  ___| | __")
        print("  \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \    | |/ _ \  |  _ <| |/ _` |/ __| |/ /   | |/ _` |/ __| |/ /")
        print("   \  /\  /  __/ | (_| (_) | | | | | |  __/    | | (_) | | |_) | | (_| | (__|   < |__| | (_| | (__|   < ")
        print("    \/  \/ \___|_|\___\___/|_| |_| |_|\___|    |_|\___/  |____/|_|\__,_|\___|_|\_\____/ \__,_|\___|_|\_\ ")

    def win(self, pt, dt):
        # Defines and checks win conditions based on player and dealer totals
        # Returns a 0 if the player loses and a 1 if they win
        if dt == 21 or pt > 21:
            print("You lose!")
            return 0
        elif pt == 21 or dt > 21:
            print("You win!")
            return 1
        elif dt >= 17:
            if dt >= pt:
                print("You lose!")
                return 0
            else:
                print("You win!")
                return 1

    def gameOver(self):
        # Called when the player wins or loses
        answer = input("Would you like to play again? (Y/N): ")
        if answer.lower() == 'y':
            self.restart()
        elif answer.lower() == 'n':
            print("Okay! Have a great day!")
            exit(0)
        else:
            print("Answer must be Y or N!")
            self.gameOver()

    def restart(self):
        # Called if the player chooses to play again
        self.deck = Deck()

        self.playerHand = []
        self.playerTotal = 0

        self.dealerHand = []
        self.dealerTotal = 0

        self.clear()
        self.printHeader()

        self.turnOne()

    def hitOrStand(self):
        choice = input("Would you like to hit or stand? (H/S): ")
        if choice.lower() == "h" or choice.lower() == "s":
            return choice.lower()
        else:
            print("Your choice must be an H or an S!\n")
            self.hitOrStand()

    def updateTotal(self, card, total):
        # Takes a card and a total and then adds the value of the card to the total
        if card.value > 10:
            return total + 10
        elif card.value == 1:
            return total + 11
        else:
            return total + card.value

    def showHand(self, hand):
        for card in hand:
            card.showCard()

    def turnOne(self):
        # This plays the first turn of a hand of blackjack
        # The first turn is defined separately because it follows a different procedure to subsequent turns

        # This is how a player makes their bets and can see their current balance
        print(f"{self.player.name}'s current balance is ${self.player.balance}")

        self.bet = self.player.bet()
        print("---------------------------")
        time.sleep(1)

        # This loop adds cards to the hands of the player and the dealer
        for i in range(2):
            playerCard = self.deck.drawCard()
            self.playerTotal = self.updateTotal(playerCard, self.playerTotal)
            self.playerHand.append(playerCard)

            dealerCard = self.deck.drawCard()
            self.dealerHand.append(dealerCard)

        # Prints the dealer's hand and updates their total
        print("Dealer's hand:")
        card = self.dealerHand[0]
        card.showCard()
        self.dealerTotal = self.updateTotal(card, self.dealerTotal)
        print("? of ?")
        print(f"Dealer's total is {self.dealerTotal}")
        print("---------------------------")

        time.sleep(1)

        # Prints the player's hand and total
        print(f"{self.player.name}'s hand:")
        self.showHand(self.playerHand)
        print(f"{self.player.name}'s total is: {self.playerTotal}")
        print("---------------------------")

        time.sleep(1)

        # Checks if the player has won or lost and ends the game if they have
        gameWin = self.win(self.playerTotal, self.dealerTotal)

        if gameWin == 1:
            self.player.deposit(self.bet * 2)
            self.gameOver()

        elif gameWin == 0:
            self.gameOver()

        # If the player has not won or lost, this checks whether or not they choose to hit or to stand
        HSresult = self.hitOrStand()

        if HSresult == "s":
            self.stand()
        elif HSresult == "h":
            self.hit()
        else:
            print("Your choice must be an H or an S!")

    def hit(self):
        self.clear()
        print(f"Dealer's total is: {self.dealerTotal}")
        for card in self.dealerHand:
            card.showCard()
        print("---------------------------")

        playerCard = self.deck.drawCard()
        print(f"{self.player.name}'s new card is a:")
        playerCard.showCard()
        self.playerTotal = self.updateTotal(playerCard, self.playerTotal)
        self.playerHand.append(playerCard)
        print("---------------------------")

        time.sleep(1)

        # Prints the player's hand and total
        print(f"{self.player.name}'s hand:")
        for card in self.playerHand:
            card.showCard()
        print(f"{self.player.name}'s total is: {self.playerTotal}")
        print("---------------------------")

        time.sleep(1)

        # Checks if the player has won or lost and ends the game if they have
        gameWin = self.win(self.playerTotal, self.dealerTotal)

        if gameWin == 1:
            self.player.deposit(self.bet * 2)
            self.gameOver()

        elif gameWin == 0:
            self.gameOver()

        # Checks whether the player would like to hit or stand
        HSresult = self.hitOrStand()

        if HSresult == "s":
            self.stand()
        elif HSresult == "h":
            self.hit()
        else:
            print("Your choice must be an H or an S!")

    def stand(self):
        self.clear()

        card = self.dealerHand[1]
        self.dealerTotal = self.updateTotal(card, self.dealerTotal)

        print(f"{self.player.name}'s total is: {self.playerTotal}")
        for card in self.playerHand:
            card.showCard()
        print("---------------------------")

        time.sleep(1)

        print(f"Dealer's total is: {self.dealerTotal}")
        for card in self.dealerHand:
            card.showCard()

        time.sleep(1)

        while self.dealerTotal < 17:
            self.clear()
            print(f"{self.player.name}'s total is: {self.playerTotal}")
            for card in self.playerHand:
                card.showCard()
            print("---------------------------")

            time.sleep(1)

            print(f"Dealer's total is: {self.dealerTotal}")
            for card in self.dealerHand:
                card.showCard()

            card = self.deck.drawCard()
            self.dealerHand.append(card)
            print("---------------------------")
            print("Dealer's new card is: ")
            card.showCard()
            self.dealerTotal = self.updateTotal(card, self.dealerTotal)
            time.sleep(2)

        print("---------------------------")
        print(f"Dealer's total is: {self.dealerTotal}")

        gameWin = self.win(self.playerTotal, self.dealerTotal)

        if gameWin == 1:
            self.player.deposit(self.bet * 2)
            self.gameOver()

        elif gameWin == 0:
            self.gameOver()


game = Game()
game.__init__()
