import sys
sys.path.append("..")

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from utils import composer #Throws error in IDE but works ;)


class Results(Page):

    def is_displayed(self):
        return self.participant.vars['quiz_successful']

    def vars_for_template(self):
        #print('Weight Round 1:' + str(self.participant.vars['weight_1']))
        weight = []
        value = []
        rounds = self.participant.vars['rounds']
        print('Rounds:' + str(rounds))
        for r in range(1,rounds+1):
            weight.append(self.participant.vars['weight_' + str(r)])
            value.append(self.participant.vars['value_' + str(r)])
        
        print(weight)
        print(value)

        (sumvalue_cent, sumvalue_dollar, result_table) = composer.buildResultTable(rounds, weight, value)

        self.player.final_total_payoff = self.participant.payoff_plus_participation_fee()
        self.player.payoff = self.participant.payoff_plus_participation_fee()
        total_payoff = self.player.final_total_payoff

        return{
            'result_table' : result_table,
            'sumvalue_cent' : sumvalue_cent,
            'sumvalue_dollar' : sumvalue_dollar,
            'fixed_reward_dollar' : self.session.config['participation_fee'],
            'total_payoff' : total_payoff
        }


class Questionnaire(Page):

    def is_displayed(self):
        return (self.participant.vars['quiz_successful'] and not(self.participant.vars['treatment']=='no_sol'))

    def vars_for_template(self):

        questions = ['The algorithm performed reliably.',
                    'I was able to rely on the algorithm to function properly.',
                    'The algorithm uses appropriate methods to reach decisions.',
                    'The algorithm makes use of all the knowledge and information available to it to produce its solution to the problem.',
                    'I understood how the algorithm assisted me with decisions I had to make.',
                    'Although I may not know exactly how the algorithm worked, I know how to use it to make decisions about the inventory levels.',
                    'When I was uncertain about a decision, I believed the algorithm rather than myself.',
                    'Even if I have no reason to expect the algorithm will be able to solve a difficult problem, I still feel certain that it will.',
                    'I found the algorithm suitable to my style of decision-making.',
                    'I liked using the algorithm for decision-making.',
                    'I enjoyed the task in this HIT.',
                    'I am satisfied with the reward I receive for participating in this HIT.',
                    'I would take part in a similar HIT again in the future.']

        (num_questions, questionnaire_table) = composer.buildLikertScale(questions)

        return{
            'questionnaire_1' : questionnaire_table,
            'num_questions' : num_questions
        }

    form_model = 'player'
    form_fields = ['questionnaire_answers']


page_sequence = [
    Questionnaire,
    Results
]
