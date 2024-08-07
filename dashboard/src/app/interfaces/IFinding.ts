import { ICategory } from './ICategory';
import { ISolution } from './ISolution';
export interface IFinding {
  title: string;
  source: string[];
  description: string;
  cwe_ids: string[];
  cve_ids: string[];
  severity: number;
  priority: number;
  category: ICategory;
  solution: ISolution;
}
