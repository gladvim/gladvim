import os
from pathlib import Path
from shutil import copy2 as copy, rmtree

from git import Repo

from . import util
from .DB import DB

OK = True
NOT_OK = False


class GladVim:
    REMOTE = 'https://github.com/gladvim'
    USER_HOME = Path(os.environ['HOME'])
    LOCAL = USER_HOME / '.gladvim'
    VIM = USER_HOME / '.vim'
    DB = LOCAL / 'gladvim.db'

    def __init__(self):
        self.db = None

        if GladVim.is_init():
            self.init_database()
        else:
            if not GladVim.LOCAL.exists():
                os.mkdir(GladVim.LOCAL)
                self.init_database(migrate=True)
            elif not GladVim.LOCAL.is_dir():
                util.fatal('cannot initialise local storage')

    def init_database(self, migrate=False):
        self.db = DB(self.DB)
        if migrate:
            self.db.migrate()

    def fetch(self, package):
        if self.db.fetched(package):
            return OK, 'already fetched'

        hash = GladVim.git_clone(package)
        flag = hash is not None

        if flag:
            if self.db.recorded(package):
                self.db.set_fetched(package)
            else:
                self.db.record(package, hash)
            return OK, None
        else:
            return NOT_OK, 'failed to clone'

    def remove(self, package):
        if not self.db.fetched(package):
            return OK, 'already removed'

        try:
            rmtree(GladVim.LOCAL / package)
            self.db.set_fetched(package, status=False)
            return OK, None
        except:
            return NOT_OK, 'failed to remove local files'

    def plug(self, package):
        if not self.db.fetched(package):
            return NOT_OK, 'not yet fetched'

        if self.db.plugged(package):
            return OK, 'already plugged in'

        self.plug_fetched(package)
        return OK, None

    def unplug(self, package):
        if not self.db.fetched(package):
            return NOT_OK, 'not yet fetched'

        if not self.db.plugged(package):
            return OK, 'already unplugged'

        self.unplug_fetched(package)
        return OK, None

    def plug_fetched(self, package):
        package_path = GladVim.LOCAL / package
        for feature_folder in os.listdir(package_path):
            feature_path = package_path / feature_folder
            if feature_path.is_dir() and feature_folder != '.git':
                vim_subdir = GladVim.VIM / feature_folder
                if not vim_subdir.exists():
                    os.mkdir(vim_subdir)
                GladVim.copy_all(feature_path, vim_subdir)

        self.db.set_plugged(package)

    def unplug_fetched(self, package):
        package_path = GladVim.LOCAL / package
        for feature_folder in os.listdir(package_path):
            feature_path = package_path / feature_folder
            if feature_path.is_dir() and feature_folder != '.git':
                vim_subdir = GladVim.VIM / feature_folder
                if not vim_subdir.exists():
                    continue
                GladVim.remove_all(vim_subdir, package)

        self.db.set_plugged(package, status=False)

    @staticmethod
    def git_clone(package):
        try:
            repo = Repo.clone_from(f'{GladVim.REMOTE}/{package}',
                                   GladVim.LOCAL / package)
            return repo.head.object.hexsha
        except:
            return None

    @staticmethod
    def is_init():
        return GladVim.is_existing_dir(GladVim.LOCAL)

    @staticmethod
    def is_existing_dir(path):
        return path.exists() and path.is_dir()

    @staticmethod
    def abs_listdir(path):
        return [path / child for child in os.listdir(path)]

    @staticmethod
    def copy_all(src_dir, trg_dir):
        for file in GladVim.abs_listdir(src_dir):
            copy(file, trg_dir)

    @staticmethod
    def remove_all(dir, basename):
        for filename in os.listdir(dir):
            if filename.startswith(basename):
                os.remove(dir / filename)
