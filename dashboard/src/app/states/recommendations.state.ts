import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { catchError, finalize, Observable, tap } from 'rxjs';
import { IFinding } from 'src/app/interfaces/IFinding';
import { RecommendationsService } from '../services/recommendations.service';
import { UploadFile } from './recommendations.actions';

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

  @Action(UploadFile)
  uploadFile(
    context: StateContext<RecommendationsStateModel>,
    { payload }: UploadFile
  ): void {
    const findings = payload.data.message.content.map((finding: any) => ({
      findingTitle: finding.title_list[0].element,
      description:
        finding?.description_list && !!finding.description_list.length
          ? finding.description_list[0].element
          : null,
      priority: finding.priority,
      source: finding.title_list[0].source,
      lastFound: finding.last_found,
    }));

    this.recommendationService
      .uploadFindings(payload.data.message.content)
      .pipe(
        catchError<void, Observable<never>>((error) => {
          context.patchState({ hasError: true });
          throw error;
        }),
        tap(() => {
          void context.patchState({ findings, fileName: payload.fileName });
        }),
        finalize(() => void context.patchState({ isLoading: false }))
      )
      .subscribe();

    // context.patchState({
    //   findings,
    //   fileName: payload.fileName,
    // });
  }
}
