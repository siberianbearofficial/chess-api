from utils.exceptions import NotFoundError


class InvitationNotFoundError(NotFoundError):
    def __str__(self):
        return 'Invitation not found.'


class ReadInvitationDenied(PermissionError):
    def __str__(self):
        return 'Author does not have read_invitations permission.'


class InsertInvitationDenied(PermissionError):
    def __str__(self):
        return 'Author does not have insert_invitations permission.'


class UpdateInvitationDenied(PermissionError):
    def __str__(self):
        return 'Author does not have update_invitations permission.'


class DeleteInvitationDenied(PermissionError):
    def __str__(self):
        return 'Author does not have delete_invitations permission.'
