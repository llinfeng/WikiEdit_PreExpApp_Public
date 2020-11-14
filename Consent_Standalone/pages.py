from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from . import models


class InformedConsent(Page):
    # This is taken from an old oTree project, from https://github.com/chapkovski/consent_form
    form_model = models.Player
    form_fields = ['consent']
    timeout_submission = {'consent': False}

    def vars_for_template(self):
        pass
        # if self.session.config.get('name') == 'survey':
        #     self.template_name = 'consent/AltConsent.html'
        # return {'consent_timeout_min': math.ceil(self.timeout_seconds / 60)}

    def is_displayed(self):
        return self.round_number == 1

    def consent_error_message(self, value):
        if not value:
            return 'You must accept the consent form in order to proceed with the study!'

page_sequence = [InformedConsent]
