import re

def sub_string(string, start, end):
    """
    Retrieve substring of a string between specified start and end
    """
    return re.search('%s(.*)%s' % (start, end), string).group(1)