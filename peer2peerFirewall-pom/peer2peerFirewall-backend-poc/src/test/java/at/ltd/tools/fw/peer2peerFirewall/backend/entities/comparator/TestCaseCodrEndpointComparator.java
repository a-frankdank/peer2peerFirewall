package at.ltd.tools.fw.peer2peerFirewall.backend.entities.comparator;

import static org.junit.Assert.assertEquals;

import java.time.LocalDateTime;

import org.junit.Before;
import org.junit.Test;

import at.ltd.tools.fw.peer2peerFirewall.backend.entities.CodrEndpoint;

public class TestCaseCodrEndpointComparator {

	private CodrEndpointComparator classUnderTest;
	private CodrEndpoint endpoint1;
	private CodrEndpoint endpoint2;

	@Before
	public void setUp() throws Exception {
		classUnderTest = new CodrEndpointComparator();

		endpoint1 = new CodrEndpoint();
		endpoint1.setDstAdress("127.0.0.1");
		endpoint1.setDstPort(80);
		endpoint1.setSrcAdress("127.0.0.1");
		endpoint1.setSrcPort(80);

		endpoint2 = new CodrEndpoint(endpoint1);
		endpoint2.setDstAdress("127.0.0.1");
		endpoint2.setDstPort(81);
	}

	@Test
	public void testCompare() throws Exception {
		assertEquals(0, classUnderTest.compare(endpoint1, endpoint1));
		assertEquals(-1, classUnderTest.compare(endpoint1, endpoint2));
		assertEquals(1, classUnderTest.compare(endpoint2, endpoint1));

		endpoint2 = new CodrEndpoint(endpoint1);
		endpoint1.setTimeLastChanged(LocalDateTime.now());
		assertEquals(0, classUnderTest.compare(endpoint1, endpoint2));
	}

	@Test
	public void testCompare_moreCases() throws Exception {
		endpoint2 = new CodrEndpoint(endpoint1);
		endpoint2.setDstAdress("128.0.0.1");
		assertEquals(-1, classUnderTest.compare(endpoint1, endpoint2));
		assertEquals(+1, classUnderTest.compare(endpoint2, endpoint1));

		endpoint2 = new CodrEndpoint(endpoint1);
		endpoint2.setSrcPort(81);
		assertEquals(-1, classUnderTest.compare(endpoint1, endpoint2));
		assertEquals(+1, classUnderTest.compare(endpoint2, endpoint1));

		endpoint2 = new CodrEndpoint(endpoint1);
		endpoint2.setSrcAdress("128.0.0.1");
		assertEquals(-1, classUnderTest.compare(endpoint1, endpoint2));
		assertEquals(+1, classUnderTest.compare(endpoint2, endpoint1));
	}

}
