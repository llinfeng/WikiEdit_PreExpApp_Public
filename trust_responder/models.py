from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import random
import datetime

doc = """
This is a standalone Trust-responder game, where each participant is allocated with 5 tokens. The game is implemented using strategy method, where participant will see an investment of 0, 1, 2, 3, 4, 5 sequentially.
One round is chosen for payment. This game is adopted from: 
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
Credits: The implementation for this game is adopted from the trust game
    template from the standard otree demo games.
"""


class Constants(BaseConstants):
    name_in_url = 'TR'
    players_per_group = None
    num_rounds = 1

    instructions_template = 'trust_responder/instructions.html'

    # Initial amount allocated to each player
    endowment = 5
    multiplier = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # This is the responder portion, with 6 variables to collect for strategy method
    sent_back_given_0 = models.IntegerField(doc="""Tokens sent by responder""", 
            min=0, max=5,
            label = "Please enter an amount between 0 and 5"
            )
    sent_back_given_1 = models.IntegerField(doc="""Tokens sent by responder""", 
            min=0, max=8,
            label = "Please enter an amount between 0 and 8"
            )
    sent_back_given_2 = models.IntegerField(doc="""Tokens sent by responder""", 
            min=0, max=11,
            label = "Please enter an amount between 0 and 11"
            )
    sent_back_given_3 = models.IntegerField(doc="""Tokens sent by responder""",
            min=0, max=14,
            label = "Please enter an amount between 0 and 14"
            )
    sent_back_given_4 = models.IntegerField(doc="""Tokens sent by responder""",
            min=0, max=17,
            label = "Please enter an amount between 0 and 17"
            )
    sent_back_given_5 = models.IntegerField(doc="""Tokens sent by responder""",
            min=0, max=20,
            label = "Please enter an amount between 0 and 20"
            )
    payment_round = models.IntegerField()
    sent_back_amount = models.IntegerField()

    payoff_token = models.IntegerField() 

    def set_payoffs(self):
        # Gen payment round
        random.seed(self.participant.label) # use participant_id to set the seed
        rand_int_for_payment_round = random.randint(0,5) # get back an index
        # Store payment round
        self.payment_round = rand_int_for_payment_round
        
        # Collect sent-back-amount
        full_sentback = [
                self.sent_back_given_0, self.sent_back_given_1, 
                self.sent_back_given_2, self.sent_back_given_3, 
                self.sent_back_given_4, self.sent_back_given_5
                ]
        # the sent amount = rand_int_for_payment_round, as the indexes coincide
        sent_back_given_n = full_sentback[rand_int_for_payment_round]
        # Store sent back amount 
        self.sent_back_amount = sent_back_given_n


        # Modifying the p2 payoff: add endowment as well
        self.payoff_token = Constants.endowment \
            + rand_int_for_payment_round * Constants.multiplier\
            - self.sent_back_amount 

        self.payoff = self.payoff_token * 20


    # Put into the player class, as we'd like to keep these click-time entries in the dataset
    # Get a timetag
    clicktime_pg0 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg1 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg2 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg3 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg4 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg5 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg6 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg7 = models.StringField() #get time of participant when welcome page is submitted
    def get_time0(self):
        self.clicktime_pg0 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time1(self):
        self.clicktime_pg1 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time2(self):
        self.clicktime_pg2 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time3(self):
        self.clicktime_pg3 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time4(self):
        self.clicktime_pg4 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time5(self):
        self.clicktime_pg5 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time6(self):
        self.clicktime_pg6 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time7(self):
        self.clicktime_pg7 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
