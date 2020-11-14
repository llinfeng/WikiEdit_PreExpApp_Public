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

from django import forms as djforms


author = 'Linfeng Li'

doc = """
To present consent info, and collect the decision to participate via the checkbox.
"""


class Constants(BaseConstants):
    name_in_url = 'Consent'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(widget=djforms.CheckboxInput,
                                  initial=False
                                  )

