import random

def create():
    """
        Creates a standard deck of 52 cards and returns a list containing a
        nested dictionary for each card.

        Usage:
        deck_variable = deck()

        """
    # Initialise suit names in tuple for building deck list
    suit_names = ("hearts", "diamonds", "spades", "clubs")

    # Initialise card faces in tuple for building deck list
    card_faces = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')

    # Initialise empty deck
    deck = []

    # Iteration through suit_names tuple (4 Loops)
    for suit in suit_names:
        # Iteration through card_faces tuple for each suit (13 Loops x the 4 loops above)
        for face in card_faces:
            # Temporary variable 'card' is used to create a dictionary of a singular suit and face as a key/pair value (1 playing card)
            card = {'suit': suit,
                    'face': face}
            # For each iteration of the 'card_faces' for loop, card is appending to the deck (e.g. deck = [{'suit': "hearts",'face':'A'}, {other}, {cards}, {in}, {deck}] etc.)
            deck.append(card)
    # Returns the fully appended deck to the specified variable (e.g [{'suit': "hearts",'face':'A'}, {other}, {cards}, {in}, {deck}, {52}, {total}, {dictionaries}])
    return deck

def shuffle(deck):
    """
        Shuffles given deck list a random amount of times between 1 and 5
        and returns it.

        Usage:
        shuffle(deck_variable) - deck_variable being the chosen defined variable that was initialised by create()

        """
    # Loops a random number of times between 1 and 5
    for i in range(random.randint(1,5)):
        # Deck list of 52 dictionaries(cards) is completely shuffled a random amount of times between 1 and 5
        random.shuffle(deck)
    return

def deal(deck):
    """
        Takes deck as input, returns 1 card (nested dictionary) whilst removing
        from the list.

        Usage:
        ***THERE MUST BE A HAND ALREADY INITIALISED AS A LIST BEFORE CARDS CAN BE DEALT***
        
        hand_variable = []
        hand_variable.append(deal(deck_variable)) - deck_variable being the chosen defined variable that was initialised by create()
        
        """
    # No actions are taken inside the function but it returns the last entry in the deck list whilst removing it from the main deck list (deck needs to be shuffled first)
    return deck.pop()

def value(hand):
    """
        Takes hand as input, returns integer value of hand based on card values
        contained below.

        Usage:
        hand_value_variable = value(hand_variable)
        
        """
    # Initialise card_values in a dictionary to be used in calculations
    card_values = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,
                   '8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
    
    # Initialise the total variable to integer 0 for consistency each time a hand value is checked
    total = 0

    # Iteration through each card (dictionaries) stored in the chosen hand_variable
    for card in hand:
        # The temporary player_card variable is initialised each iteration with the extracted 'face' value from the single card dictionary for that iteration using the get() method.
        # e.g. hand_variable = [{'suit': "hearts",'face':'A'}] so that means player_card = 'A'
        player_card = card.get('face')
        # The value from the card_values dictionary(above) is extracted using the get() method based on the player_card value.
        # e.g. player_card = 'A' so card_values.get(player_card) returns integer 1, this is then added to total and then total is assigned the new value using += operator
        total += card_values.get(player_card)
    # Once iteration through the hand is completed, the total integer value is returned for use in the chosen hand_value_variable for printing, comparisons etc 
    return total