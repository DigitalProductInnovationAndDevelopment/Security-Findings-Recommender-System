import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { lastValueFrom, Observable } from 'rxjs';
import { RecommendationsService } from 'src/app/services/recommendations.service';
import { setInformation } from 'src/app/states/recommendations.actions';
import { RecommendationsState } from 'src/app/states/recommendations.state';
import { example_gpt4o, example_llama3 } from 'src/assets/example';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss'],
})
export class OverviewComponent {
  @Select(RecommendationsState.fileName) fileName$!: Observable<
    string | undefined
  >;

  constructor(
    private router: Router,
    private store: Store,
    private recommendationsService: RecommendationsService
  ) {}

  async openExample(which = 'llama3') {
    let exampleFindings;
    switch (which) {
      case 'llama3':
        exampleFindings = example_llama3;
        break;
      case 'claude-opus':
        exampleFindings = await lastValueFrom(
          this.recommendationsService.getExampleData('claude')
        );
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
        new setInformation({
          data: exampleFindings,
          fileName: `${which}.json`,
          exampleProcess: true,
        })
      )
      .subscribe();
    this.router.navigate(['results']);
  }
}
