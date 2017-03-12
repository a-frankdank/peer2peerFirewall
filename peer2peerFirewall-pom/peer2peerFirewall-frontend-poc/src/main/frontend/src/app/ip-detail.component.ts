import { Component, Input } from '@angular/core';

@Component({
    selector: "my-ip-detail",
      templateUrl: './ip-detail.component.html',
  styleUrls: ['./app.component.css']
})

export class IpDetailComponent {
    @Input()
    ip: string;
}
