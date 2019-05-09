from tkinter import *
from tkinter import font
from random import randint
from Snake import Snake


class Interface:
    """
    GUI
    """

    def __init__(self):
        self.display_menu()
        self.window.mainloop()

    def init_var(self):
        """
        Initialise les variables essentielles
        :return:
        """
        self.difficulty = 1
        self.level = 1
        self.direction = "Right"

    def display_menu(self):
        """
        Affiche la fenêtre de menu pour sélectionner la difficulté
        :return:
        """
        self.init_var()
        if hasattr(self, 'window'):
            self.window.destroy()
        self.window = Tk()
        self.window.focus_force()
        self.window.resizable(0, 0)
        screen_length = 400
        widthBox = screen_length//(screen_length//10)
        self.canvas_menu = Canvas(self.window, width=screen_length, height=screen_length)
        self.canvas_menu.pack()
        self.set_font("Purisa", 24)

        self.canvas_menu.create_text(screen_length//2, screen_length//6, text="SNAKE", fill='green',
                                     font=self.font_title)
        easy = Button(self.canvas_menu, text="EASY", width=widthBox*3, activebackground="#d1d1d1",
                      command=lambda: self.select_difficulty(1))
        self.canvas_menu.create_window(screen_length//2, screen_length//3+50, window=easy)
        medium = Button(self.canvas_menu, text="MEDIUM", width=widthBox*3, activebackground="#d1d1d1",
                        command=lambda: self.select_difficulty(2))
        self.canvas_menu.create_window(screen_length//2, screen_length//3+100, window=medium)
        hard = Button(self.canvas_menu, text="HARD", width=widthBox*3, activebackground="#d1d1d1",
                      command=lambda: self.select_difficulty(3))
        self.canvas_menu.create_window(screen_length//2, screen_length//3+150, window=hard)

    def select_difficulty(self, difficulty):
        """
        Initialise la difficulté
        :param difficulty:
        :return:
        """
        self.difficulty = difficulty
        self.canvas_menu.destroy()
        self.init_window()

    def set_font(self, _font, size):
        """
        Créer des polices d'écritures
        :param _font:
        :param size:
        :return:
        """
        self.font = font.Font(self.window, font=(_font, size))
        self.font.height = self.font.metrics("linespace")
        self.font_title = font.Font(self.window, font=(_font, size*2))

    def init_window(self):
        """
        Initialise la fenêtre du jeu en fonction de la diffculté choisie
        :param difficulty:
        :return:
        """
        if hasattr(self, 'window'):
            self.window.destroy()
        self.window = Tk()
        self.window.focus_force()
        self.window.resizable(0, 0)
        self.set_font("Purisa", 24)
        if self.difficulty == 1:
            self.screen_length = 800
        elif self.difficulty == 2:
            self.screen_length = 600
        elif self.difficulty == 3:
            self.screen_length = 400
        self.squares = self.screen_length // 10
        self.widthBox = self.screen_length // self.squares
        self.canvas = Canvas(self.window, width=self.screen_length, height=self.screen_length)
        self.canvas.pack()

        self.display_level_information(self.level)

    def display_level_information(self, level):
        """
        Affiche une fenêtre avant le début du niveau
        :param level:
        :return:
        """
        self.canvas.delete(ALL)
        self.window.bind("<Key-space>", self.start)
        self.canvas.create_text(self.screen_length//2, self.screen_length//3, text="LEVEL " + str(level),
                                font=self.font_title, fill='blue')
        self.canvas.create_text(self.screen_length // 2, self.screen_length // 2, text='Ready ? Press « space »',
                                font=self.font, fill='black')

    def start(self, event):
        """
        Affiche le serpent au centre de la fenêtre
        :param event:
        :param snake:
        :return:
        """
        self.window.unbind("<Key-space>")
        self.window.bind("<KeyPress>", self.eval_key)
        self.canvas.delete(ALL)
        self.snake = Snake(10)
        self.apples = self.create_apples(5 * self.level)

        center = self.squares//2
        self.snake.body = [(center, center)]
        for x in range(1, self.snake.length//2 + 1):
            self.snake.body.insert(0, (center-x, center))
        for x in range(1, self.snake.length//2):
            self.snake.body.append((center + x, center))
        self.display()
        self.animation()

    def create_apples(self, number):
        """
        Initialise une liste contenant les positions des pommes
        :param number:
        :return:
        """
        apples = []
        for x in range(number):
            x, y = randint(0, self.squares-1), randint(0, self.squares-1)
            apples.append((x, y))
        return apples

    def eat_apple(self):
        """
        Mange une pomme
        :return:
        """
        for apple in self.apples:
            if apple in self.snake.body:
                end = self.snake.body[0]
                self.apples.remove(apple)
                self.snake.eat(end[0], end[1])

    def is_out(self, l):
        """
        Vérifie si la tête du serpent est sortie de la zone
        :param l:
        :return:
        """
        head = l[-1]
        if head[0] >= self.squares or head[0] < 0 or head[1] >= self.squares or head[1] < 0:
            return True
        return False

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
        self.display_list(l[:-1], 'green')
        self.display_one_box(l[-1], 'blue')

    def display(self):
        """
        Rafraîchit l'affichage
        :return:
        """
        self.canvas.delete(ALL)
        self.display_snake(self.snake.body)
        self.display_list(self.apples, 'red')

    def eval_key(self, event):
        """
        Change la direction du serpent en fonction de la touche appuyée
        :param event:
        :return:
        """
        if event.keysym in ["Up", "Right", "Down", "Left"]:
            self.snake.move(self.direction)
            self.direction = event.keysym

    def animation(self):
        """
        Boucle principale
        :return:
        """
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

    def next_level(self):
        """
        Lance le niveau supérieur
        :return:
        """
        self.level += 1
        self.direction = "Right"
        self.display_level_information(self.level)

    def defeat(self):
        """
        Affiche le message de défaite
        :return:
        """
        self.canvas.create_rectangle(self.screen_length//5, self.screen_length//5, self.screen_length//5*4,
                                     self.screen_length//5*4, fill='white')
        self.canvas.create_text(self.screen_length//2, self.screen_length//3, text="GAME OVER", font=self.font,
                                fill='red')
        menu = Button(self.canvas, text="Back to menu", width=self.widthBox * 2, activebackground="#d1d1d1",
                      command=self.display_menu)
        self.canvas.create_window(self.screen_length // 2, self.screen_length // 2 + 100, window=menu)

    def victory(self):
        """
        Affiche le message de victoire
        :return:
        """
        self.canvas.create_rectangle(self.screen_length//5, self.screen_length//5, self.screen_length//5*4,
                                     self.screen_length//5*4, fill='white')
        self.canvas.create_text(self.screen_length//2, self.screen_length//3, text="VICTORY", font=self.font,
                                fill='green')
        next_level = Button(self.canvas, text="Next level", width=self.widthBox * 2, activebackground="#d1d1d1",
                            command=self.next_level)
        self.canvas.create_window(self.screen_length // 2, self.screen_length // 2 + 50, window=next_level)
        menu = Button(self.canvas, text="Back to menu", width=self.widthBox * 2, activebackground="#d1d1d1",
                      command=self.display_menu)
        self.canvas.create_window(self.screen_length // 2, self.screen_length // 2 + 100, window=menu)


if __name__ == '__main__':
    Interface()