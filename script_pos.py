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
    pos.update('bob', 15)
    pos.update('alice', 100)
    pos.update('phil', 45)
    pos.update('jimmy',22)

    bob_wins=0
    alice_wins=0
    phil_wins=0
    jimmy_wins=0

    for i in range(100):
        forger = pos.forger(get_random_string(i))
        if forger == 'bob':
            bob_wins += 1
        elif forger == 'alice':
            alice_wins += 1
        elif forger == 'phil':
            phil_wins += 1
        elif forger == 'jimmy':
            jimmy_wins += 1
    
    print(f'Bob won {bob_wins} times') 
    print(f'Alice won {alice_wins} times')
    print(f'Phil won {phil_wins} times')
    print(f'Jimmy won {jimmy_wins} times')

if __name__ == '__main__':
    main()