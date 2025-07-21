# Redis Python Excel Integration

A simple Python project demonstrating Redis integration and Excel data processing.

## Features

- **Redis Operations**: Connect to Redis, store/retrieve data, manage keys
- **Excel Processing**: Read/write Excel files, data manipulation
- **Integration Examples**: Combine Redis caching with Excel data processing

## Setup

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Linux/Mac
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start Redis server (if not running):**
   ```bash
   # On Windows with Redis installed
   redis-server
   
   # Or using Docker
   docker run -d -p 6379:6379 redis:alpine
   ```

4. **Run the examples:**
   ```bash
   # Interactive main application
   python main.py
   
   # Or run individual examples:
   python src/redis_examples.py      # Basic Redis operations
   python src/excel_examples.py      # Excel processing
   python src/redis_excel_integration.py  # Combined examples
   ```

## Project Structure

```
├── src/
│   ├── redis_examples.py      # Basic Redis operations
│   ├── excel_examples.py      # Excel file processing
│   ├── redis_excel_integration.py  # Combined examples
│   └── config.py              # Configuration settings
├── data/
│   ├── sample_data.xlsx       # Sample Excel file (auto-generated)
│   └── sample_data.csv        # Sample CSV file
├── .vscode/
│   ├── tasks.json             # VS Code tasks for running examples
│   └── launch.json            # Debug configurations
├── main.py                    # Interactive main application
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Quick Start

🚀 **Run the interactive main application:**
```bash
python main.py
```

This will present you with a menu to explore all examples:
- 📊 Excel Operations Demo
- 🔗 Redis Operations Demo  
- ⚡ Redis-Excel Integration Demo
- 📈 Performance Comparison

## VS Code Integration

The project includes VS Code configurations:
- **Tasks** (Ctrl+Shift+P → "Tasks: Run Task"):
  - `Run Main Application` - Launch interactive menu
  - `Run Redis Examples` - Basic Redis operations
  - `Run Excel Examples` - Excel file processing
  - `Run Redis-Excel Integration` - Combined examples

- **Debug Configurations** (F5):
  - Debug any of the example scripts with breakpoints

## Examples

### Redis Operations
- Connect to Redis server
- Store and retrieve key-value pairs
- Work with different data types (strings, lists, sets, hashes)
- Implement caching patterns

### Excel Processing
- Read Excel files into pandas DataFrames
- Write data to Excel files
- Format cells and sheets
- Handle multiple worksheets

### Integration Scenarios
- Cache Excel data in Redis for faster access
- Store processed Excel results in Redis
- Use Redis as a queue for Excel processing tasks
