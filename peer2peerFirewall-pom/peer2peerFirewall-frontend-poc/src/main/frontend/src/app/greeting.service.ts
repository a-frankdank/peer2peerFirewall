import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Greeting } from './greeting';

import { GREETINGS } from './mock-greetings';

@Injectable()
export class GreetingService {
    private greetingsUrl = 'api/greetings';
    private headers = new Headers({ 'Content-Type': 'application/json' });

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
        const url = `${this.greetingsUrl}/${id}`;
        return this.http.get(url)
            .toPromise()
            .then(response => response.json().data as Greeting)
            .catch(this.handleError);
        //return this.getGreetings().then(greetings => greetings.find(greeting => greeting.id === id));
    }

    update(greeting: Greeting): Promise<Greeting> {
        const url = `${this.greetingsUrl}/${greeting.id}`;
        return this.http
            .put(url, JSON.stringify(greeting), { headers: this.headers })
            .toPromise()
            .then(() => greeting)
            .catch(this.handleError);
    }

    create(text: string): Promise<Greeting> {
        let tmpGreeting = { content: text };
        return this.http
            .post(this.greetingsUrl, JSON.stringify(tmpGreeting), { headers: this.headers })
            .toPromise()
            .then(res => res.json().data as Greeting)
            .catch(this.handleError);
    }

    delete(id: number): Promise<void> {
        const url = `${this.greetingsUrl}/${id}`;
        return this.http.delete(url, { headers: this.headers })
            .toPromise()
            .then(() => null)
            .catch(this.handleError);
    }

    private handleError(error: any): Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    }
}