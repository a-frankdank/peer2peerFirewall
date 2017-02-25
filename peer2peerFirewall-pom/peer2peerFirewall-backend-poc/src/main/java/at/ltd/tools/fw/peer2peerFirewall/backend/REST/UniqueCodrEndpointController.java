package at.ltd.tools.fw.peer2peerFirewall.backend.REST;

import java.util.Set;
import java.util.concurrent.Executors;

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
	@Autowired
	private CodrEndpointFactory factory;
	private NetworkUniqueCodrEndpointRunner runner;

	@RequestMapping("/api/uniqueCodrs")
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
			Executors.newSingleThreadExecutor().execute(runner);
		}
		return runner.getUniqueEntities();
	}
}
