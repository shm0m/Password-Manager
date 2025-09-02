# Password Manager

A simple password manager in Python that allows you to securely store, encrypt, and retrieve your passwords.

## Features

- Add passwords for different websites
- Retrieve saved passwords
- List registered websites
- Encrypt passwords with a key derived from a master password
- Interactive command-line interface

## Prerequisites

- Python 3.13
- MySQL Server
- The following modules:
   - `mysql-connector-python`
   - `cryptography`
   - `rich`

## Installation

1. Clone the repository:
    ```sh
    git clone <repo-url>
    cd Password-Manager
    ```

2. Install dependencies:
    ```sh
    pip install mysql-connector-python cryptography rich
    ```

3. Configure your MySQL database:
    - Create a database named `password_manager`
    - Edit the connection settings in [`secure.py`](secure.py) if needed

## Usage

Run the main script:
```sh
python secure.py
```

Follow the on-screen instructions to add, retrieve, or list your passwords.

## Security

- Passwords are encrypted with Fernet (AES) before being stored in the database.
- The master password is used to derive the encryption key.
- Never share your master password.

## Author

Shaima DEROUICH
