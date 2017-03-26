import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';

import { GreetingDetailComponent } from './greeting-detail.component';
import { GreetingComponent } from './greeting.component';
import { GreetingService } from './greeting.service';

import { CodrEndpointDetailComponent } from './codr-endpoint-detail.component';
import { CodrEndpointComponent } from './codr-endpoint.component';
import { CodrEndpointService } from './codr-endpoint-service';

import { IpDetailComponent } from './ip-detail.component';
import { IpComponent } from './ip.component';

import { DashboardComponent } from './dashboard.component';


@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AppRoutingModule,
  ],
  declarations: [
    AppComponent,
    GreetingDetailComponent,
    GreetingComponent,
    CodrEndpointDetailComponent,
    CodrEndpointComponent,
    IpDetailComponent,
    IpComponent,
    DashboardComponent
  ],
  providers: [
    GreetingService,
    CodrEndpointService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
