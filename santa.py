import bisect
from random import randint, random
import re
from typing import Tuple

class Santa:
    def __init__(self) -> None:
        self.tot_prob = 0
        self.distr = []

         # update the total probability at startup
        for x in Santa.NAMES:
            self.tot_prob += x.get("probability")

        # set the distribution of the available names
        self.cdf()

        pass

    def santa_egg(sentence) -> None | str:
        res: re.Match = re.search("s.*?a.*?n.*?t.*?a", sentence)

        if res:
            indexes = []
            app: str = res.group()
            last = 0

            for char in "santa":
                last = app.index(char, last)

                indexes.append(last)

            ret: str = ""
            for i in range(len(app)):
                if i in indexes:
                    ret += app[i].upper()
                else:
                    ret += app[i]
            
            return ret
        else:
            return None

    def get_citation(self) -> str:
        return Santa.CITATIONS[randint(0, len(Santa.CITATIONS) - 1)]
    
    def cdf(self) -> None:
        cumsum = 0
        for w in Santa.NAMES:
            cumsum += w.get("probability")
            self.distr.append(cumsum / self.tot_prob)

    def get_rand_name(self) -> str:    
        return Santa.NAMES[bisect.bisect(self.distr, random())].get("name")

    def prep_reply(self) -> str:
        return f"{self.get_citation()} mh... {self.get_rand_name()}"
    
    def game_name(self):
        bound = randint(1, 5)
        trials = []
        i = 0

        while i < bound:
            name = self.get_rand_name()

            if name not in trials:
                trials.append(name)
                i+=1

        return trials
    
    GREATINGS = [
        "ciao",
        "buongiorno",
        "ehi",
        "ehy",
        "buonanotte"
    ]
    
    CITATIONS = [
        "That's it, end of the story", 
        "Bless you", 
        "Wendy's triple bacon...",
        "UIC - University of Indians and Chineses",
        "Thanks for playing with us... but no",
        "Join our coult... Join NECSTLab",
        "Can we do better?",
        "Shut",
        "We're going to do science",
        "Have a nice weekend even though it's wednedsay",
        "Awesome",
        "Super awesome",
        "At the end of the day",
        "It's a kind of game name"
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
        "illinois"
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