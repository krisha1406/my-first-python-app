import tkinter as tk
from tkinter import messagebox
import random

class BhaagBetaBhaag:
    def __init__(self, root):
        self.root = root
        self.root.title("Bhaag Beta Bhaag")

        self.canvas_width = 800
        self.canvas_height = 400
        self.ground_y = 350

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="skyblue")
        self.canvas.pack()

        self.canvas.create_rectangle(10, 10, self.canvas_width - 10, self.canvas_height - 10)

        self.ground = self.canvas.create_rectangle(
            10, self.ground_y, self.canvas_width - 10, self.canvas_height - 10,
            fill="green"
        )

        self.player = self.canvas.create_text(80, self.ground_y - 20, text="🕊️", font=("Arial", 24))

        self.start_btn = tk.Button(root, text="START", bg="red", fg="white", command=self.start_game)
        self.start_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.jump_btn = tk.Button(root, text="JUMP", bg="green", fg="white", command=self.jump)
        self.jump_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.restart_btn = tk.Button(root, text="RESTART", bg="orange", fg="white", command=self.restart_game)
        self.restart_btn.pack(side=tk.LEFT, padx=10, pady=10)

        self.score = 0
        self.score_text = self.canvas.create_text(self.canvas_width - 80, 20, text="Score: 0", font=("Arial", 14), fill="black")

        self.obstacles = []
        self.clouds = []
        self.flying_birds = []
        self.running = False
        self.is_jumping = False

        self.obstacle_speed = 10
        self.obstacle_interval = 50

        self.plant_emojis = ["🌵", "🌱", "🌿"]
        self.create_background()

    def create_background(self):
        for _ in range(5):
            x = random.randint(50, self.canvas_width - 100)
            y = random.randint(30, 100)
            cloud = self.canvas.create_text(x, y, text="☁️", font=("Arial", 20))
            self.clouds.append(cloud)

        for _ in range(2):
            x = random.randint(100, self.canvas_width - 100)
            y = random.randint(80, 160)
            bird = self.canvas.create_text(x, y, text="🐦", font=("Arial", 16))
            self.flying_birds.append(bird)

    def start_game(self):
        if not self.running:
            self.running = True
            self.move_game()
            self.move_clouds()
            self.move_flying_birds()

    def move_game(self):
        if not self.running:
            return

        self.score += 1
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

        if self.score == 500:
            self.obstacle_speed += 4
            self.obstacle_interval = 35

        if self.score % self.obstacle_interval == 0:
            plant = random.choice(self.plant_emojis)
            obs = self.canvas.create_text(self.canvas_width, self.ground_y - 20, text=plant, font=("Arial", 24))
            self.obstacles.append(obs)

        to_remove = []

        for obs in self.obstacles:
            self.canvas.move(obs, -self.obstacle_speed, 0)

            if not self.is_jumping and self.check_collision(self.player, obs):
                self.running = False
                messagebox.showinfo("Game Over", f"Game Over! Your Score: {self.score}")
                return

            x, _ = self.canvas.coords(obs)
            if x < 0:
                to_remove.append(obs)

        for obs in to_remove:
            self.canvas.delete(obs)
            self.obstacles.remove(obs)

        self.root.after(50, self.move_game)

    def move_clouds(self):
        if not self.running:
            return
        for cloud in self.clouds:
            self.canvas.move(cloud, -1, 0)
            x, y = self.canvas.coords(cloud)
            if x < 0:
                self.canvas.move(cloud, self.canvas_width + 100, 0)
        self.root.after(100, self.move_clouds)

    def move_flying_birds(self):
        if not self.running:
            return
        for bird in self.flying_birds:
            self.canvas.move(bird, -2, 0)
            x, y = self.canvas.coords(bird)
            if x < 0:
                self.canvas.move(bird, self.canvas_width + 100, 0)
        self.root.after(150, self.move_flying_birds)

    def jump(self):
        if not self.running or self.is_jumping:
            return

        self.is_jumping = True
        def animate_jump(step=0):
            if step < 15:
                self.canvas.move(self.player, 0, -7)
                self.root.after(20, animate_jump, step + 1)
            elif step < 30:
                self.canvas.move(self.player, 0, 7)
                self.root.after(20, animate_jump, step + 1)
            else:
                self.is_jumping = False

        animate_jump()

    def check_collision(self, player, obstacle):
        p_box = self.canvas.bbox(player)
        o_box = self.canvas.bbox(obstacle)
        if not p_box or not o_box:
            return False
        px1, py1, px2, py2 = p_box
        ox1, oy1, ox2, oy2 = o_box
        overlap = not (px2 < ox1 or px1 > ox2 or py2 < oy1 or py1 > oy2)
        return overlap

    def restart_game(self):
        self.running = False
        self.canvas.delete("all")
        self.obstacles.clear()
        self.clouds.clear()
        self.flying_birds.clear()
        self.score = 0
        self.obstacle_speed = 10
        self.obstacle_interval = 50
        self.is_jumping = False

        self.canvas.create_rectangle(10, 10, self.canvas_width - 10, self.canvas_height - 10)
        self.ground = self.canvas.create_rectangle(
            10, self.ground_y, self.canvas_width - 10, self.canvas_height - 10,
            fill="green"
        )
        self.player = self.canvas.create_text(80, self.ground_y - 20, text="🕊️", font=("Arial", 24))
        self.score_text = self.canvas.create_text(self.canvas_width - 80, 20, text="Score: 0", font=("Arial", 14), fill="black")
        self.create_background()

if __name__ == "__main__":
    root = tk.Tk()
    game = BhaagBetaBhaag(root)
    root.mainloop()
