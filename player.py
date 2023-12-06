class Player:
    def __init__(self):
        self.id = None
        self.name = None
        self.points = None
        self.opponent_ids = []
        self.won_opponent_ids = []
        self.drawn_opponent_ids = []
        self.lost_opponent_ids = []
        self.results = []
        self.buchholz = None
        self.sonneborn_berger = None
        self.order = None