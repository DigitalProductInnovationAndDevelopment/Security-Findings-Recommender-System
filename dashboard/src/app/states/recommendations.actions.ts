

export class UploadFile {
    static readonly type = '[File] Upload File';

    constructor(
        public readonly payload: {
            file: File;
        }
    ) {}

}