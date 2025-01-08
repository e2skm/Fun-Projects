# Get a random joke - Fun project13
## Import the necessary library
import requests

## Define a function to get a joke
def get_joke():
    url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['type'] == 'twopart':
            print(f'Setup:{data['setup']}')
            print(f'Delivery:{data['delivery']}')
        elif data['type'] == 'single':
            print(f'Joke: {data['joke']}')
    else:
        print(f'Error unable to fetch a joke')
        
if __name__ == "__main__":
    
get_joke()