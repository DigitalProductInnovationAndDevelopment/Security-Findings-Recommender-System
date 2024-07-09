import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { Store } from '@ngxs/store';
import { filter, switchMap, take, tap } from 'rxjs';
import {
  setInformation,
  UploadFile,
} from 'src/app/states/recommendations.actions';
import { FindingsInputFilterDialogComponent } from '../findings-input-filter-dialog/findings-input-filter-dialog.component';

@Component({
  selector: 'app-findings-input',
  templateUrl: './findings-input.component.html',
  styleUrls: ['./findings-input.component.scss'],
})
export class FindingsInputComponent {
  constructor(
    private readonly store: Store,
    private router: Router,
    private dialog: MatDialog
  ) {}
  uploadFile(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        const jsonData = JSON.parse(reader.result as string);
        this.store
          .dispatch([
            new setInformation({
              fileName: file.name,
              exampleProcess: false,
            }),
            // new UploadFile({ data: jsonData }),
          ])
          .pipe(
            take(1),
            switchMap(() => {
              const dialogRef = this.dialog.open(
                FindingsInputFilterDialogComponent,
                {
                  height: '80vh',
                  width: '50%',
                  maxHeight: '80vh',
                }
              );

              return dialogRef.afterClosed();
            }),
            filter((response) => !!response),
            switchMap((response) => {
              return this.store
                .dispatch(new UploadFile({ data: jsonData, filter: response }))
                .pipe(take(1));
            }),
            filter((response) => !!response),
            tap(() => this.router.navigate(['results']))
          )
          .subscribe();
      };
      reader.readAsText(file);
    }
  }
}
