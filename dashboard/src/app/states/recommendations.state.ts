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
  filterRecs,
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
  taskId: number | undefined;
}

@State<RecommendationsStateModel>({
  name: 'RecommendationsOverview',
  defaults: {
    isLoading: false,
    hasError: false,
    findings: [],
    fileName: undefined,
    exampleProcess: false,
    taskId: undefined,
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
    return this.recommendationService
      .uploadFindings(payload.data, payload.filter)
      .pipe(
        filter((response) => response.task_id !== -1),
        tap((response) => context.patchState({ taskId: response.task_id })),
        map((response) => response.task_id),
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
  loadRecommendations(
    context: StateContext<RecommendationsStateModel>,
    { payload }: loadRecommendations
  ): void {
    const taskId = context.getState().taskId;
    if (typeof taskId === 'number') {
      interval(10000)
        .pipe(
          filter(() => taskId !== undefined),
          switchMap(() => this.recommendationService.getUploadStatus(taskId)),
          takeWhile((response) => response.status !== 'completed', true),
          filter((response) => response.status === 'completed'),
          switchMap(() =>
            this.recommendationService.getRecommendations(
              taskId,
              payload.severity
            )
          ),
          tap((findings) => context.patchState({ findings: findings.items }))
        )
        .subscribe();
    }
  }
  @Action(filterRecs)
  filterRecs(
    context: StateContext<RecommendationsStateModel>,
    { payload }: filterRecs
  ) {
    let findings = context.getState().findings;
    findings = findings.filter(
      (finding) =>
        finding.severity >= payload.severity[0] &&
        finding.severity <= payload.severity[1]
    );
    context.patchState({ findings });
  }
}
