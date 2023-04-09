"""
    TranslatedEnglish Dat class to parse different types of dat files.
"""
import json
import os
from pathlib import Path
import re
import pathlib

from datero.repositories.dat import XMLDatFile, DirMultiDatFile


def getMameDatFactory(file: str):
    """ Dat factory. """
    ext = pathlib.Path(file).suffix
    if ext in ('.dat', '.xml'):
        return MameDat
    if os.path.isdir(file):
        return MameDirDat


def get_version(s):
    search = re.findall(r'0\.[0-9]*[\.[0-9]*]?', s)
    if search:
        return search[-1]
    return None


def remove_extra_spaces(s):
    return re.sub(' +', ' ', s)


class MameDirDat(DirMultiDatFile):

    def initial_parse(self):
        # pylint: disable=R0801
        """ Parse the dat file. """

        self.company = None
        self.system = 'MAME'
        self.suffix = None
        self.preffix = 'Arcade'
        self.version = get_version(self.file)

        if 'Update' in self.file:
            self.suffix = 'Update'
        else:
            self.name = remove_extra_spaces(self.name.replace(self.version, ''))

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


class MameDat(XMLDatFile):

    def initial_parse(self):
        # pylint: disable=R0801
        """ Parse the dat file. """

        self.company = None
        self.system = 'MAME'
        self.suffix = None
        self.preffix = 'Arcade'
        self.version = get_version(self.file)

        if 'Update' in self.file:
            self.suffix = 'Update'
        else:
            self.name = remove_extra_spaces(self.name.replace(self.version, ''))
        if 'dir2dat' in self.file and 'dir2dat' not in self.name:
            self.name = f'{self.name} (dir2dat)'

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


class HomeBrewMameDat(XMLDatFile):

    def initial_parse(self):
        # pylint: disable=R0801
        """ Parse the dat file. """

        self.company = None
        self.system = 'HBMAME'
        self.suffix = None
        self.preffix = 'Arcade'
        self.version = get_version(self.file)

        if 'Update' in self.file:
            self.suffix = 'Update'
        else:
            self.name = remove_extra_spaces(self.name.replace(self.version, ''))
        if 'dir2dat' in self.file and 'dir2dat' not in self.name:
            self.name = f'{self.name} (dir2dat)'

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


class FruitMachinesDat(XMLDatFile):

    def load_metadata_file(self):
        basedir = Path(self.file).parents[0]
        filename = os.path.join(basedir, 'metadata.txt')
        if os.path.exists(filename):
            with open(filename) as f:
                metadata = json.load(f)
        return metadata


    def initial_parse(self):
        # pylint: disable=R0801
        """ Parse the dat file. """
        name = self.name
        extra_data = self.load_metadata_file()

        name = name.split('(')[0].strip()
        if 'Layouts' in self.file:
            self.suffix = 'Layouts'

        self.company = 'Fruit'
        self.system = extra_data['folder']

        self.preffix = 'Arcade'

        return [self.preffix, self.company, self.system, self.suffix, self.get_date()]


    def get_date(self):
        """ Get the date from the dat file. """
        if self.file and '(' in self.file:
            s = self.file
            self.date = s[s.find("(")+1:s.find(")")]
        return self.date
