from functools import wraps
from typing import Callable, Any, List, Type, Union
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from core.authentication import JWTAuthentication
from utils.jwt import JsonWebToken


def jwt_required(view_func: Callable[..., Response]) -> Callable[..., Response]:
    """
    Decorator that enforces JWT authentication for a specific view method.
    Also integrates with OpenAPI schema generation to show Bearer auth requirements.

    Usage:
        @jwt_required
        @extend_schema(...)
        def put(self, request: Request, ...) -> Response:
            ...

    Args:
        view_func: The view method to be decorated

    Returns:
        The decorated view method with JWT authentication
    """
    @wraps(view_func)
    def wrapper(self: Any, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Authentication wrapper for the decorated view method."""
        user, token = _authenticate_request(request)

        # Set authenticated user and token on request
        request.user = user
        request.auth = token

        return view_func(self, request, *args, **kwargs)

    # Mark function for OpenAPI schema detection
    wrapper._jwt_required = True  # type: ignore

    return wrapper


def jwt_refresh_token_required(view_func: Callable[..., Response]) -> Callable[..., Response]:
    """
    Decorator that allows expired JWT tokens for refresh token endpoints.
    This decorator validates token format and user existence but allows expired tokens.

    Usage:
        @jwt_refresh_token_required
        @extend_schema(...)
        def post(self, request: Request, ...) -> Response:
            ...

    Args:
        view_func: The view method to be decorated

    Returns:
        The decorated view method with refresh token authentication
    """
    @wraps(view_func)
    def wrapper(self: Any, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Refresh token authentication wrapper for the decorated view method."""
        user, token = _authenticate_refresh_token_request(request)

        # Set authenticated user and token on request
        request.user = user
        request.auth = token

        return view_func(self, request, *args, **kwargs)

    # Mark function for OpenAPI schema detection
    wrapper._jwt_refresh_required = True  # type: ignore

    return wrapper


def jwt_role_required(
    allowed_roles: Union[str, List[str]]
) -> Callable[[Callable[..., Response]], Callable[..., Response]]:
    """
    Decorator that enforces JWT authentication with role-based access control.

    Usage:
        @jwt_role_required(['admin', 'manager'])
        @extend_schema(...)
        def delete(self, request: Request, ...) -> Response:
            ...

        @jwt_role_required('admin')
        @extend_schema(...)
        def post(self, request: Request, ...) -> Response:
            ...

    Args:
        allowed_roles: Single role string or list of role strings that are allowed access

    Returns:
        Decorator function that enforces role-based authentication
    """
    # Normalize to list
    if isinstance(allowed_roles, str):
        roles_list = [allowed_roles]
    else:
        roles_list = list(allowed_roles)

    def decorator(view_func: Callable[..., Response]) -> Callable[..., Response]:
        @wraps(view_func)
        def wrapper(self: Any, request: Request, *args: Any, **kwargs: Any) -> Response:
            """Role-based authentication wrapper for the decorated view method."""
            user, token = _authenticate_request(request)

            # Set authenticated user and token on request
            request.user = user
            request.auth = token

            # Check user role permissions
            _check_user_role_permissions(user, roles_list)

            return view_func(self, request, *args, **kwargs)

        # Mark function for OpenAPI schema detection
        wrapper._jwt_role_required = True  # type: ignore
        wrapper._required_roles = roles_list  # type: ignore

        return wrapper

    return decorator


def _authenticate_request(request: Request) -> tuple[Any, str]:
    """
    Authenticate the request using JWT authentication.

    Args:
        request: The HTTP request to authenticate

    Returns:
        Tuple of (user, token)

    Raises:
        AuthenticationFailed: If authentication fails
    """
    authenticator = JWTAuthentication()

    try:
        auth_result = authenticator.authenticate(request)
        if auth_result is None:
            raise AuthenticationFailed('Authentication credentials were not provided.')

        user, token = auth_result

        # Verify user is properly authenticated
        if not user or not getattr(user, 'is_authenticated', False):
            raise AuthenticationFailed('Invalid authentication.')

        return user, token

    except AuthenticationFailed:
        raise
    except Exception as exc:
        raise AuthenticationFailed(f'Authentication failed: {exc}') from exc


def _authenticate_refresh_token_request(request: Request) -> tuple[Any, str]:
    """
    Authenticate the request allowing expired JWT tokens for refresh operations.

    Args:
        request: The HTTP request to authenticate

    Returns:
        Tuple of (user, token)

    Raises:
        AuthenticationFailed: If authentication fails (excluding expiration)
    """
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise AuthenticationFailed('Authentication credentials were not provided.')

    try:
        _, token = auth_header.split(' ', 1)
        token = token.strip()
    except ValueError as e:
        raise AuthenticationFailed(
            'Invalid authorization header format. Expected: Bearer <token>'
        ) from e

    if not token:
        raise AuthenticationFailed('Token is required.')

    # Validate token structure and extract user (allow expired tokens)
    try:
        jwt_handler = JsonWebToken()

        # Try to decode without expiration validation first
        username = jwt_handler.get_subject(token, expiration=False)

        if not username:
            raise AuthenticationFailed('Token payload is invalid - missing username.')

        # Get user from database
        from core.models import User
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as exc:
            raise AuthenticationFailed('User not found.') from exc

        return user, token

    except AuthenticationFailed:
        raise
    except Exception as exc:
        raise AuthenticationFailed(f'Token validation failed: {exc}') from exc


def _check_user_role_permissions(user: Any, required_roles: List[str]) -> None:
    """
    Check if user has any of the required roles.

    Args:
        user: The authenticated user object
        required_roles: List of roles that are allowed access

    Raises:
        PermissionDenied: If user doesn't have required role permissions
    """
    if not required_roles:
        return  # No role restrictions

    # Get user role - assuming user has a 'role' attribute
    user_role = getattr(user, 'role', None)

    if not user_role:
        raise PermissionDenied('User role is not defined.')

    # Check if user role is in the allowed roles
    # Handle both string role and role object with 'name' attribute
    if hasattr(user_role, 'name'):
        user_role_name = user_role.name
    elif hasattr(user_role, 'value'):
        user_role_name = user_role.value
    else:
        user_role_name = str(user_role)

    if user_role_name not in required_roles:
        raise PermissionDenied(
            f'Access denied. Required roles: {", ".join(required_roles)}. '
            f'User role: {user_role_name}'
        )


def get_method_authentication_classes(
    view: Any,
    method_name: str
) -> List[Type[BaseAuthentication]]:
    """
    Determine authentication classes for a specific view method.
    Used by DRF Spectacular for OpenAPI schema generation.

    Args:
        view: The view instance
        method_name: Name of the method to check

    Returns:
        List of authentication classes required for the method
    """
    method = getattr(view, method_name, None)
    if method and (
        getattr(method, '_jwt_required', False) or
        getattr(method, '_jwt_refresh_required', False) or
        getattr(method, '_jwt_role_required', False)
    ):
        return [JWTAuthentication]
    return []


def get_method_permission_classes(
    view: Any,
    method_name: str
) -> List[Type[BasePermission]]:
    """
    Determine permission classes for a specific view method.
    Used by DRF Spectacular for OpenAPI schema generation.

    Args:
        view: The view instance
        method_name: Name of the method to check

    Returns:
        List of permission classes required for the method
    """
    method = getattr(view, method_name, None)
    if method and (
        getattr(method, '_jwt_required', False) or
        getattr(method, '_jwt_refresh_required', False) or
        getattr(method, '_jwt_role_required', False)
    ):
        return [IsAuthenticated]
    return []