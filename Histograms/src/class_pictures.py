class Pictures:
    i = 1
    name = ""
    rgb = [0,0,0]
    lab = [0,0,0]
    hsv = [0,0,0]
    
    def __init__(self, cislo, name):
        self.data = []
        self.i = cislo
        self.name = name