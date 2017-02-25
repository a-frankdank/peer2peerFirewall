import { Greeting } from './greeting';
import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';


const GREETINGS: Greeting[] = [
  { id: "11", content: 'Mr. Nice' },
  { id: "12", content: 'Herbert' },
  { id: "13", content: 'Lover' },
  { id: "14", content: 'Jackson' },
  { id: "15", content: 'Hugo' },
  { id: "16", content: 'Habicht' },
];

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


@Injectable()
export class AppComponent {
  greeting: Greeting = { id: "", content: "" };
  publicIp: string;
  greetings = GREETINGS;

  constructor(http: Http) {
    http.get('/api/resource')
      .map(r => r.json())
      .catch(this.handleError)
      .subscribe(greeting => this.greeting = greeting);

    http.get('/api/publicIp')
      .catch(this.handleError)
      .subscribe((res: Response) => this.publicIp = res.json().publicIp);
  }

  private handleError(error: Response | any) {
    // In a real world app, we might use a remote logging infrastructure
    let errMsg: string;
    if (error instanceof Response) {
      const body = error.json() || '';
      const err = body.error || JSON.stringify(body);
      errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
    } else {
      errMsg = error.message ? error.message : error.toString();
    }
    console.error(errMsg);
    return Observable.throw(errMsg);
  }
  
  
}
