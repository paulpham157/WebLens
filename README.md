# WebLens - AI-Driven Automated Testing Framework with Natural Language

![WebLens](https://via.placeholder.com/800x200?text=WebLens+Testing+Framework) *(Demo image)*

## 🚀 Natural Language Testing

WebLens fully embraces browser-use's natural language capabilities! Instead of writing programmatic test steps, you simply describe what you want the test to do:

```python
@weblens_test(
    name="user_login_test",
    description=(
        "Go to example.com/login, enter username 'testuser' "
        "and password 'password123', click the login button, "
        "and verify login was successful"
    )
)
async def test_user_login(browser):
    result = await browser.run()  # Execute the natural language instructions
    assert "login successful" in result.lower()
```

[Read more about the natural language approach](docs/natural_language_approach.md)

## 🔍 The Problem with Traditional Testing Frameworks

In software development, writing and maintaining automated tests has always been challenging:

- **High Cost**: Writing automation scripts often requires effort comparable to developing the product code itself
- **Hard-Coded Steps**: Even with BDD frameworks, QA engineers must implement each step and action with code
- **Difficult Maintenance**: When UI/UX changes, test scripts typically need to be rewritten
- **Lack of Flexibility**: Test cases cannot adapt to application changes without human intervention
- **Time Consuming**: QA engineers spend most of their time writing code rather than focusing on test strategies
- **Technical Expertise Required**: Test writers need programming knowledge to write and maintain scripts

**With WebLens, all of this becomes a simple natural language instruction:**

```python
@weblens_test(
    name="user_login_test",
    description=(
        "Go to example.com/login, login with username 'testuser' "
        "and password 'password123', wait for the dashboard to appear, "
        "and verify that the username 'Test User' is displayed in the profile"
    )
)
async def test_user_login(browser):
    result = await browser.run()
    assert "username 'Test User' is displayed" in result
```

## 💡 Introducing WebLens - The AI-Powered Solution

WebLens is a modern testing framework leveraging AI through the browser-use cloud API to solve these challenges. With WebLens, QA Engineers can:

- **Write Tests in Natural Language**: Describe steps and expected results in Vietnamese or English
- **Automatic Translation**: AI automatically translates descriptions into specific browser actions
- **Adapt to Changes**: Tests can adapt to UI/UX changes without requiring rewrites
- **Easy Maintenance**: Simply adjust natural language descriptions instead of code
- **High Speed**: Leverage cloud infrastructure to run tests in parallel
- **No Complex Setup**: No need to install browsers or WebDrivers

## 🔄 WebLens vs. Traditional Testing Frameworks

| Criteria | Traditional Frameworks | WebLens (AI-Driven) |
|----------|------------------------|---------------------|
| **Test Language** | Programming or Gherkin syntax | Natural language (Vietnamese/English) |
| **Test Writing** | Implement specific steps with code | Describe scenarios with text |
| **Maintenance** | Need code changes when UI changes | Automatically adapts to changes |
| **Complexity** | High (requires programming knowledge) | Low (no programming knowledge needed) |
| **Implementation Time** | Slow (coding + debugging) | Fast (just text descriptions) |
| **Scalability** | Difficult (requires more code) | Easy (just add descriptions) |
| **Setup** | Complex (local setup) | Simple (cloud-based) |

## 🚀 Key Features

- **AI-Driven Testing**: Use AI to control browsers based on natural language descriptions
- **Cloud-Based Execution**: Test on the cloud through browser-use API
- **Rich Reporting**: Detailed reports with screenshots and videos
- **Visual Verification**: Ability to recognize and interact with UI without hard-coded selectors
- **Parallel Execution**: Run tests simultaneously on the cloud for increased performance
- **Easy Configuration**: Simple setup with just an API key
- **Natural Language Testing**: Write tests in plain English or Vietnamese with no selectors

## ⏱️ Quick Start

```bash
# Clone repository
git clone <repository-url>
cd WebLens

# Run quick start script
./quick_start.sh

# Run login test specific example
./login_test_quickstart.sh
```

For detailed installation and usage instructions, see [INSTRUCTION.md](./INSTRUCTION.md)

## 📖 Documentation

- [Usage Guide](./INSTRUCTION.md) - Detailed instructions for installation and using WebLens
- [Comprehensive Natural Language Guide](./docs/natural_language_guide_full.md) - Complete guide to the natural language approach
- [Natural Language Approach](./docs/natural_language_approach.md) - Guide to using natural language testing
- [Login Testing Guide](./docs/login_testing_guide.md) - Guide for testing login functionality
- [Browser Use Cloud API](./docs/browser_use_cloud_api.md) - Documentation about the API used in WebLens
- [Contributing Guide](./CONTRIBUTING.md) - Guidelines for contributing to the project
- [Change Log](./docs/THAY_DOI.md) - Details about recent changes to direct natural language approach

## 🏗️ Project Structure

```text
WebLens/
├── weblens/                   # Main source code
│   ├── core/                  # Core framework components
│   ├── utils/                 # Utility functions
│   └── profiles/              # Browser profile management
├── docs/                      # Documentation
│   ├── natural_language_approach.md  # Guide to natural language testing
│   └── login_testing_guide.md        # Guide for testing login functionality
├── examples/                  # Usage examples
│   ├── natural_language_test.py      # Basic natural language example
│   ├── login_test_example.py         # Login testing example
│   ├── advanced_natural_assertions.py # Advanced assertions using natural language
│   └── direct_browser_use.py         # Direct browser-use API example
├── tests/                     # Framework tests
├── INSTRUCTION.md             # Detailed instructions
└── README.md                  # Project introduction
```

## 🔭 Roadmap

- [ ] Visual regression testing
- [ ] API testing integration
- [ ] Mobile app testing support
- [x] Cloud browser support (completed)
- [ ] CI/CD integration templates
- [ ] Performance monitoring
- [ ] Test data management
- [ ] Advanced reporting dashboard

## 🤝 Contributing

We welcome contributions from the community! See [CONTRIBUTING.md](./CONTRIBUTING.md) for more details.

## 📄 License

WebLens is released under the [MIT License](./LICENSE).

---

**WebLens** - Making web testing intelligent and efficient! 🚀
