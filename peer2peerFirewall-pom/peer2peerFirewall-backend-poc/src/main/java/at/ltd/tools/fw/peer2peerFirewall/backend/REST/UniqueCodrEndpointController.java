package at.ltd.tools.fw.peer2peerFirewall.backend.REST;

import java.util.Set;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import javax.annotation.PreDestroy;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.github.ffalcinelli.jdivert.WinDivert;
import com.github.ffalcinelli.jdivert.exceptions.WinDivertException;

import at.ltd.tools.fw.peer2peerFirewall.backend.entities.CodrEndpoint;
import at.ltd.tools.fw.peer2peerFirewall.backend.runner.NetworkUniqueCodrEndpointRunner;
import at.ltd.tools.fw.peer2peerFirewall.backend.util.CodrEndpointFactory;

@RestController
@RequestMapping("/api/uniqueCodrs")
public class UniqueCodrEndpointController {
	private static final Log logger = LogFactory
	        .getLog(UniqueCodrEndpointController.class);
	@Autowired
	private CodrEndpointFactory factory;
	private NetworkUniqueCodrEndpointRunner runner;
	private ExecutorService executor;
	private WinDivert wd;

	@RequestMapping("/all")
	public Set<CodrEndpoint> getCurrentUniqueCodrEndpoints() {
		logger.debug("called getCurrentUniqueCodrEndpoints");
		lazyInit();
		return runner.getUniqueEntities();
	}

	@RequestMapping("/{id}")
	public CodrEndpoint getOneCodr(@PathVariable Integer id) {
		logger.debug("called getOneCodr");
		lazyInit();
		return runner.getUniqueEntities().parallelStream()
		        .filter(e -> id.equals(e.getId())).findAny().orElse(null);
	}

	// TODO really make it block by ip, not by exact packet
	@RequestMapping("/blockByPacket/{id}")
	public String blockOneCodr(@PathVariable(required = false) Integer id) {
		logger.debug("called blockOneCodr");
		lazyInit();
		if (id != null) {
			CodrEndpoint erg = runner.getUniqueEntities().parallelStream()
			        .filter(e -> id.equals(e.getId())).findAny().orElse(null);
			if (erg == null) {
				return "don't know this id: " + id;
			}
			erg.setBlocked(Boolean.TRUE);
			return "id:" + id + ", ie ip:" + erg.getSrcAdress() + ", blocked";
		} else {
			return "nothing to do";
		}
	}

	@RequestMapping("/shutdown")
	public String shutdown() {
		logger.debug("shutdown called");
		onExit();
		runner = null;
		return "shutdown complete";
	}

	public void lazyInit() {
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
