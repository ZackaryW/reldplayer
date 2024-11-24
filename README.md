# reldplayer
a superset to [pyldplayer](https://github.com/ZackaryW/pyldplayer)

## Install
```bash
pip install reldplayer
```
to install an older version:
```bash
pip install reldplayer==0.2.1
```
to install optional dependencies:
```bash
pip install reldplayer[full]
```

## Features
1. Provides additional overloading to obtain LDPlayer path
2. `LDWindowMgr` and `LDWindow` helpes to quickly associate a window to a LDPlayer instance
3. a cli tool to quickly interact with LDPlayer

## CLI Usage
```bash
reldplay -q "[1,2,3]"           # to select 3 instances in id
reldplay --name "test"          # to select instance named "test"
reldplay --name "test*"         # to select instance with pattern "test*"
```
for full list of commands, run `reldplay` without any arguments
