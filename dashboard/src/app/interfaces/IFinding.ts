export interface IFinding {
  findingTitle: string;
  description: string;
  priority: number;
  source: string;
  lastFound: string;
  recommendation?: string;
}