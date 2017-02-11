package at.ltd.tools.fw.entities.comparator;

import static org.junit.Assert.assertEquals;

import java.time.LocalDateTime;

import org.junit.Before;
import org.junit.Test;

import at.ltd.tools.fw.entities.ConnectionOrDataReceivedEndpoint;
import at.ltd.tools.fw.entities.comparator.ConnectionOrDataReceivedEndpointComparator;

public class TestCaseConnectionOrDataReceivedEndpointComparator {

	private ConnectionOrDataReceivedEndpointComparator classUnderTest;
	private ConnectionOrDataReceivedEndpoint endpoint1;
	private ConnectionOrDataReceivedEndpoint endpoint2;

	@Before
	public void setUp() throws Exception {
		classUnderTest = new ConnectionOrDataReceivedEndpointComparator();

		endpoint1 = new ConnectionOrDataReceivedEndpoint();
		endpoint1.setDstAdress("127.0.0.1");
		endpoint1.setDstPort(80);
		endpoint1.setSrcAdress("127.0.0.1");
		endpoint1.setSrcPort(80);

		endpoint2 = new ConnectionOrDataReceivedEndpoint(endpoint1);
		endpoint2.setDstAdress("127.0.0.1");
		endpoint2.setDstPort(81);
	}

	@Test
	public void testCompare() throws Exception {
		assertEquals(0, classUnderTest.compare(endpoint1, endpoint1));
		assertEquals(-1, classUnderTest.compare(endpoint1, endpoint2));
		assertEquals(1, classUnderTest.compare(endpoint2, endpoint1));

		endpoint2 = new ConnectionOrDataReceivedEndpoint(endpoint1);
		endpoint1.setTimeLastChanged(LocalDateTime.now());
		assertEquals(0, classUnderTest.compare(endpoint1, endpoint2));
	}

	@Test
	public void testCompare_moreCases() throws Exception {
		endpoint2 = new ConnectionOrDataReceivedEndpoint(endpoint1);
		endpoint2.setDstAdress("128.0.0.1");
		assertEquals(-1, classUnderTest.compare(endpoint1, endpoint2));
		assertEquals(+1, classUnderTest.compare(endpoint2, endpoint1));

		endpoint2 = new ConnectionOrDataReceivedEndpoint(endpoint1);
		endpoint2.setSrcPort(81);
		assertEquals(-1, classUnderTest.compare(endpoint1, endpoint2));
		assertEquals(+1, classUnderTest.compare(endpoint2, endpoint1));

		endpoint2 = new ConnectionOrDataReceivedEndpoint(endpoint1);
		endpoint2.setSrcAdress("128.0.0.1");
		assertEquals(-1, classUnderTest.compare(endpoint1, endpoint2));
		assertEquals(+1, classUnderTest.compare(endpoint2, endpoint1));
	}

}
