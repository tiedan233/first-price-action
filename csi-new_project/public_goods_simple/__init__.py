
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    PLAYERS_PER_GROUP = 6
    NUM_ROUNDS = 10
    ENDOWMENT = cu(100)
    MULTIPLIER = 3
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    session = subsession.session
    subsession.group_randomly()
class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
        group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    )
    for p in players:
        p.payoff = C.ENDOWMENT - p.contribution + group.individual_share
class Player(BasePlayer):
    contribution = models.CurrencyField(label='How much will you contribute', max=C.ENDOWMENT, min=0)
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
class Results(Page):
    form_model = 'player'
page_sequence = [Contribute, ResultsWaitPage, Results]