import { Component, OnInit } from '@angular/core';

import { Greeting } from './greeting';
import { GreetingService } from './greeting.service';

@Component({
  selector: 'my-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  greetings: Greeting[] = [];

  constructor(private greetingService: GreetingService) { }

  ngOnInit() {
    this.greetingService.getGreetings().then(greetings => this.greetings = greetings.slice(1, 5));
  }

}
