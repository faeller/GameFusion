# GameFusion

GameFusion is a unique Python application that leverages the power of OpenAI's GPT-4 model to recommend multiplayer games. It compares the Steam libraries of two users and provides personalized suggestions for games they might enjoy playing together. GameFusion is your intelligent gaming companion, offering you and your friends tailored gaming experiences.

## Installation

GameFusion is not yet available on PyPI, but you can clone the repository and run it like any other Python script.

Here's how you can install GameFusion:

1. Clone the repository:
    ```bash
    git clone https://github.com/faeller/gamefusion.git
    ```
2. Move into the `gamefusion` directory:
    ```bash
    cd gamefusion
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the script:
    ```bash
    python gamefusion.py
    ```

## Usage

To use GameFusion, you will need your OpenAI API key. You can supply the key with --key in the cli or as an environment variable, like so:

```bash
export GPT4_API_KEY=your_openai_key
```

Then you can run the tool as follows:

```bash
python3 gamefusion.py your_steam_username your_friend's_steam_username
```

That's all! GameFusion will fetch the necessary data and provide you with a list of game recommendations.

Enjoy your gaming!

## Contributing

We welcome contributions! Please feel free to submit a pull request or open an issue.

## License

This project is licensed under the terms of the MIT license.