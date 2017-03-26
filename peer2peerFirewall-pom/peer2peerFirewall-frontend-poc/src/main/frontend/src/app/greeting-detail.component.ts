import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location } from '@angular/common';

import 'rxjs/add/operator/switchMap';

import { Greeting } from "./greeting";
import { GreetingService } from './greeting.service';

@Component({
    selector: "my-greeting-detail",
    templateUrl: './greeting-detail.component.html',
    styleUrls: ['./greeting-detail.component.css']
})

export class GreetingDetailComponent implements OnInit {
    @Input()
    greeting: Greeting;

    constructor(private greetingService: GreetingService,
        private route: ActivatedRoute,
        private location: Location) {

    }


    ngOnInit() {
        this.route.params
            .switchMap((params: Params) => this.greetingService.getGreeting(+params['id']))
            .subscribe(greeting => this.greeting = greeting);
    }

    goBack(): void {
        this.location.back();
    }

}
