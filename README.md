# SauceDemo Test Automation Framework

Test automation framework for SauceDemo e-commerce application (https://www.saucedemo.com). Built with Playwright and pytest using Page Object Model pattern.

## Features

- Page Object Model architecture
- Playwright for web automation  
- pytest framework with fixtures
- HTML and Allure reporting
- YAML configuration management
- Parallel test execution
- Multiple user type support

## Test Coverage

### Test Categories
- Smoke Tests: Critical functionality
- Regression Tests: Full feature coverage  
- Negative Tests: Error scenarios

### Functional Areas
- Authentication: Login/logout with different users
- Product Catalog: Product listing and sorting
- Shopping Cart: Add/remove items
- Checkout Process: Complete purchase flow

## Quick Start

### Prerequisites
- Python 3.11+
- Git

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd dot_project_new

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies and browsers
python run_tests.py --install
```

### Running Tests
```bash
# Run all tests
python run_tests.py --all

# Run smoke tests only
python run_tests.py --smoke

# Run with parallel execution
python run_tests.py --all --parallel

# Run specific test file
python -m pytest tests/test_login.py -v
```

## Project Structure

```
dot_project_new/
├── config/
│   └── test_config.yaml     # Test configuration
├── core/
│   ├── base_page.py         # Base page class
│   ├── browser_manager.py   # Browser handling
│   └── config_manager.py    # Config loading
├── pages/
│   ├── login_page.py        # Login page objects
│   ├── inventory_page.py    # Product page objects
│   ├── cart_page.py         # Cart page objects
│   └── checkout_page.py     # Checkout page objects
├── tests/
│   ├── test_login.py        # Login tests
│   ├── test_e2e_purchase_flow.py  # E2E tests
│   └── test_checkout_validation.py # Checkout tests
├── reports/                 # Generated reports
├── logs/                    # Test logs
├── conftest.py             # pytest fixtures
├── pytest.ini             # pytest configuration
├── requirements.txt        # Dependencies
└── run_tests.py           # Test runner script
```

## Configuration

Configuration is managed through `config/test_config.yaml`:

```yaml
environment:
  base_url: "https://www.saucedemo.com"
  browser: "chromium"
  headless: false
  timeout: 30000

users:
  standard_user:
    username: "standard_user"
    password: "secret_sauce"
  # ... more users
```

## Test Data

The framework includes test data for:
- Valid user credentials (4 user types)
- Invalid login combinations
- Customer information for checkout
- Product data for cart operations

## Reporting

### HTML Reports
Basic HTML reports are generated automatically:
```bash
# Reports saved to reports/report.html
```

### Allure Reports
Rich reporting with screenshots and detailed steps:
```bash
# Generate Allure report (requires Allure installation)
allure serve reports/allure-results
```

## Browser Support

- Chromium (default)
- Firefox
- WebKit (Safari)

## Parallel Execution

Run tests in parallel for faster execution:
```bash
python run_tests.py --all --parallel
# Uses up to 10 workers automatically
```

## Development

### Adding New Tests
1. Create page objects in `pages/` directory
2. Add test methods in appropriate `tests/` file
3. Use existing fixtures from `conftest.py`
4. Follow naming conventions

### Adding New Pages
1. Create new page class inheriting from `BasePage`
2. Define locators and methods
3. Add to imports in test files

## Troubleshooting

### Common Issues

**Browser not found:**
```bash
python -m playwright install
```

**Tests failing randomly:**
- Check network connection
- Increase timeout in config
- Run tests individually to isolate issues

**Import errors:**
- Ensure virtual environment is activated
- Check Python path and dependencies

## Contributing

1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass

## License

This project is for educational and testing purposes. 