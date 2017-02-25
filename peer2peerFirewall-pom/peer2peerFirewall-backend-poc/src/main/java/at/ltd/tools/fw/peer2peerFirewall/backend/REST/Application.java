package at.ltd.tools.fw.peer2peerFirewall.backend.REST;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = { "at.ltd.tools.fw.peer2peerFirewall.backend" })
public class Application {
	public static void main(String... strings) {
		SpringApplication.run(Application.class, strings);
	}
	// TODO wenn this application shuts down, WD has to be turned off !
}
