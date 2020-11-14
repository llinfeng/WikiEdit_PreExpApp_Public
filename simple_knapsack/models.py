
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


import itertools
import random


author = 'C. Lehmann & C. Haubitz'

doc = """
Your app description
"""

import datetime

class Constants(BaseConstants):
    name_in_url = 'simple_knapsack'
    players_per_group = None
    num_rounds = 3  #Edit the number of rounds here and in the global session variables, since the round number is important for preceeding Apps as well
        # this will dictate how many rounds the game runs
    

class Subsession(BaseSubsession):
    # for p in self.get_players():
    #     #part_drawn = composer.getRandomPart(p.participant.vars['part_set_sequence'][self.round_number-1])
    #     part_drawn = composer.getRandomPart(1)
    def creating_session(self):
        treatment = itertools.cycle([
            'no_sol',
            ])
        
        # Why 3 lines are printed from this loop?
        for p in self.get_players():
            print(len(self.get_players()))
            #p.participant.vars['num_rounds'] = self.session.config['main_part_round_num']               #Max Number of rounds in Main App, which we already have to know beforehand  ###Not used anymore since we declare number of rounds in global session variables
            p.participant.vars['treatment'] = next(treatment)
            p.participant.vars['quiz_successful'] = True                #Initially we set this variable true. As soon as the quizz is failes, this is set to FALSE
            
            #DEVELOPMENT REMOVE FOR PRODUCTION
            #part_set_sequence = [1,1,1,1,1,1,1,1,1,1]
            
            # part_set_sequence = [1,2,3]
            part_set_sequence = [1,2,3]
            random.seed(p.participant.label) # use participant_id to set the seed
            random.shuffle(part_set_sequence) #==> need update here, order may be repetitive
                    # fixed sequence suffice? => pull for a random number for each round.
            p.participant.vars['part_set_sequence'] = part_set_sequence
            # parts_drawn = []
            # for part_set in part_set_sequence:
            #     parts_drawn.append(composer.getRandomPart(part_set))
            
            # p.participant.vars['parts_drawn'] = parts_drawn
            print('Participant ID in subsesseion: ' + str(p.id_in_subsession) + '| Treatment: ' + p.participant.vars['treatment'] + '\t | Part Set Sequence: ' + str(part_set_sequence))
            




    

class Group(BaseGroup):
    pass


class Player(BasePlayer):  
    round_set_number = models.IntegerField()
    round_capacity = models.FloatField()
    round_weight = models.StringField()
    round_value = models.StringField()
    round_selection = models.StringField()
    total_weight = models.FloatField()
    total_value = models.FloatField()

    clicktime_pg1 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg2 = models.StringField() #get time of participant when welcome page is submitted
    def get_time1(self):
        self.clicktime_pg1 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time2(self):
        self.clicktime_pg2 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

