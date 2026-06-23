---
name: write-unit-tests
description: Create comprehensive unit tests for code, generating the test file with proper imports and setup according to the project's testing conventions. Use when writing tests, improving test coverage, or testing edge cases.
---

# Write Unit Tests

Create comprehensive unit tests following best practices.

## Testing Guidelines

### 1. Test Coverage

- Test all public methods and functions
- Cover edge cases and error conditions
- Test both positive and negative scenarios
- Aim for high code coverage

### 2. Test Structure

- Use the project's testing framework conventions
- Write clear, descriptive test names
- Follow the Arrange-Act-Assert pattern
- Group related tests logically

### 3. Test Cases to Include

- Happy path scenarios
- Edge cases and boundary conditions
- Error handling and exception cases
- Mock external dependencies appropriately

### 4. Test Quality

- Make tests independent and isolated
- Ensure tests are deterministic and repeatable
- Keep tests simple and focused on one thing
- Add helpful assertion messages

## Output Format

1. **Test Plan**: List of functions and test cases:
   - Function name
   - Test cases to cover

2. **Test Code**: Complete test file with:
   - Proper imports and setup
   - All test cases implemented
   - Clear test names and assertions

3. **Coverage Notes**: What's covered and any gaps

## Checklist

- [ ] Tested all public methods and functions
- [ ] Covered edge cases and error conditions
- [ ] Tested both positive and negative scenarios
- [ ] Used the project's testing framework conventions
- [ ] Written clear, descriptive test names
- [ ] Followed the Arrange-Act-Assert pattern
- [ ] Included happy path scenarios
- [ ] Included edge cases and boundary conditions
- [ ] Mocked external dependencies appropriately
- [ ] Made tests independent and isolated
- [ ] Ensured tests are deterministic and repeatable
