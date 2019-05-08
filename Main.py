from tkinter import *
from tkinter import font
from random import randint

from Snake import Snake


def create_apples(number):
    """

    :param number:
    :return:
    """
    apples = []
    for x in range(number):
        x, y = randint(0, 39), randint(0, 39)
        apples.append((x, y))
    return apples

class Interface():
    """Classe"""

    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, width=400, height=400)
        self.canvas.pack()

        self.squares = 40
        self.widthBox = 400//self.squares
        self.snake = Snake(20)
        self.apples = create_apples(10)
        self.direction = "Right"
        self.start()
        self.window.bind("<KeyPress>", self.evalKey)

        self.animation()
        self.set_font("Purisa", 24)

        self.window.mainloop()

    def set_font(self, _font, size):
        self.font = font.Font(self.canvas, font=(_font, size))
        self.font.height = self.font.metrics("linespace")

    def start(self):
        """
        Affiche le serpent au centre de la fenêtre
        :param snake:
        :return:
        """
        self.snake.body = [(20, 20)]
        for x in range(1, self.snake.length//2 + 1):
            self.snake.body.insert(0, (20-x, 20))
        for x in range(1, self.snake.length//2):
            self.snake.body.append((20 + x, 20))
        self.display()

    def eat_apple(self):
        head = self.snake.body[-1]

        if head in self.apples:
            print(self.snake.body)
            self.apples.remove(head)
            self.snake.eat(head[0], head[1])
            print(self.snake.body)

    def defeat(self):
        self.canvas.create_rectangle(400//5, 400//5, 400//5*4, 400//5*4, fill='white')
        self.canvas.create_text(400//2, 400//2, text="LOST", font=self.font, fill='red')

    def victory(self):
        self.canvas.create_rectangle(400//5, 400//5, 400//5*4, 400//5*4, fill='white')
        self.canvas.create_text(400//2, 400//2, text="VICTORY", font=self.font, fill='green')


    def display_one_box(self, box, color):
        """
        Affiche une case dans une couleur donnée
        :param box:
        :param color:
        :return:
        """
        self.canvas.create_rectangle(box[0] * self.widthBox,
                                     box[1] * self.widthBox,
                                     box[0] * self.widthBox + (self.widthBox-1),
                                     box[1] * self.widthBox + (self.widthBox-1),
                                     fill=color,
                                     outline=color)

    def display_list(self, l, color):
        """
        Affiche en couleur toutes les cases de la liste
        :param l:
        :param color:
        :return:
        """
        for box in l:
            self.display_one_box(box, color)

    def display_snake(self, l):
        """
        Affiche le serpent avec le corp en vert et la tête en bleu
        :param l:
        :return:
        """
        self.canvas.delete(ALL)
        self.display_list(l[:-1], 'green')
        self.display_one_box(l[-1], 'blue')

    def is_out(self, l):
        """

        :param l:
        :return:
        """
        head = l[-1]
        if head[0] > 39 or head[0] < 0 or head[1] > 39 or head[1] < 0:
            return True
        return False

    def display(self):
        """

        :return:
        """
        self.display_snake(self.snake.body)
        self.display_list(self.apples, 'red')

    def evalKey(self, event):
        """

        :param event:
        :return:
        """
        if event.keysym in ["Up", "Right", "Down", "Left"]:
            self.snake.move(self.direction)
            self.direction = event.keysym

    def animation(self):
        if self.is_out(self.snake.body) or self.snake.has_bitten():
            self.defeat()
            return
        if len(self.apples) == 0:
            self.victory()
            return
        self.snake.move(self.direction)
        self.eat_apple()
        self.display()
        self.window.after(40, self.animation)


if __name__ == '__main__':
    Interface()