import { Component, Input } from '@angular/core';
import { CodrEndpoint } from "./codr-endpoint";

@Component({
    selector: "my-codr-endpoint-detail",
      templateUrl: './codr-endpoint-detail.component.html',
  styleUrls: ['./app.component.css']
})

export class CodrEndpointDetailComponent {
    @Input()
    codrEndpoint: CodrEndpoint;
}
