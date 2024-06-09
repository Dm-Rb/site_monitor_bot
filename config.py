from configparser import ConfigParser


def read_ini_file(filename='config.ini', section=None) -> dict:
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)
    # get section, default to mysql
    data = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        for section in parser.sections():
            items = parser.items(section)
            for item in items:
                data[item[0]] = item[1]
    return data

