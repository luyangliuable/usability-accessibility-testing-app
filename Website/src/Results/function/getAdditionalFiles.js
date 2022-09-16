export function getAdditionalFiles(objectState) {
    const additionalFiles = {};

    objectState.algorithmsInfo.forEach(file => {
        if ( file.additionalFiles.length  > 0 ) {
            additionalFiles[file.uuid] = {
                file: file.additionalFiles,
                type: Object.keys(file.additionalInputFileTypes),
                algorithm: file.uuid,
            };
        }
    });

    return additionalFiles;
};
