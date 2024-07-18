import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { IFinding } from 'src/app/interfaces/IFinding';
import {
  clearFindings,
  filterRecs,
  loadRecommendations,
} from 'src/app/states/recommendations.actions';
import { RecommendationsState } from 'src/app/states/recommendations.state';

export interface ReceivedRecommendations {
  items: IFinding[];
  pagination: {
    offset: string;
    limit: string;
    total: number;
    count: number;
  };
}

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss'],
})
export class ResultsComponent implements OnInit, OnDestroy {
  @Select(RecommendationsState.fileName) fileName$!: Observable<string>;
  @Select(RecommendationsState.findings) findings$!: Observable<any | null>;
  @Select(RecommendationsState.exampleProcess)
  exampleProcess$!: Observable<boolean>;
  public loading: boolean = false;
  public severityMinValue = 0;
  public severityMaxValue = 100;

  constructor(private router: Router, private store: Store) {}

  ngOnInit(): void {
    this.getRecommendations();
  }

  ngOnDestroy(): void {
    this.store.dispatch([new clearFindings()]);
  }

  private async getRecommendations() {
    const fileName = this.store.selectSnapshot<string | undefined>(
      RecommendationsState.fileName
    );
    const exampleProcess = this.store.selectSnapshot<boolean>(
      RecommendationsState.exampleProcess
    );
    if (!fileName) {
      this.router.navigate(['home']);
    } else if (!exampleProcess) {
      this.store.dispatch(new loadRecommendations({})).subscribe();
    }
  }

  public filterRecommendations(): void {
    console.log(this.severityMinValue, this.severityMaxValue);
    this.store.dispatch(
      new filterRecs({
        severity: [this.severityMinValue, this.severityMaxValue],
      })
    );
  }
}
