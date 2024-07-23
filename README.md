# Shell Command Generator

## Description

Shell Command Generator is a Python-based CLI application that generates shell commands based on user queries using the Anthropic API. It supports multiple shell environments and provides an interactive interface for users to input their command queries and receive generated commands.

## Technologies Used

- Python 3.x
- Click (for CLI interface)
- Anthropic API (for command generation)
- python-dotenv (for environment variable management)
- pyperclip (for clipboard functionality)

## How It Works

1. The user selects their preferred shell environment (cmd, powershell, or bash).
2. The user inputs a query describing the command they need.
3. The application sends the query to the Anthropic API, which generates a suitable shell command.
4. The generated command is displayed to the user and can be copied to the clipboard.
5. The process repeats until the user chooses to exit.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/shell-command-generator.git
   cd shell-command-generator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```
   python main.py
   ```

2. Select your preferred shell environment when prompted.

3. Enter your command queries when prompted. The application will generate and display the corresponding shell commands.

4. Choose whether to copy the generated command to your clipboard.

5. Type 'exit' when you're done to quit the application.

## Testing

To run the unit tests:

```
python -m unittest test_main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
