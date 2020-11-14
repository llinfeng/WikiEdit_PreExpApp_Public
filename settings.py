


from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 0.00,
    'main_part_round_num' : 5,  #Edit the number of rounds here or in the models.py of the respective App
    'doc': "",
}

SESSION_CONFIGS = [
    {
        # Game 1 - Holt & Laury, multiple price list
        'name': 'production',
        'display_name': "Consent + Games + Survey for production",
        'num_demo_participants': 1,
        'app_sequence': ['Consent', 'mpl',
            # Elicit the strategy profile using the strategy method first,
            'trust_responder',
            # Given the elicitation, students now know how the opponent plays.
            'trust_investor', 
            'guess_two_thirds', 
            'simple_knapsack', 
            'survey'
            ],
    },
    # Test each game individually
    {
        'name': 'Intro',
        'display_name': "Consent Form - Test",
        'num_demo_participants': 1,
        'app_sequence': ['Consent'],
    },
    {
        'name': 'HT',
        'display_name': "Multiple Price List - Test",
        'num_demo_participants': 1,
        'app_sequence': ['mpl'],
    },
    dict(
        # Game 3 - Trust - responder
        name='TR',
        display_name="Trust Responder - Test",
        num_demo_participants=1,
        app_sequence=['trust_responder'],
    ),
    dict(
        # Game 2 - Trust - investor
        name='TI',
        display_name="Trust Investor - Test",
        num_demo_participants=1,
        app_sequence=['trust_investor'],
    ),
    dict(
        # Game 4 - p-Beauty contest
        name='guess_two_thirds',
        display_name="p-Beauty contest - Test",
        num_demo_participants=1,
        app_sequence=['guess_two_thirds'],
    ),
    {
        # Game 6 - Knapsack game
        'name': 'knapsack',
        'display_name': "Packing your Suitcase - Tets",
        'num_demo_participants': 1,
        'app_sequence': ['simple_knapsack'],
    },
    dict(
        # Concluding survey: ask about gender and other survey questions
        name='survey',
        display_name='Survey - Test',
        num_demo_participants=1,
        app_sequence=['survey'],
    ),
]

ROOMS = [
    dict(
        # Note, name enters the raw URL. Need to be ambiguous as well.
        name='Econ401',
        display_name='Econ 401 students (450 max)',
        participant_label_file='_room/Econ401.txt',
        use_secure_urls=True
    ),
    dict(
        # Note, name enters the raw URL. Need to be ambiguous as well.
        name='Econ401_backup',
        display_name='Econ 401 students (Backup)',
        participant_label_file='_room/Econ401_backup.txt',
        use_secure_urls=True
    ),
    ]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
# Note, there cannot be fractions in currency
USE_POINTS = True

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')
AUTH_LEVEL = "STUDY"

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """"""

# don't share this with anybody. (This is a newly created secrete key from a burner empty repo)
SECRET_KEY = 'blahblah'


# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
