package at.ltd.tools.wf.p2p.runner;

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
		while (!Thread.currentThread().isInterrupted()) {
			try {
				doRun();
			} catch (WinDivertException e) { // fatal
				// TODO maybe switch for all errors?
				if (e.getCode() == 5) {
					logger.fatal("run me with admin privileges pls");
				}
				throw new RuntimeException(
				        "WinDivert failed, explanation: https://reqrypt.org/windivert-doc.html#divert_open ",
				        e);
			} catch (InterruptedException e) {
				Thread.currentThread().interrupt();
			}
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
}
