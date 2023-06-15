import tkinter as tk
from tkinter import Label, Canvas

from PIL import Image, ImageTk
from pathlib import Path
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 550
SPACE_SIZE = 50
BODY_PARTS = 1
SNAKE_COLOR = "#00CC00"
FOOD_COLOR = "#FFFF00"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.points = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square, points = self.create_rounded_rectangle(canvas, x, y)
            self.squares.append(square)
            self.points.append(points)

    def create_rounded_rectangle(self, canvas, x1, y1):
        radius = 5
        points = [
            x1 + radius,
            y1,
            x1 + SPACE_SIZE - radius,
            y1,
            x1 + SPACE_SIZE,
            y1 + radius,
            x1 + SPACE_SIZE,
            y1 + SPACE_SIZE - radius,
            x1 + SPACE_SIZE - radius,
            y1 + SPACE_SIZE,
            x1 + radius,
            y1 + SPACE_SIZE,
            x1,
            y1 + SPACE_SIZE - radius,
            x1,
            y1 + radius,
            x1 + radius,
            y1,
        ]

        polygon_id = canvas.create_polygon(
            points, outline="#006400", width=2, fill=SNAKE_COLOR, tag="snake"
        )
        return polygon_id, points

    def draw_head(self, canvas, direction):
        if len(canvas.find_withtag("snake_head")):
            canvas.delete("snake_head")

        try:
            with Image.open(Path("./images/snake-head.png")) as img:
                img = img.resize((SPACE_SIZE, SPACE_SIZE), Image.Resampling.LANCZOS)
                if direction == "right":
                    rotated_img = img
                elif direction == "left":
                    rotated_img = img.rotate(180)
                elif direction == "up":
                    rotated_img = img.rotate(90)
                else:  # direction == 'down':
                    rotated_img = img.rotate(270)

                self.snake_head_photo_image = ImageTk.PhotoImage(rotated_img)

                canvas.create_image(
                    self.coordinates[0][0] + SPACE_SIZE // 2,
                    self.coordinates[0][1] + SPACE_SIZE // 2,
                    anchor=tk.CENTER,
                    image=self.snake_head_photo_image,
                    tag="snake_head",
                )
                canvas.tag_raise("snake_head")
        except FileNotFoundError:
            print("Error: snake-head.png image file not found")
        except Exception as e:
            print("Error opening snake-head.png:", e)


class Food:
    def __init__(self, canvas):
        x = random.randrange(0, GAME_WIDTH - SPACE_SIZE, SPACE_SIZE)
        y = random.randrange(0, GAME_HEIGHT - SPACE_SIZE, SPACE_SIZE)

        oval_width = SPACE_SIZE
        oval_height = SPACE_SIZE

        try:
            with Image.open(Path("./images/apple.png")) as img:
                img = img.resize((oval_width, oval_height), Image.Resampling.LANCZOS)
                self.apple_image = ImageTk.PhotoImage(img)

            self.coordinates = [x, y]

            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, tag="food")
            center_x = (x + x + SPACE_SIZE) / 2
            center_y = (y + y + SPACE_SIZE) / 2
            canvas.create_image(
                center_x,
                center_y,
                anchor=tk.CENTER,
                image=self.apple_image,
                tag="apple_image",
            )
        except FileNotFoundError:
            print("Error: apple.png image file not found")
        except Exception as e:
            print("Error opening apple.png:", e)


class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake")
        self.window.resizable(False, False)

        self.score = 0
        self.direction = "right"
        self.label = Label(
            self.window, text=f"Score: {self.score}", font=("consolas", 40)
        )
        self.label.pack()

        self.canvas = Canvas(
            self.window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH
        )
        self.canvas.pack()

        self.window.update()

        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Key bindings
        self.window.bind("<Return>", lambda event: self.start_game())
        self.window.bind("<Left>", lambda event: self.change_direction("left"))
        self.window.bind("<Right>", lambda event: self.change_direction("right"))
        self.window.bind("<Up>", lambda event: self.change_direction("up"))
        self.window.bind("<Down>", lambda event: self.change_direction("down"))
        self.window.bind("<Escape>", lambda event: self.close_window())

        self.speed = 200
        self.snake_head_photo_image = None
        self.snake = Snake(self.canvas)

        self.show_start_screen()

        self.window.mainloop()

    def show_start_screen(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2 - 50,
            text="Snake Game",
            font=("consolas", 70),
            fill="white",
            justify=tk.CENTER,
        )
        self.start_label_text = self.canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2 + 50,
            text="Press Enter to Start",
            font=("consolas", 40),
            fill="white",
            justify=tk.CENTER,
        )

        self.flash_start_label()  # Start the flashing effect

    def flash_start_label(self):
        current_color = self.canvas.itemcget(self.start_label_text, "fill")
        new_color = "white" if current_color == "black" else "black"
        self.canvas.itemconfigure(self.start_label_text, fill=new_color)
        self.window.after(500, self.flash_start_label)

    def start_game(self):
        self.window.unbind("<Return>")  # Unbind the Enter key

        self.canvas.delete(tk.ALL)
        self.label.config(text=f"Score: {self.score}")
        self.food = Food(self.canvas)
        self.next_turn()

    def next_turn(self):
        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        self.snake.coordinates.insert(0, (x, y))
        square, points = self.snake.create_rounded_rectangle(self.canvas, x, y)
        self.snake.squares.insert(0, square)
        self.snake.points.insert(0, points)
        self.snake.draw_head(self.canvas, self.direction)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.canvas.delete("apple_image")
            self.food = Food(self.canvas)
            self.speed -= 5
        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]
            del self.snake.points[-1]

        if self.check_collisions():
            self.game_over()
            self.window.after(2000, self.close_window)  # Close window after 2 seconds

        else:
            for idx, square in enumerate(self.snake.squares):
                self.canvas.coords(square, self.snake.points[idx])

            self.window.after(self.speed, self.next_turn)

    def change_direction(self, new_direction):
        if new_direction == "left" and self.direction != "right":
            self.direction = new_direction

        elif new_direction == "right" and self.direction != "left":
            self.direction = new_direction

        elif new_direction == "up" and self.direction != "down":
            self.direction = new_direction

        elif new_direction == "down" and self.direction != "up":
            self.direction = new_direction

    def check_collisions(self):
        x, y = self.snake.coordinates[0]

        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            print("Game over. You hit the wall!")
            return True

        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                print("Game over. You ate yourself!")
                return True

        return False

    def game_over(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text=f"Game Over!\nYour score was: {self.score}",
            font=("consolas", 70),
            fill="red",
            justify=tk.CENTER,
        )

    def close_window(self):
        self.window.destroy()
