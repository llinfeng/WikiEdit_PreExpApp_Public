from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Survey(Page):
    # This is an all-in-one page, with all questions. The goal is to display all the questions in full
    # We can discuss slicing things into multiple pieces/pages.
    form_model = 'player'
    form_fields = [
            # Q1 
            'competitiveness',
            # Q2
            'trust',
            # Q3 - Q5
            'procrastinate1',
            'procrastinate2',
            'procrastinate3',
            # Q6
            'risk_preference',
            # Q7 - Q12
            'risk_tolarence_dirving',
            'risk_tolarence_investment',  
            'risk_tolarence_sports',      
            'risk_tolarence_professional',
            'risk_tolarence_health',      
            'risk_tolarence_strangers',   
            # Q13 - 17
            'gender',
            'ethinicity',
            'major',
            'gpa_overall',
            'Econ401_LetterGrade', # Q17 - new one.
            ]

# Don't forget the GPA prediction task


class Pg1(Page):
    form_model = 'player'
    form_fields = [
            # Q1 
            'competitiveness',
            # Q2
            'trust',
            ]
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time1()

class Pg2(Page):
    form_model = 'player'
    form_fields = [
            # Q3 - Q5
            'procrastinate1',
            'procrastinate2',
            'procrastinate3',
            ]
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time2()

class Pg3(Page):
    form_model = 'player'
    form_fields = [
            # Q6
            'risk_preference',
            # Q7 - Q12
            'risk_tolarence_dirving',
            'risk_tolarence_investment',  
            'risk_tolarence_sports',      
            'risk_tolarence_professional',
            'risk_tolarence_health',      
            'risk_tolarence_strangers',   
            ]
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time3()

class Pg4(Page):
    form_model = 'player'
    form_fields = [
            # Q13 - 17
            'gender',
            'ethinicity',
            'major',
            ]
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time4()

class Pg5(Page):
    form_model = 'player'
    form_fields = [
            'gpa_overall',
            'Econ401_LetterGrade', # Q17 - new one.
            ]
    def before_next_page(self):
        # Label the clicktime
        self.player.get_time5()



class ExpFinishPage(Page):
    pass

# page_sequence = [Survey, Demographics]
# page_sequence = [Demographicskggj
# page_sequence = [Survey, ExpFinishPage]
page_sequence = [Pg1, Pg2, Pg3, Pg4, Pg5, ExpFinishPage]
# page_sequence = [ExpFinishPage]
