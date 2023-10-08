import bisect
from random import randint, random
import re
import json
from typing import Tuple

class Santa:
    def __init__(self) -> None:
        self.tot_prob = 0
        self.distr = []
        self.response_probability = 100
        self.photos = []
        self.audio = []

         # update the total probability at startup
        for x in Santa.NAMES:
            self.tot_prob += x.get("probability")

        # set the distribution of the available names
        self.cdf()

        try:
            with open("meme/photos.json", "r") as f:
                self.photos = json.load(f)

                f.close()
        except:
            print("No photos found")

        try:
            with open("audio/audio.json", "r") as f:
                self.audio = json.load(f)

                f.close()
        except:
            print("No audio found")

        pass

    def cdf(self) -> None:
        cumsum = 0
        for w in Santa.NAMES:
            cumsum += w.get("probability")
            self.distr.append(cumsum / self.tot_prob)

    def set_probability(self, probability: int) -> None:
        self.response_probability = probability

    def santa_egg(self, sentence, bold=False) -> None | str:
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
                    if bold:
                        ret += f"<b>{app[i].upper()}</b>"
                    else:
                        ret += app[i].upper()
                else:
                    ret += app[i]
            
            return ret
        else:
            return None

    def get_citation(self) -> str:
        return Santa.CITATIONS[randint(0, len(Santa.CITATIONS) - 1)]

    def get_rand_name(self) -> str:    
        return Santa.NAMES[bisect.bisect(self.distr, random())].get("name")

    def prep_reply(self) -> str:
        return f"{self.get_citation()} mh... {self.get_rand_name()}"
    
    def game_name(self) -> list[str]:
        bound = randint(2, 5)
        trials = []
        i = 0

        while i < bound:
            name = self.get_rand_name()

            if name not in trials:
                trials.append(name)
                i+=1

        return trials

    # the photo JSON structure is: name, telegram_id
    def get_photo(self) -> Tuple[int, dict]:
        index = randint(0, len(self.photos) - 1)

        # return the index of the photo and the photo itself
        return index, self.photos[index]
    
    def update_photo(self, index: int, name: str, telegram_id: str) -> None:
        self.photos[index] = {"name": name, "id": telegram_id}

        with open("meme/photos.json", "w") as f:
            json.dump(self.photos, f)

            f.close()

    def insert_photo(self, name: str, id: str) -> None:
        self.photos.append({"name": name, "id": id})

        with open("meme/photos.json", "w") as f:
            json.dump(self.photos, f)

            f.close()

    def get_audio(self) -> Tuple[int, dict]:
        index = randint(0, len(self.audio) - 1)

        # return the index of the audio and the audio itself
        return index, self.audio[index]
    
    def get_audio(self, *args) -> Tuple[int, dict]:
        if len(args) == 1:
            index = args[0]
        else:
            index = randint(0, len(self.audio) - 1)

        # return the index of the audio and the audio itself
        return index, self.audio[index]
    
    def update_audio(self, index: int, name: str, telegram_id: str) -> None:
        self.audio[index] = {"name": name, "id": telegram_id}

        with open("audio/audio.json", "w") as f:
            json.dump(self.audio, f)

            f.close()

    def insert_audio(self, name: str, id: str) -> None:
        self.audio.append({"name": name, "id": id})

        with open("audio/audio.json", "w") as f:
            json.dump(self.audio, f)

            f.close()

    def reset_ids(self) -> None:
        for photo in self.photos:
            photo["id"] = None

        for audio in self.audio:
            audio["id"] = None

        with open("meme/photos.json", "w") as f:
            json.dump(self.photos, f)

            f.close()

        with open("audio/audio.json", "w") as f:
            json.dump(self.audio, f)

            f.close()
    
    GREATINGS = [
        "ciao",
        "buongiorno",
        "ehi",
        "ehy",
        "buonanotte",
        "salve"
    ]
    
    CITATIONS = [
        "That's it, end of the story", 
        "Bless you", 
        "Wendy's triple bacon...",
        "UIC - University of Indians and Chineses",
        "Thanks for playing with us... but no",
        "Join our cult... Join NECSTLab",
        "Can we do better?",
        "Shoot",
        "We're going to do science",
        "This is a pain in the neck",
        "It's a matter of tradeoff",
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
        "illinois",
        "free food",
        "gratis",
        "cibo gratis",
        "hooters",
        "bbq",
        "free mover",
        "piano di studi",
        "waitlist",
        "america",
        "usa",
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