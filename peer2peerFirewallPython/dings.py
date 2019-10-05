# -*- coding: UTF-8 -*-

import pydivert
from pydivert import Packet

import datetime
import subprocess

from typing import Dict

import atexit
# import sys

import psutil


class ProcessConnections:
    """the process and its connections as extracted from psutils"""
    def __init__(self, process: str = "", local_address: str = "", remote_address: str = ""):
        self.process = process
        self.local_address = local_address
        self.remote_address = remote_address

    @staticmethod
    def read_process_connections():
        inner_process_connections = {}
        for pid in psutil.pids():
            process = psutil.Process(pid)
            process_string = str(process.pid)
            if process.name():
                process_string = process.name()
            for connection in process.connections():
                left_address = NetworkPacket.concat_address(str(connection.laddr.ip), str(connection.laddr.port))
                right_address = ""
                if connection.raddr:
                    right_address = NetworkPacket.concat_address(str(connection.raddr.ip), str(connection.raddr.port))
                inner_process_connections[left_address] = ProcessConnections(process_string, left_address, right_address)
        # print("paused till you type")
        # input()

        return inner_process_connections


class NetworkPacket:
    """the network packet received or sent cross referenced with open sockets"""
    def __init__(self, timestamp: datetime, packet_input: Packet = None):
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

    @staticmethod
    def concat_address(adr, port):
        tmp_port = str(port or "")
        if tmp_port == "":
            return adr
        else:
            return adr + ":" + tmp_port


def unregister(to_close):
    try:
        to_close.close()
    except RuntimeError as e:
        if str(e) != "WinDivert handle is not open.":
            raise e
    # sys.exit(0)


print("start")

first_time = True
number = 0
process_connections = {}
try:
    # would send other packets too: we don't care for those
    with pydivert.WinDivert("tcp or udp") as w:
        for packet in w:
            if first_time:
                atexit.register(unregister, w)
                first_time = False
            if number < 1:
                print("loaded")
                process_connections = ProcessConnections.read_process_connections()
                number = 25
            number -= 1
            # print(packet)
            # TODO do we really want to print individual packets?
            #      or rather a port overview with a packet received count...
            networkPacket = NetworkPacket(datetime.datetime.now(), packet)
            process_connection = process_connections.get(
                networkPacket.local_address, ProcessConnections("no process found", "", "")
            )
            print(
                "packet: {:15s}  {:3s}/{:3s}  {:22s}  {:22s} {:30s}".format(
                    networkPacket.timestamp, networkPacket.type, networkPacket.direction, networkPacket.local_address,
                    networkPacket.remote_address, process_connection.process+"/"+process_connection.remote_address)
            )
            w.send(packet)
except KeyboardInterrupt:
    print("shutting down")
