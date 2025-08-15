import pandas as pd
from faker import Faker
import random
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def scramble_data(input_path, output_path):
    """
    Scrambles personal data from a CSV or Excel file and saves the result.

    Args:
        input_path (str): The path to the original data file.
        output_path (str): The path to save the scrambled file.

    Returns:
        str: A success or error message.
    """
    try:
        # Determine file type based on extension
        file_extension = os.path.splitext(input_path)[1].lower()
        if file_extension == '.csv':
            df = pd.read_csv(input_path)
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(input_path)
        else:
            return "Error: Unsupported file format. Please use a .csv or .xlsx file."

    except FileNotFoundError:
        return f"Error: The file at '{input_path}' was not found."
    except Exception as e:
        return f"Error while reading the file: {e}"

    Faker.seed(0)
    fake = Faker()

    scrambled_df = df.copy()

    scrambling_map = {
        'name': fake.name,
        'first_name': fake.first_name,
        'last_name': fake.last_name,
        'full_name': fake.name,
        'email': fake.email,
        'address': fake.address,
        'city': fake.city,
        'state': fake.state,
        'zip_code': fake.postcode,
        'phone_number': fake.phone_number,
        'credit_card': fake.credit_card_number,
        'ssn': fake.ssn
    }

    for column in scrambled_df.columns:
        col_lower = column.lower().strip()
        if col_lower in scrambling_map:
            scrambled_df[column] = [scrambling_map[col_lower]() for _ in range(len(scrambled_df))]
        elif col_lower == 'age':
            scrambled_df[column] = scrambled_df[column].apply(lambda x: max(0, x + random.randint(-5, 5)))

    try:
        if file_extension == '.csv':
            scrambled_df.to_csv(output_path, index=False)
        else:
            scrambled_df.to_excel(output_path, index=False)
        return "Success: The file was scrambled and saved."
    except Exception as e:
        return f"Error while saving the file: {e}"


# ----------------------------------------------------------------------------------------------------------------------

class DataScramblerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Data Scrambler")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.bg_color = "#f0f0f0"
        self.btn_color = "#4CAF50"
        self.btn_active_color = "#45a049"
        self.label_font = ("Helvetica", 12)
        self.btn_font = ("Helvetica", 10, "bold")
        self.status_font = ("Helvetica", 10, "italic")

        self.main_frame = tk.Frame(root, padx=20, pady=20, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.main_frame, text="Personal Data Scrambler", font=("Helvetica", 16, "bold"),
                                    bg=self.bg_color)
        self.title_label.pack(pady=10)

        self.input_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.input_frame.pack(pady=10, fill=tk.X)

        self.input_label = tk.Label(self.input_frame, text="Select Input File:", font=self.label_font, bg=self.bg_color)
        self.input_label.pack(side=tk.LEFT)

        self.input_entry = tk.Entry(self.input_frame, width=40, font=self.label_font)
        self.input_entry.pack(side=tk.LEFT, padx=(5, 0))

        self.browse_btn = tk.Button(self.input_frame, text="Browse", command=self.browse_file, font=self.btn_font,
                                    bg=self.btn_color, fg="white", activebackground=self.btn_active_color)
        self.browse_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.main_frame, text="Please select a file and click 'Scramble'",
                                     font=self.status_font, bg=self.bg_color)
        self.status_label.pack(pady=20)

        self.scramble_btn = tk.Button(self.main_frame, text="Scramble Data", command=self.scramble,
                                      font=("Helvetica", 14, "bold"), bg="#FF5722", fg="white",
                                      activebackground="#E64A19", width=20, height=2)
        self.scramble_btn.pack(pady=10)

        self.exit_btn = tk.Button(self.main_frame, text="Exit", command=root.quit, font=self.btn_font, bg="#9E9E9E",
                                  fg="white", activebackground="#757575")
        self.exit_btn.pack(pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Data Files", "*.csv *.xlsx"), ("All Files", "*.*")]
        )
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)
            self.status_label.config(text="File selected. Ready to scramble.")

    def scramble(self):
        input_path = self.input_entry.get()
        if not input_path:
            messagebox.showerror("Error", "Please select an input file first.")
            return

        if not os.path.exists(input_path):
            messagebox.showerror("Error", f"File not found: {input_path}")
            return

        try:
            directory, filename = os.path.split(input_path)
            base, ext = os.path.splitext(filename)
            output_path = os.path.join(directory, f"scrambled_{base}{ext}")

            self.status_label.config(text="Scrambling in progress...")
            self.root.update_idletasks()

            result_message = scramble_data(input_path, output_path)

            if result_message.startswith("Success"):
                self.status_label.config(text="Scrambling complete. Output saved.")
                messagebox.showinfo("Success", f"File successfully scrambled!\nOutput saved to:\n{output_path}")
            else:
                self.status_label.config(text="Scrambling failed.")
                messagebox.showerror("Error", result_message)
        except Exception as e:
            messagebox.showerror("An unexpected error occurred", str(e))
            self.status_label.config(text="Scrambling failed.")


if __name__ == "__main__":
    # Ensure a proper Tkinter window is created and run
    try:
        root = tk.Tk()
        app = DataScramblerApp(root)
        root.mainloop()
    except Exception as e:
        # Fallback to a simple console message if the GUI fails for some reason
        print(f"An error occurred while starting the GUI: {e}")
        print("Please ensure you have the required libraries installed with 'pip install pandas faker openpyxl'.")