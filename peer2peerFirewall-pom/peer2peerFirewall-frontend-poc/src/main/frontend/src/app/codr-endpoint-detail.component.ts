import { Component, Input } from '@angular/core';
import { CodrEndpoint } from "./codr-endpoint";

@Component({
    selector: "my-codr-endpoint-detail",
      templateUrl: './codr-endpoint-detail.component.html',
  styleUrls: ['./codr.css']
})

export class CodrEndpointDetailComponent {
    @Input()
    codrEndpoint: CodrEndpoint;
}
