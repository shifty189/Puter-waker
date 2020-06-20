# reference https://pypi.org/project/wakeonlan/

from wakeonlan import send_magic_packet
from tkinter import messagebox
import tkinter as tk
import os
# import re


def arp():
    var = [] = []
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
    # print(var[7])
    for i, data in enumerate(var):
        try:
            start = data.find("-") - 2
            macs.append(data[start:start + 17:1])
        except TypeError:
            macs.append(' ')
        if i > 0:
            if i < 17:
                ArpLabels.append(tk.Label(arp_window, text=data).grid(row=i, column=0))
                ArpButton.append(tk.Button(arp_window, text="Wake! " + str(i),
                                           command=lambda: wake(macs[i])
                                           ).grid(row=i, column=1))
                print(macs[i] + " Sent")
            else:
                ArpLabels.append(tk.Label(arp_window, text=data).grid(row=i - 17, column=3))
                ArpButton.append(tk.Button(arp_window, text="Wake!",
                                           command=lambda: wake(data[macs[int(i)]:macs[int(i)] + 17:1])
                                           ).grid(row=i - 17, column=4))
        else:
            ArpLabels.append(tk.Label(arp_window, text=data).grid(row=i, column=0))
    # test = var[5].find("-") - 2
    # print(var[5][test:test + 18:1])
        # if i < 2:
        #     break
        # else:
        #     print(i)
    #arp_display = tk.Label(arp_window, text=arpData)
    #arp_display.grid(row=0, column=0)
    #arpData[2] is the legend, 3 starts the clients
    # print(arpData[2])


def wake(x):
    print(x)
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
