from typing import Dict, Any, List, Optional
from drf_spectacular.openapi import AutoSchema


class CustomAutoSchema(AutoSchema):
    """
    Enhanced AutoSchema that automatically detects @jwt_required decorator
    and configures Bearer authentication requirements in OpenAPI schema.
    """

    def get_operation(
        self,
        path: str,
        path_regex: str,
        path_prefix: str,
        method: str,
        registry: Any
    ) -> Optional[Dict[str, Any]]:
        """
        Generate OpenAPI operation schema with automatic JWT detection.

        Args:
            path: The API path
            path_regex: The regex pattern for the path
            path_prefix: The path prefix
            method: HTTP method (GET, POST, etc.)
            registry: Component registry for schema generation

        Returns:
            OpenAPI operation dictionary or None
        """
        operation = super().get_operation(path, path_regex, path_prefix, method, registry)

        if not isinstance(operation, dict):
            return operation

        # Check for JWT authentication requirement
        if self._requires_jwt_auth(method):
            self._add_bearer_auth_security(operation)

        return operation

    def _requires_jwt_auth(self, method: str) -> bool:
        """
        Check if the view method requires JWT authentication.

        Args:
            method: HTTP method name

        Returns:
            True if JWT authentication is required
        """
        view_method = getattr(self.view, method.lower(), None)
        return (
            view_method is not None and (
                getattr(view_method, '_jwt_required', False) or
                getattr(view_method, '_jwt_refresh_required', False) or
                getattr(view_method, '_jwt_role_required', False)
            )
        )

    def _add_bearer_auth_security(self, operation: Dict[str, Any]) -> None:
        """
        Add Bearer authentication security requirement to operation.

        Args:
            operation: The OpenAPI operation dictionary to modify
        """
        if 'security' not in operation:
            operation['security'] = []

        bearer_auth_requirement = {"BearerAuth": []}
        security_list: List[Dict[str, List[str]]] = operation['security']

        if bearer_auth_requirement not in security_list:
            security_list.append(bearer_auth_requirement)