package at.ltd.tools.fw.p2p.runner;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.github.ffalcinelli.jdivert.Packet;
import com.github.ffalcinelli.jdivert.exceptions.WinDivertException;

public class NetworkDroppingChosenIpRunner extends AbstractNetworkRunner {
	private static final Log logger = LogFactory
	        .getLog(NetworkDroppingChosenIpRunner.class);

	private Packet packet;

	public void doRun() throws WinDivertException {
		packet = getWd().recv();
		if (packet.getDstAddr().equals("46.196.199.74")
		        || packet.getSrcAddr().equals("46.196.199.74")) {
			logger.info("dropped a packet");
		} else {
			getWd().send(packet);
		}
	}

}
