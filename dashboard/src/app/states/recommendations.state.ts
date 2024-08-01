import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import {
  filter,
  finalize,
  interval,
  lastValueFrom,
  map,
  Observable,
  switchMap,
  takeWhile,
  tap,
} from 'rxjs';
import { IFinding } from 'src/app/interfaces/IFinding';
import { RecommendationsService } from '../services/recommendations.service';
import { IAggregatedSolution } from './../interfaces/ISolution';
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
  vulnerabilityReport: {
    findings: IFinding[];
    aggregated_solutions: IAggregatedSolution[];
  };
  fileName: string | undefined;
  exampleProcess: boolean;
  taskId: number | undefined;
}

@State<RecommendationsStateModel>({
  name: 'RecommendationsOverview',
  defaults: {
    isLoading: false,
    hasError: false,
    vulnerabilityReport: {
      findings: [],
      aggregated_solutions: [],
    },
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
  static vulnerabilityReport(state: RecommendationsStateModel): {
    findings: IFinding[];
    aggregated_solutions: IAggregatedSolution[];
  } {
    return state.vulnerabilityReport;
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
    payload.data.aggregataed_solutions = payload.data.aggregated_solutions.sort(
      (a: IAggregatedSolution, b: IAggregatedSolution) =>
        b.findings.length - a.findings.length
    );
    context.patchState({
      ...(payload.data && { vulnerabilityReport: payload.data }),
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
      vulnerabilityReport: { findings: [], aggregated_solutions: [] },
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
          tap((findings) =>
            context.patchState({ vulnerabilityReport: findings.items })
          )
        )
        .subscribe();
    }
  }
  @Action(filterRecs)
  async filterRecs(
    context: StateContext<RecommendationsStateModel>,
    { payload }: filterRecs
  ) {
    const exampleProcess = context.getState().exampleProcess;
    let vulnerabilityReport = context.getState().vulnerabilityReport;
    let findings;
    console.log(exampleProcess);
    console.log(vulnerabilityReport);
    if (exampleProcess) {
      const aiModel = context.getState().fileName?.split('.json')[0] || '';
      vulnerabilityReport = await lastValueFrom(
        this.recommendationService.getExampleData(aiModel)
      );
      findings = vulnerabilityReport.findings.filter(
        (f) =>
          f.severity >= payload.severity.minValue &&
          f.severity <= payload.severity.maxValue
      );
      const aggregated_solutions =
        vulnerabilityReport.aggregated_solutions.sort(
          (a: IAggregatedSolution, b: IAggregatedSolution) =>
            b.findings.length - a.findings.length
        );
      vulnerabilityReport = { findings, aggregated_solutions };
      context.patchState({ vulnerabilityReport });
    } else {
      const taskId = context.getState().taskId;
      const severity = payload.severity;
      const recommendations = await lastValueFrom(
        this.recommendationService.getRecommendations(taskId, severity)
      );
      vulnerabilityReport = recommendations.items;
      const aggregated_solutions =
        vulnerabilityReport.aggregated_solutions.sort(
          (a: IAggregatedSolution, b: IAggregatedSolution) =>
            b.findings.length - a.findings.length
        );
      vulnerabilityReport = { ...vulnerabilityReport, aggregated_solutions };
      context.patchState({ vulnerabilityReport });
    }
  }
}
