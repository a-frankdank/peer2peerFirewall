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

	@RequestMapping("/api/uniqueCodrs")
	// @JsonDeserialize(using = LocalDateTimeDeserializer.class)
	public Set<CodrEndpoint> getCurrentUniqueCodrEndpoints() {
		if (runner == null) {
			runner = new NetworkUniqueCodrEndpointRunner(factory);
			// TODO set wd not hard coded
			final WinDivert wd = new WinDivert(" not icmp ");
			runner.setWd(wd);
			runner.init();
			try {
				wd.open();
			} catch (WinDivertException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			executor = Executors.newSingleThreadExecutor();
			executor.execute(runner);
		}
		logger.debug("before getUniqueEntities");
		return runner.getUniqueEntities();
	}

	@PreDestroy
	public void onExit() {
		if (runner != null) {
			executor.shutdownNow();
			runner.getWd().close();
		}
	}
}
