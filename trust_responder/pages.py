from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


# variables for all templates
def vars_for_all_templates(self):
    # Count current game over full app_sequence
    current_game = 'trust_responder' # Hard coding the current game
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


class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'player'
    form_fields = ['sent_back_amount']
    investment_amount = 0

    def vars_for_template(self):
        tripled_amount = self.investment_amount * Constants.multiplier
        responder_total = tripled_amount + Constants.endowment
        return dict(
                investment_amount = self.investment_amount,
                tripled_amount=tripled_amount,
                responder_total=responder_total
        )

# 2020-10-28 - for unknown reasons, these cannot be SendBack0, SendBack1 ==> fails to deploy on Heroku.
class SendBack_0(SendBack):
    investment_amount = 0
    form_model = 'player'
    form_fields = ['sent_back_given_0']
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time1()

class SendBack_1(SendBack):
    investment_amount = 1
    form_model = 'player'
    form_fields = ['sent_back_given_1']
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time2()

class SendBack_2(SendBack):
    investment_amount = 2
    form_model = 'player'
    form_fields = ['sent_back_given_2']
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time3()

class SendBack_3(SendBack):
    investment_amount = 3
    form_model = 'player'
    form_fields = ['sent_back_given_3']
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time4()

class SendBack_4(SendBack):
    investment_amount = 4
    form_model = 'player'
    form_fields = ['sent_back_given_4']

    def before_next_page(self):
        # Label the clicktime
        self.player.get_time5()

class SendBack_5(SendBack):
    investment_amount = 5
    form_model = 'player'
    form_fields = ['sent_back_given_5']

    def before_next_page(self):
        self.player.set_payoffs()
        self.player.get_time6()

    


class Results(Page):
    """This page displays the earnings of each player"""

    def vars_for_template(self):
        sent_amount = self.player.payment_round, #payment round coincides with the sent-amount

        return dict(
                # Notify which round was picked for payment
                payment_round = self.player.payment_round + 1,
                sent_amount = sent_amount[0],
                tripled_amount=sent_amount[0] * Constants.multiplier,
                p2_send_back = self.player.sent_back_amount,
                )
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time7()

# This is for responder: we will have multiple send_back pages, and a
# payoff page announcing the round chosen for payment
page_sequence = [
    Introduction,
    SendBack_0, SendBack_1, SendBack_2, SendBack_3, SendBack_4, SendBack_5,
    Results,
]
