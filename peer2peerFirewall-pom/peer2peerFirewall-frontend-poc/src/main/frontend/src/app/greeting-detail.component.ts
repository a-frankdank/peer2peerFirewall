import { Component, Input } from '@angular/core';
import { Greeting } from "./greeting";

@Component({
    selector: "my-greeting-detail",
      templateUrl: './greeting-detail.component.html',
  styleUrls: ['./app.component.css']
})

export class GreetingDetailComponent {
    @Input()
    greeting: Greeting;
}
