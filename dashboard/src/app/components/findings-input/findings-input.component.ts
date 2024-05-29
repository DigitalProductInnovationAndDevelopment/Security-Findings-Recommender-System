import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Store } from '@ngxs/store';
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
      this.store.dispatch(new UploadFile({file: input.files[0]}));
      this.router.navigate(['results'])
    }
  }
}
