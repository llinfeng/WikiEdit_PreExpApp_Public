from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency,
)


import datetime

doc = """
a.k.a. Keynesian beauty contest.

Players all guess a number; whoever guesses closest to
2/3 of the average wins.

See https://en.wikipedia.org/wiki/Guess_2/3_of_the_average

2020-10-28: note - did not implement the payment report page at the end.
    * No apparent reason to do it.
    * Sufficient feedback are given at the end of each round, for repeated beauty-context game.
"""

import json
import random



class Constants(BaseConstants):
    name_in_url = 'guess_two_thirds'
    players_per_group = None
    num_rounds = 5


    jackpot = Currency(100)
    guess_max = 100

    instructions_template = 'guess_two_thirds/instructions.html'

    with open("2019_Data.json", "r") as f:
        GuessRecord_Full = json.loads(f.read())['GS']
                


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # Do no bother with groups, as each individual is making individual decisions.
    # If specified, all subjects' group variable will be overwritten.
    pass


class Player(BasePlayer):
    guess = models.IntegerField(
        min=0, max=Constants.guess_max, label="Please pick a number between 0 and 100:"
    )
    is_winner = models.BooleanField(initial=False)

    two_thirds_avg = models.FloatField()
    best_guess = models.IntegerField()
    num_winners = models.IntegerField()
    payment_round = models.IntegerField() # Round picked for payment, in [1,5]

    def collect_all_guesses(self, round_number):
        # Initialize with seeding, the three opponents
        # 1. use participant_id to set the seed 
            # Note when testing with otree Demo: "self.participant.label" will be None == seed not set
            # running the demo session with Room, shall populate the participant.label properly.
        random.seed(self.participant.label)
        print(self.participant.label)
        # 2. Pull without replacement, from the historical record
        opponents_guesses = random.sample(Constants.GuessRecord_Full, 3)
        print(opponents_guesses)

        # Compose the guesses for the given round
        player_guess = self.guess
        others_guesses = [guess[round_number-1] for guess in opponents_guesses]

        # Collect into one guesses var
        others_guesses.append(player_guess)
        guesses = others_guesses
        # Convert all guesses into integers
        guesses = [
                # Note, only the guesses for the given round is collected into guesses
                # Converting into int works;
                int(guess) for guess in guesses
                ]
        return guesses


    def set_payoffs(self, round_number):

        # read off the guesses
        guesses = self.collect_all_guesses(round_number)

        num_players = 4

        two_thirds_avg = (2 / 3) * sum(guesses) / num_players

        self.two_thirds_avg = round(two_thirds_avg, 2)

        self.best_guess = min(
            guesses, key=lambda guess: abs(guess - self.two_thirds_avg)
        )

        winner_guess = [guess for guess in guesses if guess == self.best_guess]
        self.num_winners = len(winner_guess)


        if self.guess == self.best_guess:
            self.is_winner = True
            self.payoff = Constants.jackpot / self.num_winners

    def two_thirds_avg_history(self):
        return [p.two_thirds_avg for p in self.in_previous_rounds()]

    def calc_final_payment(self):
        all_payments = [p.payoff for p in self.in_previous_rounds()] + [self.payoff]
        # Seed with label, and decide which round to pay
        random.seed(self.participant.label)
        round_for_payment = random.randint(0, 4) # index for the round for payment
        # log the round for payment
        self.payment_round = round_for_payment + 1
        return (round_for_payment+1, all_payments[round_for_payment])

    clicktime_pg1 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg2 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg3 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg4 = models.StringField() #get time of participant when welcome page is submitted
    def get_time1(self):
        self.clicktime_pg1 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time2(self):
        self.clicktime_pg2 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time3(self):
        self.clicktime_pg3 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time4(self):
        self.clicktime_pg4 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
