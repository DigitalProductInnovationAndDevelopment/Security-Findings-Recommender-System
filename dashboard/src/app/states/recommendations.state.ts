import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { catchError, finalize, Observable, tap } from 'rxjs';
import { IFinding } from 'src/app/interfaces/IFinding';
import { RecommendationsService } from '../services/recommendations.service';
import { setFindings, UploadFile } from './recommendations.actions';

export interface RecommendationsStateModel {
  isLoading: boolean;
  hasError: boolean;
  findings: IFinding[];
  fileName: string;
}

@State<RecommendationsStateModel>({
  name: 'RecommendationsOverview',
  defaults: {
    isLoading: false,
    hasError: false,
    findings: [],
    fileName: '',
  },
})
@Injectable()
export class RecommendationsState {
  constructor(private readonly recommendationService: RecommendationsService) {}

  @Selector()
  static isLoading(state: RecommendationsStateModel): boolean {
    return state.isLoading;
  }

  @Selector()
  static hasError(state: RecommendationsStateModel): boolean {
    return state.hasError;
  }

  @Selector()
  static fileName(state: RecommendationsStateModel): string {
    return state.fileName;
  }

  @Selector()
  static findings(state: RecommendationsStateModel): IFinding[] {
    return state.findings;
  }

  @Action(setFindings)
  setFindings(
    context: StateContext<RecommendationsStateModel>,
    { payload }: setFindings
  ): void {
    context.patchState({
      findings: payload.data,
      fileName: (payload.fileName = 'example.json'),
    });
  }

  @Action(UploadFile)
  uploadFile(
    context: StateContext<RecommendationsStateModel>,
    { payload }: UploadFile
  ): Observable<void> {
    return this.recommendationService.uploadFindings(payload.data).pipe(
      catchError<void, Observable<never>>((error) => {
        context.patchState({ hasError: true });
        throw error;
      }),
      tap(() => {
        void context.patchState({
          fileName: payload.fileName,
        });
      }),
      finalize(() => void context.patchState({ isLoading: false }))
    );
  }
}
