package at.ltd.tools.fw.peer2peerFirewall.backend.ip;

import java.util.Map;

import org.apache.commons.collections4.map.HashedMap;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class PublicIpController {

	@Autowired
	private PublicIpGetter getter;

	@RequestMapping("/api/publicIp")
	public Map<String, Object> getPublicIp() {
		Map<String, Object> hashMap = new HashedMap<>();
		hashMap.put("publicIp", getter.getMyPublicIp());
		return hashMap;
	}

}
