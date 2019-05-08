
class Snake():
    def __init__(self, length):
        self.body = []
        self.length = length

    def move(self, direction):
        """
        Déplace le serpent d'une case dans la direction donnée
        :param direction:
        :return:
        """
        last_box = self.body[-1]
        if direction == "Right":
            self.body.append((last_box[0] + 1, last_box[1]))
        elif direction == "Left":
            self.body.append((last_box[0] - 1, last_box[1]))
        elif direction == "Down":
            self.body.append((last_box[0], last_box[1] + 1))
        elif direction == "Up":
            self.body.append((last_box[0], last_box[1] - 1))
        self.body.pop(0)

    def has_bitten(self):
        """

        :return:
        """
        head = self.body[-1]
        if head in self.body[:-1]:
            return True
        return False

    def eat(self, x, y):
        for i in range(3):
            self.body.insert(0, (x, y))

