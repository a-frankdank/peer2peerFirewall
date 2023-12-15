package at.ltd.tools.fw.peer2peerFirewall.backend.util;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import com.github.ffalcinelli.jdivert.Packet;

import at.ltd.tools.fw.peer2peerFirewall.backend.entities.CodrEndpoint;

@RunWith(MockitoJUnitRunner.class)
public class TestCaseCodrEndpointFactory {

	private CodrEndpointFactory classUnderTest;
	@Mock
	private Packet packet;

	@Before
	public void setUp() throws Exception {
		classUnderTest = new CodrEndpointFactory();
	}

	@Test
	public void testCreateCodrEndpoint() throws Exception {
		when(packet.getDstAddr()).thenReturn("dstAddr");
		when(packet.getDstPort()).thenReturn(1);
		when(packet.getSrcAddr()).thenReturn("srcAddr");
		when(packet.getSrcPort()).thenReturn(2);

		CodrEndpoint erg = classUnderTest.createCodrEndpoint(packet);

		assertEquals("dstAddr", erg.getDstAdress());
		assertEquals("srcAddr", erg.getSrcAdress());
		assertEquals(new Integer(1), erg.getDstPort());
		assertEquals(new Integer(2), erg.getSrcPort());
	}

}
