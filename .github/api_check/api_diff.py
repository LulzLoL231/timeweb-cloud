# -*- coding: utf-8 -*-
import json
import subprocess as sp

from tap import Tap
from markdown_strings import esc_format


class ArgumentParser(Tap):
    '''Returns openapi file difference in json format'''
    old: str  # Old OpenAPI specs file path
    new: str  # New OpenAPI specs file path
    ignore_ids: list[int] = []  # IDs for ignore
    # Output json string compact. Ignoring if sort_by_code.
    compact: bool = False
    sort_by_code: bool = False  # Sort output by code
    get_md: bool = False  # Output like markdown. Only with sort_by_code.


argparser = ArgumentParser()
CleanDiff = list[dict[str, str | int]]
SortedDiff = dict[str, list[str]]


def get_clean_diff(old_filepath: str, new_filepath: str) -> CleanDiff:
    cmd = f'openapi-compare -o {old_filepath} -n {new_filepath} -f Json'
    output = sp.check_output(cmd.split(' '))
    return json.loads(output)


def get_diff(args: ArgumentParser):
    diff = get_clean_diff(args.old, args.new)
    return list(
        filter(
            lambda m: m['Id'] not in args.ignore_ids,
            diff
        )
    )


def get_sorted_diff(diff: CleanDiff) -> SortedDiff:
    sorted_diff: SortedDiff = {}
    tmp = '{} ({} -> {})'
    tmp2 = '{} ({})'
    for msg in sorted(diff, key=lambda v: v['Severity']):
        if msg['OldJsonRef'] is None or msg['NewJsonRef'] is None:
            refs = [msg['NewJsonRef'] or msg['OldJsonRef']]
            cnt_tmp = tmp2
        else:
            if msg['OldJsonRef'] == msg['NewJsonRef']:
                refs = [msg['OldJsonRef']]
                cnt_tmp = tmp2
            else:
                refs = [msg['OldJsonRef'], msg['NewJsonRef']]
                cnt_tmp = tmp
        if msg['Code'] in sorted_diff.keys():
            sorted_diff[str(msg['Code'])].append(cnt_tmp.format(
                msg['Message'], *refs
            ))
        else:
            sorted_diff[str(msg['Code'])] = [cnt_tmp.format(
                msg['Message'], *refs
            )]
    return sorted_diff


def ext_esc_format(text) -> str:
    return esc_format(text).replace('~', '\\~')


def get_md(diff: SortedDiff) -> str:
    cnt = '## Differences\n\n'
    if not diff:
        cnt += '*No changes*'
        return cnt
    for k, msgs in diff.items():
        set_header = False
        for msg in msgs:
            if not set_header:
                cnt += f'### {k}:\n'
                set_header = True
            cnt += f'  * {ext_esc_format(msg)}\n'
        cnt += '\n'
    return cnt


if __name__ == '__main__':
    args = argparser.parse_args()
    diff = get_diff(args)
    if args.sort_by_code:
        sorted_diff = get_sorted_diff(diff)
        if args.get_md:
            print(get_md(sorted_diff))
        else:
            print(sorted_diff)
    else:
        if args.compact:
            print(json.dumps(diff, separators=(',', ':')))
        else:
            print(json.dumps(diff))
