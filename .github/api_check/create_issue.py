# -*- coding: utf-8 -*-
import re
import json
import argparse
import subprocess as sp

import httpx


ISSUE_PATTERN = re.compile(r'\[API\] New version: (?P<etag>.+)')
OPENAPI_URL = 'https://timeweb.cloud/api-docs-data/bundle.json'
argparser = argparse.ArgumentParser(description='Create issue about new API version.')
argparser.add_argument('etag', help='New API version etag.')
argparser.add_argument('--get-link', action='store_true', help='Print issue link and exit.', default=False)
args = argparser.parse_args()


def have_active_issue(etag: str) -> bool:
    list_issue = sp.check_output(
        ['gh', 'issue', 'list', '--json', 'title', '--label', 'timeweb.cloud', '--state', 'open']
    )
    list_issue_data: list[dict] = json.loads(list_issue.decode('utf-8'))
    for issue in list_issue_data:
        match = ISSUE_PATTERN.match(issue['title'])
        if match and match.group('etag') == etag:
            return True
    return False


def get_issue_link(etag: str) -> str:
    list_issue = sp.check_output(
        ['gh', 'issue', 'list', '--json', 'title,url',
            '--label', 'timeweb.cloud', '--state', 'open']
    )
    list_issue_data: list[dict] = json.loads(list_issue.decode('utf-8'))
    for issue in list_issue_data:
        match = ISSUE_PATTERN.match(issue['title'])
        if match and match.group('etag') == etag:
            return issue['url']
    return ''


def get_issue_body() -> str:
    resp = httpx.get(OPENAPI_URL)
    resp.raise_for_status()
    with open('bundle.json', 'wb') as f:
        f.write(resp.content)
    diff = sp.check_output(['git', 'diff', '--no-index', '.github/api_check/current_bundle.json', 'bundle.json'])
    diff_data = diff.decode('utf-8')
    return f'''New API version is available.

    ```diff
    {diff_data}
    ```
    '''


def create_issue(etag: str) -> None:
    params = [
        'gh', 'issue', 'create', '--title',
        f'[API] New version: {etag}', '--label', 'timeweb.cloud',
        '--body', get_issue_body()
    ]
    sp.run(params)


if args.get_link:
    print(get_issue_link(args.etag))
    exit(0)
else:
    if not have_active_issue(args.etag):
        create_issue(args.etag)
        exit(0)
    print('Issue already exists.')
    exit(1)
