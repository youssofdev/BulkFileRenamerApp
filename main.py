import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

def preview_rename(directory, rename_option, custom_text, replace_existing):
    preview_list.delete(0, tk.END)  # Clear previous entries

    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            new_name = apply_rename_rules(filename, rename_option, custom_text, replace_existing)
            preview_list.insert(tk.END, f"{filename} -> {new_name}")

def rename_files(directory, rename_option, custom_text, replace_existing):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            new_name = apply_rename_rules(filename, rename_option, custom_text, replace_existing)
            new_path = os.path.join(directory, new_name)
            
            # Check if the new filename already exists
            if os.path.exists(new_path):
                base_name, file_extension = os.path.splitext(new_name)
                count = 1
                while True:
                    count += 1
                    new_name = f"{base_name} ({count}){file_extension}"
                    new_path = os.path.join(directory, new_name)
                    if not os.path.exists(new_path):
                        break
                        
            os.rename(os.path.join(directory, filename), new_path)

def apply_rename_rules(filename, rename_option, custom_text, replace_existing):
    base_name, file_extension = os.path.splitext(filename)
    if rename_option == "Lowercase":
        base_name = base_name.lower()
    elif rename_option == "Uppercase":
        base_name = base_name.upper()
    elif rename_option == "Remove Spaces":
        base_name = base_name.replace(" ", "")

    if replace_existing:
        return custom_text + file_extension
    else:
        if custom_text:
            return custom_text + base_name + file_extension
        else:
            return base_name + file_extension

def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)
    preview_rename(folder_path, rename_option_var.get(), custom_text_entry.get(), replace_existing_var.get())

def rename_button_click():
    directory = folder_entry.get()
    rename_option = rename_option_var.get()
    custom_text = custom_text_entry.get()
    replace_existing = replace_existing_var.get()
    if directory:
        rename_files(directory, rename_option, custom_text, replace_existing)
        preview_rename(directory, rename_option, custom_text, replace_existing)  # Update previews
        result_label.config(text="Files renamed successfully")
    else:
        result_label.config(text="Please select a folder")

app = tk.Tk()
app.title("Bulk File Renamer Application")

# Use ThemedStyle to set the theme for your application
style = ttk.Style()
style.theme_use("clam")  # Change the theme name as needed (e.g., "alt")

# Create and configure GUI elements
folder_label = ttk.Label(app, text="Select a folder:")  # Use ttk widgets
folder_label.pack()

folder_entry = ttk.Entry(app, width=40)
folder_entry.pack()

browse_button = ttk.Button(app, text="Browse", command=browse_folder)
browse_button.pack()

rename_option_var = tk.StringVar()
rename_option_var.set("Lowercase")  # Default option
rename_option_label = ttk.Label(app, text="Select Rename Option:")
rename_option_label.pack()

rename_option_menu = ttk.OptionMenu(app, rename_option_var, "Lowercase", "Uppercase", "Remove Spaces")
rename_option_menu.pack()

custom_text_label = ttk.Label(app, text="Custom Text:")
custom_text_label.pack()

custom_text_entry = ttk.Entry(app, width=40)
custom_text_entry.pack()

replace_existing_var = tk.BooleanVar()
replace_existing_var.set(False)  # Default is to add to the filename
replace_existing_checkbox = ttk.Checkbutton(app, text="Replace Existing Filename", variable=replace_existing_var)
replace_existing_checkbox.pack()

preview_label = ttk.Label(app, text="Preview of Renamed Files:")
preview_label.pack()

preview_list = tk.Listbox(app, width=40, height=6)
preview_list.pack()

rename_button = ttk.Button(app, text="Rename Files", command=rename_button_click)
rename_button.pack()

result_label = ttk.Label(app, text="", foreground="green")
result_label.pack()

github_label = ttk.Label(app, text="GitHub: youssofdev")
github_label.pack()

app.mainloop()
