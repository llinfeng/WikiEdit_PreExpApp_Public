from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

# variables for all templates
def vars_for_all_templates(self):
    # Count current game over full app_sequence
    current_game = 'trust_investor' # Hard coding the current game
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
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time0()


class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'player'
    form_fields = ['sent_amount']

    def before_next_page(self):
        self.player.set_payoffs()
        self.player.get_time1()
    




class Results(Page):
    """This page displays the earnings of each player"""

    def vars_for_template(self):
        # Update the payoff piece
        return dict(
                sent_amount = self.player.sent_amount,
                sent_back_amount = self.player.responder_return_amount,
                )
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time2()


page_sequence = [
    Introduction,
    Send,
    Results,
]
