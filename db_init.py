import configparser

def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Database")
    config.set("Database", "hostname", "localhost")
    config.set("Database", "databasename", "pokedex")
    config.set("Database", "username", "root")
    config.set("Database", "password","kH8m!HCkQ")
    
    with open(path, "w") as config_file:
        config.write(config_file)

createConfig ("server.config")