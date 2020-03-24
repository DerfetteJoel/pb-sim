natures = ["hardy", "bold", "modest", "calm", "timid", "lonely", "docile", "mild", "gentle", "hasty", "adamant",
           "impish", "bashful", "careful", "jolly", "naughty", "lax", "rash", "quirky", "naive", "brave", "relaxed",
           "quiet", "sassy", "serious"]


class Nature:
    def __init__(self, name):
        if name in natures:
            self.name = name
        else:
            self.name = "hardy"
        if self.name == "hardy":
            self.decreased_stat = None
            self.increased_stat = None
        elif self.name == "bold":
            self.decreased_stat = 1
            self.increased_stat = 2
        elif self.name == "modest":
            self.decreased_stat = 1
            self.increased_stat = 3
        elif self.name == "calm":
            self.decreased_stat = 1
            self.increased_stat = 4
        elif self.name == "timid":
            self.decreased_stat = 1
            self.increased_stat = 5
        elif self.name == "lonely":
            self.decreased_stat = 2
            self.increased_stat = 1
        elif self.name == "docile":
            self.decreased_stat = None
            self.increased_stat = None
        elif self.name == "mild":
            self.decreased_stat = 2
            self.increased_stat = 3
        elif self.name == "gentle":
            self.decreased_stat = 2
            self.increased_stat = 4
        elif self.name == "hasty":
            self.decreased_stat = 2
            self.increased_stat = 5
        elif self.name == "adamant":
            self.decreased_stat = 3
            self.increased_stat = 1
        elif self.name == "impish":
            self.decreased_stat = 3
            self.increased_stat = 2
        elif self.name == "bashful":
            self.decreased_stat = None
            self.increased_stat = None
        elif self.name == "careful":
            self.decreased_stat = 3
            self.increased_stat = 4
        elif self.name == "jolly":
            self.decreased_stat = 3
            self.increased_stat = 5
        elif self.name == "naughty":
            self.decreased_stat = 4
            self.increased_stat = 1
        elif self.name == "lax":
            self.decreased_stat = 4
            self.increased_stat = 2
        elif self.name == "rash":
            self.decreased_stat = 4
            self.increased_stat = 3
        elif self.name == "quirky":
            self.decreased_stat = None
            self.increased_stat = None
        elif self.name == "naive":
            self.decreased_stat = 4
            self.increased_stat = 5
        elif self.name == "brave":
            self.decreased_stat = 5
            self.increased_stat = 1
        elif self.name == "relaxed":
            self.decreased_stat = 5
            self.increased_stat = 2
        elif self.name == "quiet":
            self.decreased_stat = 5
            self.increased_stat = 3
        elif self.name == "sassy":
            self.decreased_stat = 5
            self.increased_stat = 4
        elif self.name == "serious":
            self.decreased_stat = None
            self.increased_stat = None
