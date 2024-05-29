import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { IFinding } from "../interfaces/IFinding";

@Injectable({
    providedIn: 'root'
})

export class RecommendationsService {
    constructor(private readonly http: HttpClient) {}

    public getRecommendations(file: File): Observable<IFinding[]> {
        
        return this.http.post<IFinding[]>('', file).pipe();
    }
}