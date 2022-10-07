"""This is my take on a Windows based WOL (Wake On Lan) program
Press the "Display current ARP table" button to see a list of mac address your computers Arp table
from that window you can send a WOL packet to any of the listed devices
"""
from wakeonlan import send_magic_packet
from tkinter import messagebox
import tkinter as tk
import os
import re

global path
# arp function creates a new window showing all known MAC address on client computer


def manual_save(x, y):
    # print("Y is " + y)
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", x.lower()):
        if y == '':
            save(x)
        else:
            save(x + "          " + y)
    else:
        messagebox.showerror(title="MAC Error", message="Incorrect MAC address entered " + x)

    try:
        savedWindow.destroy()
    except:
        pass


def arp():
    global arp_window
    var = []
    arpLabels = []
    arpButton = []
    saveButton = []
    macs = []
    IPs = []
# os.popen allows you to work the windows command line, "as a" lets us take the return and store it by line in a list
    with os.popen("arp -a") as a:
        arpData = a.readlines()

    # use tkinter to make the gui main window
    arp_window = tk.Tk(screenName="Current Arp Table")
    arp_window.title("Current Arp Table")

    """loop threw the arp -a return leave out the first blank line, then go threw each line and extract the MAC from the 
    line + store it in a new list. if no MAC on the line new list gets ' '"""
    for i, a in enumerate(arpData):
        if i > 0:
            try:
                if a[2].isnumeric():
                    try:
                        ip_end = a.find(" ", 3)
                        IPs.append(a[2:ip_end:1])
                    except:
                        pass
                    try:
                        start = a.find("-") - 2
                        macs.append(a[start:start + 17:1])
                    except TypeError:
                        macs.append(' ')
            except ValueError:
                macs.append(' ')
                IPs.append(' ')
            except IndexError:
                macs.append(' ')
                IPs.append(' ')

    # for each MAC address make a label and button to wake device
    for i, data in enumerate(macs):
        if data[0] != " ":
            if i < 17:
                arpLabels.append(tk.Label(arp_window, text=IPs[i] + ":... " + data).grid(row=i, column=0))
# These button functions needed 2 lambdas or else it would always call there function with the lst MAC in the list
                arpButton.append(tk.Button(arp_window, text="Wake! ",
                                           command=(lambda num = i: lambda: wake(macs[num]))()
                                           ).grid(row=i, column=1))
                saveButton.append(tk.Button(arp_window, text="Save ",
                                           command=(lambda num=i: lambda: save(macs[num]))()
                                           ).grid(row=i, column=2))

            elif i > 16:
                arpLabels.append(tk.Label(arp_window, text=IPs[i] + ":... " + data).grid(row=i - 17, column=3))
                arpButton.append(tk.Button(arp_window, text="Wake!",
                                           command=(lambda num = i: lambda: wake(macs[num]))()
                                           ).grid(row=i - 17, column=4))
                saveButton.append(tk.Button(arp_window, text="Save ",
                                            command=(lambda num=i: lambda: save(macs[num]))()
                                            ).grid(row=i, column=5))
        else:
            arpLabels.append(tk.Label(arp_window, text=data).grid(row=i, column=0))


def wake(x):
    global savedWindow
    global arp_window

    try:
        send_magic_packet(x[0:17])
        if len(x) > 17:
            messagebox.showinfo(title="Wake sent", message="WOL sent to " + x[27:len(x)])
        else:
            messagebox.showinfo(title="Wake sent", message="WOL sent to " + x[0:17])
    except ValueError:
        messagebox.showerror(title="MAC Error", message=f"Incorrect MAC address entered (sending) {x}")

    try:
        arp_window.destroy()
    except:
        pass

    try:
        savedWindow.destroy()
    except:
        pass


def save(x):
    global path
    global arp_window
    if not os.path.exists(path + "\\Documents\\Puter Waker\\Saved.txt"):
        with open(path + "\\Documents\\Puter Waker\\Saved.txt", "w") as file:
            saveTemp = []
            file.write(x + "\n")
    else:
        with open(path + "\\Documents\\Puter Waker\\Saved.txt", "+r") as file:
            saveTemp = file.readlines()
            file.write(x + "\n")
    tk.messagebox.showinfo(title="Saved", message=x + " Was saved")
    try:
        arp_window.destroy()
    except:
        pass
    try:
        savedWindow.destroy()
    except:
        pass


def savedmacs():
    global path
    global savedWindow
    savedLabel = []
    wakeButton = []
    if not os.path.exists(path + "\\Documents\\Puter Waker\\Saved.txt"):
        with open(path + "\\Documents\\Puter Waker\\Saved.txt", "w") as file:
            temp = []
    else:
        with open(path + "\\Documents\\Puter Waker\\Saved.txt", "r") as file:
            temp = file.readlines()
    savedWindow = tk.Tk(screenName="Saved Devices")
    clearSaved = tk.Button(savedWindow, text="Clear saved list", command=deleteSaved).grid(row=0, column=1)
    manualEnterLabel = tk.Label(savedWindow, text="Enter MAC to be saved").grid(row=1, column=0)
    manualEntryField = tk.Entry(savedWindow)
    manualEntryField.grid(row=1, column=1)
    manualNameField = tk.Label(savedWindow, text="Enter name (Optional)").grid(row=1, column=2)
    manualNameEntry = tk.Entry(savedWindow)
    manualNameEntry.grid(row=1, column=3)
    manualEntryButton = tk.Button(savedWindow,
                                  text="Save",
                                  command=lambda: manual_save(manualEntryField.get(),
                                                              manualNameEntry.get()
                                                              )
                                  ).grid(row=1, column=4)

    for i, x in enumerate(temp):
        if x.find("\n") != -1:
            # print(x)
            savedLabel.append(tk.Label(savedWindow, text=x).grid(row=i + 2, column=0))
            wakeButton.append(tk.Button(savedWindow, text="Wake! ",
                                           command=(lambda num=i, mac=x: lambda: wake(x))()
                                        ).grid(row=i + 2, column=1))


def deleteSaved():
    global path
    global savedWindow
    file = open(path + "\\Documents\\Puter Waker\\Saved.txt", "w")
    file.close()
    tk.messagebox.showinfo(title="deleted", message="Saved messages have been deleted")
    savedWindow.destroy()


# noinspection PyRedeclaration
path = os.path.expanduser("~")
if not os.path.exists(path + "\\Documents\\Puter Waker"):
    os.makedirs(path + "\\Documents\\Puter Waker")

main = tk.Tk(screenName="Puter Waker", baseName="Waker", className="Waker")
main.title('Puter Waker 2.8')

describe_lab = tk.Label(main, text="Enter the MAC address of the computer you want to wake").grid(row=0, columnspan=2)
mac_text = tk.StringVar()
mac_entry = tk.Label(main, text="Mac Address:").grid(row=1, column=0)
mac_input = tk.Entry(main, textvariable=mac_text).grid(row=1, column=1)
enter_button = tk.Button(main, text="Wake!", command=lambda: wake(mac_text.get())).grid(row=4, columnspan=2)
arp_button = tk.Button(main, text="Display current ARP table", command=arp).grid(row=5, column=0)
saved_button = tk.Button(main, text="Display saved devices", command=savedmacs).grid(row=5, column=1)

tk.mainloop()
