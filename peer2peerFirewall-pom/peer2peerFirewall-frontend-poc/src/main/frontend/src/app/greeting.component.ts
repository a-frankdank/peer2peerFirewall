import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import { OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { Greeting } from './greeting';
import { GreetingService } from './greeting.service';

@Component({
  selector: 'my-greeting',
  templateUrl: './greeting.component.html',
  styleUrls: ['./app.component.css'],
  providers: [GreetingService],
})


@Injectable()
export class GreetingComponent implements OnInit {
  selectedGreeting: Greeting;
  greetings: Greeting[];

  ngOnInit(): void {
    this.getGreetings();
  }

  onSelect(greeting: Greeting): void {
    this.selectedGreeting = greeting;
  }

  getGreetings(): void {
    this.greetingService.getGreetings().then(greeting => this.greetings = greeting);
  }

  gotoDetail(): void {
    this.router.navigate(['/greetingDetail', this.selectedGreeting.id]);
  }

  add(text: string): void {
    text = text.trim();
    if (!text) { return; }
    this.greetingService.create(text)
      .then(greeting => {
        this.greetings.push(greeting);
        this.selectedGreeting = null;
      });
  }

  delete(greeting: Greeting): void {
    this.greetingService
      .delete(greeting.id)
      .then(() => {
        this.greetings = this.greetings.filter(h => h !== greeting);
        if (this.selectedGreeting === greeting) { this.selectedGreeting = null; }
      });
  }

  constructor(private greetingService: GreetingService, private http: Http, private router: Router) {
  }
}
