# Rare Hashes Telegram Bot

### Description

This microservice is responsible for notifying users via Telegram when new rare hashes are added to the system.

It acts as a bridge between the web server and Telegram users. When the web server detects a newly found rare hash, it sends a message through RabbitMQ. This service listens for those messages, checks the user database and notification rules, and sends updates to the appropriate users via Telegram.

The project is part of a system consisting of three microservice components:

- A [web interface](https://github.com/YaroslavWork/RareHashesWebsite) displaying the rarest hashes found.
- A Telegram bot that notifies users about new rare hashes.
- An [automated searching bot](https://github.com/YaroslavWork/RareHashFinder) that scans and uploads rare hashes to the database.

This combination highlights advanced backend processing, database management, and real-time user notification integration.

*"Do one thing, and do it well."*

---

### Installation (for Linux)

1. Install Rare Hash Website:

    [Follow the installation process.](https://github.com/YaroslavWork/RareHashesWebsite?tab=readme-ov-file#installation-for-linux)

2. Create a Telegram bot:
    [See the official Telegram documentation.](https://core.telegram.org/bots/tutorial)

3. Create a **.env** file:

    This file contains all necessary private information. Your **.env** must contain:

    ```
    TOKEN=4839574812:AAFD39kkdpWt3ywyRZergyOLMaJhac60qc
    RABBIT_LOGIN=telegramBot
    RABBIT_PASSWORD=insanelyStrongPassword
    RABBIT_HOST=127.0.0.1:5672
    ```

    This configuration file contains:
    - `TOKEN` - Telegram bot token;
    - `RABBIT_LOGIN` - login for RabbitMQ communicator;
    - `RABBIT_PASSWORD` - password for RabbitMQ communicator;
    - `RABBIT_HOST` - connection to RabbitMQ communicator;

---

### Usage

1. [Follow the usage process.](https://github.com/YaroslavWork/RareHashesWebsite?tab=readme-ov-file#usage)

2. Create an image:
    ```sh
    docker build -t tel-bot .
    ```

3. Create and run a container:
    ```sh
    docker run --rm -it --name tel-bot-cont tel-bot
    ```

---

### Project Structure

The project is organized into separate Python modules, each responsible for a specific part of the system. The entry point is **main.py**:

- **database_operation.py** - Handles reading from and writing to a local `.txt` file used as a simple database.
- **command_operation.py** - Processes commands received from the web server via RabbitMQ.
- **notification.py** - Manages logging output to the command line and writing logs to `logs.txt`.
- **telegram_utils.py** - Sends notifications to users via Telegram.
- **Dockerfile** and **requirements.txt** - Used to build and run the application in Docker containers.
- **tests/*** - Contains unit tests for validating the functionality of the service.

---

### Dependencies

- Python 3.10.9+
- All Python modules are listed in **requirements.txt**.

---

### License

MIT License - see the `LICENSE` file for details.

---

### Demo

If my server isn’t being used for something else, the project should be running [here](https://158.220.119.11:6798/). I created my own certificate for this project. Web browsers will warn you about this, and you will need to confirm to proceed to the page.

**[Rare Hashes Web Server - Demo](https://158.220.119.11:6798/)**