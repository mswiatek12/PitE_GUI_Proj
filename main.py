import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

import numpy as np



class PlotApp:
    def __init__(self, root):

        self.root = root
        self.root.title("GpyUthIon")
        self.root.configure(bg="#484850")  # background color

        # Lets add some style
        style = ttk.Style()
        style.configure("TButton",
                        font=("Courier", 12),
                        padding=6,
                        bg="#484850",
                        relief="flat",
                        anchor="center")
        
        style.configure("TLabel", font=("Courier", 12), background="#484850",  fg="white")
        style.configure("TCombobox", font=("Courier", 12), padding=5)
        style.configure("TText", font=("Courier", 10), padding=5)
        style.map("TButton",
            background=[("active", "#3f51c1"),
                        ("!active", "#484850")],  # Set background on hover
            relief=[("active", "flat")])

        # tk.button for file selection
        self.file_label = tk.Label(root, text="NO FILE", bg="#484850", font=("Courier", 12),  fg="white")
        self.file_label.pack(pady=10)

        self.browse_button = ttk.Button(root, text="Select File", command=self.browse_file)
        self.browse_button.pack(pady=10)

        # readin' Data
        self.preview_label = tk.Label(root, text="Data in file:", bg="#484850", font=("Courier", 12),  fg="white")
        self.preview_label.pack(pady=5)

        self.text_preview = tk.Text(root, height=10, width=80, wrap=tk.WORD)
        self.text_preview.pack(pady=10)

        # plottin'
        self.options_frame = tk.Frame(root, bg="#484850")
        self.options_frame.pack(pady=10)

        self.x_label = tk.Label(self.options_frame, text="X:", bg="#484850", font=("Courier", 12),  fg="white")
        self.x_label.grid(row=0, column=0, padx=5)

        self.x_combobox = ttk.Combobox(self.options_frame, state="readonly")
        self.x_combobox.grid(row=0, column=1, padx=5)

        self.y_label = tk.Label(self.options_frame, text="Y:", bg="#484850", font=("Courier", 12), fg="white")
        self.y_label.grid(row=0, column=2, padx=5)

        self.y_combobox = ttk.Combobox(self.options_frame, state="readonly")
        self.y_combobox.grid(row=0, column=3, padx=5)

        self.plot_type_label = tk.Label(self.options_frame, text="Plot Type:", bg="#484850", font=("Courier", 12),  fg="white")
        self.plot_type_label.grid(row=0, column=4, padx=5)

        self.plot_type_combobox = ttk.Combobox(self.options_frame, state="readonly")
        self.plot_type_combobox["values"] = ["Line", "Bar", "Scatter"]
        self.plot_type_combobox.set("Line")
        self.plot_type_combobox.grid(row=0, column=5, padx=5)

        self.plot_button = ttk.Button(root, text="Plot", command=self.plot_data)
        self.plot_button.pack(pady=10)

        # frame for plotting area (toolbar added)
        self.toolbar_frame = tk.Frame(root)
        self.toolbar_frame.pack(pady=5)

        self.plot_frame = tk.Frame(root)
        self.plot_frame.pack(pady=10)

    def browse_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), 
                                                        ("Excel files", "*.xlsx"),
                                                        ("Text files", "*.txt"), 
                                                        ("All files", "*.*")])
        if filepath:
            self.file_label.config(text=filepath)
            self.load_data(filepath)
            self.plot_button.pack()

    def load_data(self, filepath):
        try:
            if filepath.endswith('.csv'):
                self.data = pd.read_csv(filepath)
            elif filepath.endswith('.xlsx'):
                self.data = pd.read_excel(filepath)
            elif filepath.endswith('.txt'):
                self.data = pd.read_csv(filepath, delimiter="\t")  # default case set
            else:
                raise ValueError("Unsupported file format")

            # update data preview and combobox options
            self.text_preview.delete("1.0", tk.END)
            self.text_preview.insert(tk.END, self.data.head().to_string())  # returns first 5 lines of the data

            columns = self.data.columns.tolist()
            self.x_combobox["values"] = columns
            self.y_combobox["values"] = columns
        except Exception as e:
            self.text_preview.delete("1.0", tk.END)
            self.text_preview.insert(tk.END, f"Error loading file: {e}")
            # we handle the error as clearing preview box and writing error

    def plot_data(self):
        x_col = self.x_combobox.get()
        y_col = self.y_combobox.get()  # we getting chosen options-_-
        plot_type = self.plot_type_combobox.get()

        if not x_col or not y_col:
            self.text_preview.insert(tk.END, "\nChoose the plot's axis first")
            return

        # plottin'
        fig, ax = plt.subplots(figsize=(5, 4))
        colors = np.random.rand(len(self.data))  # random colors for Scatter or Bar plot

        if plot_type == "Line":
            ax.plot(self.data[x_col], self.data[y_col], color="pink", label=f"{y_col} vs {x_col}")

        elif plot_type == "Bar":
            ax.bar(self.data[x_col], self.data[y_col], label=f"{y_col} vs {x_col}")

        elif plot_type == "Scatter":
            ax.scatter(self.data[x_col], self.data[y_col], cmap="viridis", label=f"{y_col} vs {x_col}")

        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.legend()

        # clear previous plot and embed the new one
        for widget in self.plot_frame.winfo_children():
            widget.destroy()  # remove the existing plot (if any)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)  # taking a figure and embedding to frame
        canvas.draw()
        canvas.get_tk_widget().pack()

        for widget in self.toolbar_frame.winfo_children():
            widget.destroy()
        toolbar = NavigationToolbar2Tk(canvas, self.toolbar_frame)
        toolbar.update()

# run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PlotApp(root)
    root.mainloop()
