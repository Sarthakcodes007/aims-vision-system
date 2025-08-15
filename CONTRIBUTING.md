# Contributing to AIMS Vision System

We welcome contributions to the AIMS Vision System! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/aims-vision-system.git
   cd aims-vision-system
   ```
3. **Set up the development environment**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🎯 Types of Contributions

We welcome several types of contributions:

- **Bug fixes** - Fix issues in the codebase
- **Feature enhancements** - Add new functionality
- **Documentation improvements** - Improve README, comments, or guides
- **Performance optimizations** - Improve speed or memory usage
- **UI/UX improvements** - Enhance the user interface
- **Test coverage** - Add or improve tests

## 📝 Contribution Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

### Frontend Guidelines
- Use semantic HTML5 elements
- Follow CSS BEM methodology for class naming
- Optimize for performance (minimize DOM manipulations)
- Ensure cross-browser compatibility
- Test on different screen sizes

### Commit Messages
Use clear, descriptive commit messages:
```
type(scope): brief description

Detailed explanation if needed
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `perf`: Performance improvements

Examples:
```
feat(detection): add batch processing support
fix(ui): resolve mobile responsiveness issues
docs(readme): update installation instructions
```

## 🧪 Testing

Before submitting your contribution:

1. **Test your changes** thoroughly
2. **Run the application** in different modes:
   ```bash
   python api_server.py    # Test API backend
   python app.py          # Test Streamlit interface
   python launch.py       # Test auto-launcher
   ```
3. **Test with different images** and query types
4. **Verify browser compatibility** for frontend changes

## 📋 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update the README** if you've added features
5. **Create a pull request** with:
   - Clear title and description
   - Reference any related issues
   - Screenshots for UI changes
   - Performance impact notes

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] Verified browser compatibility

## Screenshots (if applicable)
[Add screenshots here]

## Additional Notes
[Any additional information]
```

## 🐛 Reporting Issues

When reporting issues, please include:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Environment details**:
  - OS and version
  - Python version
  - Browser (for frontend issues)
  - GPU information (if relevant)
- **Error messages** or logs
- **Screenshots** if applicable

## 💡 Feature Requests

For feature requests:

1. **Check existing issues** to avoid duplicates
2. **Describe the feature** clearly
3. **Explain the use case** and benefits
4. **Consider implementation complexity**
5. **Be open to discussion** and feedback

## 🏗️ Development Areas

Areas where contributions are especially welcome:

### Backend Improvements
- Model optimization and caching
- API rate limiting and security
- Batch processing capabilities
- Alternative model support
- Database integration for results

### Frontend Enhancements
- Mobile responsiveness improvements
- Accessibility features
- Advanced visualization options
- Real-time detection streaming
- User preference settings

### Performance Optimizations
- GPU memory management
- Image preprocessing optimization
- 3D rendering performance
- Lazy loading implementations
- Caching strategies

### Documentation
- API documentation
- Tutorial videos or guides
- Code examples and demos
- Architecture diagrams
- Deployment guides

## 📞 Getting Help

If you need help:

1. **Check the documentation** first
2. **Search existing issues** for similar problems
3. **Create a new issue** with the "question" label
4. **Join community discussions**

## 🎉 Recognition

Contributors will be:
- Listed in the project's contributors section
- Mentioned in release notes for significant contributions
- Invited to join the core team for outstanding contributions

Thank you for contributing to AIMS Vision System! 🚀