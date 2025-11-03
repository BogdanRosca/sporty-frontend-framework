# Frontend Test Automation Framework
## Scope
Scope of this project is to validate the start of a StarWars II stream on https://m.twitch.tv/.

## Technical notes
- Tests are using Chrome mobile device emulation, for an iPhome 12 device ( value configurable in the `confing/mobile.yaml`)
- Tests can be executed against 2 configutrations, web and mobile, passed throug `--env` flag (mobile is the default onfiguration)
- Failed test cases are retried, through pytest-retry library, a maximum of 3 times (value configurable in `pytest.ini`)
- Tests execution is generating Allure results, and a report is automatically built and served after each local execution

## Project Structure
```
fronted-test-automation/
├── config/                      # Environment configurations
│   ├── mobile.yaml             
│   └── web.yaml                
├── pages/                       # Page Object Model classes
│   └── directory_page.py      
├── tests_suits/                 # Test suites and test cases
│   ├── test_sample.py          
│   └── test_start_streeming.py 
├── utils/                       # Utility modules and helpers
│   └── selenium.py            
├── reports/                     # Generated test reports
│   ├── index.html             
│   ├── app.js                 
│   ├── styles.css             
│   ├── data/                  
│   ├── export/               
│   ├── history/               
│   ├── plugin/               
│   └── widgets/               
├── screenshots/                 # Test execution screenshots
├── conftest.py               
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

## Running Tests
### Basic Test Execution
```bash
# Run tests with mobile configuration (default)
pytest

# Run tests with web configuration
pytest --env=web

# Run specific test file
pytest tests_suits/tests_suits/test_start_streeming.py
```

## Test execution recording
![Test Execution Demo](Screen%20Recording%202025-11-03%20at%2017.38.03.gif)

## Using AI
During coding tasks, I have used Github copilot integration in VS Code and Claude Sonnet 4 model for:
- Understanding the `request` parameter in config fixture 
- Understand what `config.option` relates to command line parameter ( eg. `config.option.reruns` vs cli `--reruns 5` )
- Understand how to unblock execution test thread when generating the Allure report ( using `threading` )
- Generate draft structure for README file

During merge I have used Github Copilot for:
- PR summary 
- Code review