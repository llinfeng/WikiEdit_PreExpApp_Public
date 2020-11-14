from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

# Prepare for rand number generator, a test of what random numbers are we getting
from random import randrange
from random import seed as rand_set_seed


# variables for all templates
def vars_for_all_templates(self):
    # Count current game over full app_sequence
    current_game = Constants.name_in_url
    full_app_sequence = self.session.config['app_sequence']
    current_game_count = full_app_sequence.index(current_game)
        # Note: +1 for adjusting the index, and -1 again for skipping Intro page as a "Game"
    total_game_count = len(full_app_sequence) - 2
        # -2 to exclude Consent app + Concluding Survey app as a "Game".

    return {
        'lottery_a_lo': c(Constants.lottery_a_lo),
        'lottery_a_hi': c(Constants.lottery_a_hi),
        'lottery_b_lo': c(Constants.lottery_b_lo),
        'lottery_b_hi': c(Constants.lottery_b_hi), 

        # Enumerate all games as it is.
        'Current_Game_enum': current_game_count,
        'Total_GameCount' : total_game_count
    }


# *** CLASS INSTRUCTIONS *** #
class Instructions(Page):

    # only display instruction in round 1
    def is_displayed(self):
        return self.subsession.round_number == 1

    # variables for template
    def vars_for_template(self):
        return {
            'num_choices':  len(self.participant.vars['mpl_choices'])
        }

    def before_next_page(self):
        # Label the clicktime
        self.player.get_time1()


# *** PAGE DECISION *** #
class Decision(Page):

    # form model
    form_model = 'player'

    # form fields
    def get_form_fields(self):

        # unzip list of form_fields from <mpl_choices> list
        form_fields = [list(t) for t in zip(*self.participant.vars['mpl_choices'])][1]

        # provide form field associated with pagination or full list
        if Constants.one_choice_per_page:
            page = self.subsession.round_number
            return [form_fields[page - 1]]
        else:
            return form_fields

    # variables for template
    def vars_for_template(self):

        # specify info for progress bar
        total = len(self.participant.vars['mpl_choices'])
        page = self.subsession.round_number
        progress = page / total * 100

        if Constants.one_choice_per_page:
            return {
                'page':      page,
                'total':     total,
                'progress':  progress,
                'choices':   [self.player.participant.vars['mpl_choices'][page - 1]]
            }
        else:
            return {
                'choices':   self.player.participant.vars['mpl_choices']
            }

    # set player's payoff
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time2()

        # unzip indices and form fields from <mpl_choices> list
        round_number = self.subsession.round_number
        form_fields = [list(t) for t in zip(*self.participant.vars['mpl_choices'])][1]
        indices = [list(t) for t in zip(*self.participant.vars['mpl_choices'])][0]
        index = indices[round_number - 1]

        # if choices are displayed sequentially
        if Constants.one_choice_per_page:

            # replace current choice in <choices_made>
            current_choice = getattr(self.player, form_fields[round_number - 1])
            self.participant.vars['mpl_choices_made'][index - 1] = current_choice

            # if current choice equals index to pay ...
            if index == self.player.participant.vars['mpl_index_to_pay']:
                # set payoff
                self.player.set_payoffs()

            # after final choice
            if round_number == Constants.num_choices:
                # determine consistency
                self.player.set_consistency()
                # set switching row
                self.player.set_switching_row()

        # if choices are displayed in tabular format
        if not Constants.one_choice_per_page:

            # replace choices in <choices_made>
            for j, choice in zip(indices, form_fields):
                choice_i = getattr(self.player, choice)
                self.participant.vars['mpl_choices_made'][j - 1] = choice_i

            # set payoff
            self.player.set_payoffs()
            # determine consistency
            self.player.set_consistency()
            # set switching row
            self.player.set_switching_row()


# This is the Curiosity elicitation page 
class Curiosity(Page):
    '''
    Elicit WTP bounded from above by $4 ==> since the lowest-paying lottery is
    1, this number is more or less arbitrary
    '''
    form_model = 'player'
    form_fields = [
            'mpl_WTP',
            # No need to include these as form fields, as we are not submitting them?
            # 'curiosity_random_num', 'curiosity_reveal'
            ]

    def vars_for_template(self):
        # Code copied from the Result page

        # unzip <mpl_choices> into list of lists
        choices = [list(t) for t in zip(*self.participant.vars['mpl_choices'])]
        indices = choices[0]

        # get index, round, and choice to pay
        index_to_pay = self.player.participant.vars['mpl_index_to_pay']
        round_to_pay = indices.index(index_to_pay) + 1

        choice_to_pay = self.participant.vars['mpl_choices'][round_to_pay - 1]

        if Constants.one_choice_per_page:
            return {
                # 'choice_to_pay':  [choice_to_pay],
                # 'option_to_pay':  self.player.in_round(round_to_pay).option_to_pay,
                'payoff':         self.player.in_round(round_to_pay).payoff,
            }
        else:
            return {
                # 'choice_to_pay':  [choice_to_pay],
                # 'option_to_pay':  self.player.option_to_pay,
                'payoff':         self.player.payoff
            }

    def before_next_page(self):
        # Label the clicktime
        self.player.get_time3()
        # Set the seed using the participant label
        rand_set_seed(self.participant.label)
        curiosity_random_num =  randrange(0, 40, 1) # Gen the random number
        self.player.curiosity_random_num  = curiosity_random_num # keep a copy of it.
        # Keep a log of what was the original lottery outcome
        self.player.payoff_lottrey = self.player.payoff

        print("The random number chosen is: {}".format(curiosity_random_num))

        if self.player.mpl_WTP >= curiosity_random_num:
            self.player.payoff -= curiosity_random_num
            self.player.curiosity_reveal = True
        else:
            # not change to payoff, and
            self.player.curiosity_reveal = False
            print("WTP < random number ==> no payment change")






# *** PAGE RESULTS *** #
class Results(Page):
    # Show the result page only when WTP is larger than the random number
    # ==> computer 

    def is_displayed(self):
        # Generate a random number here
        # make the random available to the template, and inspect

        if Constants.one_choice_per_page:
            return self.subsession.round_number == Constants.num_rounds
        else:
            return True

    # variables for template
    def vars_for_template(self):

        # unzip <mpl_choices> into list of lists
        choices = [list(t) for t in zip(*self.participant.vars['mpl_choices'])]
        indices = choices[0]

        # get index, round, and choice to pay
        index_to_pay = self.player.participant.vars['mpl_index_to_pay']
        round_to_pay = indices.index(index_to_pay) + 1

        choice_to_pay = self.participant.vars['mpl_choices'][round_to_pay - 1]



        if Constants.one_choice_per_page:
            return {
                'choice_to_pay':  [choice_to_pay],
                'option_to_pay':  self.player.in_round(round_to_pay).option_to_pay,
                'payoff':         self.player.in_round(round_to_pay).payoff,
            }
        else:
            return {
                'choice_to_pay'       : [choice_to_pay],
                'option_to_pay'       : self.player.option_to_pay,
                'payoff'              : self.player.payoff, # This is updated from the previous page if WTP is paid
                'computer_random_num' : c(self.player.curiosity_random_num),
                'real_computer_random_num' : self.player.curiosity_random_num,
                'curiosity_reveal'    : self.player.curiosity_reveal,
                'WTP'                 : c(self.player.mpl_WTP),
                
            }
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time4()


# *** PAGE SEQUENCE *** #
page_sequence = [Decision, Curiosity]

if Constants.instructions:
    page_sequence.insert(0, Instructions)

if Constants.results:
    page_sequence.append(Results)
