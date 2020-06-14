from wakeonlan import send_magic_packet
from tkinter import messagebox
import tkinter as tk
# import re

def wake():
    #regextext = "^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$"
    #print(re.match(regextext, mac_text.get()))
    print(mac_text.get())
    try:
        send_magic_packet(mac_text.get())
    except ValueError:
        messagebox.showerror(message="Incorrect MAC address entered")
    # if re.match(regextext, mac_text.get()):
    #     send_magic_packet(mac_text.get())
    #     messagebox.showinfo(message='Magic Packet sent to ' + mac_text.get())
    # else:
    #     messagebox.showerror(title= "Enter Mac", message="Must enter MAC address of target device\n example: 00:11:22:33:44:55")

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
