#!/bin/bash

# SonarQube Analysis Runner for Essenza Django Backend
# This script helps run SonarQube analysis with proper configuration

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if SonarQube Scanner is installed
check_sonar_scanner() {
    if ! command -v sonar-scanner &> /dev/null; then
        print_error "SonarQube Scanner not found!"
        print_status "Please install SonarQube Scanner:"
        echo "  macOS: brew install sonar-scanner"
        echo "  Linux: apt-get install sonar-scanner"
        echo "  Or download from: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/"
        exit 1
    fi
    print_success "SonarQube Scanner found"
}

# Check if sonar-project.properties exists
check_config() {
    if [ ! -f "sonar-project.properties" ]; then
        print_error "sonar-project.properties not found in current directory"
        exit 1
    fi
    print_success "Configuration file found"
}

# Validate environment variables
check_environment() {
    if [ -z "$SONAR_HOST_URL" ]; then
        print_warning "SONAR_HOST_URL not set. Using default: http://localhost:9000"
        export SONAR_HOST_URL="http://localhost:9000"
    fi

    if [ -z "$SONAR_TOKEN" ]; then
        print_warning "SONAR_TOKEN not set. You may need to provide authentication."
        read -p "Do you want to continue without token? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Please set SONAR_TOKEN environment variable"
            echo "export SONAR_TOKEN=your_sonar_token"
            exit 1
        fi
    else
        print_success "SonarQube token configured"
    fi
}

# Clean previous analysis data
clean_analysis() {
    if [ -d ".scannerwork" ]; then
        print_status "Cleaning previous analysis data..."
        rm -rf .scannerwork
        print_success "Cleanup completed"
    fi
}

# Run pre-analysis security checks
security_check() {
    print_status "Running pre-analysis security checks..."

    # Check for potential hardcoded secrets
    if grep -r "SECRET_KEY.*=" --include="*.py" . | grep -v "os.getenv\|environ\|settings" > /dev/null 2>&1; then
        print_warning "Potential hardcoded SECRET_KEY found. Please review your code."
    fi

    # Check for DEBUG = True
    if grep -r "DEBUG.*=.*True" --include="*.py" . > /dev/null 2>&1; then
        print_warning "DEBUG=True found. Make sure this is disabled in production."
    fi

    # Check for ALLOWED_HOSTS = ['*']
    if grep -r "ALLOWED_HOSTS.*=.*\[\s*\"\*\"\s*\]" --include="*.py" . > /dev/null 2>&1; then
        print_warning "ALLOWED_HOSTS=['*'] found. This should be restricted in production."
    fi

    print_success "Security checks completed"
}

# Run SonarQube analysis
run_analysis() {
    print_status "Starting SonarQube analysis..."
    print_status "This may take a few minutes depending on project size..."

    # Run the analysis
    if sonar-scanner \
        -Dsonar.host.url="$SONAR_HOST_URL" \
        ${SONAR_TOKEN:+-Dsonar.login="$SONAR_TOKEN"} \
        -Dsonar.projectBaseDir=. \
        -Dsonar.verbose=false; then

        print_success "SonarQube scanner executed successfully!"
        print_status "View results at: $SONAR_HOST_URL/dashboard?id=essenza-web-backend"

        # Now check actual issues from SonarQube
        check_sonar_issues
    else
        print_error "SonarQube analysis failed!"
        exit 1
    fi
}

# Check SonarQube issues via API
check_sonar_issues() {
    print_status "Checking for code quality issues..."

    # Get project issues from SonarQube API
    local api_url="${SONAR_HOST_URL}/api/issues/search?componentKeys=essenza-web-backend&statuses=OPEN"

    if command -v curl &> /dev/null; then
        # Use curl to get issues
        local response
        if [ -n "$SONAR_TOKEN" ]; then
            response=$(curl -s -u "$SONAR_TOKEN:" "$api_url" 2>/dev/null)
        else
            response=$(curl -s "$api_url" 2>/dev/null)
        fi

        # Parse JSON response to count issues
        if command -v python3 &> /dev/null; then
            local issue_count
            issue_count=$(echo "$response" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    issues = data.get('issues', [])
    total = data.get('total', len(issues))

    # Count issues by severity
    blocker = sum(1 for i in issues if i.get('severity') == 'BLOCKER')
    critical = sum(1 for i in issues if i.get('severity') == 'CRITICAL')
    major = sum(1 for i in issues if i.get('severity') == 'MAJOR')
    minor = sum(1 for i in issues if i.get('severity') == 'MINOR')
    info = sum(1 for i in issues if i.get('severity') == 'INFO')

    print(f'{total}|{blocker}|{critical}|{major}|{minor}|{info}')
except:
    print('0|0|0|0|0|0')
" 2>/dev/null)

            IFS='|' read -r total blocker critical major minor info <<< "$issue_count"

            # Report findings
            if [ "$total" -gt 0 ]; then
                print_warning "Found $total code quality issue(s):"
                [ "$blocker" -gt 0 ] && print_error "  🚫 Blocker: $blocker"
                [ "$critical" -gt 0 ] && print_error "  🔴 Critical: $critical"
                [ "$major" -gt 0 ] && print_warning "  🟡 Major: $major"
                [ "$minor" -gt 0 ] && print_status "  🔵 Minor: $minor"
                [ "$info" -gt 0 ] && print_status "  ℹ️  Info: $info"

                echo ""
                print_warning "❌ Code quality issues detected! Please review and fix them."
                print_status "Dashboard: $SONAR_HOST_URL/dashboard?id=essenza-web-backend"
                return 1
            else
                print_success "✅ No code quality issues found!"
                return 0
            fi
        else
            print_warning "Python3 not available - cannot parse issue details"
            print_status "Please check dashboard manually: $SONAR_HOST_URL/dashboard?id=essenza-web-backend"
            return 0
        fi
    else
        print_warning "curl not available - cannot check issues automatically"
        print_status "Please check dashboard manually: $SONAR_HOST_URL/dashboard?id=essenza-web-backend"
        return 0
    fi
}

# Show analysis summary
show_summary() {
    print_status "Analysis Summary:"
    echo "  ✓ Project: Essenza Web Backend"
    echo "  ✓ Focus: Security & Code Quality"
    echo "  ✓ Coverage: Disabled (as requested)"
    echo "  ✓ Source directories: apps, config, core, services, utils, docs"
    echo ""
    print_status "Next steps:"
    echo "  1. Review security hotspots in SonarQube dashboard"
    echo "  2. Fix critical and high severity issues"
    echo "  3. Set up quality gates for your CI/CD pipeline"
    echo "  4. Configure branch analysis for pull requests"
}

# Main execution
main() {
    print_status "Starting SonarQube Analysis for Essenza Django Backend"
    print_status "=================================================="

    check_sonar_scanner
    check_config
    check_environment
    clean_analysis
    security_check

    # Run analysis and capture result
    run_analysis
    local analysis_result=$?

    show_summary

    # Exit with appropriate status based on issues found
    if [ $analysis_result -eq 0 ]; then
        print_success "✅ Analysis completed - No issues found! 🎉"
        exit 0
    else
        print_error "❌ Analysis completed - Issues found! Please review and fix them."
        exit 1
    fi
}

# Parse command line arguments
case "${1:-}" in
    --help|-h)
        echo "SonarQube Analysis Runner for Essenza Django Backend"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h          Show this help message"
        echo "  --clean-only        Only clean previous analysis data"
        echo "  --check-only        Only run security checks without analysis"
        echo ""
        echo "Environment variables:"
        echo "  SONAR_HOST_URL      SonarQube server URL (default: http://localhost:9000)"
        echo "  SONAR_TOKEN         SonarQube authentication token"
        echo ""
        echo "Example:"
        echo "  export SONAR_TOKEN=your_token_here"
        echo "  export SONAR_HOST_URL=https://sonarcloud.io"
        echo "  $0"
        exit 0
        ;;
    --clean-only)
        print_status "Cleaning analysis data only..."
        clean_analysis
        exit 0
        ;;
    --check-only)
        print_status "Running security checks only..."
        security_check
        exit 0
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac