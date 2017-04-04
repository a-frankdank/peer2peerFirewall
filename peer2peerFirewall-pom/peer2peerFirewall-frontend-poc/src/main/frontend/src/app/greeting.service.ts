import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Greeting } from './greeting';

import { GREETINGS } from './mock-greetings';

@Injectable()
export class GreetingService {
    private greetingsUrl = 'api/greetings';

    constructor(private http: Http) {

    }

    getGreetings(): Promise<Greeting[]> {
        
        return this.http.get(this.greetingsUrl)
            .toPromise()
            .then(response => response.json().data as Greeting[])
            .catch(this.handleError);
          
            //return Promise.resolve(GREETINGS);
    }
    getGreeting(id: number): Promise<Greeting> {
        return this.getGreetings().then(greetings => greetings.find(greeting => greeting.id === id));
    }

    private handleError(error: any): Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    }
}