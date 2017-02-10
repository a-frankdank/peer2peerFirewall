package at.ltd.tools.wf.entities.comparator;

import java.util.Comparator;

import org.apache.commons.lang3.ArrayUtils;

import at.ltd.tools.wf.entities.ConnectionOrDataReceivedEndpoint;

public class ConnectionOrDataReceivedEndpointComparator
        implements Comparator<ConnectionOrDataReceivedEndpoint> {

	@SuppressWarnings("unchecked")
	@Override
	public int compare(ConnectionOrDataReceivedEndpoint o1,
	        ConnectionOrDataReceivedEndpoint o2) {
		// a negative integer, zero, or a positive integer as the first argument
		// is
		// less than, equal to, or greater than the second.

		return calcResults(o1, o2,
		        (x, y) -> x.getSrcAdress().compareTo(y.getSrcAdress()),
		        (x, y) -> x.getSrcPort().compareTo(y.getSrcPort()),
		        (x, y) -> x.getDstAdress().compareTo(y.getDstAdress()),
		        (x, y) -> x.getDstPort().compareTo(y.getDstPort()));
	}

	public int calcResults(ConnectionOrDataReceivedEndpoint o1,
	        ConnectionOrDataReceivedEndpoint o2,
	        @SuppressWarnings("unchecked") ComparatorLambda<ConnectionOrDataReceivedEndpoint>... elems) {
		if (ArrayUtils.isNotEmpty(elems)) {
			int result = -2;
			for (ComparatorLambda<ConnectionOrDataReceivedEndpoint> elem : elems) {
				result = elem.comp(o1, o2);
				if (result != 0) {
					return result;
				}
			}
			return result;
		} else {
			throw new RuntimeException("u are using this method wrong");
		}
	}

}
