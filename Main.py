# This is my take on a Windows based WOL (Wake On Lan) program
# Press the "Display current ARP table" button to see a list of mac address your computers Arp table
# from that window you can send a WOL packet to any of the listed devices

from wakeonlan import send_magic_packet
from tkinter import messagebox
import tkinter as tk
import os

global path
# arp function creates a new window showing all known MAC address on client computer
def arp():
    var = []
    ArpLabels = []
    ArpButton = []
    SaveButton = []
    macs = []
    IPs = []
    # os.popen allows you to work the windows command line, "as a" lets us take the return and store it by line in a list
    with os.popen("arp -a") as a:
        arpData = a.readlines()

    # use tkinter to make the gui main window
    arp_window = tk.Tk(screenName="Current Arp Table")
    arp_window.title("Current Arp Table")

    # loop threw the arp -a return leave out the first blank line, then put the rest in another list (needs work here)
    for i, a in enumerate(arpData):
        if i > 0:
            var.append(a)
    # go threw each line and extract the MAC from the line and store it in a new list. if no MAC on the line new list gets ' '
    for i, data in enumerate(var):
        try:
            if data[2].isnumeric():
                try:
                    ip_end = data.find(" ", 3)
                    IPs.append(data[2:ip_end:1])
                    print(IPs[i])
                except:
                    # This variable means nothing, i just needed something to put under except
                    yesll = 23
                try:
                    start = data.find("-") - 2
                    macs.append(data[start:start + 17:1])
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
                ArpLabels.append(tk.Label(arp_window, text=IPs[i] + ":... " + data).grid(row=i, column=0))
                # These button functions needed 2 lambdas or else it would always call there function with the lst MAC in the list
                ArpButton.append(tk.Button(arp_window, text="Wake! ",
                                           command=(lambda num = i: lambda: wake(macs[num]))()
                                           ).grid(row=i, column=1))
                SaveButton.append(tk.Button(arp_window, text="Save ",
                                           command=(lambda num=i: lambda: save(macs[num]))()
                                           ).grid(row=i, column=2))

            elif i > 16:
                ArpLabels.append(tk.Label(arp_window, text=IPs[i] + ":... " + data).grid(row=i - 17, column=3))
                ArpButton.append(tk.Button(arp_window, text="Wake!",
                                           command=(lambda num = i: lambda: wake(macs[num]))()
                                           ).grid(row=i - 17, column=4))
                SaveButton.append(tk.Button(arp_window, text="Save ",
                                            command=(lambda num=i: lambda: save(macs[num]))()
                                            ).grid(row=i, column=5))
        else:
            ArpLabels.append(tk.Label(arp_window, text=data).grid(row=i, column=0))


def wake(x):
    try:
        send_magic_packet(x)
        messagebox.showinfo(title="Wake sent", message="WOL sent to " + x)
    except ValueError:
        messagebox.showerror(title="MAC Error", message="Incorrect MAC address entered " + x)
    except:
        print('something went wrong')

def save(x):
    global path
    if os.path.exists(path + "\Documents\Puter Waker\Saved.txt") == False:
        file = open(path + "\Documents\Puter Waker\Saved.txt", "w")
        saveTemp = []
    else:
        file = open(path + "\Documents\Puter Waker\Saved.txt", "+r")
        saveTemp = file.readlines()
    file.write(x + "\n")
    tk.messagebox.showinfo(title="Saved", message=x + " Was saved")
    file.close()

def savedMacs():
    global path
    savedLabel = []
    wakeButton = []
    if os.path.exists(path + "\Documents\Puter Waker\Saved.txt") == False:
        file = open(path + "\Documents\Puter Waker\Saved.txt", "w")
        temp = []
    else:
        file = open(path + "\Documents\Puter Waker\Saved.txt", "r")
        temp = file.readlines()
    file.close()
    savedWindow = tk.Tk(screenName="Saved Devices")
    clearSaved = tk.Button(savedWindow, text="Clear saved list", command=deleteSaved).grid(row=0, column=0)

    for i, x in enumerate(temp):
        if x.find("\n") != -1:
            savedLabel.append(tk.Label(savedWindow, text=x).grid(row=i + 1, column=0))
            wakeButton.append(tk.Button(savedWindow, text="Wake! ",
                                           command=(lambda num = i: lambda: wake(x))()
                                           ).grid(row=i + 1, column=1))


def deleteSaved():
    global path
    file = open(path + "\Documents\Puter Waker\Saved.txt", "w")
    file.close()
    tk.messagebox.showinfo(title="deleted", message="Saved messages have been deleted")

path = os.path.expanduser("~")
if os.path.exists(path + "\Documents\Puter Waker") == False:
    os.makedirs(path + "\Documents\Puter Waker")

main = tk.Tk(screenName="Puter Waker", baseName="Waker", className="Waker")
main.title('Puter Waker 1.5')

# print(os.path.expanduser("~"))

describe_lab = tk.Label(main, text="Enter the MAC address of the computer you want to wake").grid(row=0, columnspan=2)
mac_text = tk.StringVar()
mac_entry = tk.Label(main, text="Mac Address:").grid(row=1, column=0)
mac_input = tk.Entry(main, textvariable=mac_text).grid(row=1, column=1)
enter_button = tk.Button(main, text="Wake!", command=lambda: wake(mac_text.get())).grid(row=4, columnspan=2)
arp_button = tk.Button(main, text="Display current ARP table", command=arp).grid(row=5, column=0)
saved_button = tk.Button(main, text="Display saved devices", command=savedMacs).grid(row=5, column=1)

tk.mainloop()
