import os
import time
import git


class RepoWatcher:
    def __init__(self, repo_path, callback_fn):
        self.repo_path = repo_path
        self.callback_fn = callback_fn
        self.repo = git.Repo(self.repo_path)
        self.repo.git.update_environment(GIT_WORK_TREE=self.repo_path)
        self.modified_files = set()

    def _get_file_contents(self, commit, path):
        """Get the contents of a file at a given commit."""
        contents = commit.tree[path].data_stream.read().decode()
        return contents

    def _process_commit(self, commit):
        """Process a given commit."""
        for modified_file in commit.stats.files.keys():
            if modified_file.endswith(".py"):
                old_contents = self._get_file_contents(commit.parents[0], modified_file)
                new_contents = self._get_file_contents(commit, modified_file)
                if old_contents != new_contents:
                    if modified_file not in self.modified_files:
                        self.modified_files.add(modified_file)
                        self.callback_fn(old_contents, new_contents)

    def start_watching(self):
        """Start watching the repository for changes."""
        while True:
            self.repo.remotes.origin.fetch()
            origin_head = self.repo.head.reference
            self.repo.git.reset("--hard", origin_head)
            self._process_commit(self.repo.head.commit)
            time.sleep(1)