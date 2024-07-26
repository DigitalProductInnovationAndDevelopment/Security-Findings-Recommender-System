import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { lastValueFrom, Observable } from 'rxjs';
import { RecommendationsService } from 'src/app/services/recommendations.service';
import { setInformation } from 'src/app/states/recommendations.actions';
import { RecommendationsState } from 'src/app/states/recommendations.state';

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
    const exampleFindings = await lastValueFrom(
      this.recommendationsService.getExampleData(which)
    );
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
