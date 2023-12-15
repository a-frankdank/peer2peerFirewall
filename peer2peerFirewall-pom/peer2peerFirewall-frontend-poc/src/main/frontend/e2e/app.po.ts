import { browser, element, by } from 'protractor';

export class Peer2peerFirewallPage {
  navigateTo() {
    return browser.get('/');
  }

  getParagraphText() {
    return element(by.css('app-root h1')).getText();
  }
}
