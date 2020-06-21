from wakeonlan import send_magic_packet
from tkinter import messagebox
import tkinter as tk
import os


def arp():
    var = []
    ArpLabels = []
    ArpButton = []
    macs = []
    with os.popen("arp -a") as a:
        arpData = a.readlines()

    arp_window = tk.Tk(screenName="Current Arp Table")
    arp_window.title("Current Arp Table")

    for i, a in enumerate(arpData):
        if i > 0:
            var.append(a)
    for i, data in enumerate(var):
        try:
            start = data.find("-") - 2
            macs.append(data[start:start + 17:1])
        except TypeError:
            macs.append(' ')
    for i, data in enumerate(macs):
        d = data
        if i > 0:
            if i < 17:
                ArpLabels.append(tk.Label(arp_window, text=data).grid(row=i, column=0))
                ArpButton.append(tk.Button(arp_window, text="Wake! " + str(i),
                                           command=(lambda num = i:lambda:wake(macs[num]))()
                                           ).grid(row=i, column=1))

            else:
                ArpLabels.append(tk.Label(arp_window, text=data).grid(row=i - 17, column=3))
                ArpButton.append(tk.Button(arp_window, text="Wake!",
                                           command=lambda: wake(data[macs[int(i)]:macs[int(i)] + 17:1])
                                           ).grid(row=i - 17, column=4))
        else:
            ArpLabels.append(tk.Label(arp_window, text=data).grid(row=i, column=0))


def wake(x):
    try:
        send_magic_packet(x)
        messagebox.showinfo(title="Wake sent", message="WOL sent to " + str(x))
    except ValueError:
        messagebox.showerror(title="MAC Error", message="Incorrect MAC address entered " + x)
    except:
        print('something went wrong')


main = tk.Tk(screenName="Puter Waker", baseName="Waker", className="Waker")
main.title('Puter Waker 1.1')

describe_lab = tk.Label(main, text="Enter the MAC address of the computer you want to wake").grid(row=0, columnspan=2)
mac_text = tk.StringVar()
mac_entry = tk.Label(main, text="Mac Address:").grid(row=1, column=0)
mac_input = tk.Entry(main, textvariable=mac_text).grid(row=1, column=1)
enter_button = tk.Button(main, text="Wake!", command=lambda: wake(mac_text.get())).grid(row=4, columnspan=2)
arp_button = tk.Button(main, text="Display current ARP table", command=arp).grid(row=5, columnspan=2)

tk.mainloop()
