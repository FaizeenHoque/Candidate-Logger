import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import random
import os

# Function to add a candidate to the CSV file
def add_candidate():
    genre = genre_entry.get()
    username = name_entry.get()
    age = age_entry.get()
    candidate_id = f"1100{random.randint(1111, 9999)}"
    
    if not genre or not username or not age:
        messagebox.showerror("Error", "All fields must be filled out")
        return
    
    # Check if the CSV file exists and write headers if it does not
    if not os.path.exists(csv_name):
        with open(csv_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Genre', 'Name', 'Age'])  # Write header row
    
    with open(csv_name, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([candidate_id, genre, username, age])
    
    messagebox.showinfo("Success", f"Candidate with ID {candidate_id} has been added")
    update_candidates_list()

# Function to remove a candidate from the CSV file
def remove_candidate():
    candidate_id = remove_id_entry.get()
    rows = []
    
    if not os.path.exists(csv_name):
        messagebox.showerror("Error", "CSV file does not exist")
        return

    with open(csv_name, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader, None)
        rows = list(reader)

    with open(csv_name, 'w', newline='') as file:
        writer = csv.writer(file)
        if headers:
            writer.writerow(headers)
        removed = False
        for row in rows:
            if row[0] != candidate_id:
                writer.writerow(row)
            else:
                removed = True

    if removed:
        messagebox.showinfo("Success", f"Candidate with ID {candidate_id} has been removed")
    else:
        messagebox.showerror("Error", "Candidate ID not found")
    update_candidates_list()

# Function to update the candidates list
def update_candidates_list():
    candidates_listbox.delete(0, tk.END)
    if os.path.exists(csv_name):
        with open(csv_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                candidates_listbox.insert(tk.END, f"ID: {row[0]}, Genre: {row[1]}, Name: {row[2]}, Age: {row[3]}")
    else:
        return 0

# Main program
def main():
    global csv_name
    csv_name = simpledialog.askstring("Input", "Please enter a name for the CSV file (include .csv extension): ")
    if not csv_name.endswith('.csv'):
        messagebox.showerror("Error", "The file name must end with '.csv'")
        return

    global root, genre_entry, name_entry, age_entry, remove_id_entry, candidates_listbox

    root = tk.Tk()
    root.title("Candidate Logger")
    root.geometry("1200x400")
    root.resizable(False, False)

    title_label = tk.Label(root, text="Candidate Logger", font=("Helvetica", 18))
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    add_frame = tk.Frame(root)
    add_frame.grid(row=1, column=0, padx=10, pady=10)

    tk.Label(add_frame, text="Genre: ", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
    genre_entry = tk.Entry(add_frame, font=("Helvetica", 12))
    genre_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_frame, text="Name: ", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5)
    name_entry = tk.Entry(add_frame, font=("Helvetica", 12))
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_frame, text="Age: ", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5)
    age_entry = tk.Entry(add_frame, font=("Helvetica", 12))
    age_entry.grid(row=2, column=1, padx=10, pady=5)

    add_button = tk.Button(root, text="Add Candidate", command=add_candidate, font=("Helvetica", 12))
    add_button.grid(row=2, column=0, pady=10)

    remove_frame = tk.Frame(root)
    remove_frame.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(remove_frame, text="Remove by ID: ", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5)
    remove_id_entry = tk.Entry(remove_frame, font=("Helvetica", 12))
    remove_id_entry.grid(row=0, column=1, padx=10, pady=5)

    remove_button = tk.Button(remove_frame, text="Remove Candidate", command=remove_candidate, font=("Helvetica", 12))
    remove_button.grid(row=1, column=0, columnspan=2, pady=10)

    candidates_frame = tk.Frame(root)
    candidates_frame.grid(row=0, column=2, rowspan=3, padx=20, pady=10, sticky="nsew")

    candidates_label = tk.Label(candidates_frame, text="Candidates", font=("Helvetica", 14))
    candidates_label.pack()

    scrollbar = tk.Scrollbar(candidates_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    candidates_listbox = tk.Listbox(candidates_frame, font=("Helvetica", 12), yscrollcommand=scrollbar.set, height=18, width=55)
    candidates_listbox.pack(fill=tk.BOTH, expand=True)

    scrollbar.config(command=candidates_listbox.yview)

    update_candidates_list()

    root.mainloop()

if __name__ == "__main__":
    main()
