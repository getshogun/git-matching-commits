#!/usr/bin/env python3

# Modules
import argparse
import re
import os
import subprocess
from git import Repo
from github_action_utils import set_output

# Default values
DefaultStartTagPattern = 'v[0-9]+.[0-9]+.[0-9]+'
DefaultEndTagPattern = 'HEAD'
DefaultCommitMessagePattern = '.*'
Debug = False

# Arguments
parser = argparse.ArgumentParser(description='Match Git commits based on matching commit message')
parser.add_argument('--start_tag_pattern', type=str, help='Start tag pattern')
parser.add_argument('--end_tag_pattern', type=str, help='End tag pattern')
parser.add_argument('--commit_message_pattern', type=str, help='Commit message pattern')
args = parser.parse_args()

# Global variables
StartTagPattern = args.start_tag_pattern if (args.start_tag_pattern != None) else DefaultStartTagPattern
EndTagPattern = args.end_tag_pattern if (args.end_tag_pattern != None) else DefaultEndTagPattern
CommitMessagePattern = args.commit_message_pattern if (args.commit_message_pattern != None) else DefaultCommitMessagePattern

# Path to the Git repository
repo_path = '.'

# Open the Git repository
repo = Repo(repo_path)
git = repo.git

# Get most recent matching tags
start_tags = git.tag('--sort=committerdate', '--list', '{0}'.format(StartTagPattern)).split('\n')
start_tag = start_tags[-1]
tag = repo.tags[start_tag]
start_commit = tag.commit
end_tag = 'HEAD'
head = repo.head.commit
if Debug:
    print("start_tag={0}".format(start_tag))
    print("start_commit={0}".format(start_commit))
    print("end_tag={0}".format(end_tag))

# if EndTagPattern != 'HEAD':
#     end_tags = git.tag('--sort=committerdate', '--list', '{0}'.format(EndTagPattern))
#     end_tag = end_tags[-1]
if Debug:
    print("start_tag={0}".format(start_tag))
    print("end_tag={0}".format(end_tag))
    print("CommitMessagePattern={0}".format(CommitMessagePattern))

# Get all commits between the two tags (not including the start tag)
commits = list(repo.iter_commits('{0}..{1}'.format(start_tag, end_tag), reverse=True, paths=None, since=None, until=None, author=None, committer=None, message=None, name_only=False))
matched_commits = []
for commit in commits:
    if commit.hexsha == start_commit.hexsha:
        next # Skip start commit
    if re.search(CommitMessagePattern, commit.message):
        matched_commits.append(commit.hexsha)
    if commit.hexsha == head.hexsha:
        break

# Return matching commits
matching_commits = ','.join(matched_commits)
# os.environ['COMMITS'] = matching_commits
print("commits={0}".format(matching_commits))
# set_output('commits', matching_commits)
# os.system("echo commits={0} >> $GITHUB_OUTPUT'.format(matching_commits))

# End of file
