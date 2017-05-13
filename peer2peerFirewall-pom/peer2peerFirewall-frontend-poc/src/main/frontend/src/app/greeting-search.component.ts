import { Component, OnInit } from '@angular/core';
import { Router }            from '@angular/router';

import { Observable }        from 'rxjs/Observable';
import { Subject }           from 'rxjs/Subject';

// Observable class extensions
import 'rxjs/add/observable/of';

// Observable operators
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/debounceTime';
import 'rxjs/add/operator/distinctUntilChanged';

import { GreetingSearchService } from './greeting-search.service';
import { Greeting } from './greeting';

@Component({
  selector: 'greeting-search',
  templateUrl: './greeting-search.component.html',
  styleUrls: [ './greeting-search.component.css' ],
  providers: [GreetingSearchService]
})

export class GreetingSearchComponent implements OnInit {
  greetings: Observable<Greeting[]>;
  private searchTerms = new Subject<string>();

  constructor(
    private greetingSearchService: GreetingSearchService,
    private router: Router) {}

  // Push a search term into the observable stream.
  search(term: string): void {
    this.searchTerms.next(term);
  }

  ngOnInit(): void {
    this.greetings = this.searchTerms
      .debounceTime(300)        // wait 300ms after each keystroke before considering the term
      .distinctUntilChanged()   // ignore if next search term is same as previous
      .switchMap(term => term   // switch to new observable each time the term changes
        // return the http search observable
        ? this.greetingSearchService.search(term)
        // or the observable of empty greetinges if there was no search term
        : Observable.of<Greeting[]>([]))
      .catch(error => {
        // TODO: add real error handling
        console.log(error);
        return Observable.of<Greeting[]>([]);
      });
  }

  gotoDetail(greeting: Greeting): void {
    let link = ['/greetingDetail', greeting.id];
    this.router.navigate(link);
  }
}