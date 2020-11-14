from ._builtin import Page, WaitPage

# variables for all templates
def vars_for_all_templates(self):
    # Count current game over full app_sequence
    current_game = 'guess_two_thirds' # Hard coding the current game
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

    def before_next_page(self):
        # Label the clicktime
        self.player.get_time1()


class Guess(Page):
    form_model = 'player'
    form_fields = ['guess']

    def before_next_page(self):
        self.player.set_payoffs(
                round_number = self.round_number
                )
        # Label the clicktime
        self.player.get_time2()

    def vars_for_template(self):
        return dict(
                the_round_number = self.round_number
                )


class Results(Page):
    def vars_for_template(self):
        sorted_guesses = sorted(self.player.collect_all_guesses(self.round_number))

        return dict(
                sorted_guesses = sorted_guesses,
                the_round_number = self.round_number
                )

    def before_next_page(self):
        # Label the clicktime
        self.player.get_time3()

class FinalResult(Page):
    def is_displayed(self):
        return self.round_number == 5

    def vars_for_template(self):
        # select a round for payment
        paid_round_number, paid_amount = self.player.calc_final_payment()
        return dict(
                payment_round = paid_round_number,
                payment_amount = paid_amount
                )

    def before_next_page(self):
        # Label the clicktime
        self.player.get_time4()


page_sequence = [Introduction, Guess, Results, FinalResult]
