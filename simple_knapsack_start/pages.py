import sys
sys.path.append("..")

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from utils import composer #Throws error in IDE but works ;)


class WelcomePage(Page):
    def vars_for_template(self):
        return{
            'fixed_reward_dollar' : self.session.config['participation_fee']
        }


class Treatment(Page):
    def vars_for_template(self):

        treatment = self.participant.vars['treatment']
    
        #Get Text for Treatment
        (title, text_begin, table_explanation) = composer.getTextTreatmentPage(treatment)
              
        #Get Example Table for Treatment
        (decision_table, capacity) = composer.build_table('example', treatment)  #Add Table ID here (probably an example table)
        
        return{
            'text_begin': text_begin,
            'table_explanation': table_explanation,
            'round_capacity' : capacity,
            'decision_table': decision_table,
            'treatment' : treatment,
            'fixed_reward_dollar' : self.session.config['participation_fee'],
            'num_rounds' : 3
            }

class Comprehension(Page):

    form_model = 'player'
    form_fields = ['Q1', 'Q2', 'Q3']

    def error_message(self, value):
        print('values is', value)
        if ((value['Q1'] != '1') or (value['Q2'] != '1') or (value['Q3'] != '1')):
            self.player.number_trials += 1
            self.participant.vars['quiz_successful'] = False


class Test_Not_Passed(Page):

    def is_displayed(self):
        return not(self.participant.vars['quiz_successful'])



page_sequence = [
    #WelcomePage, 
    Treatment,
    Comprehension,
    Test_Not_Passed
]
