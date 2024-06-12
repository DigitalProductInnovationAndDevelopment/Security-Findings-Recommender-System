import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { marked } from 'marked';
import { IFinding } from 'src/app/interfaces/IFinding';

@Component({
  selector: 'app-finding-details-dialog',
  templateUrl: './finding-details-dialog.component.html',
  styleUrl: './finding-details-dialog.component.scss',
})
export class FindingDetailsDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<FindingDetailsDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: IFinding
  ) {}

  closeDialog(): void {
    this.dialogRef.close();
  }

  convertMarkdown(text: string) {
    return marked(text);
  }
}
