export enum ISolutionCategory {
  'USER' = 'User',
  'SYSTEM' = 'System',
  'CODE' = 'Code',
  'DEFAULT' = 'Default',
}

export interface ISolution {
  short_description: string;
  long_description: string;
  search_terms: string[];
}
