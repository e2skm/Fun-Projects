# Lucky Sevens Lottery - Pylearn project6
## Import the random liabrary
import random

## Create a variable to contain users number
playerNumbers =[0,0,0,0,0,0,0]

## Define a function to retrieve 7 user numbers
def get_numbers():
	for p in range(len(playerNumbers)):
		print(f'Enter your {p+1} lucky number from 1 to 69')
		playerNumbers[p] = int(input())
	return playerNumbers

## Create a variable to contain the draw numbers
drawNumbers = [1,1,1,1,1,1,1]

## Define a function to generate 7 random numbers between 1 to 69
def generate_seven_numbers():
	for i in range(len(drawNumbers)):
		drawNumbers[i] = random.randint(1,70)
	return drawNumbers

## Create a variable to store the winning numbers
matchingNumbers =[]

## Define a function to check for matching numbers using user entered numbers and generated numbers	
def check_matching_numbers(playerNumbers,drawNumbers):
	for i in range(7):
		for j in range(7):
			if playerNumbers[i] == drawNumbers[j]:
				matchingNumbers.append(drawNumbers[j])
	return matchingNumbers

## Store,Sort, and Display user entered numbers
playerNumbers = get_numbers()
playerNumbers.sort()
print(f'Here are your numbers in numerical order {playerNumbers}')

## Store,Sort, and Display generated numbers
drawNumbers = generate_seven_numbers()
drawNumbers.sort()
print(f'Here are the winning numbers in numerical order {drawNumbers}')

## Check if there are any numbers appearing in both lists 
matchingNumbers = check_matching_numbers(playerNumbers,drawNumbers)
if len(matchingNumbers) != 0:
	print(f'Congratulations your have {len(matchingNumbers)} winning number(s): {matchingNumbers} ')
else:
	print('Better luck next time, the more you bet the higher your chances of being a Millionaire, do not give up on your dreams.')
	
### NOTES:  Program does not ensure user does not enter a number from 1 to 69.
# Also it does not ensure user does not enter the same number.
# Draw numbers can contain a number more than once. 
# It is a lottery game with no money being involved.