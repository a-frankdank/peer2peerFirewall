package at.ltd.tools.wf;

import java.util.concurrent.Executors;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.junit.Test;

import com.github.ffalcinelli.jdivert.WinDivert;

import at.ltd.tools.fw.p2p.runner.NetworkDroppingChosenIpRunner;
import at.ltd.tools.fw.p2p.runner.NetworkLoggingRunner;
import at.ltd.tools.fw.p2p.runner.NetworkUniqueLoggingRunner;

public class TestIntegrationJDivertCapabilities {

	private static final Log logger = LogFactory
	        .getLog(TestIntegrationJDivertCapabilities.class);

	@Test
	public void testLogging() throws Exception {
		final WinDivert wd = new WinDivert("not icmp and not icmpv6");

		wd.open(); // packets will be captured from now on

		logger.info("hello testLogging");

		NetworkLoggingRunner runner = new NetworkLoggingRunner();
		runner.setWd(wd);
		Thread t = Executors.defaultThreadFactory().newThread(runner);

		t.start();
		t.join(5000);

		wd.close(); // stop capturing packets
	}

	@Test
	public void testDropping() throws Exception {
		//@formatter:off
		final WinDivert wd = new WinDivert(
				" not icmp and "
		        + "not icmpv6 and "
				+" not tcp and "
		        // TODO how to manage manual excludes?
		        +" not udp.SrcPort = 53 and not udp.DstPort = 53 ");
		//@formatter:on

		wd.open(); // packets will be captured from now on

		// should be dropping this ip: 46.196.199.74
		logger.info("hello testDropping");

		NetworkDroppingChosenIpRunner runner = new NetworkDroppingChosenIpRunner();
		runner.setWd(wd);
		runner.init();
		Thread t = Executors.defaultThreadFactory().newThread(runner);

		t.start();
		t.join(5000);

		wd.close(); // stop capturing packets
	}

	@Test
	public void testUdpLogging() throws Exception {
		//@formatter:off
		final WinDivert wd = new WinDivert(
				" not icmp and "
		        + "not icmpv6 and "
				+" not tcp and "
		        +" not udp.SrcPort = 53 and not udp.DstPort = 53 ");
		//@formatter:on

		wd.open(); // packets will be captured from now on

		logger.info("hello testUdpLogging");

		NetworkUniqueLoggingRunner runner = new NetworkUniqueLoggingRunner();
		runner.setWd(wd);
		runner.init();
		Thread t = Executors.defaultThreadFactory().newThread(runner);

		t.start();
		t.join(5000);

		wd.close(); // stop capturing packets
	}
}
