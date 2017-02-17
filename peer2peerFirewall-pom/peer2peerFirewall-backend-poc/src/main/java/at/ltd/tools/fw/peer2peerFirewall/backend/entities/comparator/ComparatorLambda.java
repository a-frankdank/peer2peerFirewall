package at.ltd.tools.fw.peer2peerFirewall.backend.entities.comparator;

@FunctionalInterface
public interface ComparatorLambda<T> {
	int comp(T t1, T t2);
}
