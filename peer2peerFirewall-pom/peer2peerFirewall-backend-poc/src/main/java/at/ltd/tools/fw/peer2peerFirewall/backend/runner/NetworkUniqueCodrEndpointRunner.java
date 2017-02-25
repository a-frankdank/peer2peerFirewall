package at.ltd.tools.fw.peer2peerFirewall.backend.runner;

import java.util.LinkedHashSet;
import java.util.Set;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.github.ffalcinelli.jdivert.Packet;
import com.github.ffalcinelli.jdivert.exceptions.WinDivertException;

import at.ltd.tools.fw.peer2peerFirewall.backend.entities.CodrEndpoint;
import at.ltd.tools.fw.peer2peerFirewall.backend.util.CodrEndpointFactory;

public class NetworkUniqueCodrEndpointRunner extends AbstractNetworkRunner {
	private static final Log logger = LogFactory
	        .getLog(NetworkUniqueCodrEndpointRunner.class);

	private Packet packet;

	private CodrEndpointFactory factory;

	private Set<CodrEndpoint> uniqueEntities;

	public NetworkUniqueCodrEndpointRunner(CodrEndpointFactory factory) {
		this.factory = factory;
	}

	@Override
	public void init() {
		uniqueEntities = new LinkedHashSet<>();
	}

	public void doRun() throws WinDivertException {
		packet = getWd().recv();
		uniqueEntities.add(factory.createCodrEndpoint(packet));

		getWd().send(packet);
	}

	public Set<CodrEndpoint> getUniqueEntities() {
		return uniqueEntities;
	}

}
