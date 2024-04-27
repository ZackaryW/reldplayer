class MetaContainer:
    def __init__(self, path : str, matchtype : str = "*", model = None):
        assert model is not None
        self.__path = path
        self.__model = model
        self.__matchtype = matchtype

        self.__cache = {}

    

class MetaMgr:
    def __init__(self, path : str):
        self.__path = path
    
    @property
    def configPath(self):
        return os.path.join(self.__path, "vms", "config")

    @property
    def customizeConfigsPath(self):
        return os.path.join(self.__path, "vms", "customizeConfigs")
    
    @property
    def operationRecordsPath(self):
        return os.path.join(self.__path, "vms", "operationRecords")

    @property
    def recommendConfigsPath(self):
        return os.path.join(self.__path, "vms", "recommendConfigs")

    @cached_property
    def hostConfigs(self):
        return MetaContainer(self.configPath,"leidians.config", model=LeidiansCfg)

    @cached_property
    def configs(self):
        return MetaContainer(self.configPath, "ledian{id}.config", model=LeidianCfg)
    
    @cached_property
    def customizedKmps(self):
        return MetaContainer(self.customizeConfigsPath, "*.kmp", KMP)
    
    @cached_property
    def recommendedKmps(self):
        return MetaContainer(self.recommendConfigsPath, "*.kmp", KMP)
    
    @cached_property
    def operationRecords(self):
        return MetaContainer(self.operationRecordsPath, "*.kmp", model=KMP)
    

