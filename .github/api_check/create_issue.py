# -*- coding: utf-8 -*-
import re
import os
import argparse
import subprocess as sp

import httpx


OWNER = 'LulzLoL231'
REPO = 'timeweb-cloud'
ISSUE_PATTERN = re.compile(r'\[API\] New version: (?P<etag>.+)')
OPENAPI_URL = 'https://timeweb.cloud/api-docs-data/bundle.json'

argparser = argparse.ArgumentParser(description='Create issue about new API version.')
argparser.add_argument('etag', help='New API version etag.')
argparser.add_argument('--get-link', action='store_true', help='Print issue link and exit.', default=False)
argparser.add_argument('--issue-created', action='store_true', help='Print true or false, if issue created.')
argparser.add_argument('--run-url', type=str, help='Workflow run url', default='')
argparser.add_argument('--batch', action='store_true',
                       help='Don\'t print any info, except requested.', default=False)

gh = httpx.Client(
    headers={
        'Authorization': f'token {os.environ["GH_TOKEN"]}',
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }, base_url='https://api.github.com'
)


def log(msg: str):
    if not args.batch:
        print(msg)


def create_github_issue(etag: str, run_url: str):
    issue_data = {
        'title': f'[API] New version: {etag}',
        'body': get_issue_body(run_url), 'labels': ['timeweb.cloud']
    }
    issue = gh.post(
        f'/repos/{OWNER}/{REPO}/issues', json=issue_data
    )
    if issue.is_success:
        log(f'Created issue: {issue.json()}')
    else:
        log('Can\'t create issue with full body, using short body.')
        short_issue_data = issue_data.copy()
        short_issue_data['body'] = get_short_issue_body(run_url)
        short_issue = gh.post(
            f'/repos/{OWNER}/{REPO}/issues', json=short_issue_data
        )
        if short_issue.is_success:
            log(f'Created issue: {short_issue.json()}')
        else:
            raise RuntimeError('Can\'t create any issue!')


def get_active_issue(etag: str) -> dict:
    response = gh.get(
        f'/repos/{OWNER}/{REPO}/issues',
        params={
            'state': 'open',
            'labels': 'timeweb.cloud'
        }
    )
    log(f'Response status: {response.status_code}')
    issues: list[dict] = response.json()
    log(f'Fetched issues: {issues}')
    for issue in issues:
        match = ISSUE_PATTERN.match(issue['title'])
        if match and match.group('etag') == etag.replace('"', ''):
            return issue
    return {}


def get_issue_link(etag: str) -> str:
    issue = get_active_issue(etag)
    log(f'Fetched issue: {issue}')
    return issue.get('html_url', '')


def get_issue_body(run_url: str) -> str:
    resp = httpx.get(OPENAPI_URL)
    resp.raise_for_status()
    with open('bundle.json', 'wb') as f:
        f.write(resp.content)
    output = sp.check_output('python3 .github/api_check/api_diff.py --old .github/api_check/current_bundle.json --new ./bundle.json --ignore_ids 1001 --sort_by_code --get_md'.split(' '))
    diff_data = output.decode('utf-8')
    return f'''{get_short_issue_body(run_url)}

{diff_data}
'''


def get_short_issue_body(run_url: str) -> str:
    return f'''New API version is available.
Workflow run: {run_url}'''


def create_issue(etag: str, run_url: str) -> None:
    create_github_issue(etag, run_url)


if __name__ == '__main__':
    args = argparser.parse_args()

    if args.issue_created:
        print(bool(get_active_issue(args.etag)))
        exit(0)
    if args.get_link:
        print(get_issue_link(args.etag))
        exit(0)
    if not get_active_issue(args.etag):
        create_issue(args.etag, args.run_url)
        exit(0)
    print('[!] Issue already exists.')
