
from otree.api import *
c = cu

doc = '\nOne player decides how to divide a certain amount between himself and the other\nplayer.\nSee: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness\nand the assumptions of economics." Journal of business (1986):\nS285-S300.\n'
class C(BaseConstants):
    NAME_IN_URL = 'nodisclosure'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    ODD_ROLE = 'odd player'
    EVEN_PLAYER = 'even player'
    INSTRUCTIONS_TEMPLATE = 'nodisclosure/instructions.html'
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    kept = models.CurrencyField(doc='Amount dictator decided to keep for himself', label='I will keep', max=C.ENDOWMENT, min=0)
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = C.ENDOWMENT - group.kept
class Player(BasePlayer):
    option1or2 = models.StringField(choices=[['option1', 'option1'], ['option2', 'option2']], widget=widgets.RadioSelect)
    option2aor2b = models.StringField(choices=[['option2a', 'option2a'], ['option2b', 'option2b']], widget=widgets.RadioSelect)
class Introduction(Page):
    form_model = 'player'
class Option1or2(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.role==C.ODD_ROLE 
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(offer=C.ENDOWMENT - group.kept)
class Option2aor2b(Page):
    form_model = 'player'
    form_fields = ['option2aor2b']
    @staticmethod
    def is_displayed(player: Player):
        return player.role==C.ODD_ROLE and player.option1or2=="option1or2"
page_sequence = [Introduction, Option1or2, ResultsWaitPage, Results, Option2aor2b]