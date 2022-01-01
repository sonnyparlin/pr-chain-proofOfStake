from ProofOfStake import ProofOfStake
from Lot import Lot
import string
import random

def get_random_string(length):
    letters = string.ascii_lowercase
    result_string = ''.join(random.choice(letters) for i in range(length))
    return result_string

def main():
    pos = ProofOfStake()
    pos.update('bob', 10)
    pos.update('alice', 100)

    bob_wins=0
    alice_wins=0

    for i in range(100):
        forger = pos.forger(get_random_string(i))
        if forger == 'bob':
            bob_wins += 1
        elif forger == 'alice':
            alice_wins += 1
    
    print(f'Bob won {bob_wins} times') 
    print(f'Alice won {alice_wins} times')

if __name__ == '__main__':
    main()