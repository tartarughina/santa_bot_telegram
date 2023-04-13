import bisect
from random import randint, random

class Config:
    def __init__(self) -> None:
        self.tot_prob = 0
        self.distr = []

         # update the total probability at startup
        for x in Config.NAMES:
            self.tot_prob += x.get("probability")

        # set the distribution of the available names
        self.cdf()

        pass

    def get_citation(self) -> str:
        return Config.CITATIONS[randint(0, len(Config.CITATIONS) - 1)]
    
    def cdf(self) -> None:
        cumsum = 0
        for w in Config.NAMES:
            cumsum += w.get("probability")
            self.distr.append(cumsum / self.tot_prob)

    def get_rand_name(self) -> str:    
        return Config.NAMES[bisect.bisect(self.distr, random())].get("name")

    def prep_reply(self) -> str:
        return f"{self.get_citation()} mh... {self.get_rand_name()}"
    
    CITATIONS = [
        "That's it, end of the story", 
        "Bless you", 
        "Wendy's triple bacon...", 
        "Crincio",
        "UIC - University of Indians and Chineses",
        "Thanks for playing with us... but no",
        "Join our coult... Join NECSTLab",
        "Can we do better?",
        "Shut",
        "We're going to do science",
        "Have a nice weekend even though it's wednedsay",
        "Awesome",
        "Super awesome",
        "At the end of the day"
    ]

    TRIGGERS = [
        "santambrogio",
        "santa",
        "jenna",
        "uic",
        "chicago",
        "letterman",
        "ds160",
        "uslenghi",
        "piergiorgio",
        "visa",
    ]

    NAMES = [
        {"name": "Andrea", "probability": 3},
        {"name": "Pietro", "probability": 1},
        {"name": "Riccardo", "probability": 1},
        {"name": "Simone", "probability": 1},
        {"name": "Marco", "probability": 1},
        {"name": "Alessandro", "probability": 1},
        {"name": "Filippo", "probability": 2},
        {"name": "Claudio", "probability": 1},
        {"name": "Gabriele", "probability": 1},
        {"name": "Calliope", "probability": 1},
        {"name": "Matteo", "probability": 1}
    ]