import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

# File path for the config file
CONFIG_FILE = 'config.json'

# Define the API URL
API_URL = 'https://api.cloudflare.com/client/v4'

# Function to get the current IP address
def get_current_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        response.raise_for_status()
        ip = response.json()['ip']
        return ip
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Error getting current IP: {e}")
        return None

# Function to update DNS records
def update_dns_record(manual=True):
    # Check if all fields are filled
    for tab in tab_control.tabs():
        record_frame = tab_control.nametowidget(tab)
        api_token = record_frame.api_token_entry.get()
        zone_id = record_frame.zone_id_entry.get()
        record_name = record_frame.record_name_entry.get()
        record_id = record_frame.record_id_entry.get()

        if not all([api_token, zone_id, record_name, record_id]):
            messagebox.showerror("Error", "Please Fill In All Fields")
            return

    # If all fields are filled, proceed with updating DNS records
    current_ip = get_current_ip()
    if current_ip:
        # Update the current IP label for all tabs
        for tab in tab_control.tabs():
            record_frame = tab_control.nametowidget(tab)
            if hasattr(record_frame, 'current_ip_label'):
                record_frame.current_ip_label.config(text=f"Current IP: {current_ip}")

        # Proceed with DNS record update
        for tab in tab_control.tabs():
            record_frame = tab_control.nametowidget(tab)
            url = f"{API_URL}/zones/{record_frame.zone_id_entry.get()}/dns_records/{record_frame.record_id_entry.get()}"
            headers = {
                'Authorization': f'Bearer {record_frame.api_token_entry.get()}',
                'Content-Type': 'application/json',
            }
            data = {
                'type': 'A',
                'name': record_frame.record_name_entry.get(),
                'content': current_ip,
                'ttl': 1,
                'proxied': record_frame.proxy_var.get()
            }
            try:
                response = requests.put(url, headers=headers, data=json.dumps(data))
                response.raise_for_status()
                if hasattr(record_frame, 'record_ip_label'):
                    record_frame.record_ip_label.config(text=f"Record IP: {current_ip}")
                if manual:
                    messagebox.showinfo("Success", f"DNS record updated successfully to {current_ip}")
            except requests.RequestException as e:
                messagebox.showerror("Error", f"Error updating DNS record: {e}")

# Function to save the configuration to a file
def save_config():
    config_data = []
    for tab in tab_control.tabs():
        record_frame = tab_control.nametowidget(tab)
        record_data = {
            'api_token': record_frame.api_token_entry.get(),
            'zone_id': record_frame.zone_id_entry.get(),
            'record_name': record_frame.record_name_entry.get(),
            'record_id': record_frame.record_id_entry.get(),
            'proxy_enabled': record_frame.proxy_var.get(),
            'update_interval': record_frame.update_interval.get()
        }
        config_data.append(record_data)

    try:
        with open(CONFIG_FILE, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        messagebox.showinfo("Save", "Configuration saved successfully.")
    except IOError as e:
        messagebox.showerror("Error", f"Error saving configuration: {e}")

# Function to load the configuration from a file
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as config_file:
                config_data = json.load(config_file)

            # Remove existing tabs before loading new ones
            for tab in tab_control.tabs():
                tab_control.forget(tab)

            for record_data in config_data:
                if isinstance(record_data, dict):  # Ensure record_data is a dictionary
                    new_tab = tk.Frame(tab_control)
                    create_record_frame(new_tab)
                    tab_control.add(new_tab, text=f"Record {len(tab_control.tabs()) + 1}")
                    tab_control.select(new_tab)

                    record_frame = tab_control.nametowidget(tab_control.select())
                    record_frame.api_token_entry.insert(0, record_data.get('api_token', ''))
                    record_frame.zone_id_entry.insert(0, record_data.get('zone_id', ''))
                    record_frame.record_name_entry.insert(0, record_data.get('record_name', ''))
                    record_frame.record_id_entry.insert(0, record_data.get('record_id', ''))
                    record_frame.proxy_var.set(record_data.get('proxy_enabled', False))
                    record_frame.update_interval.set(record_data.get('update_interval', '10'))
                    
                    # Update the current IP label after loading config
                    current_ip = get_current_ip()
                    if current_ip and hasattr(record_frame, 'current_ip_label'):
                        record_frame.current_ip_label.config(text=f"Current IP: {current_ip}")

            messagebox.showinfo("Load", "Configuration loaded successfully.")
        except IOError as e:
            messagebox.showerror("Error", f"Error loading configuration: {e}")
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Error decoding JSON: {e}")
    else:
        messagebox.showwarning("Load", "No configuration file found.")

# Function to add a new tab
def add_record_tab():
    if len(tab_control.tabs()) < 6:  # Limit to 6 tabs
        new_tab = tk.Frame(tab_control)
        create_record_frame(new_tab)
        tab_control.add(new_tab, text=f"Record {len(tab_control.tabs()) + 1}")
        tab_control.select(new_tab)
    else:
        messagebox.showwarning("CFAutoDNS", "Maximum number of records reached.")

# Function to delete the current tab
def delete_record_tab():
    if len(tab_control.tabs()) > 1:
        tab_control.forget(tab_control.select())
    else:
        messagebox.showwarning("CFAutoDNS", "You must have at least one record.")

# Function to create the record management interface inside a tab
def create_record_frame(record_frame):
    entry_width = 50

    tk.Label(record_frame, text="API Token:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    record_frame.api_token_entry = tk.Entry(record_frame, width=entry_width)
    record_frame.api_token_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=2, sticky="w")

    tk.Label(record_frame, text="Zone ID:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    record_frame.zone_id_entry = tk.Entry(record_frame, width=entry_width)
    record_frame.zone_id_entry.grid(row=1, column=1, padx=10, pady=5, columnspan=2, sticky="w")

    tk.Label(record_frame, text="Record Name:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    record_frame.record_name_entry = tk.Entry(record_frame, width=entry_width)
    record_frame.record_name_entry.grid(row=2, column=1, padx=10, pady=5, columnspan=2, sticky="w")

    tk.Label(record_frame, text="Record ID:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    record_frame.record_id_entry = tk.Entry(record_frame, width=entry_width - 10)
    record_frame.record_id_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    get_id_button = tk.Button(record_frame, text="Get", command=lambda: get_record_id(record_frame), width=7)
    get_id_button.grid(row=3, column=2, padx=5, pady=5, sticky="w")

    record_frame.proxy_var = tk.BooleanVar(value=False)
    proxy_checkbox = tk.Checkbutton(record_frame, text="Enable Proxy", variable=record_frame.proxy_var)
    proxy_checkbox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    tk.Label(record_frame, text="Update Interval (Minutes):").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    record_frame.update_interval = tk.StringVar(value='10')
    interval_spinbox = tk.Spinbox(record_frame, from_=1, to=1440, textvariable=record_frame.update_interval, width=10)
    interval_spinbox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    update_button = tk.Button(record_frame, text="Force Update Now", command=lambda: update_dns_record())
    update_button.grid(row=7, column=0, columnspan=3, pady=10)

    record_frame.current_ip_label = tk.Label(record_frame, text="Current IP: N/A")
    record_frame.current_ip_label.grid(row=8, column=0, columnspan=3, pady=5)

    record_frame.record_ip_label = tk.Label(record_frame, text="Record IP: N/A")
    record_frame.record_ip_label.grid(row=9, column=0, columnspan=3, pady=5)

# Function to get the record ID from Cloudflare
def get_record_id(record_frame):
    api_token = record_frame.api_token_entry.get()
    zone_id = record_frame.zone_id_entry.get()
    record_name = record_frame.record_name_entry.get()

    if not all([api_token, zone_id, record_name]):
        messagebox.showerror("Error", "Please fill in API Token, Zone ID, and Record Name.")
        return

    url = f"{API_URL}/zones/{zone_id}/dns_records?name={record_name}"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        records = response.json().get('result', [])

        if records:
            record_id = records[0].get('id', 'Not found')
            record_frame.record_id_entry.delete(0, tk.END)
            record_frame.record_id_entry.insert(0, record_id)
        else:
            messagebox.showinfo("Info", "Record not found.")
            record_frame.record_id_entry.delete(0, tk.END)
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Error retrieving record ID: {e}")

# Main application window
root = tk.Tk()
root.title("CFAutoDNS")

tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill='both')

# Create the initial tab
initial_tab = tk.Frame(tab_control)
create_record_frame(initial_tab)
tab_control.add(initial_tab, text="Record 1")

# Create the button panel
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

add_tab_button = tk.Button(button_frame, text="Add Record", command=add_record_tab)
add_tab_button.grid(row=0, column=0, padx=5)

delete_tab_button = tk.Button(button_frame, text="Delete Record", command=delete_record_tab)
delete_tab_button.grid(row=0, column=1, padx=5)

save_button = tk.Button(button_frame, text="Save Configuration", command=save_config)
save_button.grid(row=0, column=2, padx=5)

load_button = tk.Button(button_frame, text="Load Configuration", command=load_config)
load_button.grid(row=0, column=3, padx=5)

# Load configuration on startup
load_config()

# Start the main loop
root.mainloop()
