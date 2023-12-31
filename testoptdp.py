import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

'''
Name: Justine Tran
UHID: 1986572

The purpose of this project was to research the Worst-Case Execution Time (WCET) 
of a branch prediction table when combined with a decision tree.

Originally integrated for testing in gem5, however, due to some issues 
with missing or unincorporated functions in gem5, we created a 
dummy version of a branch prediction table to store results chosen by 
the user and updated values within the CSV to represent branch predictions.

Our goal was to learn more about how a decision tree would perform 
in predicting the initial application a user might choose when turning on a PC.

How the Program Works:
The table is loaded with data from four different users: Admin, Guest, User1, and User2,
each containing different data. Every time they turn on the PC, the initial 
application chosen by them is recorded.

The decision tree takes this data and creates four different tables, and a prediction is made
based on the number of occurrences the user has picked a specific program.

You can update the list by acting as the user and clicking an application when a PC has started.
For every button click, we assume that the PC has just started. The predicted decision tree has a
predicted application and compares if the application chosen by you matches. It will
update the queue as taken = 1 or not taken = 0, then update its data in the CSV.
'''

class BHTVisualizer:
    # Contains all labels, comments, and methods in widget
    def __init__(self, root, num_entries):
        self.root = root
        self.root.title("Branch History Table Visualizer")

        # Initialize the BHT with given num_entries assume max 10 entries
        self.bht = self.initialize_bht(num_entries)
        self.counter = 0

        # Create Key for user to understand different categories
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

        # Create Legend that allows users to understand queue and prediction made by decision tree
        self.legend_taken = tk.Label(root, text="Taken = 1", fg="green", font=("Helvetica", 10))
        self.legend_taken.pack(anchor=tk.W, padx=10)

        self.legend_not_taken = tk.Label(root, text="Not Taken = 0", fg="red", font=("Helvetica", 10))
        self.legend_not_taken.pack(anchor=tk.W, padx=10)

        self.predicted_label = tk.Label(root, text="Predicted Application:", font=("Helvetica", 10), fg="purple")
        self.predicted_label.pack(anchor=tk.W, padx=10)

        # Setting Up Widget based on num_entries
        canvas_width = num_entries * (50 + 10)
        canvas_height = 2 * (50 + 10)

        # Setting up Queue to be updated by Buttons Clicked by User
        self.canvas_title_label_predicted = tk.Label(root, text="Predicted by Decision Tree", font=("Helvetica", 10), fg="purple")
        self.canvas_title_label_predicted.pack()

        self.predicted_canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.predicted_canvas.pack()

        self.canvas_title_label_actual = tk.Label(root, text="Actual Execution", font=("Helvetica", 10), fg="purple")
        self.canvas_title_label_actual.pack()

        self.actual_canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
        self.actual_canvas.pack()

        # Setting up buttons to allow users to update queue and data.csv
        self.subtitle_label = tk.Label(root, text="Start the program with a button click each time it's the user's first program launched", font=("Helvetica", 10), fg="blue")
        self.subtitle_label.pack(pady=10)

        # Calling methods, to update queue and allow button interaction
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

        # Calling method to produce decision tree results and table
        self.decision_tree()

    # Determine which user profile has been selected: Admin, Guest, User 1, User 2
    def user_profile_selected(self, event):
        self.decision_tree()

    # Creating Decision Tree:
    # (1) Given provided data, separate data into 4 groups: Admin, Guest, User 1. and User 2
    # (2) Create table, from table sort based on occurances
    # (3) Make predicition on most likely applcation user to select, when turning on PC
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

        # Used to update table occurances based on button
        # When a user clicks a button to a specific application occurance is updated
        # Representing a branch predicition table, updates
        if hasattr(self, 'selected_application'):
            selected_application = self.selected_application
            selected_profile = self.selected_user_profile.get()

            # Find the row corresponding to the selected application and profile
            mask = (df['Application'] == selected_application) & (df['User Profile'] == selected_profile)
            if not df[mask].empty:
                # Update occurrences for the selected application and profile
                df.loc[mask, 'Occurrences'] += 1

        # Place occurance into data.csv
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


    # Allows User to View prediction made from, View Tree
    # Resets view_tree_button_clicked when new user has been changed to view their data
    def button_click_handler(self):
        self.view_tree_button_clicked = True
        self.decision_tree()
        self.view_tree_button_clicked = False

    # Setting Up Queue for predicted and actual 
    def initialize_bht(self, num_entries):
        return [0] * num_entries
    
    # Used to update Queue, when user clicks a button
    # Taken = 1 and Not Taken = 0, used within def on_button_click(self, button_number):
    def update_bht(self, index, outcome):
        self.bht[index] = outcome

    # Created to represent decision tree predicted application
    # All is set to match the predicted application aka. if it is Google Chrome
    # Then we will compare Google Chrome == [Button Chosen by user]
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

    # Created to represent Users Chosen Application
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

    # Used to Produce buttons to be chosen by user
    def create_buttons(self):
        button_texts = [
            "Google Chrome", "Microsoft Edge", "Mozilla Firefox",
            "Microsoft Word", "Microsoft Excel", "Microsoft PowerPoint",
            "Windows Media Player", "Spotify", "Microsoft Outlook", "Mozilla Thunderbird"
        ]

        for i, text in enumerate(button_texts):
            button = tk.Button(self.root, text=text, command=lambda i=i: self.on_button_click(i + 1))
            button.pack(pady=5)

    # When a user clicks a button, the queue gets updated
    # And the data.csv gets updated
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

        # Used to only allow users to click num_entries applcation
        counter = self.counter % len(self.bht)
        self.counter += 1

        # When a user has selected a program Updata Queue
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
        
        # Call decision_tree to update occurrences in the DataFrame, after button has been selected
        self.selected_application = selected_application
        self.decision_tree()


if __name__ == "__main__":
    root = tk.Tk()
    num_entries = 10
    app = BHTVisualizer(root, num_entries)
    root.mainloop()