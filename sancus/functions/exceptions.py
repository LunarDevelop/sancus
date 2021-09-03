class NoLogChannel(Exception):
    print("No log Channel")

class NoActionChannel(Exception):
    pass

class CommandOnCooldown(Exception):
    
    def __init__(self,remain):
        self.remaining = remain