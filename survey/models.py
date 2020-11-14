from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import datetime

from django.forms.widgets import CheckboxSelectMultiple
# To incorporate a MCMA field. Source: https://github.com/yatsky/otree-examples

def make_scaled_fields(levels):
    '''
    Produce a radio-button with **horizontal** layout.
    - levels: accepts an integer, denoting the total number of levels. 
    - labels: Leave the label blank, as each questions have "two pieces: 
            along with the question, there is a second piece explaining what
            are the options.  
            We need to typeset each question individually.
    '''
    return models.IntegerField(
            widget = widgets.RadioSelectHorizontal,
            choices=list(range(0, levels+1)),
            label="",
    )

class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

    # In HTML: {% formfields %} sufficies to pull in all the survey questions assigned to this page.


class Player(BasePlayer):
    '''
    ## Rearranging the questions
    1. Competitiveness 
    2. trust, 
    3. procrastinate 
    4. risk
    5. individual characteristics
    All things about yourself should be clustered to the end.
    '''

    clicktime_pg1 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg2 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg3 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg4 = models.StringField() #get time of participant when welcome page is submitted
    clicktime_pg5 = models.StringField() #get time of participant when welcome page is submitted
    def get_time1(self):
        self.clicktime_pg1 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time2(self):
        self.clicktime_pg2 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time3(self):
        self.clicktime_pg3 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time4(self):
        self.clicktime_pg4 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def get_time5(self):
        self.clicktime_pg5 = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Q1 - 10 point scale
    competitiveness = make_scaled_fields(10)
    # Q: How competitive do you consider yourself to be?
    # Please choose a value on the scale below, where the value 0 means 'not competitive at all' and the value 10 means 'very competitive'.

    # Q2 - radio select
    trust = models.IntegerField(
            widget=widgets.RadioSelect,
            label="",
            # We went with the following and did not hear a complaint.
            choices=(
                # Let the trust question be monotone in "trust". 
                [4, "Most people can be trusted"],
                [3, "Can't be too careful"],
                [2, "Other, depends"],
                [1, "Don't know"],
                ),
            )

    # Q3, Q4, Q5 - Plan Procrastinate questions (#3)
    procrastinate1 = make_scaled_fields(10)
    procrastinate2 = make_scaled_fields(10)
    procrastinate3 = make_scaled_fields(10)

    #Q6 - Risk Preference
    risk_preference             = make_scaled_fields(10)
    #Q7 - Q12 - Risk tolerance in 6 scenario
    risk_tolarence_dirving      = make_scaled_fields(10) #Q7
    risk_tolarence_investment   = make_scaled_fields(10) #Q8
    risk_tolarence_sports       = make_scaled_fields(10) #Q9
    risk_tolarence_professional = make_scaled_fields(10) #Q10
    risk_tolarence_health       = make_scaled_fields(10) #Q11
    risk_tolarence_strangers    = make_scaled_fields(10) #Q12
    
    # Q13 - Gender
    # Gender question should be kept towards the end of the survey questions
    gender = models.StringField(
            label='',
            blank=False,
            widget=CheckboxSelectMultiple(
                # We went with the following and did not hear a complaint.
                choices=(
                    ("Female", "Female"),
                    ("Male", "Male"),
                    ("Transgender", "Transgender"),
                    ("Prefer not to say", "Prefer not to say"),
                    ),
                )
            )
    # Q14 - Ethnicity
    ethinicity = models.StringField(
            label='',
            widget=CheckboxSelectMultiple(
                # We went with the following and did not hear a complaint.
                choices=[
                    ("American Indian or Alaskan Native", "American Indian or Alaskan Native"),
                    ("Asian or Pacific Islander", "Asian or Pacific Islander"),
                    ("Black", "Black"),
                    ("Hispanic", "Hispanic"),
                    ("White", "White"),
                    ("Other", "Other"),
                    ("Decline to answer", "Decline to answer"),
                    ],
                )
            )

    # Q15 - major
    major = models.StringField(
            label='',
            widget=CheckboxSelectMultiple(
                # We went with the following and did not hear a complaint.
                choices=[
                    ("Economics", "Economics"),
                    ("Mathematics", "Mathematics"),
                    ("Statistics", "Statistics"),
                    ("Philosophy", "Philosophy"),
                    ("Business", "Business"),
                    ],
                )
            )

    # Q16 - GPA
    gpa_overall = models.FloatField(
            label = "",
            min = 0, max=4.3
            )
    
    # D12 - letter grade for Econ 401
    # Econ401_LetterGrade
    Econ401_LetterGrade = models.FloatField( 
            # Source: https://lsa.umich.edu/lsa/academics/lsa-requirements/grade-point-average/computing-your-grade-point-average.html
            choices=[
                [4.3, 'A+'], 
                [4.0, 'A'], 
                [3.7, 'A-'], 
                [3.3, 'B+'],
                [3.0, 'B'],
                [2.7, 'B-'],
                [2.3, 'C+'],
                [2.0, 'C'],
                [1.7, 'C-'],
                [1.3, 'D+'],
                [1.0, 'D'],
                [0.7, 'D-'],
                [0.0, 'E'],
                ],
            label = '',
            # Without a widget, the formfield will be a dropdown list by default.
            # widget=widgets.RadioSelect
            )  
    

