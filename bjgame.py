
# all that stuff

import random
import time
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)


class Deck:
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['\033[2;31;50m♥\033[0m', '\033[2;31;50m♦\033[0m', '♣', '♠']
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]


class Dealer:
    def __init__(self):
        self.hand = []
        self.score = 0


    def add_card(self, deck):
        card = random.choice(deck.cards)
        self.hand.append(card)
        self.score += card.value()
        deck.cards.remove(card)



class Player:
    def __init__(self):
        self.nick = input("Enter your nickname: ")
        self.hand = []
        self.score = 0
        self.ace_count = 0
        self.money = 10000


    def add_card(self, deck):
        card = random.choice(deck.cards)
        self.hand.append(card)
        self.score += card.value()
        if card.rank == 'A':
            self.ace_count += 1
        while self.score > 21 and self.ace_count:
            self.score -= 10
            self.ace_count -= 1
        deck.cards.remove(card)


class BlackjackGame:
    def __init__(self):
        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck()
        self.blackjack = False
        self.bet = 0
        self.better_money = 0
        print(f"""----------------------------------------------------------------

                        • ♥ ♦ ♣ ♠ •
          Hi, {self.player.nick}. Welcome to the \033[2;35;50mBlackjack\033[0m Game!
                        • ♥ ♦ ♣ ♠ •

----------------------------------------------------------------
        """)


    def get_bets(self):
        if self.player.money > 0:
            try:
                self.better_money = f'{self.player.money:,}'.replace(',', '.')
                bet_input = input(f"Your current money is \033[2;32;50m${self.better_money}\033[0m\nPlace bets: ")
                self.bet = int(bet_input.replace('.', ''))
                if 0 < self.bet <= self.player.money:
                    self.player.money -= self.bet
                    self.better_money = f'{self.player.money:,}'.replace(',', '.')
                    better_bet = f'{self.bet:,}'.replace(',', '.')
                    print(f"Your bet is placed as \033[2;32;50m${better_bet}\033[0m\nYour current money is \033[2;32;50m${self.better_money}\033[0m")
                else:
                    if self.player.money <= 0:
                        print("\033[2;31;50mYou ran out of money :(\033[0m")
                    else:
                        print("\033[2;31;50mInvalid bet.\033[0m")
            except ValueError:
                print("\033[2;31;50mInvalid input.\033[0m")
        else:
            print("\033[2;35;50mYou are broke now but ill let you play anyways.\033[0m")


    def deal_cards(self):
        print(f"Dealing 2 cards to the dealer and the {self.player.nick}...")
        for i in range(2):
            self.player.add_card(self.deck)
            self.dealer.add_card(self.deck)
        time.sleep(2)
        if self.player.score == 21:
            print(f"""
            {self.player.nick} has: {self.player.hand[0].suit}{self.player.hand[0].rank} {self.player.hand[1].suit}{self.player.hand[1].rank} → {self.player.score} \033[2;35;50m!!BLACKJACK!!\033[0m
            Dealer has: {self.dealer.hand[0].suit}{self.dealer.hand[0].rank}
            """)
        else:
            print(f"""
            {self.player.nick} has: {self.player.hand[0].suit}{self.player.hand[0].rank} {self.player.hand[1].suit}{self.player.hand[1].rank} → {self.player.score}
            Dealer has: {self.dealer.hand[0].suit}{self.dealer.hand[0].rank}
            """)

    def player_turn(self):
        choice = input("\nDo you want to \033[2;32;50mhit\033[0m, \033[2;31;50mstay\033[0m, or \033[2;33;50mdouble\033[0m? ").lower()

        if choice == 'hit':
            self.hit()
        elif choice == 'stay':
            self.stand()
        elif choice == 'double':
            self.double()
        else:
            time.sleep(0.5)
            print("You choose to stand.")

    def hit(self):
        self.player.add_card(self.deck)
        time.sleep(0.5)
        print(f"Dealing a card to {self.player.nick}.")
        time.sleep(1)
        print(f"{self.player.nick}s current hand is:")
        for card in self.player.hand:
            print(f"{card.suit}{card.rank}", end=' ')
        print(f"→ {self.player.score}")
        if self.player.score > 21:
            pass

    @staticmethod
    def stand():
        time.sleep(0.5)
        print("You choose to stand.")

    def double(self):
        if self.player.money >= self.bet:
            self.bet *= 2
            self.player.money -= self.bet // 2
            time.sleep(1)
            print(f"{self.player.nick} chooses to double the bet.")
            self.hit()
            print("You cannot hit anymore.")
        else:
            time.sleep(1)
            print("\033[2;31;50mNot enough money to double.\033[0m")
            self.hit()

    def dealer_turn(self):
        time.sleep(1)
        print(f"Dealer had: {self.dealer.hand[0].suit}{self.dealer.hand[0].rank} {self.dealer.hand[1].suit}{self.dealer.hand[1].rank} → {self.dealer.score}")
        time.sleep(2)
        while self.dealer.score < 17:
            time.sleep(1.5)
            print("\nDealer chooses to hit.")
            self.dealer.add_card(self.deck)
            time.sleep(1)
            print(f"\nDealers current hand is:")
            for card in self.dealer.hand:
                print(f"{card.suit}{card.rank}", end=' ')
            print(f"→ {self.dealer.score}")

    def get_winner(self):
        if self.blackjack:
            self.player.money += int(self.bet * 2.5)
            print(f"\n{self.player.nick} got a Blackjack! You won \033[2;32;50m${int(self.bet * 2.5)}\033[0m dollars.")
        elif self.player.score > 21:
            print(f"\n\033[2;31;50m{self.player.nick} went bust. Dealer wins.\033[0m")
        elif self.dealer.score > 21:
            self.player.money += self.bet * 2
            print(f"\n\033[2;31;50mDealer went bust.\033[0m {self.player.nick} wins \033[2;32;50m${self.bet * 2}\033[0m dollars.")
        elif self.player.score > self.dealer.score:
            self.player.money += self.bet * 2
            print(f"\n{self.player.nick} wins \033[2;32;50m${self.bet * 2}\033[0m dollars.")
        elif self.dealer.score > self.player.score:
            print("\n\033[2;31;50mDealer wins.\033[0m")
        else:
            print("\n\033[2;33;50mIts a tie.\033[0m")
            self.player.money += self.bet

        self.better_money = f'{self.player.money:,}'.replace(',', '.')
        print(f"Your current money is \033[2;32;50m${self.better_money}\033[0m")

    def play_game(self):
        while True:
            self.player.hand = []
            self.dealer.hand = []
            self.bet = 0
            self.better_money = 0
            self.player.score = 0
            self.dealer.score = 0

            self.get_bets()
            time.sleep(2)
            self.deal_cards()

            if self.player.score == 21:
                self.blackjack = True

            if not self.blackjack:
                print(f"{self.player.nick}'s turn.")
                self.player_turn()

            time.sleep(1)

            if self.player.score <= 21:
                print(f"Dealers turn.")
                self.dealer_turn()
            else:
                print(f"Dealer had: {self.dealer.hand[0].suit}{self.dealer.hand[0].rank} {self.dealer.hand[1].suit}{self.dealer.hand[1].rank} → {self.dealer.score}")
            time.sleep(1)
            self.get_winner()
            time.sleep(1)
            choice = input("One more? (\033[2;32;50my\033[0m/\033[2;31;50mn\033[0m): ")
            if choice == 'n':
                print(f"\033[2;35;50mBye {self.player.nick}. See you later!\033[0m")
                break
            elif choice == 'y':
                pass
            else:
                print("\033[2;31;50mSo that means yes?\033[0m")

if __name__ == '__main__':
    game = BlackjackGame()
    game.play_game()
