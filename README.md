# WebLens - AI-Driven Automated Testing Framework

![WebLens](https://via.placeholder.com/800x200?text=WebLens+Testing+Framework) *(Demo image)*

## 🔍 The Problem with Traditional Testing Frameworks

In software development, writing and maintaining automated tests has always been challenging:

- **High Cost**: Writing automation scripts often requires effort comparable to developing the product code itself
- **Hard-Coded Steps**: Even with BDD frameworks, QA engineers must implement each step and action with code
- **Difficult Maintenance**: When UI/UX changes, test scripts typically need to be rewritten
- **Lack of Flexibility**: Test cases cannot adapt to application changes without human intervention
- **Time Consuming**: QA engineers spend most of their time writing code rather than focusing on test strategies
- **Technical Expertise Required**: Test writers need programming knowledge to write and maintain scripts

**Traditional testing forces you to write detailed code for each test step:**

```python
# Traditional approach with Selenium or similar frameworks
async def test_user_login(page):
    # Navigate to website
    await page.goto("https://example.com/login")
    
    # Fill in login form
    await page.fill("#username", "testuser")
    await page.fill("#password", "password123")
    
    # Click login button
    await page.click("button[type=submit]")
    
    # Check login was successful
    await page.wait_for_selector(".dashboard-welcome")
    assert await page.is_visible(".user-profile")
    
    # Check username is displayed
    user_name = await page.text_content(".username")
    assert user_name == "Test User"
```

## 💡 Introducing WebLens - The AI-Powered Solution

WebLens is a modern testing framework leveraging AI through the browser-use cloud API to solve these challenges. With WebLens, QA Engineers can:

- **Write Tests in Natural Language**: Describe steps and expected results in Vietnamese or English
- **Automatic Translation**: AI automatically translates descriptions into specific browser actions
- **Adapt to Changes**: Tests can adapt to UI/UX changes without requiring rewrites
- **Easy Maintenance**: Simply adjust natural language descriptions instead of code
- **High Speed**: Leverage cloud infrastructure to run tests in parallel
- **No Complex Setup**: No need to install browsers or WebDrivers

**With WebLens, testing becomes intuitive and efficient:**

```python
# WebLens approach using natural language
@weblens_test(
    name="User Login Test", 
    description="Verify user can login successfully"
)
async def test_user_login(agent):
    await agent.run("""
    1. Open the login page of example.com
    2. Enter username 'testuser' and password 'password123'
    3. Click the login button
    4. Ensure login was successful by checking we're on the dashboard
    5. Verify the displayed username is "Test User"
    """)
```

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
- **Multi-Profile Support**: Automatically test across different device configurations
- **Rich Reporting**: Detailed reports with screenshots and videos
- **Visual Verification**: Ability to recognize and interact with UI without hard-coded selectors
- **Parallel Execution**: Run tests simultaneously on the cloud for increased performance
- **Easy Configuration**: Simple setup with just an API key

## ⏱️ Quick Start

```bash
# Clone repository
git clone <repository-url>
cd WebLens

# Run quick start script
./quick_start.sh
```

For detailed installation and usage instructions, see [INSTRUCTION.md](./INSTRUCTION.md)

## 📖 Documentation

- [Usage Guide](./INSTRUCTION.md) - Detailed instructions for installation and using WebLens
- [Browser Use Cloud API](./docs/browser_use_cloud_api.md) - Documentation about the API used in WebLens
- [Contributing Guide](./CONTRIBUTING.md) - Guidelines for contributing to the project

## 🏗️ Project Structure

```text
WebLens/
├── weblens/                   # Main source code
├── docs/                      # Documentation
├── examples/                  # Usage examples
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

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙋‍♂️ Support

Nếu bạn gặp vấn đề hoặc có câu hỏi:

1. Check [Issues](../../issues) existing
2. Create new issue với detailed description
3. Contact maintainers

## 🗺️ Roadmap

- [ ] Visual regression testing
- [ ] API testing integration
- [ ] Mobile app testing support
- [x] Cloud browser support (đã hoàn thành)
- [ ] CI/CD integration templates
- [ ] Performance monitoring
- [ ] Test data management
- [ ] Advanced reporting dashboard

---

**WebLens** - Making web testing intelligent and efficient! 🚀
