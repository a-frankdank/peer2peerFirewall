# -*- coding: UTF-8 -*-

from typing import Dict

import tkinter as tk
import tkinter.ttk as ttk

import peer2peerFirewall as p2pFw


class P2pGui:
    """renders the gui for the peer2peer firewall"""

    root: tk.Tk
    tree_view: ttk.Treeview

    on_or_off_button: ttk.Button

    combo_box: ttk.Combobox
    combo_box_commands: Dict[str, str]

    # p2pFwId: str
    keep_gui_looping = True
    start_up_p2pFw = False

    def on_or_off(self):
        if self.on_or_off_button["text"] == "on ":
            self.on_or_off_button["text"] = "off"
            self.on_or_off_button.configure(style="pR.TButton")
            self.combo_box.configure(state="readonly")
            # self.root.after_cancel(self.p2pFwId)
            p2pFw.stop()
            self.start_up_p2pFw = False
            for child in self.tree_view.get_children():
                self.tree_view.delete(child)
        else:
            self.on_or_off_button["text"] = "on "
            self.on_or_off_button.configure(style="pG.TButton")
            self.combo_box.configure(state="disabled")
            # self.p2pFwId = self.root.after(
            #     0, p2pFw.main_loop, self.combo_box_commands[self.combo_box.get()], False
            # )
            self.start_up_p2pFw = True

    def update_tree_view(self):
        # TODO deleting and updating is way too slow!
        for child in self.tree_view.get_children():
            self.tree_view.delete(child)
        network_lines = p2pFw.read_network_lines()
        i = 0
        for line in network_lines.values():
            if i % 5 == 0:
                self.root.update()
            self.tree_view.insert(
                "", i, line.packet.discriminator,
                text=line.packet.timestamp_text,
                values=(
                    line.packet.type + "/" + line.packet.direction,
                    line.packet.local_address,
                    line.packet.remote_address,
                    line.process.process,
                    line.count
                )
             )
            i += 1
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

    def exit_gui(self):
        p2pFw.stop()
        self.start_up_p2pFw = False
        self.keep_gui_looping = False
        self.root.destroy()

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(True, True)
        self.root.minsize(width=780, height=200)
        self.root.protocol('WM_DELETE_WINDOW', self.exit_gui)
        style = ttk.Style(self.root)
        style.theme_use('alt')
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
            "protocol/direction",
            "local address port",
            "remote address port",
            "process",
            "packet count"
        )
        self.tree_view.column("#0", stretch=True, width=145, minwidth=145, anchor="w")
        self.tree_view.column("protocol/direction", stretch=True, width=70, minwidth=60, anchor="w")
        self.tree_view.column("local address port", stretch=True, width=170, minwidth=160, anchor="w")
        self.tree_view.column("remote address port", stretch=True, width=170, minwidth=160, anchor="w")
        self.tree_view.column("process", stretch=True, width=100, minwidth=100, anchor="w")
        self.tree_view.column("packet count", stretch=True, width=100, minwidth=100, anchor="w")

        self.tree_view.heading("#0", text="Timestamp", anchor="w")
        self.tree_view.heading("protocol/direction", text="Protocol/Direction", anchor="w")
        self.tree_view.heading("local address port", text="Local Address:Port", anchor="w")
        self.tree_view.heading("remote address port", text="Remote Address Port", anchor="w")
        self.tree_view.heading("process", text="Process", anchor="w")
        self.tree_view.heading("packet count", text="Packet Count", anchor="w")

        self.on_or_off_button.pack(expand=False, side="left", anchor="nw")
        label.pack(expand=False, side="left", anchor="nw")
        self.combo_box.pack(expand=False, side="left", anchor="nw")
        separator.pack(expand=False, side="left", anchor="nw")
        frame.pack(expand=False, side="top", fill='both')

        scrollbar_horizontal.pack(expand=False, side='bottom', fill='x', anchor="s")
        self.tree_view.pack(expand=True, side="left", fill='both', anchor="w")
        scrollbar_vertical.pack(expand=False, side='right', fill='y', anchor="e")
        frame2.pack(expand=True, side="top", fill='both')

        while self.keep_gui_looping:
            if self.start_up_p2pFw:
                p2pFw.main_loop(
                    self.combo_box_commands[self.combo_box.get()],
                    False,
                    self.root.update,
                    self.update_tree_view
                )
            else:
                self.root.update()


P2pGui()
