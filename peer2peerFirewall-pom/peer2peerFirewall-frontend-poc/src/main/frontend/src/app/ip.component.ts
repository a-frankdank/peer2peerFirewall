import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { OnInit } from '@angular/core';

@Component({
  selector: 'my-ip',
  templateUrl: './ip.component.html',
  styleUrls: ['./app.component.css'],
})


@Injectable()
export class IpComponent implements OnInit {
  publicIp: string;
  http: Http;

ngOnInit(): void{
    this.publicIp = "<ip>";
    this.http.get('/api/publicIp')
      .toPromise()
      .then((res: Response) => this.publicIp = res.text())
      .catch(this.handleError)
      //.subscribe((res: Response) => this.publicIp = res.json().publicIp);
}

  constructor(http: Http) {
    this.http = http;
  }

  private handleError(error: Response | any) {
    // TODO refactor this to a central place and improve logging: display on screen and write to server to log?
    
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
