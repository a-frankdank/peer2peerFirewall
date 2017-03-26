import { Injectable } from '@angular/core';

import { Greeting } from './greeting';
import { GREETINGS } from './mock-greetings';

@Injectable()
export class GreetingService {
    getGreetings(): Promise<Greeting[]> {
        return Promise.resolve(GREETINGS);
    }
    getGreeting(id: number): Promise<Greeting> {
        return this.getGreetings().then(greetings => greetings.find(greeting => greeting.id === id));
    }
}