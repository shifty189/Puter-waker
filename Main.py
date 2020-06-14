# this program is designed to work in windows to produce "Magic Packets" to wake devices over the LAN

from wakeonlan import send_magic_packet
from tkinter import messagebox
import tkinter as tk
# import re

def wake():
    print(mac_text.get())
    try:
        send_magic_packet(mac_text.get())
    except ValueError:
        messagebox.showerror(message="Incorrect MAC address entered")
    
main = tk.Tk(screenName="Puter Waker", baseName="Waker", className="Waker")
main.title('Puter Waker 0.3')

describe_lab = tk.Label(main, text="Enter the MAC address of the computer you want to wake").grid(row=0, columnspan=2)
mac_text = tk.StringVar()
# mac_text.set(" ")
mac_entry = tk.Label(main, text="Mac Address:").grid(row=1, column=0)
mac_input = tk.Entry(main, textvariable= mac_text).grid(row=1, column=1)
#or_label = tk.Label(main, text="or").grid(row=2, columnspan=2)
#ip_text = tk.StringVar()
#ip_text.set("Not working just yet")
#ip_entry = tk.Label(main, text="IP Address", textvariable= ip_text).grid(row=3, column=0)
#ip_input = tk.Entry(main).grid(row=3, column=1)
enter_button = tk.Button(main, text="Wake!", command=wake).grid(row=4, columnspan=2)

tk.mainloop()
