package at.ltd.tools.fw.peer2peerFirewall.backend.REST;

import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import javax.annotation.PreDestroy;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.github.ffalcinelli.jdivert.WinDivert;
import com.github.ffalcinelli.jdivert.exceptions.WinDivertException;

import at.ltd.tools.fw.peer2peerFirewall.backend.entities.CodrEndpoint;
import at.ltd.tools.fw.peer2peerFirewall.backend.runner.NetworkUniqueCodrEndpointRunner;
import at.ltd.tools.fw.peer2peerFirewall.backend.util.CodrEndpointFactory;

@RestController
public class UniqueCodrEndpointController {
	private static final Log logger = LogFactory
	        .getLog(UniqueCodrEndpointController.class);
	@Autowired
	private CodrEndpointFactory factory;
	private NetworkUniqueCodrEndpointRunner runner;
	private ExecutorService executor;
	private WinDivert wd;

	@RequestMapping("/api/uniqueCodrs")
	public Set<CodrEndpoint> getCurrentUniqueCodrEndpoints() {
		logger.debug("called getCurrentUniqueCodrEndpoints");
		if (runner == null) {
			runner = new NetworkUniqueCodrEndpointRunner(factory);
			wd = new WinDivert(" not icmp ");
			runner.setWd(wd);
			runner.init();
			try {
				wd.open();
			} catch (WinDivertException e) {
				logger.fatal("Windivert said:" + e.getStackTrace());
			}
			executor = Executors.newSingleThreadExecutor();
			executor.execute(runner);
		}
		return runner.getUniqueEntities();
	}

	@RequestMapping("/api/uniqueCodrsShutdown")
	public String shutdown() {
		logger.debug("shutdown called");
		onExit();
		runner = null;
		return "shutdown";
	}

	@PreDestroy
	public void onExit() {
		logger.debug("onExit called");
		if (runner != null) {
			runner.interrupt();
			executor.shutdownNow();
			runner.getWd().close();
			if (wd != null) {
				wd.close();
			}
		}
	}
}
