import tkinter as tk
from tkinter import messagebox
import random

class SuperSaverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SUPERSAVER - Grocery Shopping App")
        self.root.geometry("400x700")

        self.cart = []
        self.images = {}
        self.products = {
            'Vegetables': [
                ("Onion", 25, "C:/Users/ADMIN/Downloads/jpg2png/onion.png"),
                ("Potato", 20, "C:/Users/ADMIN/Downloads/jpg2png/potato.png"),
                ("Tomato", 30, "C:/Users/ADMIN/Downloads/jpg2png/tomato.png"),
                ("Cucumber", 15, "C:/Users/ADMIN/Downloads/jpg2png (1)/cucumber.png")
            ],
            'Snacks': [
                ("Wafers", 10, "C:/Users/ADMIN/Downloads/jpg2png/lays.png"),
                ("Soft Drink", 40,"C:/Users/ADMIN/Downloads/jpg2png/softdrink.png" ),
                ("Biscuits", 25, "C:/Users/ADMIN/Downloads/jpg2png (1)/biscuiys.png")
            ],
            'Fruits': [
                ("Apple", 80, "C:/Users/ADMIN/Downloads/jpg2png (1)/apple.png"),
                ("Banana", 20, "C:/Users/ADMIN/Downloads/jpg2png (1)/bnana.png"),
                ("Grapes", 60, "C:/Users/ADMIN/Downloads/jpg2png (1)/grapes.png")
            ],
            'Drinks': [
                ("Juice", 50, "C:/Users/ADMIN/Downloads/jpg2png (1)/juice.png"),
                ("Milk", 35, "C:/Users/ADMIN/Downloads/jpg2png (1)/milk.png"),
                ("Tea", 30,"C:/Users/ADMIN/Downloads/jpg2png (1)/tea.png"),
                ("Coffee", 45, "C:/Users/ADMIN/Download/jpg2png (1)/coffee.png"),
                ("Cold Coffee", 60, "C:/Users/ADMIN/Downloads/jpg2png (1)/cold coffee.png"),
                ("Lemonade", 25, "C:/Users/ADMIN/Downloads/jpg2png (1)/leonade.png"),
                ("Energy Drink", 55, "C:/Users/ADMIN/Downloads/jpg2png (1)/energy drink.png"),
            ]
        }
        self.filtered_products = self.products.copy()
        self.show_home_page()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_home_page(self):
        self.clear_screen()

        outer_frame = tk.Frame(self.root)
        outer_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer_frame)
        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame, text="SUPERSAVER", font=("Arial", 22, "bold"), bg="#f0f0f0").pack(fill="x", pady=10)

        top_btn_frame = tk.Frame(scrollable_frame)
        top_btn_frame.pack(pady=5)
        tk.Button(top_btn_frame, text="Sort by Category", command=self.sort_by_category).pack(side="left", padx=5)
        tk.Button(top_btn_frame, text="Filter by Price", command=self.filter_by_price).pack(side="left", padx=5)
        tk.Button(top_btn_frame, text="Go to Cart", command=self.show_cart_page).pack(side="left", padx=5)

        for category, items in self.filtered_products.items():
            tk.Label(scrollable_frame, text=f"🛍️ {category}", font=("Arial", 18, "bold")).pack(pady=10)

            row_frame = None
            for idx, (name, price, image_path) in enumerate(items):
                if idx % 3 == 0:
                    row_frame = tk.Frame(scrollable_frame)
                    row_frame.pack(pady=5)
                self.add_product(row_frame, name, price, image_path)

    def add_product(self, parent, name, price, image_path):
        frame = tk.Frame(parent, bd=1, relief="solid")
        frame.pack(side="left", padx=5, pady=5)

        try:
            image = tk.PhotoImage(file=image_path)
            self.images[name] = image
            tk.Label(frame, image=image).pack()
        except:
            tk.Label(frame, text="[Image]", bg="grey", width=12, height=6).pack()

        tk.Label(frame, text=name, font=("Arial", 10)).pack()
        tk.Label(frame, text=f"₹{price}", font=("Arial", 10)).pack()
        tk.Button(frame, text="Add", command=lambda: self.add_to_cart(name, price)).pack(pady=5)

    def add_to_cart(self, name, price):
        self.cart.append((name, price))
        messagebox.showinfo("Cart", f"{name} added to cart")

    def sort_by_category(self):
        categories = list(self.products.keys())
        win = tk.Toplevel(self.root)
        win.title("Sort by Category")
        tk.Label(win, text="Select Category:").pack(pady=5)
        var = tk.StringVar()
        menu = tk.OptionMenu(win, var, *categories)
        menu.pack(pady=5)

        def apply():
            cat = var.get()
            if cat:
                self.filtered_products = {cat: sorted(self.products[cat], key=lambda x: x[0])}
                self.show_home_page()
                win.destroy()

        tk.Button(win, text="Apply", command=apply).pack(pady=5)

    def filter_by_price(self):
        win = tk.Toplevel(self.root)
        win.title("Filter by Price")

        tk.Label(win, text="Min Price:").pack()
        min_entry = tk.Entry(win)
        min_entry.pack()

        tk.Label(win, text="Max Price:").pack()
        max_entry = tk.Entry(win)
        max_entry.pack()

        def apply():
            try:
                min_p = float(min_entry.get())
                max_p = float(max_entry.get())
                self.filtered_products = {}
                for cat, items in self.products.items():
                    filtered = [item for item in items if min_p <= item[1] <= max_p]
                    if filtered:
                        self.filtered_products[cat] = filtered
                self.show_home_page()
                win.destroy()
            except:
                messagebox.showerror("Invalid", "Please enter valid numbers")

        tk.Button(win, text="Apply Filter", command=apply).pack(pady=5)

    def show_cart_page(self):
        self.clear_screen()
        tk.Button(self.root, text="⬅ Back", command=self.show_home_page).pack(anchor="w", padx=5, pady=5)
        tk.Label(self.root, text="🛒 Cart", font=("Arial", 18, "bold")).pack(pady=10)

        total = 0
        for name, price in self.cart:
            tk.Label(self.root, text=f"{name} - ₹{price}", font=("Arial", 12)).pack()
            total += price

        tk.Label(self.root, text=f"Total: ₹{total}", font=("Arial", 14, "bold")).pack(pady=10)

        if total > 99:
            tk.Label(self.root, text="✅ Free Delivery Unlocked!", fg="green").pack()

        tk.Label(self.root, text="Enter Address:").pack()
        tk.Entry(self.root).pack(pady=5)

        tk.Button(self.root, text="Confirm Order", command=self.show_order_confirmed_page).pack(pady=20)

    def show_order_confirmed_page(self):
        self.clear_screen()
        tk.Label(self.root, text="🎉 Order Confirmed! 🎉", font=("Arial", 20, "bold")).pack(pady=20)

        canvas = tk.Canvas(self.root, width=400, height=300, bg="white")
        canvas.pack()

        colors = ["red", "green", "blue", "yellow", "purple", "orange"]
        for _ in range(100):
            x, y = random.randint(0, 400), random.randint(0, 300)
            r = random.randint(2, 6)
            canvas.create_oval(x, y, x + r, y + r, fill=random.choice(colors), outline="")

        tk.Button(self.root, text="Back to Home", command=self.show_home_page).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SuperSaverApp(root)
    root.mainloop()


