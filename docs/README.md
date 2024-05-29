# reldplayer
[![Documentation Status](https://readthedocs.org/projects/reldplayer/badge/?version=latest)](https://reldplayer.readthedocs.io/en/latest/?badge=latest)

**"Reimagined pyldplayer"**

`reldplayer` is a powerful Python library designed to extend and enhance the capabilities of the LDPlayer emulator. It offers advanced programmable control over emulator instances, allowing users to automate and customize their interactions efficiently.

## Features

- **Emulator Command Execution**: Launch LDConsole commands.
- **Window Management**: Resize, rearrange, and manage the state of emulator windows efficiently.
- **Configuration and Record Management**: Load and modify emulator configurations and records programmatically.
- **Interactive Controls**: Perform operations on emulator windows by mimicking keyboard and mouse events.
- **Advanced Querying**: Utilize robust querying capabilities to manage and interact with emulator instances dynamically.

## Installation

To install `reldplayer`, you can use pip to download it directly from PyPI:

```bash
pip install reldplayer
```

## Quick Start
Here is a simple example of how to use reldplayer to manage an emulator instance:
```python
from reldplayer import Player, PlayerConfig

# Initialize player with configuration
config = PlayerConfig(path="your_config_path")
player = Player(config)

# Select and manage emulator instances
player.select_actives()  # Select all active windows
print(player.query_instance("some_query"))  # Query instances based on criteria

# Perform actions on emulator instances
player.console.launch()
player.console.quitall()
```

## Contributing
Contributions are welcome! If you'd like to contribute, please fork the repository and use a new branch for your contributions.