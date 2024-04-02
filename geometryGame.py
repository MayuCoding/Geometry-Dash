""" Import the tkinter module """
import tkinter as tk
import random

class GeometryDashGame:
    """
    Implemetation of a simplistic version of the game Geometry Dash
    """
    def __init__(self, root: tk.Tk):
        """
        Initializes the game data and creates the window
        """
        self.root = root
        self.root.title("Geometry Dash")
        self.root.geometry("800x400")
        self.canvas = tk.Canvas(self.root, width=800, height=400)
        self.canvas.pack()

        self.player = self.canvas.create_rectangle(50, 300, 100, 350, fill="blue")
        self.obstacles = []

        # Player's gravity
        self.gravity = 1
        # Player's jump power
        self.jump_power = -20
        # Player's current velocity
        self.velocity = 0
        # Whether or not the player is on the ground
        self.on_ground = True
        # The player's score
        self.score = 0

        self.canvas.bind("<space>", self.jump)
        self.canvas.bind("<KeyPress-Right>", self.move_right)
        self.canvas.bind("<KeyPress-Left>", self.move_left)

        self.canvas.focus_set()

        self.play_again_button = tk.Button(
            self.canvas, text="Play Again", command=self.restart_game
        )
        self.game_over_text = self.canvas.create_text(
            400, 200, text="", fill="red", font=("Helvetica", 36)
        )
        self.score_text = self.canvas.create_text(
            400, 250, text="", fill="blue", font=("Helvetica", 24)
        )

        self.update()

        self.create_obstacle(800)
        self.update()

    def jump(self, event):
        """
        Function to make the player jump
        """
        if self.on_ground:

            self.velocity = self.jump_power
            self.on_ground = False

    def move_right(self, event):
        """
        Controls the player moving right
        """
        self.canvas.move(self.player, 10, 0)

    def move_left(self, event):
        """
        Controls the player moving left
        """
        self.canvas.move(self.player, -10, 0)

    def create_obstacle(self, x):
        """
        Craetes randlomly sized and shape obstacles. Generates a random integer between 0 and 4
        0 = small square
        1 = tall rectangle
        2 = wide rectangle
        3 = triangle
        4 = tall triangle
        """
        obstacle_type = random.randint(0, 4)
        if obstacle_type == 0:
            obstacle = self.canvas.create_rectangle(x, 350, x + 50, 400, fill="red")
        elif obstacle_type == 1:
            obstacle = self.canvas.create_rectangle(x, 250, x + 50, 400, fill="red")
        elif obstacle_type == 2:
            obstacle = self.canvas.create_rectangle(x, 350, x + 100, 400, fill="red")
        elif obstacle_type == 3:
            obstacle = self.canvas.create_polygon(x, 400, x + 50, 400, x + 25, 350, fill="red")
        elif obstacle_type == 4:
            obstacle = self.canvas.create_polygon(x, 400, x + 50, 400, x + 25, 250, fill="red")
        self.obstacles.append(obstacle)


    def check_collision(self):
        """
        Checks if the player has collided with any of the obstacles
        """
        player_coords = self.canvas.coords(self.player)
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle)
            # coords = [x1, y1, x2, y2]
            if (player_coords[2] > obstacle_coords[0] and player_coords[0] < obstacle_coords[2] and
                player_coords[3] > obstacle_coords[1] and player_coords[1] < obstacle_coords[3]):
                return True
        return False

    def update(self):
        """
        Updates the game state
        """
        self.canvas.move(self.player, 0, self.velocity)
        self.velocity += self.gravity


        self.score += 1
        if self.score % 100 == 0:
            self.create_obstacle(800)

        for obstacle in self.obstacles:
            self.canvas.move(obstacle, -5, 0)
            if self.canvas.coords(obstacle)[2] <= 0:
                self.canvas.delete(obstacle)
                self.obstacles.remove(obstacle)

        self.root.after(20, self.update)

        if self.canvas.coords(self.player)[3] >= 400:
            self.on_ground = True
            self.velocity = 0

        if self.check_collision():
            self.game_over()



    def restart_game(self):
        """
        Restarts the game
        """
        self.canvas.delete("all")
        self.player = self.canvas.create_rectangle(50, 300, 100, 350, fill="blue")
        self.obstacles = []
        self.velocity = 0
        self.on_ground = True
        self.score = 0
        self.play_again_button.destroy()
        self.game_over_text = self.canvas.create_text(
            400, 200, text="", fill="red", font=("Helvetica", 36)
        )
        self.score_text = self.canvas.create_text(
            400, 250, text="", fill="blue", font=("Helvetica", 24)
        )
        self.create_obstacle(800)
        self.update()

    def game_over(self):
        """
        Displays the game over screen and the restart button
        """
        self.canvas.delete("all")
        self.canvas.itemconfig(self.game_over_text, text="Game Over!")
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        self.play_again_button.pack()
        self.play_again_button.place(x=350, y=300)

if __name__ == "__main__":
    root = tk.Tk()
    game = GeometryDashGame(root)
    root.mainloop()
