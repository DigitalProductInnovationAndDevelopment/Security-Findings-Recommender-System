import { Injectable } from "@angular/core";
import { Action, Selector, State, StateContext } from "@ngxs/store";
import { IFinding } from "../interfaces/IFinding";
import { RecommendationsService } from "../services/recommendations.service";
import { UploadFile } from "./recommendations.actions";

export interface RecommendationsStateModel {
    isLoading: boolean;
    hasError: boolean;
    selectedFile: File|null;
    findings: IFinding[];
}

@State<RecommendationsStateModel>({
    name: 'RecommendationsOverview',
    defaults: {
        isLoading: false,
        hasError: false,
        selectedFile: null,
        findings: []
    }
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
    static selectedFile(state: RecommendationsStateModel): File|null {
        return state.selectedFile;
    }

    @Selector()
    static findings(state: RecommendationsStateModel): IFinding[] {
        return state.findings;
    }

    @Action(UploadFile)
    uploadFile(context: StateContext<RecommendationsStateModel>, { payload }: UploadFile): void {
        context.patchState({selectedFile: payload.file});
        // this.recommendationService.
    }


}