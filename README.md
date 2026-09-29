# LobbyAdmin

A Python CLI tool to automate guest user creation on Cisco wireless LAN controllers via the Lobby Admin portal.

## Features

- Creates guest user accounts on Cisco WLC
- SSL/TLS support with custom cipher handling
- Session and cookie management
- Base64-encoded credentials in config

## Requirements

- Python 3.6+
- `requests` library (`pip install requests`)

## Setup

### Windows

1. Place all files in a directory (e.g., `C:\Users\you\LobbyAdmin`)
2. Create `lobbyA.bat` in the same directory:

```bat
@echo off
python "%~dp0https_comm.py" %*
```

3. Add the directory to your PATH, or place `lobbyA.bat` in a folder already in PATH

### Linux

1. Place all files in a directory (e.g., `~/LobbyAdmin`)
2. Make the script executable:

```bash
chmod +x https_comm.py
```

3. Create a symlink:

```bash
sudo ln -s ~/LobbyAdmin/https_comm.py /usr/local/bin/lobbyA
```

Or add a shebang to `https_comm.py`:

```python
#!/usr/bin/env python3
```

Then:

```bash
chmod +x https_comm.py
```

## Configuration

Edit `config.txt`:

```
host=YOUR_HOST
auth_user=BASE64_ENCODED_USERNAME
auth_pass=BASE64_ENCODED_PASSWORD
guest_wlan_id=28
```

Encode credentials to base64:

```bash
echo -n "your_username" | base64
echo -n "your_password" | base64
```

PowerShell:

```powershell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("your_username"))
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("your_password"))
```

## Usage

```bash
lobbyA -u username -p password -d "description"
```

### Options

| Flag | Required | Description |
|------|----------|-------------|
| `-u` | Yes | Guest username |
| `-p` | Yes | Guest password |
| `-d` | No | Guest description |

### Output

```
operation succeed
```
or
```
operation FAILED
```
