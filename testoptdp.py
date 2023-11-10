import tkinter as tk

class BHTVisualizer:
    def __init__(self, root, num_entries):
        self.root = root
        self.root.title("Branch History Table Visualizer")

        # Initialize the BHT
        self.bht = self.initialize_bht(num_entries)

        # Initialize the BHT
        self.bht = self.initialize_bht(num_entries)

        # Create widgets
        self.title_label = tk.Label(root, text="Branch History Table Visualizer", font=("Helvetica", 10))
        self.title_label.pack()

        self.legend_frame = tk.Frame(root)
        self.legend_frame.pack(side=tk.LEFT, anchor=tk.NW)

        self.legend_taken = tk.Label(self.legend_frame, text="Taken = 1", fg="green")
        self.legend_taken.pack()

        self.legend_not_taken = tk.Label(self.legend_frame, text="Not Taken = 0", fg="red")
        self.legend_not_taken.pack()

        tk.Label(root, text="\n").pack()
        
        self.canvas_title_label = tk.Label(root, text="Predicted by Decision Tree", font=("Helvetica", 10))
        self.canvas_title_label.pack(side=tk.LEFT)

        canvas_width = num_entries * (50 + 10)
        canvas_height = 2 * (50 + 10)

        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.canvas.pack(side=tk.LEFT)

        self.update_canvas()

    def initialize_bht(self, num_entries):
        return [0] * num_entries

    def update_bht(self, index, outcome):
        self.bht[index] = outcome

    def update_canvas(self):
        self.canvas.delete("all")
        x = 20
        y = 50

        for i, entry in enumerate(self.bht):
            color = "green" if entry == 1 else "red"
            self.canvas.create_rectangle(x, y, x + 40, y + 40)
            self.canvas.create_text(x + 20, y - 10, text=f"a={i}", fill="black")
            self.canvas.create_text(x + 20, y + 20, text=str(entry), fill=color)
            x += 40 + 10

        # Move to the next row after displaying a certain number of entries per row
        if (i + 1) % 8 == 0:
            x = 20
            y += 40 + 10


    def reset_bht(self):
        self.bht = self.initialize_bht(len(self.bht))
        self.update_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    num_entries = 16  # Change this to the desired number of BHT entries
    app = BHTVisualizer(root, num_entries)
    root.mainloop()