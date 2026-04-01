# Advanced Network Port Scanner (Beautiful GUI)
# ==================================================

import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# ==============================
# PORT SCAN FUNCTION
# ==============================
def scan_port(target, port, results):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown"
            results.append((port, service))

        sock.close()
    except:
        pass

# ==============================
# MAIN SCAN
# ==============================
def start_scan():
    target = entry.get()

    if not target:
        messagebox.showwarning("Warning", "Enter target IP or domain")
        return

    result_box.delete(*result_box.get_children())
    status_label.config(text="Scanning...")

    ports = range(1, 1025)
    threads = []
    results = []

    def run():
        for port in ports:
            t = threading.Thread(target=scan_port, args=(target, port, results))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        for port, service in sorted(results):
            result_box.insert("", "end", values=(port, service))

        status_label.config(text="Scan Complete")

    threading.Thread(target=run).start()

# ==============================
# GUI DESIGN (Modern)
# ==============================
root = tk.Tk()
root.title("Advanced Port Scanner")
root.geometry("650x500")
root.configure(bg="#1e1e2f")

# Title
label = tk.Label(root, text="Advanced Network Port Scanner", font=("Arial", 18, "bold"), bg="#1e1e2f", fg="white")
label.pack(pady=15)

# Input Frame
frame = tk.Frame(root, bg="#1e1e2f")
frame.pack(pady=10)

entry = tk.Entry(frame, width=30, font=("Arial", 12))
entry.grid(row=0, column=0, padx=10)

scan_btn = tk.Button(frame, text="Scan", command=start_scan, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
scan_btn.grid(row=0, column=1)

# Table (Treeview)
columns = ("Port", "Service")
result_box = ttk.Treeview(root, columns=columns, show="headings")

result_box.heading("Port", text="Port")
result_box.heading("Service", text="Service")

result_box.pack(pady=20, fill="both", expand=True)

# Status
status_label = tk.Label(root, text="Idle", bg="#1e1e2f", fg="lightgreen")
status_label.pack(pady=5)

root.mainloop()