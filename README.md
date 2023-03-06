# timeweb-cloud
API Timeweb Cloud позволяет вам управлять ресурсами в облаке программным способом с использованием обычных HTTP-запросов.

Множество функции, которые доступны в панели управления Timeweb Cloud, также доступны через API, что позволяет вам автоматизировать ваши собственные сценарии.

Эта библиотека позволяет вам легко использовать API Timeweb Cloud в вашем приложении на Python.

[Документация API](https://timeweb.cloud/api-docs)

[![OpenAPI etag: 63ff51f3-106a07](https://img.shields.io/badge/OpenAPI%20etag-63ff51f3--106a07-blue)](https://github.com/LulzLoL231/timeweb-cloud/wiki/) [Как определяется etag?](#etag)

[![PyPI version](https://badge.fury.io/py/timeweb-cloud.svg)](https://badge.fury.io/py/timeweb-cloud) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/timeweb-cloud)](https://pypi.org/project/timeweb-cloud/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/timeweb-cloud)](https://pypi.org/project/timeweb-cloud/) [![PyPI - License](https://img.shields.io/pypi/l/timeweb-cloud)](https://github.com/LulzLoL231/timeweb-cloud/blob/master/LICENSE)

## Установка

```bash
pip install timeweb-cloud
```

## Пример использования
Библиотека поддерживает синхронный и асинхронный варианты использования. В примерах ниже используется синхронный вариант, но вы можете использовать асинхронный вариант, заменив `tw = Timeweb(...)` на `tw = AsyncTimeweb(...)`

```python
from timeweb import Timeweb

tw = Timeweb('token')
account_status = tw.account.get_status()  # schemas.account.AccountStatus
print(account_status)
```

## Что доступно?

 - [x] Аккаунт `tw.account`
 - [x] Базы данных `tw.dbs`
 - [x] Балансировщики `tw.balancers`
 - [x] Выделенные серверы `tw.servers.dedics`
 - [x] Домены `tw.domains`
 - [x] Облачные серверы `tw.servers.cloud`
 - [x] Образы `tw.images`
 - [x] Проекты `tw.projects`
 - [x] Токены API `tw.tokens`
 - [x] Kubernetes `tw.k8s`
 - [x] S3-хранилище `tw.s3`
 - [x] SSH-ключи `tw.ssh_keys`
 - [x] Почта `tw.mail`

## Etag
Etag - это уникальный идентификатор, который используется для проверки изменений в API. Он будет использоваться чтобы определять текущею версию Swagger API, т.к. сейчас Swagger API Timeweb Cloud не имеет версионности и/или changelog'а. Получается он из запроса к спецификации OpenAPI по ссылке https://timeweb.cloud/api-docs-data/bundle.json. Сервер сам его возвращает и мы пока операемся на него. В будущем, когда/если Swagger API Timeweb Cloud будет иметь версионность и/или changelog, будем опираться на их версию Swagger API.