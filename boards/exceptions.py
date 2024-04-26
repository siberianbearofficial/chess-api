from utils.exceptions import NotFoundError


class BoardNotFoundError(NotFoundError):
    def __str__(self):
        return 'Board not found.'


class ReadBoardDenied(PermissionError):
    def __str__(self):
        return 'Author does not have read_boards permission.'


class InsertBoardDenied(PermissionError):
    def __str__(self):
        return 'Author does not have insert_boards permission.'


class UpdateBoardDenied(PermissionError):
    def __str__(self):
        return 'Author does not have update_boards permission.'


class DeleteBoardDenied(PermissionError):
    def __str__(self):
        return 'Author does not have delete_boards permission.'
