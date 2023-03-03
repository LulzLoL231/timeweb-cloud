# -*- coding: utf-8 -*-
import argparse


argparser = argparse.ArgumentParser(
    description='Преобразование синхронного кода в асинхронный.'
)
argparser.add_argument(
    'path', type=str, help='Путь к файлу'
)
args = argparser.parse_args()


def main():
    with open(args.path, 'rb') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if line.startswith(b'from httpx import Client'):
            lines[i] = line.replace(b'from httpx import Client', b'from httpx import AsyncClient')
        elif line.startswith(b'from .base import BaseClient'):
            lines[i] = line.replace(b'from .base import BaseClient', b'from .base import BaseAsyncClient')
        elif b'API(BaseClient)' in line:
            lines[i] = line.replace(b'API(BaseClient)', b'API(BaseAsyncClient)')
        elif line.startswith(b'    def __init__'):
            lines[i] = line.replace(b'client: Client', b'client: AsyncClient')
        elif line.startswith(b'            client (Client'):
            lines[i] = line.replace(b'            client (Client', b'            client (AsyncClient')
        elif line.startswith(b'    def'):
            if not line.startswith(b'    def __init__'):
                lines[i] = line.replace(b'    def', b'    async def')
        elif b'self._request' in line:
            lines[i] = line.replace(b'self._request', b'await self._request')
    with open(args.path, 'wb') as file:
        file.writelines(lines)


if __name__ == '__main__':
    main()
