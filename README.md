# reldplayer
reimagined pyldplayer

# install

```bash
pip install reldplayer
```

# usage
example
```py
# instantiate using factory descriptor
r = ReLDPlayer.factory

# make a query using pythonic syntax
instances = r.query("q['name'].startswith('{name}')", returnIds=True)

# set batch applied instances
r.currentApplied = instances

# launch them all
r.console.launch()

# wait till all of them are loaded
r.waitTillBatchLoaded()
sleep(5)

# set orientation
r.wndMgr.quickGrid("2X2", monitor=3)

# set primary instance and open synchronizer
r.autogui.setPrimary(name="{name}").synchronizer()

```