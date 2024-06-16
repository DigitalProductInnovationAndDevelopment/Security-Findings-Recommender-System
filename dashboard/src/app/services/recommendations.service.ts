import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, Observable, of } from 'rxjs';
import { environment } from 'src/environments/environment.prod';
import { ReceivedRecommendations } from './../pages/results/results.component';

@Injectable({
  providedIn: 'root',
})
export class RecommendationsService {
  constructor(private readonly http: HttpClient) {}

  public checkConnection(): Observable<void> {
    return this.http.get<void>(environment.apiUrl + '/');
  }

  public uploadFindings(inputData: string): Observable<number> {
    return this.http
      .post<number>(environment.apiUrl + '/upload', {
        data: inputData,
        user_id: 1,
      })
      .pipe(
        catchError((error: HttpErrorResponse) => {
          if (
            error.status === 400 &&
            error.error.detail ===
              'Recommendation task already exists for today'
          ) {
            return new Observable<number>((observer) => {
              observer.next(100);
              observer.complete();
            });
          } else {
            return of(-1);
          }
        })
      );
  }

  public getRecommendations(): Observable<ReceivedRecommendations> {
    return this.http.post<ReceivedRecommendations>(
      environment.apiUrl + '/recommendations',
      {
        user_id: 1,
        pagination: {
          offset: 0,
          limit: 1,
        },
        filter: {
          date: '',
          location: '',
          severity: '',
          cve_id: '',
          source: '',
        },
      }
    );
  }

  public getUploadStatus(): Observable<{ status: string }> {
    return this.http.get<{ status: string }>(environment.apiUrl + '/status');
  }
}
