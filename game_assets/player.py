def create_player(player_name=''):
    """
    Creates a new player profile. If a save file does not exist, it creates one. 
    If the save file does exist, it reads the file to check for existing player names. 
    After obtaining a valid name, it writes the player's information to the save file.
    
    Returns:
        dict: A dictionary containing the player's name and initial credits.

    Example Usage:
        loaded_player = create_player()
        print(player)
        >>> {'name': 'Test', 'credits': 1000}

        Can also be used standalone (doesn't need to initialise a variable, will write to the text file only)
    """
    # Loop to check if save_file.txt exists
    while True:
        
        # Program will try to open save_file.txt in read mode ("r")
        try:
            file = open("save_file.txt","r")
            
            # new_file variable set to false as file already exists (used further down in this function)
            new_file = False
            
            # File closed to allow proper running of the code outside of this loop
            file.close()
            
            # Break the loop if save_file.txt successfully opens
            break
        
        # Catches the execption if save_file.txt is missing
        except:
            print("Save file not found. Created 'save_file.txt' in file directory")
            
            # save_file.txt is created in write mode ("w") to program directory
            file = open("save_file.txt","w")
            
            # new_file variable set to true as program created new text file above
            new_file = True
            
            # File closed to allow proper running of the code outside of this loop
            file.close()
            
            # Break the loop as no further actions required at this stage
            break
        
    # Opens the existing/next save_file.txt file in read mode ("r") and assigns to variable 'file'
    file = open("save_file.txt","r")
    
    # Initialise empty list to store existing player names from save_file
    player_names = []
    
    # Iteration through save_file.txt line by line
    for line in file:
        
        # Temporary variable line_dict is assigned the line which is converted to dict type using eval() function
        line_dict = eval(line)
        
        # player_names list is appended with the name extracted from the line_dict using get() method
        player_names.append(line_dict.get('name'))
        
    # File closed as the required information has been read and saved at this stage
    file.close()
    
    # Loop to take user input of name
    if player_name != '':
        # Player dictionary variable is initialised with player_input name and starting credits of 1000
        player = {'name':player_name,'credits':1000}

        # save_file.txt is opened in append mode ("a") and assigned to 'file' variable
        file = open("save_file.txt","a")

        # Checks if new_file variable initialised earlier is boolean True
        if new_file:
            # If true, player dictionary is written to text file as string, without a new line
            file.write(str(player))
            return player
        else:
            # If false, a new line is written to text file before player dictionary is written to text file
            file.write('\n')
            file.write(str(player))
            file.close()
            return player

def load(player_name_string):
    """
    Loads a player's profile from the save file based on the given player name string. 
    If the save file does not exist, it prompts the user to create a new player profile.
    
    Argument:
        player_name (str): The name of the player to load.
    
    Returns:
        dict: A dictionary containing the loaded player's information (name and credits).

    Example Usage:
        name = 'Test'
        current_player = load(name)
        print(current_player)
        >>> {'name': 'Test', 'credits': 1000}
    """
    
    # Loop to check if save_file.txt exists
    while True:

        # Program will try to open save_file.txt in read mode ("r")
        try:
            file = open("save_file.txt","r")

            # File closed to allow proper running of the code outside of this loop
            file.close()

            # Break loop as no further action required
            break

        # Handle exception if save_file.txt not found
        except:
            create_player(player_name_string)
            
    # Opens the existing/next save_file.txt file in read mode ("r") and assigns to variable 'file'          
    file = open("save_file.txt","r")

    # Initialise empty list to store full, existing player profile dictionaries from save_file.txt
    player_profiles = []

    # Iteration through save_file.txt line by line
    for line in file:

        # Temporary variable player_profile_dict is assigned the line which is converted to dict type using eval() function
        player_profile_dict = eval(line)

        # player_profile_dict is appended with the dictionary entry extracted from the line in the iteration through save_file.txt
        player_profiles.append(player_profile_dict)

    # File closed as the required information has been read and saved at this stage    
    file.close()

    # Range loop for the total length of the amount of player_profile_dict entries in player_profiles list
    for i in range(len(player_profiles)):

        # If statement checks each index(i) of player_profiles, using get() method as it is iterated against player_name string given as input to the function
        if player_profiles[i].get('name') == player_name_string:
    
            # If found, the player profile dictionary is returned to the program to whatever variable was specified
            return player_profiles[i]

    else:
        # Message is player_name string isn't found after iterating
        print("Player name not found in player file. Creating player instead.")
        return create_player(player_name_string)
        
def save(loaded_player_dict, amount=0):
    """
    Saves the updated player information to the save file. 
    It updates the credits of the loaded player with the provided amount.
    
    Arguments:
        loaded_player (dict): A dictionary containing the player's information (name and credits).
        amount (int, optional): The amount to update the player's credits by. Defaults to 0.
        
    Example Usage:
        winnings = 500
        current_player = {'name': 'Test', 'credits': 1000}
        
        save(current_player, winnings)
        
        name = 'Test'
        current_player = load(name)
        
        print(current_player)
        >>> current_player = {'name': 'Test', 'credits': 1500}
        
    """
    # Loop to check if save_file.txt exists
    while True:
        # Program will try to open save_file.txt in read mode ("r")
        try:
            file = open("save_file.txt","r")
            # File closed to allow proper running of the code outside of this loop
            file.close()
            # Break loop as no further action required
            break
        # Handle exception if save_file.txt not found
        except:
            # Loop to take choice if save_file.txt doesn't exist
            while True:
                # Request user input, error handle for incorrect options entered
                choice = input("Save file not found. Do you want to create a player? (Y/N): ")
                choice = choice.lower()
                choice = choice.strip()
                if not choice:
                    print("You didn't choose a valid option.")
                elif choice.isdigit():
                    print("You didn't choose a valid option.")
                elif choice == 'y':
                    # Call create() if customer wants to create a new player
                    create_player()
                    # Ends the function to prevent issues after create() is called and completed
                    return
                elif choice == 'n':
                    # Ends the function as not possible to proceed without save_file.txt
                    return
                else:
                    print("You didn't choose a valid option.")
    # Opens the existing/next save_file.txt file in read mode ("r") and assigns to variable 'file'                
    file = open("save_file.txt","r")

    # player_name variable is initiated by the extracted value of 'name' in the current player dictionary
    player_name = loaded_player_dict.get('name')

    # Initialise empty list to store the existing and updated player profiles for writing later
    updated_profiles = []

    # Iteration through save_file.txt line by line
    for line in file:

        # Remove any empty spaces/line breaks that *might* be in save_file.txt (bug prevention)
        line = line.strip()

        # If statement to catch the line for analysis each iteration (equal to if line == 'True', basically line has a value)
        if line:
            # Regardless of contents at this stage, player_profile_dict is initialsed by converting line in save_file to dict
            player_profile_dict = eval(line)

            # If statement to catch if current iteration/player profile input 'name' value matches the name from save_file.txt line iteration
            if player_profile_dict.get('name') == player_name:

                # If true, the currently loaded player dictionary credit value is added to or subtracted from based on input (defaul=0)
                loaded_player_dict["credits"] += amount

                # Updated player dictionary (with new credit value amount) is appended to updated_profiles list 
                updated_profiles.append(str(loaded_player_dict))
            else:
                # If player_name from input doesn't match, the line is copied like-for-like from save_file.txt to updated_profiles
                updated_profiles.append(line)

    # File closed as the required information has been read and saved at this stage                
    file.close()

    # save_file.txt is opened in write mode ("w") which overwrites the existing one (at this stage, empty txt file) 
    file = open("save_file.txt","w")

    # index number initialised for consistency when writing lines (first entry must not have a \n or new line before it)
    index = 0
    
    # updated_profiles list initialised and appended to earlier is iterated through
    for profile in updated_profiles:

        # If statement to check if index is less than the length of updated_profiles - 1
        if index < len(updated_profiles) - 1:

            # save_file.txt is written to with the current iterations profile (player dictionary with a new line)
            file.write(profile)
            file.write('\n')
        else:
            # The first entry is written to the file without a new line
            file.write(profile)
        # Index is incrementally increased to ensure lines after include new line \n
        index += 1
    # File closed as no further actions required, file is written with new, appended player profile (if applicable)    
    file.close()

def get_info(loaded_player_dict):
    """
    Displays the player's name and credits.

    Arguments:
        loaded_player (dict): A dictionary containing the player's information (name and credits).
    
    Returns:
        tuple: A tuple containing the player's name and credits.

    Example Usage:
        loaded_player_dict = {'name': 'Test', 'credits': 1000}
        
        player_name, player_credits = show(current_player)
        
        print(player_name)
        print(player_credits)
        >>> Test
        >>> 1000
    """
    # player_name variable initialised by the current loaded player provided dictionary variable, extracting the 'name' value using get() method
    player_name = loaded_player_dict.get('name')

    # player_credits variable initialised by the current loaded player provided dictionary variable, extracting the 'credits' value using get() method
    player_credits = loaded_player_dict.get('credits')

    # Tuple of player_name, player_credits returned. 
    return player_name, player_credits

def check(loaded_player_dict,amount):
    """
    Checks if the provided amount is valid for betting based on the player's current credits.
    
    Arguments:
        loaded_player (dict): A dictionary containing the player's information (name and credits).
        amount (int): The bet amount to check.
    
    Returns:
        bool: True if the bet amount is valid (within the player's credit balance), False otherwise.

    Example Usage:
        loaded_player = {'name': 'Test', 'credits': 1000}
        bet_amount = 500

        if check(loaded_player, bet_amount) == True:
            print("Bet Valid")
            loop breaks, rest of code below
        elif check(loaded_player, bet_amount) == False:
            print("Bet Exceeds Balance")
            loop doesn't break, code won't proceed until True

        >>> Bet Valid
    """
    # player_credits variable initialised by the current loaded player provided dictionary variable, extracting the 'credits' value using get() method
    player_credits = loaded_player_dict.get('credits')

    # If statement to compare amount (provided as an argument to this function) with player_credits
    if amount <= player_credits:
        # If amount is less than or equal to player_credits function returns bool 'True'
        # e.g. bet = input(), if check(player, bet) == 'True': (code block runs)
        return True
    else:
        # If amount is more than player_credits, function returns bool 'False'
        # e.g. if check(player,bet) == 'False' (error message given, loop doesn't break)
        return False