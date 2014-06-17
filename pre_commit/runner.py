from __future__ import unicode_literals

import os
import os.path
from asottile.cached_property import cached_property

import pre_commit.constants as C
from pre_commit import git
from pre_commit.clientlib.validate_config import load_config
from pre_commit.repository import Repository
from pre_commit.store import Store


class Runner(object):
    """A `Runner` represents the execution context of the hooks.  Notably the
    repository under test.
    """

    def __init__(self, git_root):
        self.git_root = git_root

    @classmethod
    def create(cls):
        """Creates a PreCommitRunner by doing the following:
            - Finds the root of the current git repository
            - chdirs to that directory
        """
        root = git.get_root()
        os.chdir(root)
        return cls(root)

    @cached_property
    def config_file_path(self):
        return os.path.join(self.git_root, C.CONFIG_FILE)

    @cached_property
    def repositories(self):
        """Returns a tuple of the configured repositories."""
        config = load_config(self.config_file_path)
        return tuple(Repository.create(x, self.store) for x in config)

    @cached_property
    def pre_commit_path(self):
        return os.path.join(self.git_root, '.git', 'hooks', 'pre-commit')

    @cached_property
    def pre_commit_legacy_path(self):
        """The path in the 'hooks' directory representing the temporary
        storage for existing pre-commit hooks.
        """
        return self.pre_commit_path + '.legacy'

    @cached_property
    def cmd_runner(self):
        # TODO: remove this and inline runner.store.cmd_runner
        return self.store.cmd_runner

    @cached_property
    def store(self):
        return Store()
