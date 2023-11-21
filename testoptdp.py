import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

class BHTVisualizer:
    def __init__(self, root, num_entries):
        self.root = root
        self.root.title("Branch History Table Visualizer")

        # Reading Data and Store into array
        self.actual_execution_content = self.read_file('actualExecution.csv')

        # Initialize the BHT
        self.bht = self.initialize_bht(num_entries)

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

        self.subtitle_label = tk.Label(root, text="Execution by User: ", font=("Helvetica", 10), fg="blue")
        self.subtitle_label.pack(pady=10)

        self.actual_execution_content = tk.Label(root, text='\n'.join(self.actual_execution_content), font=("Helvetica", 10))
        self.actual_execution_content.pack()

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
       
        # Create a Treeview widget to display the table
        self.tree = ttk.Treeview(self.legend_frame, columns=['Category', 'Application', 'Occurrences', 'User Profile'], show='headings')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Application', text='Application')
        self.tree.heading('Occurrences', text='Occurrences')
        self.tree.heading('User Profile', text='User Profile')
        self.tree.pack(pady=10)

        self.decision_tree()

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

    def user_profile_selected(self, event):
        self.decision_tree()

    def decision_tree(self):
        # collecting data from csv file
        col_names = ['Category', 'Application', 'Occurrences', 'User Profile']
        df = pd.read_csv("data.csv", header=0, names=col_names)

        # filter row of choice
        selected_profile = self.selected_user_profile.get()
        filtered_df = df[df['User Profile'] == selected_profile]

        # Clearing current items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Inserting data
        for index, row in filtered_df.iterrows():
            # Use df.columns[-1] to reference the last column dynamically
            values = (row['Category'], row['Application'], row['Occurrences'], row['User Profile'])
            self.tree.insert("", "end", values=values)

        # Prepare data for training the decision tree
        features = filtered_df[['Category', 'Occurrences', 'User Profile']]
        target = filtered_df['Application']

        # Encode categorical variables if needed
        features_encoded = pd.get_dummies(features)
        features_train, features_test, target_train, target_test = train_test_split(features_encoded, target, test_size=0.2, random_state=42)

        # Train a decision tree classifier
        clf = DecisionTreeClassifier()
        clf.fit(features_encoded, target)

        # Make predictions for the existing data
        predictions = clf.predict(features_encoded)
        
        # Visualize the decision tree
        plt.figure(figsize=(12, 8))
        plot_tree(clf, feature_names=features_encoded.columns, class_names=target.unique(), filled=True, rounded=True)
        plt.show()

        # Order of array represents likelihood of each application being started first
        print("Predicted Applications for the existing data:")
        print(predictions)       

if __name__ == "__main__":
    root = tk.Tk()
    num_entries = 10
    app = BHTVisualizer(root, num_entries)
    root.mainloop()
