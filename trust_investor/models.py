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

import json
import random
import datetime


doc = """
This is a standalone Trust-Investor game. Both participants are endowed with 5 tokens and participant always play as an investor.
The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
Credits: The implementation for this game is adopted from the trust game
    template from the standard otree demo games.
The tokens are chosen to make the choices discrete: that people can only pass along integer units.
"""


class Constants(BaseConstants):
    name_in_url = 'TI'
    players_per_group = None
    num_rounds = 1
    token_to_point = 20 # Conversion rate for token to points: 1:20

    # Note, this is sourcing from another app that goes first. The game does
    # not change, except for the change of fixed roles.
    instructions_template = 'trust_responder/instructions.html'

    # Initial amount allocated to each player
    endowment = 5
    multiplier = 3

    with open("2019_Data.json", "r") as f:
        TR_list = json.loads(f.read())['TR']



class Subsession(BaseSubsession):
    # full TR profile: for determining the payoff
    pass

class Group(BaseGroup):
    pass
    # sent_back_amount = models.CurrencyField(doc="""Amount sent back by P2""", min=c(0))

    # def sent_back_amount_max(self):
    #     return self.sent_amount * Constants.multiplier

    # def set_payoffs(self):
    #     p1 = self.get_player_by_id(1)
    #     # p2 = self.get_player_by_id(2)
    #     p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
    #     p2.payoff = self.sent_amount * Constants.multiplier - self.sent_back_amount


class Player(BasePlayer):
    sent_amount = models.IntegerField(
        min=0,
        max=Constants.endowment,
        doc="""Amount sent by P1""",
        label="Please enter an amount between 0 and 5:",
    )
    payoff_token = models.IntegerField()
    # This is an index out of all responses collected previously
    random_responder_index = models.IntegerField() 
    responder_return_amount = models.IntegerField()
    

    def set_payoffs(self):
        # Pull for a random responder, for the profile
        random.seed(self.participant.label) # use participant_id to set the seed
        random_responder_index = random.choice(range(0, len(Constants.TR_list)))
        random_responder_profile = Constants.TR_list[random_responder_index]
        # Keep a copy of responder profile
        self.random_responder_index = random_responder_index
        # pull for responder choice with the sent amount
        responder_return = int(random_responder_profile[self.sent_amount])
        # Keep a copy of the returned amount
        self.responder_return_amount = responder_return


        # P1 payoff: endownment - sent + returned
        self.payoff_token = int(Constants.endowment \
                - self.sent_amount \
                + self.responder_return_amount)
        self.payoff = self.payoff_token * 20

    clicktime_pg0 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg1 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg2 = models.StringField() #get time of participant when welcome page is submitted
    def get_time0(self):
        self.clicktime_pg0 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time1(self):
        self.clicktime_pg1 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time2(self):
        self.clicktime_pg2 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
