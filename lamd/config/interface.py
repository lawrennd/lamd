import lynguine

class Interface(lynguine.config.interface.Interface):
    @classmethod
    def default_config_file(cls):
        """
        Return the default configuration file name
        """
        return "_lamd.yml"
    
