import { Injectable } from '@angular/core';

import { Greeting } from './greeting';
import { GREETINGS } from './mock-greetings';

@Injectable()
export class GreetingService{
    getGreetings(): Promise<Greeting[]>{
        return Promise.resolve(GREETINGS);
    } 
}