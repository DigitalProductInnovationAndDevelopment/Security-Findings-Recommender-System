import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable, Subscription } from 'rxjs';
import { IFinding } from 'src/app/interfaces/IFinding';
import { RecommendationsService } from 'src/app/services/recommendations.service';
import {
  clearFindings,
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
  private subscription!: Subscription;

  constructor(
    private router: Router,
    private recommendationService: RecommendationsService,
    private store: Store
  ) {}

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
      this.store.dispatch(new loadRecommendations()).subscribe();
    }
  }
}
