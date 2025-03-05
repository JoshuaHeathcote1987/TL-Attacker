class Command:
    def __init__(self, cooldown: int, button: str, duration: float, amount: int):
        self.cooldown = cooldown    # How long before the action can be used again
        self.button = button        # What button is pressed
        self.duration = duration    # How long the button is pressed for
        self.amount = amount        # How many times the button should be pressed