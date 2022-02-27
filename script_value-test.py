import random
import time

def main():
    SUPPLY=1000000000
    ORIGINAL_SUPPLY = SUPPLY
    LIQUIDITY = 2000000
    TOKEN_PRICE = LIQUIDITY / SUPPLY
    NUMBER_OF_TRANSACTIONS = 2000000
    PRICE_RANGE_LOW=20
    PRICE_RANGE_HIGH=1000

    start = time.time()
    for i in range(NUMBER_OF_TRANSACTIONS):
        USD_PRICE=random.randint(PRICE_RANGE_LOW,PRICE_RANGE_HIGH)
        NUM_TOKENS = USD_PRICE / TOKEN_PRICE

        if NUM_TOKENS < SUPPLY:
            if i % 10 != 5 and i % 10 != 9 and i % 10 != 3:
                #print(f'Buying {NUM_TOKENS} coins at {TOKEN_PRICE} per coin for {USD_PRICE}')
                # buy
                SUPPLY -= NUM_TOKENS
                LIQUIDITY += USD_PRICE
            else:
                #print(f'Selling {NUM_TOKENS} coins at {TOKEN_PRICE} per coin for {USD_PRICE}')
                #sell
                SUPPLY += NUM_TOKENS
                LIQUIDITY -= USD_PRICE

        TOKEN_PRICE = LIQUIDITY / SUPPLY
    end = time.time()

    print(f'Execution time was {end-start}')

    formatted_remaining_supply = "{:,.8f}".format(ORIGINAL_SUPPLY-SUPPLY)
    formatted_supply = "{:,.0f}".format(SUPPLY)
    formatted_price = "{:,.8f}".format(TOKEN_PRICE)
    formatted_liquidity = "{:,.0f}".format(LIQUIDITY)

    print(f'The number of tokens purchased {formatted_remaining_supply}')
    print(f'The current price of our coin is ${formatted_price}')
    print(f'We have {formatted_supply} tokens left')
    print(f'Market cap: ${formatted_liquidity}')

if __name__ == '__main__':
    main()
