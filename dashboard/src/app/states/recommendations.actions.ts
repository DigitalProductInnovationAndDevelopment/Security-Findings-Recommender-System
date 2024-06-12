

export class UploadFile {
  static readonly type = '[File] Upload File';

  constructor(
    public readonly payload: {
      data: any;
      fileName: string;
    }
  ) {}
}

export class setFindings {
  static readonly type = '[Findings] set Findings';

  constructor(
    public readonly payload: {
      data: any;
      fileName?: string;
    }
  ) {}
}
