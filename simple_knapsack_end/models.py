from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'C. Lehmann & C. Haubitz'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'simple_knapsack_end'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    questionnaire_answers = models.StringField()
    final_total_payoff = models.CurrencyField()