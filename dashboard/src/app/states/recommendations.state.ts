import { Injectable } from '@angular/core';
import { Action, Selector, State, StateContext } from '@ngxs/store';
import { IFinding } from 'src/app/interfaces/IFinding';
import { RecommendationsService } from '../services/recommendations.service';
import { UploadFile } from './recommendations.actions';

export interface RecommendationsStateModel {
  isLoading: boolean;
  hasError: boolean;
  selectedFile: any | null;
  findings: IFinding[];
}

@State<RecommendationsStateModel>({
  name: 'RecommendationsOverview',
  defaults: {
    isLoading: false,
    hasError: false,
    selectedFile: null,
    findings: [],
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
  static selectedFile(state: RecommendationsStateModel): File | null {
    return state.selectedFile;
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
    const findings = payload.file.message.content.map((finding: any) => ({
      findingTitle: finding.title_list[0].element,
      description:
        finding?.description_list && finding.description_list.length > 0
          ? finding.description_list[0].element
          : null,
      priority: finding.priority,
      source: finding.title_list[0].source,
      lastFound: finding.last_found,
    }));

    context.patchState({
      selectedFile: payload.file,
      findings,
    });
  }
}
