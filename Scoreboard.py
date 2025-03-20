class Scoreboard:
    def __init__(self, player1_name, player2_name, player1_score = 0, player2_score = 0, round = 0):
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.round = round
    
    def get_p1_score(self):
        return self.player1_score
    
    def get_p2_score(self):
        return self.player2_score

    def get_round(self):
        return self.round
    
    def increment_p1_score(self):
        self.player1_score += 1
    
    def increment_p2_Score(self):
        self.player2_score += 1
    
    def increment_round(self):
        self.round += 1

