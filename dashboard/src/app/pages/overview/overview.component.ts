import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable, take, tap } from 'rxjs';
import { setFindings } from 'src/app/states/recommendations.actions';
import { RecommendationsState } from 'src/app/states/recommendations.state';
import { example_llama3, example_claude, example_gpt4o } from 'src/assets/example';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss'],
})
export class OverviewComponent {
  @Select(RecommendationsState.fileName) fileName$!: Observable<string>;

  constructor(private router: Router, private store: Store) {}

  openExample(which='llama3') {
    let exampleFindings;
    switch (which) {
      case 'llama3':
        exampleFindings = example_llama3;
        break;
      case 'claude-opus':
        exampleFindings = example_claude;
        break;
      case 'gpt4o':
        exampleFindings = example_gpt4o;
        break;
      default:
        exampleFindings = example_llama3;
        break;
    }

    this.store
      .dispatch(
        new setFindings({
          data: exampleFindings,
        })
      )
      .pipe(
        take(1),
        tap(() => this.router.navigate(['results']))
      )
      .subscribe();
  }
}
