# reldplayer
reimagined pyldplayer

# install

```bash
pip install reldplayer
```
this package uses a lot of passive imports, you can use `pip install reldplayer[all]` to install all dependencies

# usage examples

## common examples
to launch and sort the instances utilizing the synchronizer
```py
player = Reldplayer(Config({PATH}))
player.synchronizer.setq([1, 2, 3, 4])
player.console.launch()
player.wndmgr.gridOrientation(gridStr="2X2")
```

traditional methods works too
```py
player = Reldplayer(Config({PATH}))
player.console.launch(1)
player.console.launch(2)
player.console.launch(3)
player.console.launch(4)
player.wndmgr.gridOrientation(gridStr="2X2")
```

## modify root status
```py
player = Reldplayer(Config({PATH}))
player.synchronizer.setq([1])
player.console.modify(root=True)
player.console.launch()
<do whatever you want>
```
> this is currently not available for LDPlayer 4 or below

# Acknowledgements
- [pdoc](https://pdoc3.github.io/pdoc) for documentation