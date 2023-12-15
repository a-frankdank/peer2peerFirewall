package at.ltd.tools.fw.peer2peerFirewall.backend.ip;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.charset.Charset;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.stereotype.Component;

@Component
public class PublicIpGetter {
	public static final String PUBLICIPSERVICE = "https://api.ipify.org";
	private static final Log logger = LogFactory.getLog(PublicIpGetter.class);

	public String readAll(Reader rd) throws IOException {
		StringBuilder sb = new StringBuilder();
		int cp;
		while ((cp = rd.read()) != -1) {
			sb.append((char) cp);
		}
		return sb.toString();
	}

	public String getMyPublicIp() {
		URL url;
		StringBuilder errorString = new StringBuilder();
		try {
			url = new URL(PUBLICIPSERVICE);
			try (BufferedReader rd = new BufferedReader(new InputStreamReader(
			        url.openStream(), Charset.forName("UTF-8")));) {
				return readAll(rd);
			} catch (IOException e) {
				logger.error("error getting public ip", e);
				errorString.append(e.getMessage());
			}
		} catch (MalformedURLException mre) {
			logger.error("error getting public ip", mre);
			errorString.append(mre.getMessage());
		}
		return "error getting public ip: " + errorString;
	}
}
