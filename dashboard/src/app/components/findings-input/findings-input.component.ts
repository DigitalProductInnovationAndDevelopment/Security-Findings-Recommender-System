import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngxs/store';
import { take, tap } from 'rxjs';
import { UploadFile } from 'src/app/states/recommendations.actions';

@Component({
  selector: 'app-findings-input',
  templateUrl: './findings-input.component.html',
  styleUrls: ['./findings-input.component.scss'],
})
export class FindingsInputComponent {
  constructor(private readonly store: Store, private router: Router) {}
  uploadFile(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        const jsonData = JSON.parse(reader.result as string);
        this.store
          .dispatch(new UploadFile({ data: jsonData, fileName: file.name }))
          .pipe(
            take(1),
            tap(() => this.router.navigate(['results']))
          )
          .subscribe();
      };
      reader.readAsText(file);
    }
  }
}
