# -*- coding: utf-8 -*-
import os
import argparse


OPENAPI_URL = 'https://timeweb.cloud/api-docs-data/bundle.json'
argparser = argparse.ArgumentParser(
    description='Save openapi file.'
)
argparser.add_argument(
    'etag', help='Etag of openapi file.'
)
args = argparser.parse_args()


if __name__ == '__main__':
    etag = args.etag.replace('"', '').replace("W", '')
    os.system(f'curl -s {OPENAPI_URL} -o .github/api_check/{etag}.json')
    print(f'{etag}.json')
