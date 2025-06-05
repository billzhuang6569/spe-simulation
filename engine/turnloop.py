class TurnEngine:
    def __init__(self, turns: int = 10):
        self.turns = turns

    def run_dummy(self):
        for i in range(self.turns):
            yield f"Turn {i + 1}: dummy event"
