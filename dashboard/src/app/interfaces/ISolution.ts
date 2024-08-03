import { IFinding } from './IFinding';

export interface ISolution {
  short_description: string;
  long_description: string;
  search_terms: string[];
}

export interface IAggregatedSolution {
  findings: IFinding[];
  solution: string;
  metadata: {
    reason: string;
  };
}
