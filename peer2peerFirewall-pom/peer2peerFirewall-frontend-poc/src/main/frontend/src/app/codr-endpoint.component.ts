import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { OnInit } from '@angular/core';

import { CodrEndpoint } from './codr-endpoint';
import { CodrEndpointService } from './codr-endpoint-service';

@Component({
  selector: 'my-codr-endpoint',
  templateUrl: './codr-endpoint.component.html',
  styleUrls: ['./app.component.css'],
  providers: [CodrEndpointService],
})


@Injectable()
export class CodrEndpointComponent implements OnInit {
  codrs: CodrEndpoint[];
  selectedCodr: CodrEndpoint;
  http: Http;

  ngOnInit(): void {
    this.getCodrEndpoints();
    // works, but don't want that anymore
    // this.http.get('/api/uniqueCodrs')
    //   .map(r => r.json())
    //   .catch(this.handleError)
    //   .subscribe(codrs => this.codrs = codrs);
  }

  onSelectCodr(codr: CodrEndpoint): void {
    this.selectedCodr = codr;
  }

  getCodrEndpoints(): void {
    this.codrEndpointService.getCodrEndpoints().then(codrs => this.codrs = codrs);
  }

  constructor(private codrEndpointService: CodrEndpointService, http: Http) {
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
