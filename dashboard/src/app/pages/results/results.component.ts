import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Select } from '@ngxs/store';
import { combineLatest, filter, map, Observable, switchMap } from 'rxjs';
import { RecommendationsService } from 'src/app/services/recommendations.service';
import { RecommendationsState } from 'src/app/states/recommendations.state';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss'],
})
export class ResultsComponent implements OnInit {
  @Select(RecommendationsState.fileName)
  fileName$!: Observable<string>;
  @Select(RecommendationsState.findings) findings$!: Observable<any | null>;

  constructor(
    private router: Router,
    private recommendationService: RecommendationsService
  ) {}

  ngOnInit(): void {
    this.getRecommendations();
  }

  private getRecommendations(): void {
    combineLatest([this.findings$, this.fileName$])
      .pipe(
        map(([findings, fileName]) => {
          if (!fileName) {
            this.router.navigate(['home']);
            return null;
          } else if (findings.length) {
            return null;
          } else {
            return findings;
          }
        }),
        filter((result) => !!result),
        switchMap(() => this.recommendationService.getRecommendations())
      )
      .subscribe();
    // this.findings$
    //   .pipe(
    //     take(1),
    //     tap((findings) => !findings.length && this.router.navigate(['home']))
    //     // TODO Add getRecommendations request
    //   )
    //   .subscribe();
  }
}
