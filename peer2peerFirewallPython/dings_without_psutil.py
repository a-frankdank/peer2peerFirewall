# -*- coding: UTF-8 -*-

import pydivert
from pydivert import Packet

import datetime
import subprocess

from typing import Dict

import atexit
# import sys


class Task:
    """a transformed task list line"""
    def __init__(self, description: str="", pid: str="", service_name: str=""):
        self.description = description[1:-1]
        if service_name != "\"Nicht zutreffend\"" and service_name != "":
            self.description = description[1:-1] + "/" + service_name[1:-1]
        self.pid = pid[1:-1]

    @staticmethod
    def init_tasks():
        # receive csv of pid and their names, and services (if they have some)
        try:
            tasks_output = subprocess.check_output(['tasklist', '/svc', '/nh', '/fo', 'csv'])
        except Exception:
            raise ValueError("couldn't launch tasklist. exiting")

        # print("output: "+output.decode("windows-1252"))
        # eg
        # "System Idle Process","0","Nicht zutreffend"
        # "System","4","Nicht zutreffend"
        tasks_lines = tasks_output.decode("windows-1252").split("\r\n")
        tasks = {}
        # packing task list result into tasks dictionary
        for task_line in tasks_lines:
            task_columns = task_line.split(",")
            if len(task_columns) == 3:
                task = Task(task_columns[0], task_columns[1], task_columns[2])
                # print("task: "+task.pid + " "+task.description)
                tasks[task.pid] = task

        # print("paused till you type")
        # input()

        return tasks


class Socket:
    """the transformed netstat output enriched by Task information"""
    def __init__(self, protocol: str="", local_address: str="", remote_address: str="", pid: str="",
                 tasks: Dict[str, Task]=None):
        self.protocol = protocol
        self.local_address = local_address
        self.remote_address = remote_address
        self.process_information = tasks.get(pid, Task("\"only pid:"+pid+"\"", "\""+pid+"\"")).description

    @staticmethod
    def init_sockets(tasks: Dict[str, Task]=None):
        # show all open ports and their corresponding pids
        try:
            socket_output = subprocess.check_output(['netstat', '-nao'])
        except Exception:
            raise ValueError("couldn't launch netstat. exiting")
        # print("socket_output: "+socket_output.decode("windows-1252"))

        socket_lines = socket_output.decode("windows-1252").split("\r\n")
        sockets = {}
        # the first three to four socket_lines contain rubbish...
        for socket_line in socket_lines:
            # print(socket_line)
            socket_columns = socket_line.split()
            if len(socket_columns) == 5:
                # socket_output from fourth socket_line on:
                #   Proto  Lokale Adresse         Remoteadresse          Status           PID
                #   TCP    127.0.0.1:49695        127.0.0.1:49696        HERGESTELLT     8796
                # print(socket_columns[0]+";"+socket_columns[1]+";"+socket_columns[2]+";"+socket_columns[4])
                # results in:
                # TCP;127.0.0.1:49695;127.0.0.1:49696;8796
                socket = Socket(socket_columns[0], socket_columns[1], socket_columns[2], socket_columns[4], tasks)
                sockets[socket.local_address] = socket
                # print("socket: "+socket.protocol+" "+socket.local_address+" "
                #      + socket.remote_address+" "+socket.process_information)

        # print("paused till you type")
        # input()

        return sockets


class NetworkPacket:
    """the network packet received or sent cross referenced with open sockets"""
    def __init__(self, timestamp: datetime, packet_input: Packet=None, sockets: Dict[str, Socket]=None):
        self.direction = "OUT" if packet_input.is_outbound else "IN"
        self.type = "TCP" if packet_input.tcp else ("UDP" if packet_input.udp else "UNKNOWN")
        src_address = NetworkPacket.concat_address(packet_input.src_addr, packet_input.src_port)
        dst_address = NetworkPacket.concat_address(packet_input.dst_addr, packet_input.dst_port)
        # 'we' aka my ip is always the local address, as being always left in comodo
        if packet_input.is_outbound:
            self.local_address = src_address
            self.remote_address = dst_address
        else:
            self.local_address = dst_address
            self.remote_address = src_address
        self.timestamp = timestamp.strftime("%H:%M:%S.%f")
        self.socket = sockets.get(self.local_address, Socket("", self.local_address, "", "no pid", {}))

    @staticmethod
    def concat_address(addr, port):
        tmp_port = str(port or "")
        if tmp_port == "":
            return addr
        else:
            return addr + ":" + tmp_port


def unregister(to_close):
    try:
        to_close.close()
    except RuntimeError as e:
        if str(e) != "WinDivert handle is not open.":
            raise e
    # sys.exit(0)


print("wiggerlover")

the_tasks = Task.init_tasks()
the_sockets = Socket.init_sockets(the_tasks)
number = 0

try:
    # would send other packets too: we don't care for those
    with pydivert.WinDivert("tcp or udp") as w:
        for packet in w:
            if number == 0:
                atexit.register(unregister, w)
            number += 1
            if number > 10000:
                the_tasks = Task.init_tasks()
                the_sockets = Socket.init_sockets(the_tasks)
            # print(packet)
            networkPacket = NetworkPacket(datetime.datetime.now(), packet, the_sockets)
            print(
                "packet: {:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s}".format(
                    networkPacket.timestamp, networkPacket.type, networkPacket.direction, networkPacket.local_address,
                    networkPacket.remote_address, networkPacket.socket.process_information)
            )
            w.send(packet)
except KeyboardInterrupt:
    print("shutting down")
