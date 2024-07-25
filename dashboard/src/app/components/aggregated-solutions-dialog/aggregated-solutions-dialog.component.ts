import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { marked } from 'marked';
import { IAggregatedSolution } from 'src/app/interfaces/ISolution';
@Component({
  selector: 'app-aggregated-solutions-dialog',
  templateUrl: './aggregated-solutions-dialog.component.html',
  styleUrl: './aggregated-solutions-dialog.component.scss',
})
export class AggregatedSolutionsDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<AggregatedSolutionsDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: IAggregatedSolution
  ) {}

  closeDialog(): void {
    this.dialogRef.close();
  }

  convertMarkdown(text: string) {
    return marked(text);
  }
}
