# reference https://pypi.org/project/wakeonlan/

from wakeonlan import send_magic_packet
from tkinter import messagebox
import tkinter as tk
import os
# import re


def arp():
    with os.popen("arp -a") as a:
        arpData = a.read()

    arp_window = tk.Tk(screenName="Current Arp Table")
    arp_window.title("Current Arp Table")

    arp_display = tk.Label(arp_window, text=arpData)
    arp_display.grid(row=0, column=0)


def wake():
    print(mac_text.get())
    try:
        send_magic_packet(mac_text.get())
        messagebox.showinfo(title="Wake sent", message="WOL sent to " + mac_text.get())
    except ValueError:
        messagebox.showerror(title="MAC Error", message="Incorrect MAC address entered")
    except:
        print('something went wrong')


main = tk.Tk(screenName="Puter Waker", baseName="Waker", className="Waker")
main.title('Puter Waker 0.4')

describe_lab = tk.Label(main, text="Enter the MAC address of the computer you want to wake").grid(row=0, columnspan=2)
mac_text = tk.StringVar()
# mac_text.set(" ")
mac_entry = tk.Label(main, text="Mac Address:").grid(row=1, column=0)
mac_input = tk.Entry(main, textvariable=mac_text).grid(row=1, column=1)
#or_label = tk.Label(main, text="or").grid(row=2, columnspan=2)
#ip_text = tk.StringVar()
#ip_text.set("Not working just yet")
#ip_entry = tk.Label(main, text="IP Address", textvariable= ip_text).grid(row=3, column=0)
#ip_input = tk.Entry(main).grid(row=3, column=1)
enter_button = tk.Button(main, text="Wake!", command=wake).grid(row=4, columnspan=2)
arp_button = tk.Button(main, text="Display current ARP table", command=arp).grid(row=5, columnspan=2)

tk.mainloop()
