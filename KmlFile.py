""" Module for playing with KML files. """

import os
import re
import linecache

def lazyproperty(func):
    """Decorator for lazy evaluation of properties."""
    attr_name = '_lazy_' + func.__name__
    @property
    def _lazyproperty(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return _lazyproperty

class KmlFile(object):
    """Object for manipulating a kml file"""

    WHEN = re.compile(r"<when>(?P<when>[0-9\.\-\s\:A-Z]*)</when>")
    COORD = re.compile(r"<gx:coord>(?P<coord>[0-9\.\-\s\:]*)</gx:coord>")

    def __init__(self, file_name):
        """Creates the kml file Object

        Params:
            - file_name - The name of the KML file.
        """
        if not os.path.isfile(file_name):
            raise ValueError("File does not exist: {}".format(file_name))
        self.file_name = file_name

    @lazyproperty
    def num_entries(self):
        """The number of GPX entries."""
        with open(self.file_name, 'r') as kml_file:
            count = 0
            for line in kml_file:
                if KmlFile.WHEN.match(line):
                    count += 1
        return count

    @lazyproperty
    def first_line_number(self):
        """The line number for the first GPX entry."""
        with open(self.file_name, 'r') as kml_file:
            line_number = 0
            for line in kml_file:
                line_number += 1
                if KmlFile.WHEN.match(line):
                    break
        return line_number

    @property
    def last_line_number(self):
        """The line number for the last GPX entry."""
        return (self.num_entries - 1) * 2 + self.first_line_number

    @property
    def first_entry(self):
        """The first GPX entry."""
        return self.get_entry(self.first_line_number)

    @property
    def last_entry(self):
        """The last GPX entry."""
        return self.get_entry(self.last_line_number)

    @property
    def entries(self):
        """Generator for all the GPX entries."""
        return (self.get_entry(line_number) for line_number in
                range(self.first_line_number, self.last_line_number + 1,
                      2))

    def get_entry(self, line_number):
        """Gets a GPX entry from the specified line."""
        r_when = KmlFile.WHEN.match(
            linecache.getline(self.file_name, line_number))
        r_coord = KmlFile.COORD.match(
            linecache.getline(self.file_name, line_number + 1))
        if r_when is None or r_coord is None:
            raise LookupError("GPX entry in {} not found on this line:"
                " {}".format(self.file_name, line_number))
        return r_when.groupdict()["when"], r_coord.groupdict()["coord"]


if __name__ == "__main__":
    test = KmlFile('history-10-30-2013.kml')
    print test.num_entries
    print test.first_entry
    print test.last_entry
    entries = test.entries
    print entries.next()
    print entries.next()
    print entries.next()
