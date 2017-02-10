package at.ltd.tools.wf.p2p.runner;

import java.util.LinkedHashSet;
import java.util.Set;
import java.util.Timer;
import java.util.TimerTask;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.github.ffalcinelli.jdivert.Packet;
import com.github.ffalcinelli.jdivert.exceptions.WinDivertException;

import at.ltd.tools.wf.p2p.util.NetworkLoggingFormatter;

public class NetworkUniqueLoggingRunner extends AbstractNetworkRunner {
	private static final Log logger = LogFactory
	        .getLog(NetworkUniqueLoggingRunner.class);

	private Packet packet;

	private Set<String> uniqueStrings = new LinkedHashSet<String>();

	@Override
	public void init() {
		Timer t = new Timer();
		t.schedule(new TimerTask() {
			@Override
			public void run() {
				logger.info("====");
				uniqueStrings.stream().forEach((x) -> logger.info(x));
			}
		}, 20000l, 10000l);
	}

	public void doRun() throws WinDivertException {
		packet = getWd().recv();
		StringBuilder strb = new StringBuilder();
		NetworkLoggingFormatter.stringFormatPacketForUniqueDisplay(strb,
		        packet);
		uniqueStrings.add(strb.toString());

		getWd().send(packet);
	}

}
