package at.ltd.tools.fw.peer2peerFirewall.backend.util;

import java.time.LocalDateTime;

import org.springframework.stereotype.Component;

import com.github.ffalcinelli.jdivert.Packet;

import at.ltd.tools.fw.peer2peerFirewall.backend.entities.CodrEndpoint;

@Component
public class CodrEndpointFactory {

	public CodrEndpoint createCodrEndpoint(Packet packet) {
		CodrEndpoint tmp = new CodrEndpoint();

		tmp.setDstAdress(packet.getDstAddr());
		tmp.setDstPort(packet.getDstPort());
		tmp.setSrcAdress(packet.getSrcAddr());
		tmp.setSrcPort(packet.getSrcPort());
		tmp.setTimeLastChanged(LocalDateTime.now());

		return tmp;
	}

}
