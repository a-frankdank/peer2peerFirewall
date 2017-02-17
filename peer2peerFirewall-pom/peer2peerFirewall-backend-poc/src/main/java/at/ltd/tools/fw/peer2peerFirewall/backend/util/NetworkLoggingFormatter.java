package at.ltd.tools.fw.peer2peerFirewall.backend.util;

import org.apache.commons.lang3.StringUtils;

import com.github.ffalcinelli.jdivert.Packet;

public class NetworkLoggingFormatter {
	public static final int IPV4LENGHT_FORMAT = 15;
	public static final int IPV6LENGHT_FORMAT = 45;
	public static final int PORTLENGTH_FORMAT = 5;

	public static void stringFormatPacketForUniqueDisplay(StringBuilder strb,
	        Packet packet) {
		strb.append(" src:");
		formatIP(strb, packet.getSrcAddr(), packet.getSrcPort(),
		        packet.isIpv4());
		strb.append(" dst:");
		formatIP(strb, packet.getDstAddr(), packet.getDstPort(),
		        packet.isIpv4());

		strb.append(" isOutbound:");
		strb.append(packet.isOutbound());
	}

	public static void stringFormatPacketForLogging(StringBuilder strb,
	        Packet packet) {
		// input example
		// INFO NetworkLoggingRunner - Packet {IPv4 {version=4,
		// srcAddr=194.232.200.142, dstAddr=10.132.174.235, IHL=5, DSCP=0,
		// ECN=0, length=392, ID=395d RESERVED=false, DF=false, MF=false,
		// fragOff=2048 TTL=119 proto=TCP, cksum=842c}, TCP {srcPort=80,
		// dstPort=65201, seqNum=-552456643, ackNum=-28205093 dataOffset=5,
		// NS=0, CWR=0, ECE=0, URG=0, ACK=1, PSH=1, RST=0, SYN=0, FIN=0,
		// window=260, cksum=5402, urgPtr=0}, direction=OUTBOUND, iface=[0, 0],
		// raw=*800 bytes of rare data i guess*}

		strb.append(" isOutbound:");
		strb.append(packet.isOutbound());

		// strb.append(" isLoopback:");
		// strb.append(packet.isLoopback());

		strb.append(" isIpv4:");
		strb.append(packet.isIpv4());
		strb.append(" isIpv6:");
		strb.append(packet.isIpv6());
		// strb.append(" isIcmpv4:");
		// strb.append(packet.isIcmpv4());
		// strb.append(" isIcmpv6:");
		// strb.append(packet.isIcmpv6());

		strb.append(" isUdp:");
		strb.append(packet.isUdp());

		strb.append(" isTcp:");
		strb.append(packet.isTcp());

		strb.append(" src:");
		formatIP(strb, packet.getSrcAddr(), packet.getSrcPort(),
		        packet.isIpv4());
		strb.append(" dst:");
		formatIP(strb, packet.getDstAddr(), packet.getDstPort(),
		        packet.isIpv4());

		if (packet.isTcp()) {
			strb.append(" Tcp:");
			strb.append(packet.getTcp());
		}
		if (packet.isUdp()) {
			strb.append(" Udp:");
			strb.append(packet.getUdp());
		}
		if (packet.isIpv4()) {
			strb.append(" Ipv4:");
			strb.append(packet.getIpv4());
		}
		if (packet.isIpv6()) {
			strb.append(" Ipv6:");
			strb.append(packet.getIpv6());
		}
		// if (packet.isIcmpv4()) {
		// strb.append(" Icmpv4:");
		// strb.append(packet.getIcmpv4());
		// }
		// if (packet.isIcmpv6()) {
		// strb.append(" Icmpv6:");
		// strb.append(packet.getIcmpv6());
		// }

		// result for example
		// INFO NetworkLoggingRunner - isOutbound:true isIpv4:true isIpv6:false
		// isIcmpv4:false isIcmpv6:false isUdp:false isTcp:true
		// dst:194.232.200.142: 80
		// src: 10.132.174.235:65201 Tcp:TCP
		// {srcPort=65201, dstPort=80, seqNum=-28205093, ackNum=-477606643
		// dataOffset=5, NS=0, CWR=0, ECE=0, URG=0, ACK=1, PSH=0, RST=0, SYN=0,
		// FIN=0, window=454, cksum=9b62, urgPtr=0} Ipv4:IPv4 {version=4,
		// srcAddr=10.132.174.235, dstAddr=194.232.200.142, IHL=5, DSCP=0,
		// ECN=0, length=40, ID=23c8 RESERVED=false, DF=false, MF=false,
		// fragOff=2048 TTL=65408 proto=TCP, cksum=9221}
	}

	public static void formatIP(StringBuilder strb, String addr, Integer port,
	        boolean isIpv4) {
		strb.append(StringUtils.leftPad(addr,
		        isIpv4 ? IPV4LENGHT_FORMAT : IPV6LENGHT_FORMAT));
		strb.append("::");
		strb.append(StringUtils.leftPad(port.toString(), PORTLENGTH_FORMAT));
	}
}
