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
    with open(args.path, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if line.startswith('from httpx import Client'):
            lines[i] = line.replace('from httpx import Client', 'from httpx import AsyncClient')
        elif line.startswith('from .base import BaseClient'):
            lines[i] = line.replace('from .base import BaseClient', 'from .base import BaseAsyncClient')
        elif 'API(BaseClient)' in line:
            lines[i] = line.replace('API(BaseClient)', 'API(BaseAsyncClient)')
        elif line.startswith('    def __init__'):
            lines[i] = line.replace('client: Client', 'client: AsyncClient')
        elif line.startswith('            client (Client'):
            lines[i] = line.replace('            client (Client', '            client (AsyncClient')
        elif line.startswith('    def'):
            if not line.startswith('    def __init__'):
                lines[i] = line.replace('    def', '    async def')
        elif 'self._request' in line:
            lines[i] = line.replace('self._request', 'await self._request')
    with open(args.path, 'w') as file:
        file.writelines(lines)


if __name__ == '__main__':
    main()
