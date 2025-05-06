import tkinter as tk
from tkinter import filedialog
import zipfile
import json
import sys

def open_file_dialog():
   file_path = filedialog.askopenfilename(title="Select a CRX file", filetypes=[("CRX Files", "*.crx")])
   if file_path:
       file_label.config(text=f"Selected CRX File: {file_path}")
       display_manifest_permissions(file_path)


def display_manifest_permissions(crx_file):
   with zipfile.ZipFile(crx_file, 'r') as zip_ref:
       manifest_content = zip_ref.read('manifest.json').decode('utf-8')
       manifest_data = json.loads(manifest_content)


   permissions_listbox.delete(0, tk.END)  # Clear previous entries
   for permission in manifest_data.get('permissions', []):
       permissions_listbox.insert(tk.END, permission)


def remove_selected_permissions():
   selected_indices = permissions_listbox.curselection()
   for index in reversed(selected_indices):  # Iterate in reverse order to handle multiple deletions
       permissions_listbox.delete(index)




def extract_and_modify(crx_file):
   ext_name = crx_file.split("/")[-1].split(".")[0]
   unzipped_ext = f"ext_{ext_name}"


   selected_permissions = list(permissions_listbox.get(0, tk.END))
  
   with zipfile.ZipFile(crx_file, 'r') as zip_ref:
       zip_ref.extractall(unzipped_ext)


   manifest_path = f"{unzipped_ext}/manifest.json"
   with open(manifest_path, 'r') as manifest_file:
       manifest_data = json.load(manifest_file)


   manifest_data['permissions'] = selected_permissions


   with open(manifest_path, 'w') as manifest_file:
       json.dump(manifest_data, manifest_file, indent=2)

   # ⚠️ Insecure use of eval (CodeQL should detect this)
   user_input = sys.argv[1]  # Simulated user input from command line
   result = eval(user_input)  # ⚠️ Dangerous

   print(f"CRX file '{crx_file}' extracted and modified in '{unzipped_ext}'")


root = tk.Tk()
root.title("CRX File Access UI")


file_label = tk.Label(root, text="Selected CRX File: None")
file_label.pack(pady=10)


open_button = tk.Button(root, text="Open CRX File", command=open_file_dialog)
open_button.pack(pady=10)


permissions_label = tk.Label(root, text="Manifest Permissions:")
permissions_label.pack()


permissions_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, exportselection=0)
permissions_listbox.pack(pady=10)


remove_button = tk.Button(root, text="Remove Selected Permissions", command=remove_selected_permissions)
remove_button.pack(pady=10)


extract_button = tk.Button(root, text="Extract and Modify", command=lambda: extract_and_modify(file_label.cget("text").split(": ")[1]))
extract_button.pack(pady=10)


root.mainloop()

