# Contributing to LibreDomains

Thank you for your interest in contributing to LibreDomains! This document provides guidelines and information for contributors.

## 🤝 Ways to Contribute

### For Users
- 🐛 **Report Bugs**: Found an issue? Let us know!
- 💡 **Suggest Features**: Have ideas for improvements?
- 📚 **Improve Documentation**: Help make our guides clearer
- 🧪 **Test New Features**: Try beta features and provide feedback

### For Developers
- 🔧 **Fix Bugs**: Help resolve reported issues
- ✨ **Add Features**: Implement new functionality
- 🏗️ **Improve Infrastructure**: Enhance CI/CD, automation
- 🔍 **Code Review**: Review pull requests from other contributors

## 🚀 Getting Started

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/LibreDomains-beta.git
   cd LibreDomains-beta
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Set Up Environment**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Add your Cloudflare API token (for testing)
   echo "CLOUDFLARE_API_TOKEN=your_token_here" >> .env
   ```

4. **Run Tests**
   ```bash
   npm test
   npm run validate requests/example-personal-website.json
   ```

### Project Structure

```
LibreDomains-beta/
├── .github/workflows/     # GitHub Actions workflows
├── config/               # Configuration files
│   ├── domains.yml      # Domain configuration
│   └── schema.json      # Request validation schema
├── docs/                # Documentation
├── domains/             # Deployed DNS records (auto-generated)
├── requests/            # User subdomain requests
└── scripts/             # Automation scripts
    ├── validate-request.js
    ├── deploy-dns.js
    ├── cloudflare-api.js
    └── ...
```

## 📝 Contribution Guidelines

### Code Style

- Use **consistent indentation** (2 spaces)
- Follow **JavaScript Standard Style**
- Add **JSDoc comments** for functions
- Use **meaningful variable names**

### Commit Messages

Follow the [Conventional Commits](https://conventionalcommits.org/) specification:

```
type(scope): description

feat(dns): add support for SRV records
fix(validation): improve IPv6 address validation
docs(readme): update installation instructions
chore(deps): update axios to v1.6.0
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write clear, concise code
   - Add tests if applicable
   - Update documentation

3. **Test Your Changes**
   ```bash
   npm test
   npm run validate requests/example-personal-website.json
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat(validation): add SRV record support"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Use a descriptive title
   - Explain what your changes do
   - Reference any related issues
   - Include screenshots if applicable

### Code Review

All contributions go through code review:

- **Be responsive** to feedback
- **Be respectful** in discussions
- **Test thoroughly** before requesting review
- **Keep PRs focused** - one feature/fix per PR

## 🧪 Testing

### Manual Testing

1. **Validate Requests**
   ```bash
   node scripts/validate-request.js requests/your-test.json
   ```

2. **Check GitHub User**
   ```bash
   node scripts/check-github-user.js username
   ```

3. **Run Troubleshooter**
   ```bash
   node scripts/troubleshoot.js
   ```

### Automated Tests

```bash
# Run all validation tests
npm test

# Test specific functionality
npm run validate requests/example-personal-website.json
npm run check-user example-user
```

## 🏗️ Development Areas

### High Priority
- [ ] Add automated tests for all scripts  
- [ ] Improve error handling and user feedback
- [ ] Add support for more DNS record types
- [ ] Enhance security and abuse prevention

### Medium Priority
- [ ] Web interface for submitting requests
- [ ] API for programmatic access
- [ ] Statistics dashboard
- [ ] Notification system for users

### Low Priority
- [ ] Multiple domain providers support
- [ ] Custom DNS servers
- [ ] Advanced analytics
- [ ] Mobile app

## 🔒 Security

### Reporting Security Issues

**DO NOT** create public issues for security vulnerabilities.

Instead:
1. Email security@libredomains.org
2. Include detailed description
3. Provide steps to reproduce
4. We'll respond within 48 hours

### Security Best Practices

- Never commit API keys or secrets
- Validate all user inputs
- Use secure communication (HTTPS)
- Follow principle of least privilege
- Regular dependency updates

## 📋 Issue Guidelines

### Bug Reports

When reporting bugs, include:

- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Node.js version, etc.)
- **Screenshots** if applicable
- **Error messages** or logs

### Feature Requests

For new features, provide:

- **Problem description** - what issue does this solve?
- **Proposed solution** - how should it work?
- **Alternatives considered** - other ways to solve it?
- **Additional context** - mockups, examples, etc.

## 🎯 Contribution Areas

### Documentation
- Improve user guides
- Add more examples
- Create video tutorials
- Translate to other languages

### Code Quality
- Add unit tests
- Improve error handling
- Optimize performance
- Enhance security

### Features
- New DNS record types
- Better validation
- Improved automation
- Enhanced monitoring

### Community
- Help answer questions
- Review pull requests
- Triage issues
- Mentor new contributors

## 🏆 Recognition

Contributors will be recognized:

- **README credits** for significant contributions
- **GitHub achievements** and badges
- **Special role** in our Discord server
- **Early access** to new features

## 📞 Getting Help

Need help contributing?

- **Discord**: Join our community server
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Reach out to maintainers directly
- **Office Hours**: Weekly video calls for contributors

## 📄 License

By contributing to LibreDomains, you agree that your contributions will be licensed under the MIT License.

---

**Ready to contribute?** Start by looking at [good first issues](https://github.com/bestZwei/LibreDomains-beta/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) or reach out if you need help getting started!
