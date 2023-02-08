# -*- coding: utf-8 -*-
import re
import os
import json
import argparse
import subprocess as sp

import httpx


ISSUE_PATTERN = re.compile(r'\[API\] New version: (?P<etag>.+)')
OPENAPI_URL = 'https://timeweb.cloud/api-docs-data/bundle.json'
argparser = argparse.ArgumentParser(description='Create issue about new API version.')
argparser.add_argument('etag', help='New API version etag.')
argparser.add_argument('--get-link', action='store_true', help='Print issue link and exit.', default=False)
argparser.add_argument('--issue-created', action='store_true', help='Print true or false, if issue created.')
argparser.add_argument('--run-url', type=str, help='Workflow run url', default='')


def create_github_issue(etag: str, body: str):
    cli = httpx.Client(
        headers={
            'Authorization': f'token {os.environ["GH_TOKEN"]}',
            'Accept': 'application/vnd.github.v3+json',
        }, base_url='https://api.github.com'
    )
    cli.post(
        '/repos/LulzLoL231/timeweb-cloud/issues',
        json={'title': f'[API] New version: {etag}', 'body': body, 'labels': ['timeweb.cloud']}
    )


def have_active_issue(etag: str) -> bool:
    list_issue = sp.check_output(
        ['gh', 'issue', 'list', '--json', 'title', '--label', 'timeweb.cloud', '--state', 'open']
    )
    list_issue_data: list[dict] = json.loads(list_issue.decode('utf-8'))
    for issue in list_issue_data:
        match = ISSUE_PATTERN.match(issue['title'])
        if match and match.group('etag') == etag.replace('"', ''):
            return True
    return False


def get_issue_link(etag: str) -> str:
    list_issue = sp.check_output(
        'gh issue list --json title,url --label timeweb.cloud --state open'.split(' ')
    )
    list_issue_data: list[dict] = json.loads(list_issue.decode('utf-8'))
    for issue in list_issue_data:
        match = ISSUE_PATTERN.match(issue['title'])
        if match and match.group('etag') == etag:
            return issue['url']
    return ''


def get_issue_body(run_url: str) -> str:
    resp = httpx.get(OPENAPI_URL)
    resp.raise_for_status()
    with open('bundle.json', 'wb') as f:
        f.write(resp.content)
    try:
        sp.check_output('git diff --no-color --no-index .github/api_check/current_bundle.json bundle.json'.split(' '))
    except sp.CalledProcessError as e:
        diff_data = e.output.decode('utf-8')
    return f'''New API version is available.
Workflow run: {run_url}

```diff
{diff_data}
```
'''


def create_issue(etag: str, run_url: str) -> None:
    create_github_issue(etag, get_issue_body(run_url))


if __name__ == '__main__':
    args = argparser.parse_args()

    if args.issue_created:
        print(have_active_issue(args.etag))
        exit(0)
    if args.get_link:
        print(get_issue_link(args.etag))
        exit(0)
    if not have_active_issue(args.etag):
        create_issue(args.etag, args.run_url)
        exit(0)
    print('[!] Issue already exists.')
