"""
Django Management Command: Application Health Check

Provides comprehensive health verification for Django applications including
database connectivity, migration status, and system readiness checks.

Usage:
    python manage.py health_check [--database=<alias>] [--quiet]
"""

import sys
from io import StringIO
from typing import Any, Dict

from django.core.management.base import BaseCommand, CommandParser
from django.db import connections
from django.db.utils import OperationalError
from django.core.management import execute_from_command_line


class Command(BaseCommand):
    """Django management command for comprehensive application health verification.

    Performs essential health checks including:
    - Database connectivity verification
    - Migration status analysis
    - System readiness validation
    """

    help = "Comprehensive health check for Django application"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add command line arguments for health check configuration."""
        parser.add_argument(
            "--database",
            type=str,
            default="default",
            help="Database alias to check (default: default)",
        )
        parser.add_argument(
            "--quiet",
            action="store_true",
            help="Run in quiet mode without detailed output",
        )

    def handle(self, *args: Any, **options: Dict[str, Any]) -> int:
        """Execute comprehensive health check for Django application."""
        database = str(options["database"])
        quiet = bool(options["quiet"])

        self._log_message("Performing health check...", quiet)

        # Execute health verification checks
        self._check_database_connection(database, quiet)
        self._check_migrations_status(quiet)

        self._log_success_message("Health check completed successfully!", quiet)
        return 0

    def _check_database_connection(self, database: str, quiet: bool) -> None:
        """Verify database connection availability and accessibility.

        Args:
            database: Database alias to test connection
            quiet: Whether to suppress output messages

        Raises:
            SystemExit: If database connection fails
        """
        try:
            with connections[database].cursor():
                pass  # Connection test successful
            self._log_success_message(f'✓ Database "{database}" connection OK', quiet)
        except OperationalError as e:
            self._log_error_and_exit(
                f'✗ Database "{database}" connection failed: {e}', quiet
            )
        except Exception as e:
            self._log_error_and_exit(f"✗ Unexpected database error: {e}", quiet)

    def _check_migrations_status(self, quiet: bool) -> None:
        """Verify migration status and detect unapplied migrations.

        Args:
            quiet: Whether to suppress output messages
        """
        try:
            migration_output = self._capture_migration_output()
            self._report_migration_status(migration_output, quiet)
        except Exception as e:
            self._log_warning_message(f"⚠ Could not check migrations: {e}", quiet)

    def _capture_migration_output(self) -> str:
        """Capture showmigrations command output safely.

        Returns:
            Migration status output as string
        """
        original_stdout = sys.stdout
        captured_output = StringIO()

        try:
            sys.stdout = captured_output
            execute_from_command_line(["manage.py", "showmigrations", "--plan"])
        finally:
            sys.stdout = original_stdout

        return captured_output.getvalue()

    def _report_migration_status(self, output: str, quiet: bool) -> None:
        """Analyze and report migration status from command output.

        Args:
            output: Output from showmigrations command
            quiet: Whether to suppress output messages
        """
        if self._has_unapplied_migrations(output):
            self._log_warning_message("⚠ Unapplied migrations detected", quiet)
        else:
            self._log_success_message("✓ All migrations applied", quiet)

    def _has_unapplied_migrations(self, output: str) -> bool:
        """Check if there are unapplied migrations in the output.

        Args:
            output: Migration status output

        Returns:
            True if unapplied migrations exist, False otherwise
        """
        return "[ ]" in output

    def _log_message(self, message: str, quiet: bool) -> None:
        """Log a standard message if not in quiet mode."""
        if not quiet:
            self.stdout.write(message)

    def _log_success_message(self, message: str, quiet: bool) -> None:
        """Log a success message with appropriate styling."""
        if not quiet:
            self.stdout.write(self.style.SUCCESS(message))

    def _log_warning_message(self, message: str, quiet: bool) -> None:
        """Log a warning message with appropriate styling."""
        if not quiet:
            self.stdout.write(self.style.WARNING(message))

    def _log_error_and_exit(self, message: str, quiet: bool) -> None:
        """Log an error message and terminate the process."""
        if not quiet:
            self.stdout.write(self.style.ERROR(message))
        sys.exit(1)
