package at.ltd.tools.wf.entities.comparator;

@FunctionalInterface
public interface ComparatorLambda<T> {
	int comp(T t1, T t2);
}
