import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import {
  filter,
  finalize,
  interval,
  map,
  Observable,
  switchMap,
  takeWhile,
  tap,
} from 'rxjs';
import { IFinding } from 'src/app/interfaces/IFinding';
import { RecommendationsService } from '../services/recommendations.service';
import {
  clearFindings,
  loadRecommendations,
  setInformation,
  UploadFile,
} from './recommendations.actions';

export interface RecommendationsStateModel {
  isLoading: boolean;
  hasError: boolean;
  findings: IFinding[];
  fileName: string | undefined;
  exampleProcess: boolean;
}

@State<RecommendationsStateModel>({
  name: 'RecommendationsOverview',
  defaults: {
    isLoading: false,
    hasError: false,
    findings: [],
    fileName: undefined,
    exampleProcess: false,
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
  static fileName(state: RecommendationsStateModel): string | undefined {
    return state.fileName;
  }

  @Selector()
  static findings(state: RecommendationsStateModel): IFinding[] {
    return state.findings;
  }
  @Selector()
  static exampleProcess(state: RecommendationsStateModel): boolean {
    return state.exampleProcess;
  }

  @Action(setInformation)
  setFindings(
    context: StateContext<RecommendationsStateModel>,
    { payload }: setInformation
  ): void {
    context.patchState({
      ...(payload.data && { findings: payload.data }),
      ...(payload.fileName && { fileName: payload.fileName }),
      ...(payload.exampleProcess && { exampleProcess: payload.exampleProcess }),
    });
  }

  @Action(UploadFile)
  uploadFile(
    context: StateContext<RecommendationsStateModel>,
    { payload }: UploadFile
  ): Observable<number> {
    console.log(payload.filter);
    return this.recommendationService
      .uploadFindings(payload.data, payload.filter)
      .pipe(
        filter((response) => response !== -1),
        map((response) => response),
        finalize(() => void context.patchState({ isLoading: false }))
      );
  }

  @Action(clearFindings)
  clearFindings(context: StateContext<RecommendationsStateModel>): void {
    context.patchState({
      findings: [],
      fileName: undefined,
      exampleProcess: false,
    });
  }

  @Action(loadRecommendations)
  loadRecommendations(context: StateContext<RecommendationsStateModel>): void {
    interval(10000)
      .pipe(
        switchMap(() => this.recommendationService.getUploadStatus()),
        takeWhile((response) => response.status !== 'completed', true),
        filter((response) => response.status === 'completed'),
        switchMap(() => this.recommendationService.getRecommendations()),
        tap((findings) => context.patchState({ findings: findings.items }))
      )
      .subscribe();
  }
}

