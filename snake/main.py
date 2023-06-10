from tkinter import *
from PIL import Image, ImageTk
import random

#from helper.rounded_rectangle import create_rounded_rectangle

GAME_WIDTH = 1000
GAME_HEIGHT = 550
SPACE_SIZE = 50
BODY_PARTS = 1
SNAKE_COLOR = '#00CC00'
FOOD_COLOR = "#FFFF00"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self) -> None:
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        self.points = []  # store the points for each polygon

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])  # starting position

        for x, y in self.coordinates:
            square, points = create_rounded_rectangle(canvas, x, y, x + SPACE_SIZE, y + SPACE_SIZE, radius=5,
                                                      outline='#006400', width=2, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)
            self.points.append(points)

    def draw_head(self, direction):
        if len(canvas.find_withtag("snake_head")):
            canvas.delete("snake_head")

        with Image.open("./images/snake-head.png") as img:
            img = img.resize((SPACE_SIZE, SPACE_SIZE), Image.LANCZOS)
            if direction == 'right':
                rotated_img = img
            elif direction == 'left':
                rotated_img = img.rotate(180)
            elif direction == 'up':
                rotated_img = img.rotate(90)
            else: # direction == 'down':
                rotated_img = img.rotate(270)

            self.snake_head_photo_image = ImageTk.PhotoImage(rotated_img)
            canvas.create_image(self.coordinates[0][0] + SPACE_SIZE // 2, self.coordinates[0][1] + SPACE_SIZE // 2,
                                anchor=CENTER, image=self.snake_head_photo_image, tag="snake_head")
            canvas.tag_raise("snake_head")

class Food:
    def __init__(self):
        x = random.randrange(0, GAME_WIDTH-SPACE_SIZE, SPACE_SIZE)
        y = random.randrange(0, GAME_HEIGHT-SPACE_SIZE, SPACE_SIZE)

        oval_width = SPACE_SIZE
        oval_height = SPACE_SIZE

        # Load and resize an apple image (PNG format)
        with Image.open("./images/apple.png") as img:
            img = img.resize((oval_width, oval_height), Image.LANCZOS)  # Resize the image
            self.apple_image = ImageTk.PhotoImage(img)  # store the resized apple_image using self

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y+SPACE_SIZE, tag="food")

        # Calculate the center of the oval
        center_x = (x + x + SPACE_SIZE) / 2
        center_y = (y + y + SPACE_SIZE) / 2

        # Draw the apple image on the center of the oval
        canvas.create_image(center_x, center_y, anchor=CENTER, image=self.apple_image,tag="apple_image")  

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1, x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius, x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2, x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius, x1 + radius, y1]

    polygon_id = canvas.create_polygon(points, **kwargs, smooth=True)
    return polygon_id, points

def next_turn(snake, food):
    x, y = snake.coordinates[0] # the first list of coordinates [x,y] is the head of the snake

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square, points = create_rounded_rectangle(canvas, x, y, x+SPACE_SIZE, y+SPACE_SIZE,radius=5,outline='#006400',width=2, fill=SNAKE_COLOR, tag='snake')
    snake.squares.insert(0, square)
    snake.points.insert(0, points)  # add the points for the new square
    snake.draw_head(direction)

    if x  == food.coordinates[0] and y == food.coordinates[1]:

        global score 
        score +=1
        global speed
        speed -= 3
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        canvas.delete("apple_image")
        food = Food()
    else: 
        # we would only delete the last body part of our snake if
        # we have not eaten a food object
        # to appear as our snake is moving
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
        del snake.points[-1]  # remove the last set of points
        canvas.delete(snake.points[-1])

    if check_collisions(snake):
        game_over()
    else:
        for idx, square in enumerate(snake.squares):
            canvas.coords(square, snake.points[idx])  # apply updated coordinates to each snake body part
        
        window.after(speed, next_turn, snake, food) 


def change_direction(new_direction):
    
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x,y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        print("Game over. You hit the wall!")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("Game over. You hit the wall!")
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("Game over. You ate yourself!")
            return True

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill='red', tag='gameover')
                       

window = Tk()
window.title("Snake")
window.resizable(False, False)

score = 0 # initial score
direction = 'right' # initial direction
label = Label(window, text=f"Score: {score}", font=('consolas',40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


speed = 150
snake_head_photo_image = None
snake = Snake()
food = Food()
next_turn(snake,food)

window.mainloop()