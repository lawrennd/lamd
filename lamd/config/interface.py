import lynguine


class Interface(lynguine.config.interface.Interface):  # type: ignore
    @classmethod
    def default_config_file(cls) -> str:
        """
        Return the default configuration file name
        """
        return "_lamd.yml"
