# BlackJack card game - Fun projectn 
## Import the random module
import random as rd

## Blueprint for creating a single card
class Card():
    ### Constructor function for a card 
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank 
    ### Function to present a card in a readable manner    
    def __str__(self):
        return f'{self.rank["rank"]} of {self.suit }' 
    
## Blueprint for creating a deck card        
class Deck:
    ### Constructor function for a deck of (52) cards
    def __init__(self):
        self.cards = []
        suits = ['spades','clubs','hearts','diamonds']
        ranks = [
            {'rank':'A','value':11},
            {'rank':'2','value':2}, 
            {'rank':'3','value':3},
            {'rank':'4','value':4},
            {'rank':'5','value':5},
            {'rank':'6','value':6},
            {'rank':'7','value':7},
            {'rank':'8','value':8},
            {'rank':'9','value':9},
            {'rank':'10','value':10},
            {'rank':'J','value':10},
            {'rank':'Q','value':10},
            {'rank':'K','value':10}
            ]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit,rank))
                
    ## Function to shuffle cards 
    def shuffle(self):
        if len(self.cards) > 1: ## We will not shuffle a single card+
            rd.shuffle(self.cards) 
        
    ## Function to deal a card
    def deal(self,number):
        dealtCards = []
        for num in range(number):
            if len(self.cards) > 0: ##  We cannot remove a card when there are no cards left
                card = self.cards.pop()
                dealtCards.append(card)
        print(f'There are {len(self.cards)} left in the deck')         
        return dealtCards
    
    ## Above function can also be written using list compression
    ##def deal(self, number):
        ###return [self.cards.pop() for _ in range(number) if self.cards]  
 
## Blueprint for creating a single hand (which posses cards)    
class Hand():
    ### Contructor function for a hand (which can either be player by default or dealer if True argument is passed). 
    def __init__(self, dealer=False):
        self.cards = []
        self.values = 0
        self.dealer = dealer
    
    ### Function to add cards to a hand            
    def add_cards(self, cardList):
        self.cards.extend(cardList)
     
    ### Function to compute the value of cards held in a hand   
    def calculate_value(self):  
        self.value = 0 
        hasAce = False
        for card in self.cards: 
            self.value += int(card.rank["value"])
            if card.rank["rank"] == 'A':
                hasAce = True
    ##def calculate_value(self):  
       ## value = sum(card.rank['value'] for card in self.cards)
        ##hasAce = any(card.rank['rank'] == 'A' for card in self.cards)
        ##return value - 10 if hasAce and value > 21 else value            
                
        if hasAce and self.value > 21:
            self.value -= 10 
    
    ### Function to get the value of cards held in a hand        
    def get_value(self):
        self.calculate_value()
        return self.value 
    
    ### Function to check if value equivalent to 21 (blackjack)
    def is_blackJack(self):
        return self.get_value() == 21  
    
    ### Function to display cards held by a hand
    def display(self,showAllDealerCards = False):
        print(f'''{"Dealer's" if self.dealer else "Player's"} hand:''')
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not showAllDealerCards and not self.is_blackJack():
                print('Hiden') # In this condition we hide the dealer's first card
            else:    
                print(card)
        
        if not self.dealer:
            print(f'Value: {self.get_value()}') # In this condition we display the value of the player's hand
        print()       

## Blueprint for a game       
class Game():
    ### Constructor to keep record of game stats
    def __init__(self):
        self.playerWins = 0
        self.dealerWins = 0
        self.tiedGames = 0
        
    ### Function to hanlde the flow of the blackjack game
    def play(self):
        gameNumber = 0
        gamesToPlay = 0
        
         
        while gamesToPlay <= 0 :
            print("Welcome to Itumeleng's blackjack table.:)")
            try:
                print("How many games would you like to play?")
                gamesToPlay = int(input())
                break
            except Exception:
                print('Error! you must enter a whole number')    
        
        ### Loop to terminate game once user's number of games to play is reached        
        while gameNumber < gamesToPlay:
            gameNumber += 1 ## counter update for each game played0
            
            ### Instantiate a deck and shuffle it
            deck = Deck()   
            deck.shuffle()  
            
            ### Instantiate the player and dealer hands respectively
            playerHand = Hand()
            dealerHand = Hand(True)   
            
            ### Deal 2 cards from deck to each hand 
            for i in range(2):
                playerHand.add_cards(deck.deal(1))
                dealerHand.add_cards(deck.deal(1))
                
            print()
            print('*'*30)    
            print(f'Game {gameNumber} of {gamesToPlay}')
            print('*'*30) 
            ### Display cards held in each hand
            playerHand.display()  
            dealerHand.display() 
            
            ### Check if there is a winner
            if self.check_winner(playerHand,dealerHand):
                continue 
            
            ### Prompt user for choice to either draw another card or keep card 
            choice = ''
            while playerHand.get_value() < 21 and choice not in ['s','stand']:
                print("Please choose 'Hit' or 'Stand':")
                choice = input().lower()
                print()
                while choice not in[ 'h','hit','s','stand']: 
                    print("Please choose 'Hit'/'H' or 'Stand'/'S':")
                    choice = input().lower()
                    print()
                if choice in ['h','hit']:
                    playerHand.add_cards(deck.deal(1))
                    playerHand.display()   
                    
            ### Check if there is a winner         
            if self.check_winner(playerHand,dealerHand):
                continue 
            
            ### Get the value of cards held by each hand
            playerHandValue = playerHand.get_value()
            dealerHandValue = dealerHand.get_value()
            
            ### Loop for dealer to keep drawing cards until held hand value is above 17
            while dealerHandValue < 17:
                dealerHand.add_cards(deck.deal(1))
                dealerHandValue = dealerHand.get_value()
            
            ### Display dealer's hand (when dealer hand value is above 17)     
            dealerHand.display(True) 
            
            ### Check if there is a winner
            if self.check_winner(playerHand,dealerHand):
                continue 
            
            ### Display the final game results
            print('Final Results:')
            print(f"Player's hand: {playerHandValue}")
            print(f"Dealer's hand: {dealerHandValue}")    
            
            ### Check if there is a winner
            self.check_winner(playerHand, dealerHand, True)
        
        ### Display end of game message and stats  
        print(f'\nFinal Stats: \n- {gamesToPlay} Games were played \n- Player won: {self.playerWins} games,\
            \n- Dealer won: {self.dealerWins} games, \n- {self.tiedGames} games ended in a tie.\nThank you for playing, come back soon goodbye :)')
    
    ### Function to check if the winner        
    def check_winner(self, playerHand, dealerHand, gameOver = False):
        playerValue, dealerValue = playerHand.get_value(), dealerHand.get_value()
        if not gameOver:
            if playerValue > 21:
                print('Player busted. Dealer wins! :(') 
                self.dealerWins += 1
                return True
            elif dealerValue > 21:
                print('Dealer busted. Player wins! :)')
                self.playerWins += 1
                return True
            elif playerHand.is_blackJack() and dealerHand.is_blackJack():
                print('Both Player and Deal have blackjack! it is a tie :]') 
                self.tiedGames += 1
                return True
            elif playerHand.is_blackJack():
                print('Player has blackjack! Player wins :)')
                self.playerWins += 1
                return True
            elif dealerHand.is_blackJack():
                print('Dealer has blackJack, Dealer wins :(')
                self.dealerWins += 1
                return True
        else: ## Conditions to check which hand has the higher value
            if playerValue > dealerValue:
                print('Player wins! :)')
                self.playerWins += 1
            elif playerValue == dealerValue:
                print('Both dealer and player hands posses equal value, it is a tie :]') 
                self.tiedGames += 1   
            else:
                print('Dealer wins! :(')  
                self.dealerWins += 1
            return True          
        return False          
        
blackJack = Game()
blackJack.play()                    
 