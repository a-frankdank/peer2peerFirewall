package at.ltd.tools.fw.peer2peerFirewall.backend.entities;

import java.time.LocalDateTime;

/**
 * A Connection Or Data Received Endpoint
 * 
 * @author ltd
 *
 */
public class CodrEndpoint {
	private String srcAdress;
	private Integer srcPort;
	private String dstAdress;
	private Integer dstPort;
	// end of 'should be in comparator'
	private LocalDateTime timeLastChanged;
	// TODO fill those elements correctly
	private String label;
	private String ipCountryImage;
	private String correspondingExe;

	public CodrEndpoint() {
		// nothing
	}

	public CodrEndpoint(CodrEndpoint endpoint) {
		this(endpoint.getSrcAdress(), endpoint.getSrcPort(),
		        endpoint.getDstAdress(), endpoint.getDstPort(),
		        endpoint.getTimeLastChanged());
	}

	public CodrEndpoint(String srcAdress, Integer srcPort, String dstAdress,
	        Integer dstPort, LocalDateTime timeLastChanged) {
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

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result
		        + ((dstAdress == null) ? 0 : dstAdress.hashCode());
		result = prime * result + ((dstPort == null) ? 0 : dstPort.hashCode());
		result = prime * result
		        + ((srcAdress == null) ? 0 : srcAdress.hashCode());
		result = prime * result + ((srcPort == null) ? 0 : srcPort.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		CodrEndpoint other = (CodrEndpoint) obj;
		if (dstAdress == null) {
			if (other.dstAdress != null)
				return false;
		} else if (!dstAdress.equals(other.dstAdress))
			return false;
		if (dstPort == null) {
			if (other.dstPort != null)
				return false;
		} else if (!dstPort.equals(other.dstPort))
			return false;
		if (srcAdress == null) {
			if (other.srcAdress != null)
				return false;
		} else if (!srcAdress.equals(other.srcAdress))
			return false;
		if (srcPort == null) {
			if (other.srcPort != null)
				return false;
		} else if (!srcPort.equals(other.srcPort))
			return false;
		return true;
	}
}
