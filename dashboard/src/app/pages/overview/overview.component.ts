import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { RecommendationsState } from 'src/app/states/recommendations.state';

@Component({
  selector: 'app-overview',
  templateUrl: './overview.component.html',
  styleUrls: ['./overview.component.scss'],
})
export class OverviewComponent {
  @Select(RecommendationsState.fileName) fileName$!: Observable<string>;
}
