#
# Command line tools.
#
# This file is part of GDE.
# See https://github.com/MichaelClerx/gde for sharing, and licensing details.
#
import argparse
import sys


def template(text, terms):
    """Extremely simple templating"""

    for k, v in terms.items():
        text = text.replace('{{' + k + '}}', v)
    return text


def main():
    """
    Parses command line arguments.
    """

    # Create parser
    parser = argparse.ArgumentParser(
        usage='gde',
        description='Command line tools for gde.',
    )
    subparsers = parser.add_subparsers(
        description='Select one of the available commands from the list below',
        title='Commands',
    )

    # Add subparsers
    add_gui_parser(subparsers)      # Launch the graph data extractor
    add_icon_parser(subparsers)     # Install icons
    add_reset_parser(subparsers)    # Remove config dir
    add_version_parser(subparsers)  # Install

    # Show help if no command given
    if len(sys.argv) == 1:
        gui(None)
        return

    # Parse!
    args = parser.parse_args()

    # Get the args' objects attributes as a dictionary
    args = vars(args)

    # Split into function and arguments
    func = args['func']
    del(args['func'])

    # Call the selected function with the parsed arguments
    func(**args)


#
# GDE
#

def gui(filename):
    """
    Runs the graph data extractor.
    """
    import gde
    gde.qt.run(gde.gui.GraphDataExtractor, filename)


def add_gui_parser(subparsers):
    """
    Adds a subcommand parser for the ``gui`` command.
    """
    parser = subparsers.add_parser(
        'gui',
        description='Runs the graph data extractor graphical user interface.',
        help='Runs the graph data extractor graphical user interface.',
    )
    parser.add_argument(
        'filename',
        default=None,
        nargs='?',
        metavar='filename',
        help='The gde file to open (optional).',
    )
    parser.set_defaults(func=gui)


#
# Icons / installation
#

def install():
    """
    Installs icons.
    """
    import platform

    plat = platform.system()
    if plat == 'Linux':
        yesno = \
            'Install launcher icons and file type associations for Gnome/KDE? '
        try:
            yesno = raw_input(yesno)
        except NameError:   # pragma: no python 2 cover
            yesno = input(yesno)
        yesno = (yesno.strip().lower())[:1] == 'y'

        if yesno:
            install_gnome_kde()

    elif plat == 'Windows':
        yesno = 'Install start menu shortcuts? '
        try:
            yesno = raw_input(yesno)
        except NameError:   # pragma: no python 2 cover
            yesno = input(yesno)
        yesno = (yesno.strip().lower())[:1] == 'y'

        if yesno:
            install_windows()

    elif plat == 'Darwin':
        print(
            'Icons for OS/X are not available (yet).')

    else:
        print('Unknown platform: ' + plat)
        print('Icons not available.')


def install_gnome_kde():
    """
    Installs launchers and associates file types for gnome/kde systems.
    """
    import os
    import shutil
    import subprocess

    import gde

    # Get user home dir
    home = os.path.expanduser('~')

    # Get template directory
    dir_templates = os.path.join(gde.DIR_DATA, 'install-lin')

    # Get icon directory
    dir_icons = os.path.join(gde.DIR_DATA, 'gui')

    # Copies file and creates directory structure
    def place_file(path, name, tpl=False):
        print('Placing ' + str(name) + ' in ' + str(path))

        orig = os.path.join(dir_templates, name)
        dest = os.path.join(path, name)
        if not os.path.exists(orig):
            print('Error: file not found ' + orig)
            sys.exit(1)
        if os.path.exists(path):
            if not os.path.isdir(path):
                print(
                    'Error: Cannot create output directory. A file exists at '
                    + path)
                sys.exit(1)
        else:
            print('  Creating directory structure: ' + path)
            os.makedirs(path)

        if tpl:
            # Process templates, create files
            with open(orig, 'r') as f:
                source = f.read()

            varmap = {
                'icons': dir_icons,
                'python': sys.executable,
            }

            with open(dest, 'w') as f:
                f.write(template(source, varmap))
        else:
            shutil.copyfile(orig, dest)

    # Desktop files
    print('Installing desktop files...')
    path = os.path.join(home, '.local', 'share', 'applications')
    place_file(path, 'gde.desktop', True)

    # Mime-type file
    print('Installing mmt mime-type...')
    path = os.path.join(home, '.local', 'share', 'mime', 'packages')
    print('Installing gde mime-type...')
    place_file(path, 'x-gde.xml')

    # Reload mime database
    print('Reloading mime database')
    path = os.path.join(home, '.local', 'share', 'mime')
    subprocess.call(['update-mime-database', path])

    print('Done')


def install_windows():
    """
    Install start-menu icons on windows systems.
    """
    import platform
    if platform.system() != 'Windows':
        raise Exception('Not a windows machine.')

    import os
    import tempfile

    import gde
    import menuinst

    # Process template to get icon directory
    tdir = tempfile.mkdtemp()
    try:
        source = os.path.join(gde.DIR_DATA, 'install-win', 'menu.json')
        with open(source, 'r') as f:
            source = f.read()

        varmap = {'icons': os.path.join(gde.DIR_DATA, 'gui')}

        output = os.path.join(tdir, 'menu.json')
        with open(output, 'w') as f:
            f.write(template(source, varmap))
        del(p)

        # Install
        menuinst.install(output)
        print('Done')

    finally:
        gde.rmtree(tdir)


def add_icon_parser(subparsers):
    """
    Adds a subcommand parser for the ``icons`` command.
    """
    parser = subparsers.add_parser(
        'icons',
        description='Installs launchers / start menu shortcuts for GDE.',
        help='Installs launchers / start menu shortcuts for GDE.',
    )
    parser.set_defaults(func=install)


#
# Reset
#

def reset(force=False):
    """
    Removes all GDE settings files.
    """
    import sys
    import gde

    # Ask user if settings should be deleted
    if force:
        remove = True
    else:
        yesno = input('Remove all GDE settings files? ')
        yesno = yesno.strip().lower()
        remove = (yesno[:1] == 'y')
    if not remove:
        print('Aborting.')
        sys.exit(1)
    del(force, remove)

    print('Removing config directory:')
    print('  ' + gde.DIR_USER)
    gde.rmtree(gde.DIR_USER)
    print('Done')


def add_reset_parser(subparsers):
    """
    Adds a subcommand parser for the ``reset`` command.
    """
    parser = subparsers.add_parser(
        'reset',
        description='Removes all GDE settings files, resetting it to its'
                    ' default configuration.',
        help='Removes all GDE settings files.',
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Delete without prompting the user first.',
    )
    parser.set_defaults(func=reset)


#
# Version
#

def version():
    """ Show the version number. """
    import gde
    print(gde.version())


def add_version_parser(subparsers):
    """
    Adds a subcommand parser for the ``version`` command.
    """
    parser = subparsers.add_parser(
        'version',
        description='Prints GDE\'s version number.',
        help='Prints GDE\'s version number.',
    )
    parser.set_defaults(func=version)


if __name__ == '__main__':
    main()
