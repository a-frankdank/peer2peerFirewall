import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

import { GreetingDetailComponent } from './greeting-detail.component';
import { GreetingComponent } from './greeting.component';
import { DashboardComponent } from './dashboard.component';

import { CodrViewComponent } from './codr-view.component';

const routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: 'greeting',
    component: GreetingComponent
  },
  {
    path: 'greetingDetail/:id',
    component: GreetingDetailComponent
  },
  {
    path: 'dashboard',
    component: DashboardComponent
  }, 
  {
    path: 'codrs',
    component: CodrViewComponent
  }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
