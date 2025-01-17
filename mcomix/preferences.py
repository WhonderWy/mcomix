""" preferences.py - Contains the preferences and the functions to read and
write them.  """

import json
import os
import pickle
import shutil
import sys

from mcomix import constants

# All the preferences are stored here.
prefs = {
    'comment extensions': constants.ACCEPTED_COMMENT_EXTENSIONS,
    'auto load last file': False,
    'page of last file': 1,
    'path to last file': '',
    'number of key presses before page turn': 3,
    'auto open next archive': True,
    'auto open next directory': True,
    'open first file in prev archive': False,
    'open first file in prev directory': False,
    'sort by': constants.SORT_NAME,  # Normal files obtained by directory listing
    'sort order': constants.SORT_ASCENDING,
    'sort archive by': constants.SORT_NAME,  # Files in archives
    'sort archive order': constants.SORT_ASCENDING,
    'bg colour': [5000, 5000, 5000],
    'thumb bg colour': [5000, 5000, 5000],
    'smart bg': False,
    'smart thumb bg': False,
    'thumbnail bg uses main colour': False,
    'checkered bg for transparent images': True,
    'cache': True,
    'stretch': False,
    'default double page': False,
    'default fullscreen': False,
    'zoom mode': constants.ZoomMode.BEST,
    'default manga mode': False,
    'lens magnification': 2,
    'lens size': 200,
    'virtual double page for fitting images': constants.SHOW_DOUBLE_AS_ONE_TITLE | \
                                              constants.SHOW_DOUBLE_AS_ONE_WIDE,
    'double step in double page mode': True,
    'show page numbers on thumbnails': True,
    'thumbnail size': 80,
    'create thumbnails': True,
    'archive thumbnail as icon' : False,
    'number of pixels to scroll per key event': 50,
    'number of pixels to scroll per mouse wheel event': 50,
    'slideshow delay': 3000,
    'slideshow can go to next archive': True,
    'number of pixels to scroll per slideshow event': 50,
    'smart scroll': True,
    'invert smart scroll': False,
    'smart scroll percentage': 0.5,
    'flip with wheel': True,
    'store recent file info': True,
    'hide all': False,
    'hide all in fullscreen': True,
    'stored hide all values': [True, True, True, True, True],
    'path of last browsed in filechooser': constants.HOME_DIR,
    'store last saved in directory': True,
    'path of last saved in filechooser': constants.HOME_DIR,
    'last filter in main filechooser': 0,
    'last filter in library filechooser': 1,
    'show menubar': True,
    'previous quit was quit and save': False,
    'show scrollbar': True,
    'show statusbar': True,
    'show toolbar': True,
    'show thumbnails': True,
    'rotation': 0,
    'auto rotate from exif': True,
    'auto rotate depending on size': constants.AUTOROTATE_NEVER,
    'vertical flip': False,
    'horizontal flip': False,
    'keep transformation': False,
    'stored dialog choices': {},
    'brightness': 1.0,
    'contrast': 1.0,
    'saturation': 1.0,
    'sharpness': 1.0,
    'auto contrast': False,
    'invert color': False,
    'max pages to cache': 7,
    'window x': 0,
    'window y': 0,
    'window height': 600,
    'window width': 640,
    'window maximized': False,
    'pageselector height': -1,
    'pageselector width': -1,
    'library cover size': 125,
    'last library collection': None,
    'lib window height': 600,
    'lib window width': 500,
    'lib sort key': constants.SORT_PATH,
    'lib sort order': constants.SORT_ASCENDING,
    'language': 'auto',
    'statusbar fields': constants.STATUS_PAGE | constants.STATUS_RESOLUTION | \
                        constants.STATUS_PATH | constants.STATUS_FILENAME | constants.STATUS_FILESIZE,
    'max threads': 3,
    'max extract threads': 1,
    'wrap mouse scroll': False,
    'scaling quality': 2,  # GdkPixbuf.InterpType.BILINEAR
    'escape quits': False,
    'fit to size width wide': 3790,
    'fit to size height wide': 960,
    'fit to size width other': 1450,
    'fit to size height other': 1800,
    'scan for new books on library startup': True,
    'openwith commands': [],  # (label, command) pairs
    'animation mode': constants.ANIMATION_NORMAL,
    'double page autoresize': constants.DOUBLE_PAGE_AUTORESIZE_SIZE,
    'space between two pages': 2,
    "mouse click flip page": False,
}


def migrate_home_config_path() -> None:
    """ Migrate the old configuration directory in the user's
    home directory to %APPDATA% on Win32, if the directory
    doesn't already exist. """
    if sys.platform == "win32":
        old_config_dir = os.path.join(os.path.expanduser("~"), "MComix")
        if os.path.isdir(old_config_dir) and not os.path.isdir(constants.CONFIG_DIR):
            shutil.move(old_config_dir, constants.CONFIG_DIR)


def read_preferences_file() -> None:
    """Read preferences data from disk."""

    saved_prefs = None

    migrate_home_config_path()

    if os.path.isfile(constants.PREFERENCE_PATH):
        try:
            config_file = open(constants.PREFERENCE_PATH, 'r')
            saved_prefs = json.load(config_file)
            config_file.close()
        except:
            # Gettext might not be installed yet at this point.
            corrupt_name = "%s.broken" % constants.PREFERENCE_PATH
            print(('! Corrupt preferences file, moving to "%s".' %
                   corrupt_name))
            if os.path.isfile(corrupt_name):
                os.unlink(corrupt_name)

            try:
                # File cannot be moved without closing it first
                config_file.close()
            except:
                pass

            os.rename(constants.PREFERENCE_PATH, corrupt_name)

    elif os.path.isfile(constants.PREFERENCE_PICKLE_PATH):
        try:
            config_file = open(constants.PREFERENCE_PICKLE_PATH, 'rb')
            version = pickle.load(config_file)
            saved_prefs = pickle.load(config_file)
            config_file.close()

            # Remove legacy format preferences file
            os.unlink(constants.PREFERENCE_PICKLE_PATH)
        except Exception:
            # Gettext might not be installed yet at this point.
            print(('! Corrupt legacy preferences file "%s", ignoring...' %
                   constants.PREFERENCE_PICKLE_PATH))

    if saved_prefs:
        for key in saved_prefs:
            if key in prefs:
                prefs[key] = saved_prefs[key]

def write_preferences_file():
    """Write preference data to disk."""
    # TODO: it might be better to save only those options that were (ever)
    # explicitly changed by the used, leaving everything else as default
    # and available (if really needed) to change of defaults on upgrade.
    config_file = open(constants.PREFERENCE_PATH, 'w')
    # XXX: constants.VERSION? It's *preferable* to not complicate the YAML
    # file by adding a `{'version': constants.VERSION, 'prefs': config}`
    # dict or a list.  Adding an extra init line sounds bad too.
    json.dump(prefs, config_file, indent=2)
    config_file.close()

# vim: expandtab:sw=4:ts=4
