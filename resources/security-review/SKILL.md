---
name: security-review
description: Perform a comprehensive security review of code and provide specific remediation steps with code examples for each security issue identified. Use when reviewing code for vulnerabilities, checking for OWASP Top 10 issues, or auditing security practices.
---

# Security Review

Comprehensive security review focusing on OWASP Top 10 and common vulnerabilities.

## Security Review Areas

### 1. Authentication & Authorization

- Verify proper authentication mechanisms
- Check authorization controls and permission systems
- Review session management and token handling
- Ensure secure password policies and storage

### 2. Input Validation & Sanitization

- Identify SQL injection vulnerabilities
- Check for XSS and CSRF attack vectors
- Validate all user inputs and API parameters
- Review file upload and processing security

### 3. Data Protection

- Ensure sensitive data encryption at rest and in transit
- Check for data exposure in logs and error messages
- Review API responses for information leakage
- Verify proper secrets management

### 4. Infrastructure Security

- Review dependency security and known vulnerabilities
- Check HTTPS configuration and certificate validation
- Analyze CORS policies and security headers
- Review environment variable and configuration security

## Output Format

1. **Vulnerabilities**: For each issue found:
   - 🔴 **Critical** / 🟠 **High** / 🟡 **Medium** / 🔵 **Low**
   - Category (e.g., Injection, Auth, Data Exposure)
   - Description of the vulnerability
   - Location in code
   - Remediation steps
   - Secure code example

2. **Summary**: Overall security assessment and priority recommendations

## Checklist

- [ ] Verified proper authentication mechanisms
- [ ] Checked authorization controls and permission systems
- [ ] Reviewed session management and token handling
- [ ] Ensured secure password policies and storage
- [ ] Identified SQL injection vulnerabilities
- [ ] Checked for XSS and CSRF attack vectors
- [ ] Validated all user inputs and API parameters
- [ ] Ensured sensitive data encryption at rest and in transit
- [ ] Checked for data exposure in logs and error messages
- [ ] Reviewed dependency security and known vulnerabilities
- [ ] Analyzed CORS policies and security headers
