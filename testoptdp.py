import tkinter as tk

class BHTVisualizer:
    def __init__(self, root, num_entries):
        self.root = root
        self.root.title("Branch History Table Visualizer")

        # Reading Data and Store into array
        self.file_content = self.read_file('data.txt')

        # Initialize the BHT
        self.bht = self.initialize_bht(num_entries)

        # Create widgets
        self.title_label = tk.Label(root, text="Branch History Table Visualizer\n", font=("Helvetica", 10))
        self.title_label.pack()

        text_content = (
            "Key:\n"
            "(1) Web Browser:\nGoogle Chrome, Microsoft Edge, Mozilla Firefox\n\n"
            "(2) Office Suite:\nMicrosoft Word, Microsoft Excel, Microsoft PowerPoint\n\n"
            "(3) Media Player:\nWindows Media Player, Spotify\n\n"
            "(4) Email Client:\nMicrosoft Outlook, Mozilla Thunderbird\n"
        )
        self.subtitle_label = tk.Label(root, text=text_content, font=("Helvetica", 10))
        self.subtitle_label.pack()

        self.subtitle_label = tk.Label(root, text="Below shows the initial program executed by the user upon powering up the computer:", font=("Helvetica", 10))
        self.subtitle_label.pack()

        self.file_content_label = tk.Label(root, text=' | '.join(self.file_content), font=("Helvetica", 10))
        self.file_content_label.pack()

        self.legend_frame = tk.Frame(root)
        self.legend_frame.pack(side=tk.LEFT, anchor=tk.NW)

        self.legend_taken = tk.Label(self.legend_frame, text="Taken = 1", fg="green", font=("Helvetica", 10))
        self.legend_taken.pack()

        self.legend_not_taken = tk.Label(self.legend_frame, text="Not Taken = 0", fg="red", font=("Helvetica", 10))
        self.legend_not_taken.pack()

        tk.Label(root, text="\n").pack()

        self.canvas_title_label_predicted = tk.Label(root, text="Predicted by Decision Tree", font=("Helvetica", 10))
        self.canvas_title_label_predicted.pack(side=tk.LEFT)

        canvas_width = num_entries * (50 + 10)
        canvas_height = 2 * (50 + 10)

        self.predicted_canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.predicted_canvas.pack(side=tk.LEFT)

        self.canvas_title_label_actual = tk.Label(root, text="Actual Execution", font=("Helvetica", 10))
        self.canvas_title_label_actual.pack(side=tk.LEFT)

        self.actual_canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.actual_canvas.pack(side=tk.LEFT)

        self.predicted_bht()
        self.actual_bht()

    # Setting Up Predicted BHT
    def initialize_bht(self, num_entries):
        return [0] * num_entries
    
    def update_bht(self, index, outcome):
        self.bht[index] = outcome

    def predicted_bht(self):
        self.predicted_canvas.delete("all")
        x = 20
        y = 50

        for i, entry in enumerate(self.bht):
            color = "green" if entry == 1 else "red"
            self.predicted_canvas.create_rectangle(x, y, x + 40, y + 40)
            self.predicted_canvas.create_text(x + 20, y - 10, text=f"a={i}", fill="black")
            self.predicted_canvas.create_text(x + 20, y + 20, text=str(entry), fill=color)
            x += 40 + 10

        # Move to the next row after displaying a certain number of entries per row
        if (i + 1) % 8 == 0:
            x = 20
            y += 40 + 10

    def actual_bht(self):
        self.actual_canvas.delete("all")
        x = 20
        y = 50

        for i, entry in enumerate(self.bht):
            color = "green" if entry == 1 else "red"
            self.actual_canvas.create_rectangle(x, y, x + 40, y + 40)
            self.actual_canvas.create_text(x + 20, y - 10, text=f"a={i}", fill="black")
            self.actual_canvas.create_text(x + 20, y + 20, text=str(entry), fill=color)
            x += 40 + 10

        # Move to the next row after displaying a certain number of entries per row
        if (i + 1) % 8 == 0:
            x = 20
            y += 40 + 10

    def reset_bht(self):
        self.bht = self.initialize_bht(len(self.bht))
        self.predicted_bht()
        self.actual_bht()

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.readlines()
                return [line.strip() for line in content]
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return []

if __name__ == "__main__":
    root = tk.Tk()
    num_entries = 10
    app = BHTVisualizer(root, num_entries)
    root.mainloop()
