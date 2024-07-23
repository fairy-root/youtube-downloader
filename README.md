# YouTube Downloader Telegram Bot

This is a Telegram bot that allows users to download YouTube videos and audio directly through Telegram. The bot uses the `pytubefix` library to fetch video information and `ffmpeg` to handle video and audio merging.

## Features

- Download YouTube videos in various resolutions.
- Download YouTube audio in various bitrates.
- Simple and interactive user interface using Telegram inline keyboards.
- Option to go back to the main menu if a wrong choice is made.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/fairy-root/youtube-downloader.git
cd youtube-downloader
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Replace `TOKEN` in the `ytbot.py` file with your Telegram bot token.

4. Make sure you have `ffmpeg` installed on your system. You can download it from [here](https://ffmpeg.org/download.html).

5. if youre using Termux use `pkg install ffmpeg`

## Usage

1. Run the bot:

```bash
python ytbot.py
```

2. Start a chat with your bot on Telegram and send a YouTube link.

3. Follow the instructions to choose the format (video or audio) and resolution/bitrate.

## Requirements

- `pytubefix`
- `python-telegram-bot`
- `ffmpeg`

## Example

1. Start the bot and send a YouTube link:
```
Send me a YouTube link to download.
```

2. The bot fetches video information:
```
Fetching information of the video...
```

3. Choose the format:
```
Choose format:
[ Video ] [ Audio ]
```

4. Select the resolution (for video) or bitrate (for audio):
```
Select resolution:
[ 1080p ] [ 720p ] [ Back ]
```
or
```
Select bitrate:
[ 160kbps ] [ 128kbps ] [ Back ]
```

5. The bot downloads and sends the file to you.

## Donation

Your support is appreciated:

- USDt (TRC20): `TGCVbSSJbwL5nyXqMuKY839LJ5q5ygn2uS`
- BTC: `13GS1ixn2uQAmFQkte6qA5p1MQtMXre6MT`
- ETH (ERC20): `0xdbc7a7dafbb333773a5866ccf7a74da15ee654cc`
- LTC: `Ldb6SDxUMEdYQQfRhSA3zi4dCUtfUdsPou`

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any issues, please open an issue or create a pull request.

### Steps to Contribute

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes.
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature/your-feature-name`
6. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

- [GitHub: FairyRoot](https://github.com/fairy-root)
- [Telegram: @FairyRoot](https://t.me/FairyRoot)