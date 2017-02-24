import { Peer2peerFirewallPage } from './app.po';

describe('peer2peer-firewall App', function() {
  let page: Peer2peerFirewallPage;

  beforeEach(() => {
    page = new Peer2peerFirewallPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
