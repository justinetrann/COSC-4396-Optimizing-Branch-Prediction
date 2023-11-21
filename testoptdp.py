import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

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
        self.subtitle_label.pack()

        self.actual_execution_content = tk.Label(root, text='\n'.join(self.actual_execution_content), font=("Helvetica", 10))
        self.actual_execution_content.pack()

        # Create a Treeview widget to display the table
        self.subtitle_label = tk.Label(self.legend_frame, text="Decision Tree Predicted Application\n", font=("Helvetica", 10), fg="blue")
        self.subtitle_label.pack()

        self.tree = ttk.Treeview(self.legend_frame)
        self.tree["columns"] = ("Category", "Predicted Application", "User Profile")
        self.tree.heading("#0", text="Index")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Predicted Application", text="Predicted Application")
        self.tree.heading("User Profile", text="User Profile")
        self.tree.pack()

        self.decision_tree()
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

    def decision_tree(self):
        # Read data from CSV - load dataset
        col_names = ['Category', 'Application', 'Occurrences', 'User Profile']
        df = pd.read_csv("data.csv", header=0, names=col_names)

        # One-hot encode categorical variables
        df_encoded = pd.get_dummies(df, columns=['Category', 'User Profile'])

        # Separate dataset features and target variable
        feature_cols = ['Category_Web Browser', 'Category_Office Suite', 'Category_Media Player', 'Category_Email Client',
                        'User Profile_Admin', 'User Profile_Guest', 'User Profile_User1', 'User Profile_User2',
                        'Occurrences']
        X = df_encoded[feature_cols]
        y = df_encoded['Application']

        # Split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)  # 70% training and 30% test

        # Train a Decision Tree Classifier
        clf = DecisionTreeClassifier()
        clf = clf.fit(X_train, y_train)

        # Predict the missing values
        missing_values = pd.DataFrame({'Category': ['Web Browser', 'Office Suite', 'Media Player', 'Email Client'],
                                    'User Profile': ['Admin', 'Admin', 'Admin', 'Admin'],
                                    'Occurrences': [0, 0, 0, 0]})  # Assuming default occurrence value is 0
        missing_values_encoded = pd.get_dummies(missing_values, columns=['Category', 'User Profile'])

        # Ensure that all columns used in training are present in missing_values_encoded
        missing_values_encoded = missing_values_encoded.reindex(columns=X.columns, fill_value=0)

        missing_values['Predicted Application'] = clf.predict(missing_values_encoded[feature_cols])

        # Display the completed table in the Treeview widget
        for index, row in missing_values.iterrows():
            self.tree.insert("", tk.END, values=(row['Category'], row['Predicted Application'], row['Occurrences'], row['User Profile']))
        
if __name__ == "__main__":
    root = tk.Tk()
    num_entries = 10
    app = BHTVisualizer(root, num_entries)
    root.mainloop()
