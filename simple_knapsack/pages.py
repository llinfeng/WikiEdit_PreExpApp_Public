import sys
sys.path.append("..")

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from utils import composer #Throws error in IDE but works ;)

# variables for all templates
def vars_for_all_templates(self):
    # Count current game over full app_sequence
    current_game = 'simple_knapsack' # Hard coding the current game
    full_app_sequence = self.session.config['app_sequence']
    current_game_count = full_app_sequence.index(current_game)
        # Note: +1 for adjusting the index, and -1 again for skipping Intro page as a "Game"
    total_game_count = len(full_app_sequence) - 2
        # -2 to exclude Consent app + Concluding Survey app as a "Game".

    return {
        # Enumerate all games as it is.
        'Current_Game_enum': current_game_count,
        'Total_GameCount' : total_game_count
    }



class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1
    
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
            'num_rounds' : 3 # this is a comment in the introduction.
            }

    def before_next_page(self):
        # Label the clicktime
        self.player.get_time1()



class SelectionPage(Page):
    # def is_displayed(self):
    #     return self.participant.vars['quiz_successful']

    def vars_for_template(self):

        # treatment = self.participant.vars['treatment']
        treatment = 'no_sol'
        part_set = self.participant.vars['part_set_sequence'][self.round_number-1]
        round_capacity = 0
        decision_table = ''

        # This is randomized in the 
        (decision_table, round_capacity) = composer.build_table(part_set, treatment)
        max_point_dic = {
                # Hard-coding the max points possible:
                1300 : 138,
                14 : 22,
                850 : 122
                }

        return{
            'round_part_set_number' : part_set,
            'round_capacity' : round_capacity,
            'max_point' : max_point_dic[round_capacity],
            'decision_table': decision_table,
            'treatment' : self.participant.vars['treatment'],
            # 'part_that_will_be_drawn' : self.participant.vars['parts_drawn'][self.round_number-1]
        }

    form_model = 'player'
    form_fields = ['round_weight', 'round_value', 'round_selection', 'total_weight', 'total_value']

    def before_next_page(self):
        self.participant.vars['rounds'] = self.round_number
        self.participant.vars['weight_' + str(self.round_number)] = int(self.player.total_weight)
        self.participant.vars['value_'+ str(self.round_number)] = int(self.player.total_value)
        self.player.payoff = int(self.player.total_value)

        self.player.get_time2()

class PayoffPage(Page):
    # Payoff page pending
    pass

page_sequence = [
        Introduction,
        SelectionPage
        ]
