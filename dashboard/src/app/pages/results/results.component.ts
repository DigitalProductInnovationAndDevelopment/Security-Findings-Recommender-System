import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Select } from '@ngxs/store';
import { Observable, take, tap } from 'rxjs';
import { RecommendationsState } from 'src/app/states/recommendations.state';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss'],
})
export class ResultsComponent implements OnInit {
  @Select(RecommendationsState.selectedFile)
  selectedFile$!: Observable<File | null>;
  @Select(RecommendationsState.findings) findings$!: Observable<any | null>;

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.initSelectedFile();
  }

  private initSelectedFile(): void {
    this.selectedFile$
      .pipe(
        take(1),
        tap((selectedFile) => !selectedFile && this.router.navigate(['home']))
      )
      .subscribe();
  }
}
