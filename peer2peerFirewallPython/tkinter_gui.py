# -*- coding: UTF-8 -*-
import threading
from typing import Dict

import tkinter as tk
import tkinter.ttk as ttk

import peer2peerFirewall as p2pFw


class P2pGui(threading.Thread):
    """renders the gui for the peer2peer firewall"""

    root: tk.Tk
    tree_view: ttk.Treeview

    on_or_off_button: ttk.Button

    combo_box: ttk.Combobox
    combo_box_commands: Dict[str, str]

    keep_gui_looping = True
    start_up_p2pFw = False

    network_lines: Dict[str, p2pFw.NetworkLine]

    def on_or_off(self):
        if self.on_or_off_button["text"] == "on ":
            self.on_or_off_button["text"] = "off"
            self.on_or_off_button.configure(style="pR.TButton")
            self.combo_box.configure(state="readonly")
            p2pFw.stop()
            self.start_up_p2pFw = False
            for child in self.tree_view.get_children():
                self.tree_view.delete(child)
        else:
            self.on_or_off_button["text"] = "on "
            self.on_or_off_button.configure(style="pG.TButton")
            self.combo_box.configure(state="disabled")
            self.tree_view.insert(
                "", 0, "startUp",
                text=" ", values=("", "", "", "starting up...", "", "", "")
            )
            self.network_lines["startUp"] = p2pFw.NetworkLine({})
            self.start_up_p2pFw = True

# TODO grouping by 'process' instead of displaying all individual packets
#      1 process, n network lines

# TODO processes: new tab in gui for this
#      individual processes are expandable / closable
#      processes: alphabetically ordered. within, the order is: local_address, then protocol / direction

# TODO buttons: expand all / close all 'process groups'

# TODO and then blocking specific sockets - with display of the black list: on/off clears it
#      blacklist entry also gets deleted when it's not seen anymore (too old)
#      extra columns: checkbox block port (both directions), block just this packet type (ie only out), ...

# TODO lag spike function: add delay to certain packets...
#      with settable delay in ms in extra column

# TODO and adding a 'first seen' counter, to mimic those 1-4 numbers when hosting in warframe
#      maybe make it nameable?

    def update_tree_view(self):
        new_network_lines = p2pFw.read_network_lines()
        # delete those not present anymore
        if self.network_lines.keys() and new_network_lines.keys():
            deleted_stuff = list({
                key for key in self.network_lines.keys()
                if key not in new_network_lines
            })
            for to_delete in deleted_stuff:
                self.tree_view.delete(to_delete)

        # edit those present
        present_stuff = {
            key: value for key, value in new_network_lines.items()
            if key in self.network_lines
        }
        for key, line in present_stuff.items():
            # what can change: ts, process, count
            self.tree_view.set(key, column=self.tree_view["columns"][0], value=line.packet.timestamp_text)
            self.tree_view.set(key, column=self.tree_view["columns"][5], value=line.process.process)
            self.tree_view.set(key, column=self.tree_view["columns"][6], value=line.count)

        # add those new
        new_stuff = {
            key: value for key, value in new_network_lines.items()
            if key not in self.network_lines
        }
        for key, line in new_stuff.items():
            self.tree_view.insert(
                "", "end", key,
                text="",
                values=(
                    line.packet.timestamp_text,
                    line.timestamp_first_occurrence_text,
                    f"{line.packet.type}/{line.packet.direction}",
                    line.packet.local_address,
                    line.packet.remote_address,
                    line.process.process,
                    line.count
                )
            )

        # sort everything by first occurrence ts
        for key in sorted(
                    new_network_lines.keys(),
                    key=lambda discriminator: new_network_lines[discriminator].timestamp_first_occurrence
                 ):
            self.tree_view.move(key, "", "end")

        if new_network_lines.keys():
            self.network_lines = new_network_lines
        # for i in range(0, 100):
        #     self.tree_view.insert(
        #             "", i, str(i),
        #             text="08:13:00.654388 " + str(i),
        #             values=(
        #                     "TCP/IN", "192.168.0.153:49484",
        #                     "205.185.216.10:80", "Dings.exe",
        #                     "" + str(i)
        #                     )
        #         )
        self.root.after(5000, self.update_tree_view)

    def exit_gui(self):
        p2pFw.stop()
        self.start_up_p2pFw = False
        self.keep_gui_looping = False
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.resizable(True, True)
        self.root.minsize(width=915, height=200)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_gui)
        style = ttk.Style(self.root)
        style.theme_use("alt")
        style.configure("pR.TButton", foreground="white", background="red2")
        style.map("pR.TButton", background=[("active", "red4"),
                                            ("pressed", "red4"),
                                            ("disabled", "dim gray"),
                                            ("readonly", "dim gray")
                                            ])
        style.configure("pG.TButton", foreground="white", background="green4")
        style.map("pG.TButton", background=[("active", "dark green"),
                                            ("pressed", "dark green"),
                                            ("disabled", "dim gray"),
                                            ("readonly", "dim gray")
                                            ])

        frame = ttk.Frame(self.root)

        self.on_or_off_button = ttk.Button(frame, text="off", command=self.on_or_off, style="pR.TButton")
        label = ttk.Label(frame, text=" filtered for Protocol(s):")
        self.combo_box_commands = {
            "TCP only": "tcp", "UDP only": "udp", "TCP and UDP": "tcp or udp"
        }
        self.combo_box = ttk.Combobox(frame, state="readonly", values=list(self.combo_box_commands.keys()))
        self.combo_box.current(2)
        separator = ttk.Separator(frame)

        frame2 = ttk.Frame(self.root)

        self.tree_view = ttk.Treeview(frame2)
        scrollbar_horizontal = ttk.Scrollbar(frame2, orient="horizontal", command=self.tree_view.xview)
        scrollbar_vertical = ttk.Scrollbar(frame2, orient="vertical", command=self.tree_view.yview)
        self.tree_view.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

        # shows eg
        # 08:13:00.654388  TCP/IN   192.168.0.153:49484     205.185.216.10:80      Warframe.x64.exe
        self.tree_view["columns"] = (
            "timestamp",
            "first timestamp",
            "protocol/direction",
            "local address port",
            "remote address port",
            "process",
            "packet count"
        )
        self.tree_view.column("#0", stretch=False, width=1, minwidth=1, anchor="w")
        self.tree_view.column("timestamp", stretch=True, width=135, minwidth=135, anchor="w")
        self.tree_view.column("first timestamp", stretch=True, width=135, minwidth=135, anchor="w")
        self.tree_view.column("protocol/direction", stretch=True, width=65, minwidth=65, anchor="w")
        self.tree_view.column("local address port", stretch=True, width=170, minwidth=160, anchor="w")
        self.tree_view.column("remote address port", stretch=True, width=170, minwidth=160, anchor="w")
        self.tree_view.column("process", stretch=True, width=100, minwidth=100, anchor="w")
        self.tree_view.column("packet count", stretch=True, width=100, minwidth=100, anchor="w")

        self.tree_view.heading("#0", text="", anchor="w")
        self.tree_view.heading("timestamp", text="Timestamp", anchor="w")
        self.tree_view.heading("first timestamp", text="First seen", anchor="w")
        self.tree_view.heading("protocol/direction", text="Protocol/Direction", anchor="w")
        self.tree_view.heading("local address port", text="Local Address:Port", anchor="w")
        self.tree_view.heading("remote address port", text="Remote Address Port", anchor="w")
        self.tree_view.heading("process", text="Process", anchor="w")
        self.tree_view.heading("packet count", text="Packet Count", anchor="w")

        self.on_or_off_button.pack(expand=False, side="left", anchor="nw")
        label.pack(expand=False, side="left", anchor="nw")
        self.combo_box.pack(expand=False, side="left", anchor="nw")
        separator.pack(expand=False, side="left", anchor="nw")
        frame.pack(expand=False, side="top", fill="both")

        scrollbar_horizontal.pack(expand=False, side="bottom", fill="x", anchor="s")
        self.tree_view.pack(expand=True, side="left", fill="both", anchor="w")
        scrollbar_vertical.pack(expand=False, side="right", fill="y", anchor="e")
        frame2.pack(expand=True, side="top", fill="both")

        self.network_lines = {}
        self.root.after_idle(self.update_tree_view)
        self.root.mainloop()

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()


p2pGui = P2pGui()
while p2pGui.keep_gui_looping:
    if p2pGui.start_up_p2pFw:
        p2pFw.main_loop(
            p2pGui.combo_box_commands[p2pGui.combo_box.get()],
            False
        )
