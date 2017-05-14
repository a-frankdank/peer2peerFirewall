package at.ltd.tools.fw.peer2peerFirewall.backend.runner;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.github.ffalcinelli.jdivert.WinDivert;
import com.github.ffalcinelli.jdivert.exceptions.WinDivertException;

/**
 * puts while and catch {@link WinDivertException} over code in {@link #doRun()}
 * inside run
 * 
 * @author ltd
 *
 */
public abstract class AbstractNetworkRunner implements Runnable {

	private static final Log logger = LogFactory
	        .getLog(AbstractNetworkRunner.class);

	private WinDivert wd;

	@Override
	public void run() {
		// TODO the interupting doesn't work as expected ...
		// Exception in thread "pool-2-thread-1" java.lang.RuntimeException:
		// WinDivert failed, explanation:
		// https://reqrypt.org/windivert-doc.html#divert_open
		// at
		// at.ltd.tools.fw.peer2peerFirewall.backend.runner.AbstractNetworkRunner.run(AbstractNetworkRunner.java:33)
		// at
		// java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
		// at
		// java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
		// at java.lang.Thread.run(Thread.java:745)
		// Caused by: WinDivertException{code=995, message='null'}
		// at
		// com.github.ffalcinelli.jdivert.exceptions.WinDivertException.throwExceptionOnGetLastError(WinDivertException.java:56)
		// at com.github.ffalcinelli.jdivert.WinDivert.recv(WinDivert.java:201)
		// at com.github.ffalcinelli.jdivert.WinDivert.recv(WinDivert.java:170)
		// at
		// at.ltd.tools.fw.peer2peerFirewall.backend.runner.NetworkUniqueCodrEndpointRunner.doRun(NetworkUniqueCodrEndpointRunner.java:37)
		// at
		// at.ltd.tools.fw.peer2peerFirewall.backend.runner.AbstractNetworkRunner.run(AbstractNetworkRunner.java:27)
		while (!Thread.currentThread().isInterrupted()) {
			try {
				doRun();
			} catch (WinDivertException e) { // fatal
				close();
				// TODO maybe switch for all errors?
				if (e.getCode() == 5) {
					logger.fatal("run me with admin privileges pls");
				}
				logger.fatal(
				        "WinDivert failed, explanation: https://reqrypt.org/windivert-doc.html#divert_open ",
				        e);
			} catch (InterruptedException e) {
				Thread.currentThread().interrupt();
			} catch (Exception e) {
				close();
				logger.fatal(
				        "Closing Windivert cuz of Exception during Windivert usage:",
				        e);
			}
		}
		shutdown();
	}

	protected abstract void shutdown();

	public void close() {
		try {
			getWd().close();
		} catch (Exception e2) {
			logger.error("Exception during closing", e2);
		}
	}

	public abstract void doRun()
	        throws WinDivertException, InterruptedException;

	public WinDivert getWd() {
		return wd;
	}

	public void setWd(WinDivert wd) {
		this.wd = wd;
	}

	/**
	 * should only be called once before starting to 'run' it
	 */
	public void init() {
	}

	public void interrupt() {
		Thread.currentThread().interrupt();
	}
}
