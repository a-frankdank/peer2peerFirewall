import { Injectable } from '@angular/core';
import { Http }       from '@angular/http';

import { Observable }     from 'rxjs/Observable';
import 'rxjs/add/operator/map';

import { Greeting }           from './Greeting';

@Injectable()
export class GreetingSearchService {
  constructor(private http: Http) {}

  search(term: string): Observable<Greeting[]> {
    return this.http
               .get(`api/greetings/?content=${term}`)
               .map(response => response.json().data as Greeting[]);
  }
}