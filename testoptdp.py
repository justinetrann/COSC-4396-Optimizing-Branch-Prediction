import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

class BHTVisualizer:
    def __init__(self, root, num_entries):
        self.root = root
        self.root.title("Branch History Table Visualizer")

        # Initialize the BHT
        self.bht = self.initialize_bht(num_entries)
        self.counter = 0

        # Create widgets
        self.title_label = tk.Label(root, text="Branch History Table Visualizer\n", font=("Helvetica", 10))
        self.title_label.pack()

        self.legend_frame = tk.Frame(root)
        self.legend_frame.pack(side=tk.LEFT, anchor=tk.NW)

        self.subtitle_label = tk.Label(self.legend_frame, text="Key:\n"
                    "(1) Web Browser:\nGoogle Chrome, Microsoft Edge, Mozilla Firefox\n\n"
                    "(2) Office Suite:\nMicrosoft Word, Microsoft Excel, Microsoft PowerPoint\n\n"
                    "(3) Media Player:\nWindows Media Player, Spotify\n\n"
                    "(4) Email Client:\nMicrosoft Outlook, Mozilla Thunderbird\n",
                    font=("Helvetica", 10))
        self.subtitle_label.pack(anchor=tk.W, padx=250)

        self.legend_taken = tk.Label(root, text="Taken = 1", fg="green", font=("Helvetica", 10))
        self.legend_taken.pack(anchor=tk.W, padx=10)

        self.legend_not_taken = tk.Label(root, text="Not Taken = 0", fg="red", font=("Helvetica", 10))
        self.legend_not_taken.pack(anchor=tk.W, padx=10)

        self.predicted_label = tk.Label(root, text="Predicted Application:", font=("Helvetica", 10), fg="purple")
        self.predicted_label.pack(anchor=tk.W, padx=10)

        # Setting Up Widget based on num_entries
        canvas_width = num_entries * (50 + 10)
        canvas_height = 2 * (50 + 10)

        self.canvas_title_label_predicted = tk.Label(root, text="Predicted by Decision Tree", font=("Helvetica", 10), fg="purple")
        self.canvas_title_label_predicted.pack()

        self.predicted_canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.predicted_canvas.pack()

        self.canvas_title_label_actual = tk.Label(root, text="Actual Execution", font=("Helvetica", 10), fg="purple")
        self.canvas_title_label_actual.pack()

        self.actual_canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.actual_canvas.pack()

        self.subtitle_label = tk.Label(root, text="Start the program with a button click each time it's the user's first program launched", font=("Helvetica", 10), fg="blue")
        self.subtitle_label.pack(pady=10)



        self.create_buttons()
        self.predicted_bht()
        self.actual_bht()

        # Drowndown menu for user profile selection
        self.user_profile_label = tk.Label(self.legend_frame, text="Select User Profile - Test Data - Decision Tree:", font=("Helvetica", 10), fg="blue")
        self.user_profile_label.pack()

        self.user_profiles = ['Admin', 'Guest', 'User1', 'User2']
        self.selected_user_profile = tk.StringVar(value=self.user_profiles[0])

        self.user_profile_dropdown = ttk.Combobox(self.legend_frame, values=self.user_profiles, textvariable=self.selected_user_profile, state="readonly")
        self.user_profile_dropdown.pack()

        self.user_profile_dropdown.bind("<<ComboboxSelected>>", self.user_profile_selected)
       
        # View Tree
        self.view_tree_button = tk.Button(self.legend_frame, text="View Tree", command=self.button_click_handler)
        self.view_tree_button.pack(pady=10)

        # Create a Treeview widget to display the table
        self.tree = ttk.Treeview(self.legend_frame, columns=['Category', 'Application', 'Occurrences', 'User Profile'], show='headings')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Application', text='Application')
        self.tree.heading('Occurrences', text='Occurrences')
        self.tree.heading('User Profile', text='User Profile')
        self.tree.pack(pady=10)

        self.decision_tree()

    def user_profile_selected(self, event):
        self.decision_tree()

    def decision_tree(self):
        global predicted_application

        # collecting data from csv file
        col_names = ['Category', 'Application', 'Occurrences', 'User Profile']
        df = pd.read_csv("data.csv", header=0, names=col_names)

        # filter row of choice
        selected_profile = self.selected_user_profile.get()
        filtered_df = df[df['User Profile'] == selected_profile]
        filtered_df = filtered_df.sort_values(by='Occurrences', ascending=False)

        # Clearing current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Inserting data
        for index, row in filtered_df.iterrows():
            # Use df.columns[-1] to reference the last column dynamically
            values = (row['Category'], row['Application'], row['Occurrences'], row['User Profile'])
            self.tree.insert("", "end", values=values)

        if hasattr(self, 'selected_application'):
            selected_application = self.selected_application
            selected_profile = self.selected_user_profile.get()

            # Find the row corresponding to the selected application and profile
            mask = (df['Application'] == selected_application) & (df['User Profile'] == selected_profile)
            if not df[mask].empty:
                # Update occurrences for the selected application and profile
                df.loc[mask, 'Occurrences'] += 1

        df.to_csv("data.csv", index=False)
        
        # Prepare data for training the decision tree
        features = filtered_df[['Category', 'Occurrences', 'User Profile']]
        target = filtered_df['Application']

        # Encode categorical variables if needed
        features_encoded = pd.get_dummies(features)

        # Train a decision tree classifier
        clf = DecisionTreeClassifier()
        clf.fit(features_encoded, target)

        # Make predictions for the existing data
        predictions = clf.predict(features_encoded)

        # When Button is clicked
        if hasattr(self, 'view_tree_button_clicked') and self.view_tree_button_clicked:
            plt.figure(figsize=(12, 8))
            plot_tree(clf, feature_names=features_encoded.columns, class_names=target.unique(), filled=True, rounded=True)
            plt.show()

        predicted_application = predictions[0]
        self.predicted_label.config(text=f"Predicted Application: {predicted_application}")


    # Reactivates tree when button is clicked
    def button_click_handler(self):
        self.view_tree_button_clicked = True
        self.decision_tree()
        self.view_tree_button_clicked = False

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

    def create_buttons(self):
        button_texts = [
            "Google Chrome", "Microsoft Edge", "Mozilla Firefox",
            "Microsoft Word", "Microsoft Excel", "Microsoft PowerPoint",
            "Windows Media Player", "Spotify", "Microsoft Outlook", "Mozilla Thunderbird"
        ]

        for i, text in enumerate(button_texts):
            button = tk.Button(self.root, text=text, command=lambda i=i: self.on_button_click(i + 1))
            button.pack(pady=5)

    def on_button_click(self, button_number):
        if button_number == 1:
            selected_application = "Google Chrome"
        elif button_number == 2:
            selected_application = "Microsoft Edge"
        elif button_number == 3:
            selected_application = "Mozilla Firefox"
        elif button_number == 4:
            selected_application = "Microsoft Word"
        elif button_number == 5:
            selected_application = "Microsoft Excel"
        elif button_number == 6:
            selected_application = "Microsoft PowerPoint"
        elif button_number == 7:
            selected_application = "Windows Media Player"
        elif button_number == 8:
            selected_application = "Spotify"
        elif button_number == 9:
            selected_application = "Microsoft Outlook"
        elif button_number == 10:
            selected_application = "Mozilla Thunderbird"

        # Increment a counter from 0 to num_entries
        counter = self.counter % len(self.bht)
        self.counter += 1

        if selected_application == predicted_application:
            print("Selected application matches the predicted application.")
            self.update_bht(counter, 1)
            self.predicted_bht()
            self.actual_bht()
        else:
            print("Selected application does not match the predicted application.")
            self.update_bht(counter, 0)
            self.predicted_bht()
            self.actual_bht()
        
        # Call decision_tree to update occurrences in the DataFrame
        self.selected_application = selected_application
        self.decision_tree()


if __name__ == "__main__":
    root = tk.Tk()
    num_entries = 10
    app = BHTVisualizer(root, num_entries)
    root.mainloop()