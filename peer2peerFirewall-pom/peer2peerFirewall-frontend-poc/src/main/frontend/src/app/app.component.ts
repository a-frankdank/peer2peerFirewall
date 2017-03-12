import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { OnInit } from '@angular/core';

import { Greeting } from './greeting';
import { GreetingService } from './greeting.service';

import { CodrEndpoint } from './codr-endpoint';
import { CodrEndpointService } from './codr-endpoint-service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [ GreetingService, CodrEndpointService ],
})


@Injectable()
export class AppComponent implements OnInit {
  selectedGreeting: Greeting;
  publicIp: string;
  greetings: Greeting[];
  codrs: CodrEndpoint[];
  selectedCodr: CodrEndpoint;
  http: Http;

ngOnInit(): void{
    this.getGreetings();
    this.getCodrEndpoints();
// works, but don't want that anymore
    // this.http.get('/api/uniqueCodrs')
    //   .map(r => r.json())
    //   .catch(this.handleError)
    //   .subscribe(codrs => this.codrs = codrs);

    this.publicIp = "<ip>";
    this.http.get('/api/publicIp')
      .catch(this.handleError)
      .subscribe((res: Response) => this.publicIp = res.json().publicIp);
}

onSelect(greeting: Greeting): void{
  this.selectedGreeting = greeting;
}

onSelectCodr(codr: CodrEndpoint): void{
  this.selectedCodr = codr;
}

getCodrEndpoints(): void{
  this.codrs = this.codrEndpointService.getCodrEndpoints();
}

getGreetings(): void{
  this.greetingService.getGreetings().then(greeting => this.greetings = greeting);
}

  constructor(private greetingService: GreetingService, 
  private codrEndpointService: CodrEndpointService,  http: Http) {
    this.greetingService = greetingService;
    this.codrEndpointService = codrEndpointService;
    this.http = http;
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
