# Lucky Sevens Lottery - PY_learn project6 version2
## Import the random liabrary 
import random

## Define a function to retrieve seven unique random numbers from player
def get_numbers():
    playerNumbers = []
    print('Enter your Seven unqiue lucky numbers from 1 to 70 :')
    while len(playerNumbers) < 7:
        try: 
            num = int(input(f'Enter number {len(playerNumbers) + 1}:'))
            if num < 1 or num > 70:
                print('Number must be between 1 and 70, try again!')
            elif num in playerNumbers:
                print('Duplicate numbers are not allowed, try again!')
            else:
                playerNumbers.append(num)
        except ValueError:
            print('Invalid input, please enter a number')
    return playerNumbers

##  Define a function to generate seven unique numbers 
def generate_draw_numbers():
    return random.sample(range(1,71),7)

## Define a function to check if there are any matching numbers between both lists
def check_matching_numbers(playerNumbers,drawNumbers):
    return[n for n in playerNumbers if n in drawNumbers]

## Define the lottery game function
def play_lottery():
    print("\nWelcome to the Lucky Sevens Lottery! :)")
    
    ### Get player numbers using defined function
    playNumbers = get_numbers()
    playNumbers.sort()
    print(f'\nYour numbers in numerical order {playNumbers}')
    
    ### Get draw numbers using defined function
    drawNumbers = generate_draw_numbers()
    drawNumbers.sort()
    print(f'\nThe winning numbers for this draw {drawNumbers}')
    
    ### Get matching numbers using defined function
    matchingNumbers = check_matching_numbers(playNumbers,drawNumbers)
    if matchingNumbers:
        print(f'\nCongratulations! {len(matchingNumbers)} number(s) matched: {matchingNumbers}')
    else:
        print('\nBetter luck next time! Keep on betting to increase you chances of winning')
    
## Define a function to offer player option to replay lottery game
def main():
    while True:
        play_lottery()
        replay = input('\nWould you like to play another round?? Enter(YES/NO) or (Y/N)').strip().upper()
        if replay not in ['YES','Y']:
            print('Thank you for playing Lucky Sevens Lottery. Goodbye! :)')
            break
if __name__ == "__main__":
    main()