
from otree.api import *
c = cu

doc = '\nIn a common value auction game, players simultaneously bid on the item being\nauctioned.<br/>\nPrior to bidding, they are given an estimate of the actual value of the item.\nThis actual value is revealed after the bidding.<br/>\nBids are private. The player with the highest bid wins the auction, but\npayoff depends on the bid amount and the actual value.<br/>\n'
class C(BaseConstants):
    NAME_IN_URL = 'Firstpriceauction'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    EVALUATE_MIN = cu(0)
    EVALUATE_MAX = cu(100)
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    session = subsession.session
    import random
    
    subsession.group_randomly()
    for p in subsession.get_players():
        if p.id_in_group == 1:
            p.role_type = "seller"
            p.bid_amount = 0 
        elif p.id_in_group == 2:
            p.role_type = "buyer"
        elif p.id_in_group == 3:
            p.role_type = "buyer"
    if subsession.round_number == 1:
        for p in subsession.get_players():
            if p.id_in_group == 1:
                p.role_type = "seller"
            elif p.id_in_group == 2:
                p.role_type = "buyer"
            elif p.id_in_group == 3:
                p.role_type = "buyer"
    # set the same role type in each match 
    elif subsession.round_number > 1:
        for p in subsession.get_players():
            p.role_type = p.in_round(subsession.round_number - 1).role_type
    for player in subsession.get_players():
        if player.role_type == "seller":
            player.item_value = 0
        else:
            value = random.uniform(C.EVALUATE_MIN, C.EVALUATE_MAX)
            player.item_value = round(value, 2)
class Group(BaseGroup):
    highest_bid = models.CurrencyField()
def set_winner(group: Group):
    import random
    players = [p for p in group.get_players() if p.role_type == "buyer"]
    group.highest_bid = max([p.bid_amount for p in players])
    players_with_highest_bid = [p for p in players if p.bid_amount == group.highest_bid]
    winner = random.choice(players_with_highest_bid) # if tie, winner is chosen at random
    winner.is_winner = True
    for p in players:
        set_payoff(p)
    if p.role_type == "seller":
          p.bid_amount = 0 
    if p.role_type == "seller":
          p.item_value = 0
class Player(BasePlayer):
    item_value = models.CurrencyField(doc='Estimate of the common value may be different for each player')
    bid_amount = models.CurrencyField(doc='Amount bidded by the player', label='Bid amount', max=100, min=0)
    is_winner = models.BooleanField(doc='Indicates whether the player is the winner', initial=False)
    role_type = models.StringField()
def set_payoff(player: Player):
    group = player.group
    for p in group.get_players():
        if p.role_type == "seller":
            p.payoff = group.highest_bid
        elif p.role_type == "buyer":
            if p.is_winner:
                p.payoff = p.item_value - p.bid_amount
                # if p.payoff < 0:
                #     p.payoff = 0
            else:
                p.payoff = 0
class Introduction(Page):
    form_model = 'player'
class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']
    timeout_seconds = 60
    @staticmethod
    def is_displayed(player: Player):
        return  player.role_type == "buyer"
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_winner
class Results(Page):
    form_model = 'player'
page_sequence = [Introduction, Bid, ResultsWaitPage, Results]