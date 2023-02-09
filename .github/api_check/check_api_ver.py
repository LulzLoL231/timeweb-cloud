# -*- coding: utf-8 -*-
# Check timeweb.cloud API version, based on openapi file etag.
import argparse

import httpx


LAST_ETAG = 'W/"63e3c467-b194f"'
OPENAPI_URL = 'https://timeweb.cloud/api-docs-data/bundle.json'


argparser = argparse.ArgumentParser(
    description='Check timeweb.cloud API version, based on openapi file etag.'
)
argparser.add_argument(
    '--check', action='store_true', help='Compare current etag with actual etag.'
)
argparser.add_argument(
    '--etag', action='store_true', help='Print last etag and exit.'
)
argparser.add_argument(
    '--actual_etag', action='store_true', help='Print actual etag and exit.'
)
argparser.add_argument(
    '--batch', action='store_true', help='Print only data.', default=False
)
args = argparser.parse_args()


def get_etag() -> str:
    response = httpx.head(OPENAPI_URL)
    response.raise_for_status()
    return response.headers['etag']


if args.check:
    etag = get_etag()
    if etag == LAST_ETAG:
        if args.batch:
            print('actual')
        else:
            print(f'Version {LAST_ETAG} is actual.')
    else:
        if args.batch:
            print('outdated')
        else:
            print(f'Version {LAST_ETAG} is outdated.')
if args.etag:
    if args.batch:
        print(LAST_ETAG)
    else:
        print(f'Last etag: {LAST_ETAG}')
if args.actual_etag:
    etag = get_etag()
    if args.batch:
        print(etag)
    else:
        print(f'Actual etag: {etag}')
