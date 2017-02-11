package at.ltd.tools.fw.entities.comparator;

@FunctionalInterface
public interface ComparatorLambda<T> {
	int comp(T t1, T t2);
}
