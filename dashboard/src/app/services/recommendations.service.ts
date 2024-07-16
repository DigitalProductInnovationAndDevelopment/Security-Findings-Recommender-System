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

  public uploadFindings(
    inputData: string,
    filter: any
  ): Observable<{ task_id: number }> {
    return this.http
      .post<any>(environment.apiUrl + '/upload', {
        data: inputData,
        user_id: 1,
        filter,
      })
      .pipe(
        catchError((error: HttpErrorResponse) => {
          if (
            error.status === 400 &&
            error.error.detail ===
              'Recommendation task already exists for today'
          ) {
            return new Observable<{ task_id: number }>((observer) => {
              observer.next({ task_id: 100 });
              observer.complete();
            });
          } else {
            return of({ task_id: -1 });
          }
        })
      );
  }

  public getRecommendations(
    taskId?: number,
    severity?: number[]
  ): Observable<ReceivedRecommendations> {
    const body: any = {};
    if (taskId !== undefined) {
      body.taskId = taskId;
    }
    if (severity !== undefined) {
      body.severity = severity;
    }

    return this.http.post<ReceivedRecommendations>(
      environment.apiUrl + '/recommendations',
      body
    );
  }

  public getUploadStatus(taskId: number): Observable<{ status: string }> {
    return this.http.get<{ status: string }>(
      environment.apiUrl + `/tasks/${taskId}/status`
    );
  }
}
