package at.ltd.tools.fw.peer2peerFirewall.backend.entities;

import java.time.LocalDateTime;

public class ConnectionOrDataReceivedEndpoint {
	private String srcAdress;
	private Integer srcPort;
	private String dstAdress;
	private Integer dstPort;
	// end of 'should be in comparator'
	private LocalDateTime timeLastChanged;

	public ConnectionOrDataReceivedEndpoint() {
		// nothing
	}

	public ConnectionOrDataReceivedEndpoint(
	        ConnectionOrDataReceivedEndpoint endpoint) {
		this(endpoint.getSrcAdress(), endpoint.getSrcPort(),
		        endpoint.getDstAdress(), endpoint.getDstPort(),
		        endpoint.getTimeLastChanged());
	}

	public ConnectionOrDataReceivedEndpoint(String srcAdress, Integer srcPort,
	        String dstAdress, Integer dstPort, LocalDateTime timeLastChanged) {
		this.srcAdress = srcAdress;
		this.srcPort = srcPort;
		this.dstAdress = dstAdress;
		this.dstPort = dstPort;
		this.timeLastChanged = timeLastChanged;
	}

	public String getSrcAdress() {
		return srcAdress;
	}

	public void setSrcAdress(String srcAdress) {
		this.srcAdress = srcAdress;
	}

	public Integer getSrcPort() {
		return srcPort;
	}

	public void setSrcPort(Integer srcPort) {
		this.srcPort = srcPort;
	}

	public String getDstAdress() {
		return dstAdress;
	}

	public void setDstAdress(String dstAdress) {
		this.dstAdress = dstAdress;
	}

	public Integer getDstPort() {
		return dstPort;
	}

	public void setDstPort(Integer dstPort) {
		this.dstPort = dstPort;
	}

	public LocalDateTime getTimeLastChanged() {
		return timeLastChanged;
	}

	public void setTimeLastChanged(LocalDateTime timeLastChanged) {
		this.timeLastChanged = timeLastChanged;
	}
}
