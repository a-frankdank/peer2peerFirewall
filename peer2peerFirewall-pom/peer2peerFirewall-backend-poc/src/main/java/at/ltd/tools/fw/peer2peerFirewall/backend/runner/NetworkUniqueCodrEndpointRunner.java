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

	private Object lock = new Object();

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
		try {
			packet = getWd().recv();
			synchronized (lock) {
				CodrEndpoint codr = factory.createCodrEndpoint(packet);
				if (!uniqueEntities.add(codr)) {
					uniqueEntities.parallelStream().forEach(x -> {
						if (x.equals(codr)) {
							x.setTimeLastChanged(codr.getTimeLastChanged());
						}
					});
				}
			}

			getWd().send(packet);
		} catch (Exception e) {
			getWd().close();
			throw e;
		}
	}

	public Set<CodrEndpoint> getUniqueEntities() {
		synchronized (lock) {
			return uniqueEntities;
		}
	}

}
