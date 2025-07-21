<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Redis Excel Integration Project Instructions

This is a Python project that demonstrates Redis integration with Excel data processing. When working on this project:

## Key Technologies
- **Redis**: Use redis-py library for Redis operations
- **Excel Processing**: Use pandas and openpyxl for Excel file handling
- **Python**: Focus on clean, readable code with proper error handling

## Code Style Guidelines
- Use descriptive function and variable names
- Include docstrings for all classes and functions
- Add proper error handling with try-catch blocks
- Use f-string formatting for string interpolation
- Follow PEP 8 style guidelines

## Project Structure
- `src/` contains main Python modules
- `data/` contains sample Excel and CSV files
- `config.py` manages configuration settings
- Use environment variables for sensitive configuration

## Common Patterns
- Always check Redis connection before operations
- Use caching patterns for expensive operations
- Handle Excel file operations with proper error checking
- Provide user-friendly console output with emojis and formatting

## Dependencies
- redis>=5.0.1
- pandas>=2.1.4
- openpyxl>=3.1.2
- python-dotenv>=1.0.0

When suggesting code improvements or new features, focus on maintainability, performance, and user experience.
