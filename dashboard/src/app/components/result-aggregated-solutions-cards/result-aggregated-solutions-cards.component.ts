import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { IAggregatedSolution } from 'src/app/interfaces/ISolution';
import { RecommendationsState } from 'src/app/states/recommendations.state';
import { AggregatedSolutionsDialogComponent } from './../aggregated-solutions-dialog/aggregated-solutions-dialog.component';

@Component({
  selector: 'app-result-aggregated-solutions-cards',
  templateUrl: './result-aggregated-solutions-cards.component.html',
  styleUrl: './result-aggregated-solutions-cards.component.scss',
})
export class ResultAggregatedSolutionsCardsComponent {
  @Select(RecommendationsState.vulnerabilityReport)
  vulnerabilityReport$!: Observable<any | null>;

  constructor(public dialog: MatDialog) {}

  public openAggregatedSolutionDetails(
    aggregatedSolution: IAggregatedSolution
  ): void {
    const dialogRef = this.dialog.open(AggregatedSolutionsDialogComponent, {
      height: '80vh',
      width: '90%',
      maxHeight: '80vh',
      data: aggregatedSolution,
    });

    dialogRef.afterClosed().pipe().subscribe();
  }
}
