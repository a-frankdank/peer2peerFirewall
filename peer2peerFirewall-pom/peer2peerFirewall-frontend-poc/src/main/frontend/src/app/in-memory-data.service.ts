import { InMemoryDbService } from 'angular-in-memory-web-api';

export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    let greetings = [
      { id: 11, content: 'bon jour' },
      { id: 12, content: 'dobar dan' },
      { id: 13, content: 'iyi günler' },
      { id: 14, content: 'good day' },
      { id: 15, content: 'buon giorno' },
    ];
    let publicIp = [ "pubIp" ];
    return { greetings, publicIp };
  }
}