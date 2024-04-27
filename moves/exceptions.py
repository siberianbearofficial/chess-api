from utils.exceptions import NotFoundError


class MoveNotFoundError(NotFoundError):
    def __str__(self):
        return 'Move not found.'


class ReadMoveDenied(PermissionError):
    def __str__(self):
        return 'Author does not have read_moves permission.'


class InsertMoveDenied(PermissionError):
    def __str__(self):
        return 'Author does not have insert_moves permission.'


class UpdateMoveDenied(PermissionError):
    def __str__(self):
        return 'Author does not have update_moves permission.'


class DeleteMoveDenied(PermissionError):
    def __str__(self):
        return 'Author does not have delete_moves permission.'


class IllegalMoveDenied(PermissionError):
    def __str__(self):
        return 'Illegal move. Consider trying another one.'
