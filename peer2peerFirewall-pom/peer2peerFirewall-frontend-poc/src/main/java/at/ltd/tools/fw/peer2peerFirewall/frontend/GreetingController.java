package at.ltd.tools.fw.peer2peerFirewall.frontend;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class GreetingController {

	@RequestMapping("/greeting")
	public String method(
	        @RequestParam(name = "name", required = false, defaultValue = "herbert") String name,
	        Model model) {
		model.addAttribute("name", name);
		return "greeting";
	}
}
