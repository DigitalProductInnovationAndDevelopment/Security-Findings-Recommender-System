import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment.prod';
import { IFinding } from '../interfaces/IFinding';

@Injectable({
  providedIn: 'root',
})
export class RecommendationsService {
  constructor(private readonly http: HttpClient) {}

  public checkConnection(): Observable<void> {
    return this.http.get<void>(environment.apiUrl + '/');
  }

  public uploadFindings(inputData: string): Observable<void> {
    return this.http.post<void>(environment.apiUrl + '/upload', inputData);
  }

  public getRecommendations(): Observable<IFinding[]> {
    return this.http.get<IFinding[]>(environment.apiUrl + '/recommendations');
  }
}