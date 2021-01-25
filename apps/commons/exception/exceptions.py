class FileImportError(Exception):
    """
        File import failure
    """

    def __init__(self, message="File import failed."):
        self.message = message
        super().__init__(self.message)