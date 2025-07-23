#!/usr/bin/env python3
"""
Test Runner for SauceDemo Test Automation Framework.

This script provides various options for running tests with different
configurations, markers, and reporting options.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional
from loguru import logger


class TestRunner:
    """
    Test runner class for executing pytest with various configurations.
    
    Provides methods for running different test suites, generating reports,
    and managing test execution environments.
    """
    
    def __init__(self):
        """Initialize test runner."""
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "reports"
        self.logs_dir = self.project_root / "logs"
        
        # Ensure directories exist
        self.reports_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        (self.reports_dir / "screenshots").mkdir(exist_ok=True)
        (self.reports_dir / "allure-results").mkdir(exist_ok=True)
        
        logger.info("Test runner initialized")
    
    def _build_pytest_command(
        self,
        test_path: Optional[str] = None,
        markers: Optional[List[str]] = None,
        parallel: bool = False,
        verbose: bool = True,
        generate_allure: bool = True,
        generate_html: bool = True,
        headless: bool = False,
        browser: str = "chromium"
    ) -> List[str]:
        """
        Build pytest command with specified options.
        
        Args:
            test_path: Specific test file or directory to run
            markers: List of pytest markers to include
            parallel: Run tests in parallel
            verbose: Verbose output
            generate_allure: Generate Allure reports
            generate_html: Generate HTML reports
            headless: Run browser in headless mode
            browser: Browser type to use
            
        Returns:
            List of command arguments
        """
        cmd = ["python", "-m", "pytest"]
        
        # Test path
        if test_path:
            cmd.append(test_path)
        else:
            cmd.append("tests/")
        
        # Markers
        if markers:
            for marker in markers:
                cmd.extend(["-m", marker])
        
        # Parallel execution
        if parallel:
            cmd.extend(["-n", "auto"])
        
        # Verbosity
        if verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")
        
        # Reporting
        if generate_html:
            cmd.extend(["--html=reports/report.html", "--self-contained-html"])
        
        if generate_allure:
            cmd.extend(["--alluredir=reports/allure-results"])
        
        # Browser configuration
        if headless:
            cmd.extend(["--headless"])
        
        cmd.extend(["--browser", browser])
        
        # Additional options
        cmd.extend([
            "--tb=short",
            "--maxfail=5",
            "--strict-markers",
            "--strict-config"
        ])
        
        return cmd
    
    def run_smoke_tests(self, headless: bool = False, parallel: bool = True) -> int:
        """
        Run smoke tests (critical functionality).
        
        Args:
            headless: Run in headless mode
            parallel: Run tests in parallel
            
        Returns:
            Exit code from pytest
        """
        logger.info("🔥 Running Smoke Tests")
        
        cmd = self._build_pytest_command(
            markers=["smoke"],
            parallel=parallel,
            headless=headless,
            verbose=True
        )
        
        logger.info(f"Command: {' '.join(cmd)}")
        return self._execute_command(cmd)
    
    def run_regression_tests(self, headless: bool = True, parallel: bool = True) -> int:
        """
        Run regression tests (full test suite).
        
        Args:
            headless: Run in headless mode
            parallel: Run tests in parallel
            
        Returns:
            Exit code from pytest
        """
        logger.info("🔄 Running Regression Tests")
        
        cmd = self._build_pytest_command(
            markers=["regression"],
            parallel=parallel,
            headless=headless,
            verbose=True
        )
        
        logger.info(f"Command: {' '.join(cmd)}")
        return self._execute_command(cmd)
    
    def run_negative_tests(self, headless: bool = False, parallel: bool = False) -> int:
        """
        Run negative tests (error scenarios).
        
        Args:
            headless: Run in headless mode
            parallel: Run tests in parallel
            
        Returns:
            Exit code from pytest
        """
        logger.info("❌ Running Negative Tests")
        
        cmd = self._build_pytest_command(
            markers=["negative"],
            parallel=parallel,
            headless=headless,
            verbose=True
        )
        
        logger.info(f"Command: {' '.join(cmd)}")
        return self._execute_command(cmd)
    
    def run_specific_tests(
        self,
        test_path: str,
        headless: bool = False,
        parallel: bool = False,
        markers: Optional[List[str]] = None
    ) -> int:
        """
        Run specific test file or directory.
        
        Args:
            test_path: Path to test file or directory
            headless: Run in headless mode
            parallel: Run tests in parallel
            markers: Additional markers to filter
            
        Returns:
            Exit code from pytest
        """
        logger.info(f"🎯 Running Specific Tests: {test_path}")
        
        cmd = self._build_pytest_command(
            test_path=test_path,
            markers=markers,
            parallel=parallel,
            headless=headless,
            verbose=True
        )
        
        logger.info(f"Command: {' '.join(cmd)}")
        return self._execute_command(cmd)
    
    def run_all_tests(self, headless: bool = True, parallel: bool = True) -> int:
        """
        Run all tests in the test suite.
        
        Args:
            headless: Run in headless mode
            parallel: Run tests in parallel
            
        Returns:
            Exit code from pytest
        """
        logger.info("🚀 Running All Tests")
        
        cmd = self._build_pytest_command(
            parallel=parallel,
            headless=headless,
            verbose=True
        )
        
        logger.info(f"Command: {' '.join(cmd)}")
        return self._execute_command(cmd)
    
    def generate_allure_report(self, serve: bool = False) -> int:
        """
        Generate Allure report from test results.
        
        Args:
            serve: Serve the report on local server
            
        Returns:
            Exit code from allure command
        """
        logger.info("📊 Generating Allure Report")
        
        allure_results = self.reports_dir / "allure-results"
        allure_report = self.reports_dir / "allure-report"
        
        if not allure_results.exists() or not any(allure_results.iterdir()):
            logger.error("No Allure results found. Run tests first.")
            return 1
        
        # Generate report
        cmd = ["allure", "generate", str(allure_results), "-o", str(allure_report), "--clean"]
        result = self._execute_command(cmd)
        
        if result == 0:
            logger.info(f"Allure report generated: {allure_report}/index.html")
            
            if serve:
                logger.info("🌐 Serving Allure Report")
                serve_cmd = ["allure", "serve", str(allure_results)]
                return self._execute_command(serve_cmd)
        
        return result
    
    def clean_reports(self) -> None:
        """Clean all generated reports and logs."""
        logger.info("🧹 Cleaning Reports and Logs")
        
        import shutil
        
        # Clean reports
        if self.reports_dir.exists():
            shutil.rmtree(self.reports_dir)
            self.reports_dir.mkdir(exist_ok=True)
            (self.reports_dir / "screenshots").mkdir(exist_ok=True)
            (self.reports_dir / "allure-results").mkdir(exist_ok=True)
        
        # Clean logs
        if self.logs_dir.exists():
            shutil.rmtree(self.logs_dir)
            self.logs_dir.mkdir(exist_ok=True)
        
        logger.info("Reports and logs cleaned")
    
    def install_dependencies(self) -> int:
        """Install required dependencies."""
        logger.info("📦 Installing Dependencies")
        
        # Install Python dependencies
        cmd = ["pip", "install", "-r", "requirements.txt"]
        result = self._execute_command(cmd)
        
        if result == 0:
            # Install Playwright browsers
            logger.info("🌐 Installing Playwright Browsers")
            playwright_cmd = ["python", "-m", "playwright", "install"]
            result = self._execute_command(playwright_cmd)
        
        return result
    
    def _execute_command(self, cmd: List[str]) -> int:
        """
        Execute command and return exit code.
        
        Args:
            cmd: Command to execute
            
        Returns:
            Exit code
        """
        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=False)
            return result.returncode
        except FileNotFoundError as e:
            logger.error(f"Command not found: {e}")
            return 1
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return 1


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description="SauceDemo Test Automation Framework Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --smoke                    # Run smoke tests
  python run_tests.py --regression --headless    # Run regression tests headless
  python run_tests.py --negative                 # Run negative tests
  python run_tests.py --all --parallel           # Run all tests in parallel
  python run_tests.py --file tests/test_login.py # Run specific test file
  python run_tests.py --clean                    # Clean reports and logs
  python run_tests.py --install                  # Install dependencies
  python run_tests.py --report --serve           # Generate and serve Allure report
        """
    )
    
    # Test execution options
    test_group = parser.add_mutually_exclusive_group()
    test_group.add_argument("--smoke", action="store_true", help="Run smoke tests")
    test_group.add_argument("--regression", action="store_true", help="Run regression tests")
    test_group.add_argument("--negative", action="store_true", help="Run negative tests")
    test_group.add_argument("--all", action="store_true", help="Run all tests")
    test_group.add_argument("--file", type=str, help="Run specific test file or directory")
    
    # Execution options
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], 
                       default="chromium", help="Browser to use for tests")
    parser.add_argument("--markers", nargs="+", help="Additional pytest markers to filter")
    
    # Utility options
    parser.add_argument("--clean", action="store_true", help="Clean reports and logs")
    parser.add_argument("--install", action="store_true", help="Install dependencies")
    parser.add_argument("--report", action="store_true", help="Generate Allure report")
    parser.add_argument("--serve", action="store_true", help="Serve Allure report (use with --report)")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    exit_code = 0
    
    try:
        if args.clean:
            runner.clean_reports()
        elif args.install:
            exit_code = runner.install_dependencies()
        elif args.report:
            exit_code = runner.generate_allure_report(serve=args.serve)
        elif args.smoke:
            exit_code = runner.run_smoke_tests(headless=args.headless, parallel=args.parallel)
        elif args.regression:
            exit_code = runner.run_regression_tests(headless=args.headless, parallel=args.parallel)
        elif args.negative:
            exit_code = runner.run_negative_tests(headless=args.headless, parallel=args.parallel)
        elif args.all:
            exit_code = runner.run_all_tests(headless=args.headless, parallel=args.parallel)
        elif args.file:
            exit_code = runner.run_specific_tests(
                args.file, 
                headless=args.headless, 
                parallel=args.parallel,
                markers=args.markers
            )
        else:
            parser.print_help()
            exit_code = 1
        
        # Generate report after test execution if tests were run
        if args.smoke or args.regression or args.negative or args.all or args.file:
            if exit_code == 0:
                logger.info("✅ Tests completed successfully")
            else:
                logger.error("❌ Some tests failed")
            
            logger.info("📊 Generating reports...")
            runner.generate_allure_report()
    
    except KeyboardInterrupt:
        logger.info("Test execution interrupted by user")
        exit_code = 130
    except Exception as e:
        logger.error(f"Error during test execution: {e}")
        exit_code = 1
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main() 