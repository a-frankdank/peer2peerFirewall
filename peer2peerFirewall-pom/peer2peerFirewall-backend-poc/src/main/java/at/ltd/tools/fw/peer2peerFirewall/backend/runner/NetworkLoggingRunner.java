package at.ltd.tools.fw.peer2peerFirewall.backend.runner;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.github.ffalcinelli.jdivert.Packet;
import com.github.ffalcinelli.jdivert.exceptions.WinDivertException;

import at.ltd.tools.fw.peer2peerFirewall.backend.util.NetworkLoggingFormatter;

public class NetworkLoggingRunner extends AbstractNetworkRunner {
	private static final Log logger = LogFactory
	        .getLog(NetworkLoggingRunner.class);

	private Packet packet;

	public void doRun() throws WinDivertException {
		packet = getWd().recv();
		StringBuilder strb = new StringBuilder();
		NetworkLoggingFormatter.stringFormatPacketForLogging(strb, packet);

		logger.info(strb.toString());
		getWd().send(packet);

		// TODO get source of that shit java binding jdivert, and fix it for you

		// TODO what is this shit
		// Exception in thread "pool-1-thread-1"
		// java.lang.IllegalArgumentException: Protocol 2 is not recognized
		// at
		// com.github.ffalcinelli.jdivert.Enums$Protocol.fromValue(Enums.java:177)
		// at
		// com.github.ffalcinelli.jdivert.headers.Ipv4.getProtocol(Ipv4.java:80)
		// at
		// com.github.ffalcinelli.jdivert.headers.Ipv4.getNextHeaderProtocol(Ipv4.java:76)
		// at
		// com.github.ffalcinelli.jdivert.headers.Header.buildHeaders(Header.java:67)
		// at com.github.ffalcinelli.jdivert.Packet.<init>(Packet.java:80)
		// at com.github.ffalcinelli.jdivert.Packet.<init>(Packet.java:61)
		// at com.github.ffalcinelli.jdivert.WinDivert.recv(WinDivert.java:203)
		// at com.github.ffalcinelli.jdivert.WinDivert.recv(WinDivert.java:170)
		// at
		// at.ltd.tools.wf.p2p.runner.NetworkLoggingRunner.doRun(NetworkLoggingRunner.java:17)
		// at
		// at.ltd.tools.wf.p2p.runner.AbstractNetworkRunner.run(AbstractNetworkRunner.java:27)
		// at java.lang.Thread.run(Thread.java:745)

	}

}
