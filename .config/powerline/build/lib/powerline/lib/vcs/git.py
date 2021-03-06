import os
import re

from powerline.lib.vcs import get_branch_name, get_file_status
from powerline.lib.shell import readlines
from powerline.lib.path import join
from powerline.lib.encoding import (get_preferred_file_name_encoding,
                                    get_preferred_file_contents_encoding)
from powerline.lib.shell import which
from powerline.lib.vcs import BaseRepository


_ref_pat = re.compile(br'ref:\s*refs/heads/(.+)')


def branch_name_from_config_file(directory, config_file):
    try:
        with open(config_file, 'rb') as f:
            raw = f.read()
    except EnvironmentError:
        return os.path.basename(directory)
    m = _ref_pat.match(raw)
    if m is not None:
        return m.group(1).decode(get_preferred_file_contents_encoding(), 'replace')
    # FIXME Use proper abbreviation length
    return raw[:7]


def git_directory(directory):
    path = join(directory, '.git')
    if os.path.isfile(path):
        with open(path, 'rb') as f:
            raw = f.read()
            if not raw.startswith(b'gitdir: '):
                raise IOError('invalid gitfile format')
            raw = raw[8:]
            if raw[-1:] == b'\n':
                raw = raw[:-1]
            if not isinstance(path, bytes):
                raw = raw.decode(get_preferred_file_name_encoding())
            if not raw:
                raise IOError('no path in gitfile')
            return os.path.abspath(os.path.join(directory, raw))
    else:
        return path

def increase(dict, key):
    if not key in dict:
        dict[key] = 1
    else:
        dict[key] += 1

class GitRepository(BaseRepository):
    def status_string(self, path=None):
        '''Return status of repository or file.

        Without file argument: returns status of the repository:

        :First column: working directory status (D: dirty / space)
        :Second column: index status (I: index dirty / space)
        :Third column: presence of untracked files (U: untracked files / space)
        :None: repository clean

        With file argument: returns status of this file. Output is
        equivalent to the first two columns of ``git status --porcelain``
        (except for merge statuses as they are not supported by libgit2).
        '''
        if path:
            gitd = git_directory(self.directory)
            # We need HEAD as without it using fugitive to commit causes the
            # current file’s status (and only the current file) to not be updated
            # for some reason I cannot be bothered to figure out.
            return get_file_status(
                directory=self.directory,
                dirstate_file=join(gitd, 'index'),
                file_path=path,
                ignore_file_name='.gitignore',
                get_func=self.do_status,
                create_watcher=self.create_watcher,
                extra_ignore_files=tuple(join(gitd, x) for x in ('logs/HEAD', 'info/exclude')),
            )
        return self.do_status(self.directory, path)

    @property
    def branch(self):
        directory = git_directory(self.directory)
        head = join(directory, 'HEAD')
        return get_branch_name(
            directory=directory,
            config_file=head,
            get_func=branch_name_from_config_file,
            create_watcher=self.create_watcher,
        )

    ICON_DICT = {
        'AHEAD': '⇡',
        'BEHIND': '⇣',
        'MODIFIED': '✎',
        'STAGED': '●',
        'CONFLICTING': '✗',
        'UNTRACKED': '…',
        'CLEAN': '✔'
    }
    @property
    def status(self):
        useful_res = self.get_useful_status()

        res = []
        for key in ['STAGED', 'CONFLICTING', 'MODIFIED']:
            if key in useful_res:
                res += [self.ICON_DICT[key] + ' ' + str(useful_res[key])]
        if 'UNTRACKED' in useful_res:
            res += [self.ICON_DICT['UNTRACKED']]
        if len(res) == 0:
            res = self.ICON_DICT['CLEAN']
        return res

    @property
    def ahead_behind(self):
        a_b = self.do_ahead_behind()

        res = []
        for k in ['AHEAD', 'BEHIND']:
            if k in a_b and a_b[k]:
                res += [self.ICON_DICT[k] + ' ' + str(a_b[k])]
        return res

    @property
    def bookmark(self):
        return self.branch
try:
    import pygit2 as git

    class Repository(GitRepository):
        @staticmethod
        def ignore_event(path, name):
            return False

        @property
        def stash(self):
            try:
                stashref = git.Repository(git_directory(self.directory)).lookup_reference('refs/stash')
            except KeyError:
                return []
            return [str(sum(1 for _ in stashref.log()))]
        def _repo(self, directory=None):
            return git.Repository(directory or self.directory)

        def do_status(self, directory, path):
            if path:
                try:
                    status = self._repo(directory).status_file(path)
                except (KeyError, ValueError):
                    return None

                if status == git.GIT_STATUS_CURRENT:
                    return None
                else:
                    if status & git.GIT_STATUS_WT_NEW:
                        return '??'
                    if status & git.GIT_STATUS_IGNORED:
                        return '!!'

                    if status & git.GIT_STATUS_INDEX_NEW:
                        index_status = 'A'
                    elif status & git.GIT_STATUS_INDEX_DELETED:
                        index_status = 'D'
                    elif status & git.GIT_STATUS_INDEX_MODIFIED:
                        index_status = 'M'
                    else:
                        index_status = ' '

                    if status & git.GIT_STATUS_WT_DELETED:
                        wt_status = 'D'
                    elif status & git.GIT_STATUS_WT_MODIFIED:
                        wt_status = 'M'
                    else:
                        wt_status = ' '

                    return index_status + wt_status
            else:
                wt_column = ' '
                index_column = ' '
                untracked_column = ' '
                for status in git.Repository(directory).status().values():
                    if status & git.GIT_STATUS_WT_NEW:
                        untracked_column = 'U'
                        continue

                    if status & (git.GIT_STATUS_WT_DELETED | git.GIT_STATUS_WT_MODIFIED):
                        wt_column = 'D'

                    if status & (
                        git.GIT_STATUS_INDEX_NEW
                        | git.GIT_STATUS_INDEX_MODIFIED
                        | git.GIT_STATUS_INDEX_DELETED
                    ):
                        index_column = 'I'
                r = wt_column + index_column + untracked_column
                return r if r != '   ' else None

        def get_useful_status(self):
            res = {}

            for status in self._repo().status().values():
                if status & git.GIT_STATUS_WT_NEW:
                    res['UNTRACKED'] = 1
                if status & (
                    git.GIT_STATUS_WT_MODIFIED
                    | git.GIT_STATUS_WT_DELETED
                ):
                    increase(res, 'MODIFIED')
                if status & git.GIT_STATUS_CONFLICTED:
                    increase(res, 'CONFLICTING')
                if status & (
                    git.GIT_STATUS_INDEX_NEW
                    | git.GIT_STATUS_INDEX_MODIFIED
                    | git.GIT_STATUS_INDEX_DELETED
                ):
                    increase(res, 'STAGED')
            return res

        def do_ahead_behind(self):
            res = (0, 0)
            repo = self._repo()

            try:
                res = repo.ahead_behind(repo.head.target, repo.revparse_single('@{upstream}').hex)
            except KeyError:
                res = (0, 0)
            return {'AHEAD': res[0], 'BEHIND': res[1]}

        @property
        def short(self):
            #TODO: Don't fix the length of the prefix
            return self._repo().head.target.hex[:7]

        @property
        def summary(self):
            repo = self._repo()
            commit = repo[repo.head.target]
            description = commit.message
            try:
                # Command `git log --format=%s` treats commit like
                # `l1\nl2\n\nl4` as having description `l1 l2`.
                return description[:description.index('\n\n')].replace('\n', ' ').strip()
            except ValueError:
                return description.replace('\n', ' ').strip()

        @property
        def name(self):
            return self.branch
except ImportError:
    class Repository(GitRepository):
        def __init__(self, *args, **kwargs):
            if not which('git'):
                raise OSError('git executable is not available')
            super(Repository, self).__init__(*args, **kwargs)

        @staticmethod
        def ignore_event(path, name):
            # Ignore changes to the index.lock file, since they happen
            # frequently and dont indicate an actual change in the working tree
            # status
            return path.endswith('.git') and name == 'index.lock'

        def gitcmd(self, *args, **kwargs):
            return readlines(('git',) + args, kwargs.get('directory', self.directory))

        def getgitline(self, *args, **kwargs):
            try:
                return next(self.gitcmd(*args, **kwargs)).rstrip('\n')
            except StopIteration:
                return None

        @property
        def stash(self):
            stcnt = sum(1 for _ in self.gitcmd(self.directory, 'stash', 'list'))
            return [str(stcnt)] if stcnt else []

        def do_status(self, directory, path):
            if path:
                try:
                    return next(self.gitcmd('status', '--porcelain', '--ignored', '--', path, directory=directory))[:2]
                except StopIteration:
                    return None
            else:
                wt_column = ' '
                index_column = ' '
                untracked_column = ' '
                for line in self.gitcmd('status', '--porcelain', directory=directory):
                    if line[0] == '?':
                        untracked_column = 'U'
                        continue
                    elif line[0] == '!':
                        continue

                    if line[0] != ' ':
                        index_column = 'I'

                    if line[1] != ' ':
                        wt_column = 'D'

                r = wt_column + index_column + untracked_column
                return r if r != '   ' else None


        def get_useful_status(self):
            res = {}
            for line in self.gitcmd('status', '--porcelain'):
                if line[0] == '?':
                    res['UNTRACKED'] = 1
                    continue
                if line[0] == '!':
                    continue
                if line[:2] in ('DD', 'AU', 'UD', 'UA', 'DU', 'AA', 'UU'):
                    increase(res, 'CONFLICTING')
                else:
                    if line[0] != ' ':
                        increase(res, 'STAGED')
                    if line[1] != ' ':
                        increase(res, 'MODIFIED')
            return res

        def do_ahead_behind(self):
            res = [int(e) for e in self.getgitline('rev-list', '--left-right', '--count', 'HEAD...@{upstream}').split()]
            return {'AHEAD': res[0], 'BEHIND': res[1]}

        @property
        def short(self):
            return self.getgitline('rev-parse', '--short', 'HEAD')

        @property
        def summary(self):
            return self.getgitline('log', '--max-count=1', '--format=%s')

        @property
        def name(self):
            return self.getgitline(
                'name-rev', '--name-only', '--no-undefined', '--always', 'HEAD').strip()
