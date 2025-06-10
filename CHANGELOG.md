# Changelog

All notable changes to WebLens will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Core browser management with browser-use cloud API integration
- Multi-profile browser support
- Test runner with parallel execution
- CLI interface for test execution
- Profile management system
- Comprehensive logging and reporting
- Screenshot and video capture on test failure
- Rich configuration management
- Example test suites (basic, advanced, and cloud)
- Unit and integration test coverage

### Removed
- Playwright dependency (chuyển hoàn toàn sang browser-use cloud API)
- Local browser configuration và management
- Các file cũ không còn được sử dụng (config_old.py, browser_manager_old.py)

### Features

- **Cloud-Based Testing**: Automated testing through browser-use cloud API
- **Profile System**: Pre-built profiles for desktop, mobile, tablet scenarios
- **AI-Powered Testing**: Integration with browser-use for smart automation
- **Parallel Execution**: Run tests concurrently on cloud for better performance
- **Rich Reporting**: JSON reports with screenshots and videos
- **CLI Tool**: Powerful command-line interface
- **Flexible Configuration**: Simplified environment-based configuration
- **Mock Support**: Fallback to mock mode when API key không available

### Documentation

- Comprehensive README with examples
- Contributing guidelines
- Setup scripts and Makefile
- Code documentation and type hints
- Hướng dẫn cloud testing

## [0.1.0] - 2024-12-10

### Added
- Initial release of WebLens testing framework
- Core functionality for web automation testing
- Browser-use integration for intelligent testing
- Multi-profile browser support

---

## Future Releases

### Planned Features
- [ ] Visual regression testing
- [ ] API testing integration  
- [ ] Mobile app testing support
- [ ] Cloud browser support (BrowserStack, Sauce Labs)
- [ ] CI/CD integration templates
- [ ] Performance monitoring and metrics
- [ ] Test data management
- [ ] Advanced reporting dashboard
- [ ] Plugin system for extensibility
- [ ] Docker support
- [ ] Kubernetes test execution
- [ ] Real device testing
- [ ] Accessibility testing enhancements
