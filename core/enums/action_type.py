from django.db import models


class ActionType(models.TextChoices):
    """Standard action types for activity logging."""

    # Core CRUD operations
    CREATE = "create", "Create"
    UPDATE = "update", "Update"
    DELETE = "delete", "Delete"
    VIEW = "view", "View"

    # Authentication actions
    LOGIN = "login", "Login"
    LOGOUT = "logout", "Logout"

    # File operations
    UPLOAD = "upload", "Upload"
    DOWNLOAD = "download", "Download"

    # Status changes
    ACTIVATE = "activate", "Activate"
    DEACTIVATE = "deactivate", "Deactivate"
    PUBLISH = "publish", "Publish"
    UNPUBLISH = "unpublish", "Unpublish"

    # Approval workflow
    APPROVE = "approve", "Approve"
    REJECT = "reject", "Reject"
    SUBMIT = "submit", "Submit"

    # Communication
    SEND = "send", "Send"
    RECEIVE = "receive", "Receive"

    # Other common actions
    EXPORT = "export", "Export"
    IMPORT = "import", "Import"
    SEARCH = "search", "Search"
    FILTER = "filter", "Filter"