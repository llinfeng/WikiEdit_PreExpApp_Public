import sys
sys.path.append("..")
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from utils import composer #Throws error in IDE but works ;)
import itertools
import random

author = 'C. Lehmann & C. Haubitz'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'simple_knapsack_start'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        treatment = itertools.cycle([
            #'no_sol',
            'opt_sol',
            'heur_sol'])
        
        for p in self.get_players():
            #p.participant.vars['num_rounds'] = self.session.config['main_part_round_num']               #Max Number of rounds in Main App, which we already have to know beforehand  ###Not used anymore since we declare number of rounds in global session variables
            p.participant.vars['treatment'] = next(treatment)
            p.participant.vars['max_trials'] = 1                        #Maximal number of trials to answer all questions in comprehension quizz correctly
            p.participant.vars['quiz_successful'] = True                #Initially we set this variable true. As soon as the quizz is failes, this is set to FALSE
            
            #DEVELOPMENT REMOVE FOR PRODUCTION
            #part_set_sequence = [1,1,1,1,1,1,1,1,1,1]
            
            part_set_sequence = [1,2,3,4,5]
            random.shuffle(part_set_sequence)
            p.participant.vars['part_set_sequence'] = part_set_sequence
            # parts_drawn = []
            # for part_set in part_set_sequence:
            #     parts_drawn.append(composer.getRandomPart(part_set))
            
            # p.participant.vars['parts_drawn'] = parts_drawn
            print('Participant ID in subsesseion: ' + str(p.id_in_subsession) + '| Treatment: ' + p.participant.vars['treatment'] + '\t | Part Set Sequence: ' + str(part_set_sequence))
            


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    participant_vars_dump_begin = models.StringField()
    number_trials = models.IntegerField(initial=0)

    Q1 = models.StringField(
        label='What is your task?',
        widget=widgets.RadioSelect)

    def Q1_choices(self):
        choices = [[1, 'It is my task to maximize the value of the selected items given the capacity of the backpack.'],
         [2, 'It is my task to minimize the value of the selected items given the capacity of the backpack.'],
         [3, 'It is my task to select the items randomly without exceeding the capacity of the backpack.']]
        random.shuffle(choices)
        return choices

    Q2 = models.StringField(
        label='What do you have to do in order to complete this HIT?',
        widget=widgets.RadioSelect)

    def Q2_choices(self):
        choices = [[1, 'I have to make my selection for ' + str(self.session.config['main_part_round_num']) + ' rounds with different sets of parts and backpacks with different capacities.'],
         [2, 'I have to selected 100 items in total.'],
         [3, 'I have to select items which value in all ' + str(self.session.config['main_part_round_num']) + ' rounds adds up to $2.']]
        random.shuffle(choices)
        return choices

    Q3 = models.StringField(
        label='My payoff includes',
        widget=widgets.RadioSelect)

    def Q3_choices(self):
        choices = [
         [1, '... the fixed reward of ' + str(self.session.config['participation_fee']) + ' and the sum of the value of all selected items in the ' + str(self.session.config['main_part_round_num']) + ' rounds.'],
         [2, '... the fixed reward of ' + str(self.session.config['participation_fee']) + ' and $0.10 for each selected item in the ' + str(self.session.config['main_part_round_num']) + ' rounds.'],
         [3, '... the fixed reward of ' + str(self.session.config['participation_fee']) + ' and $0.50 for each round in which I did not exceed the capacity of the backpack.']]
        random.shuffle(choices)
        return choices

