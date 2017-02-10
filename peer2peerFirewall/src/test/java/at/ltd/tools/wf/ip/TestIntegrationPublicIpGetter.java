package at.ltd.tools.wf.ip;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.junit.Test;

import junit.framework.TestCase;

public class TestIntegrationPublicIpGetter extends TestCase {
	private static final Log logger = LogFactory
	        .getLog(TestIntegrationPublicIpGetter.class);
	private PublicIpGetter classUnderTest = new PublicIpGetter();

	@Test
	public void testGetMyPublicIp() throws Exception {
		String ip = classUnderTest.getMyPublicIp();
		logger.info(ip);
		assertEquals(true, !"error getting public ip".equals(ip));
	}

}
