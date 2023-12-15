package at.ltd.tools.fw.peer2peerFirewall.backend.entities.comparator;

import java.util.Comparator;

import org.apache.commons.lang3.ArrayUtils;

import at.ltd.tools.fw.peer2peerFirewall.backend.entities.CodrEndpoint;

public class CodrEndpointComparator
        implements Comparator<CodrEndpoint> {

	@SuppressWarnings("unchecked")
	@Override
	public int compare(CodrEndpoint o1,
	        CodrEndpoint o2) {
		// a negative integer, zero, or a positive integer as the first argument
		// is
		// less than, equal to, or greater than the second.

		return calcResults(o1, o2,
		        (x, y) -> x.getSrcAdress().compareTo(y.getSrcAdress()),
		        (x, y) -> x.getSrcPort().compareTo(y.getSrcPort()),
		        (x, y) -> x.getDstAdress().compareTo(y.getDstAdress()),
		        (x, y) -> x.getDstPort().compareTo(y.getDstPort()));
	}

	public int calcResults(CodrEndpoint o1,
	        CodrEndpoint o2,
	        @SuppressWarnings("unchecked") ComparatorLambda<CodrEndpoint>... elems) {
		if (ArrayUtils.isNotEmpty(elems)) {
			int result = -2;
			for (ComparatorLambda<CodrEndpoint> elem : elems) {
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
