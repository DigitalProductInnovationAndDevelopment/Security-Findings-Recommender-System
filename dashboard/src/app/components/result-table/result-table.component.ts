import {
  animate,
  state,
  style,
  transition,
  trigger,
} from '@angular/animations';
import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { Select } from '@ngxs/store';
import { Observable, tap } from 'rxjs';
import { IFinding } from 'src/app/interfaces/IFinding';
import { RecommendationsState } from 'src/app/states/recommendations.state';
import { FindingDetailsDialogComponent } from '../finding-details-dialog/finding-details-dialog.component';

/**
 * @title Table with expandable rows
 */
@Component({
  selector: 'app-result-table',
  templateUrl: './result-table.component.html',
  styleUrls: ['./result-table.component.scss'],
  animations: [
    trigger('detailExpand', [
      state('collapsed,void', style({ height: '0px', minHeight: '0' })),
      state('expanded', style({ height: '*' })),
      transition(
        'expanded <=> collapsed',
        animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')
      ),
    ]),
  ],
})
export class ResultTableComponent implements OnInit {
  @Select(RecommendationsState.vulnerabilityReport)
  vulnerabilityReport$!: Observable<any | null>;
  @Input() findings?: IFinding[];
  @Input() title: string = '';
  columnsToDisplay = ['title', 'severity', 'priority', 'source'];
  columnsToDisplayWithExpand = [...this.columnsToDisplay, 'expand'];
  expandedElement: IFinding | null | undefined;

  @ViewChild(MatPaginator, { static: true }) paginator!: MatPaginator;
  totalRecords: number = 0;
  dataSource: any;
  pageSizeOptions: number[] = [10, 20, 30];
  pageEvent!: PageEvent;

  constructor(public dialog: MatDialog) {}

  ngOnInit() {
    this.initFindings();
  }

  private initFindings(): void {
    console.log(this.findings);
    if (this.findings) {
      this.dataSource = new MatTableDataSource(this.findings);
      this.totalRecords = this.dataSource.data.length;
      this.dataSource.paginator = this.paginator;
    } else {
      this.vulnerabilityReport$
        .pipe(
          tap((vulnerabilityReport) => {
            this.dataSource = new MatTableDataSource(
              vulnerabilityReport.findings
            );
            this.totalRecords = this.dataSource.data.length;
            this.dataSource.paginator = this.paginator;
          })
        )
        .subscribe();
    }
  }

  public formatColumn(col: string): string {
    return col
      .replace(/([a-z])([A-Z])/g, '$1 $2') // Insert space before capital letters
      .split(' ') // Split the string into words
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize the first letter of each word
      .join(' ');
  }

  public openFindingDetails(finding: IFinding): void {
    const dialogRef = this.dialog.open(FindingDetailsDialogComponent, {
      height: '80vh',
      width: '90%',
      maxHeight: '80vh',
      data: finding,
    });

    dialogRef.afterClosed().pipe().subscribe();
  }
}