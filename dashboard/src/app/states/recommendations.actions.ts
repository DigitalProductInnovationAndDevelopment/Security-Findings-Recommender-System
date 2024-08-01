export class UploadFile {
  static readonly type = '[File] Upload File';

  constructor(
    public readonly payload: {
      data: any;
      filter?: any;
    }
  ) {}
}

export class setInformation {
  static readonly type = '[Findings] set Findings';

  constructor(
    public readonly payload: {
      data?: any;
      fileName?: string;
      exampleProcess?: boolean;
    }
  ) {}
}

export class clearFindings {
  static readonly type = '[] clear Findings';
}

export class loadRecommendations {
  static readonly type = '[] load recommendations';

  constructor(
    public readonly payload: {
      severity?: { minValue: number; maxValue: number };
    }
  ) {}
}

export class filterRecs {
  static readonly type = '[severity] filter recommendations';

  constructor(
    public readonly payload: {
      severity: { minValue: number; maxValue: number };
    }
  ) {}
}
