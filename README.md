# timeweb-cloud
API Timeweb Cloud позволяет вам управлять ресурсами в облаке программным способом с использованием обычных HTTP-запросов.

Множество функции, которые доступны в панели управления Timeweb Cloud, также доступны через API, что позволяет вам автоматизировать ваши собственные сценарии.

Эта библиотека позволяет вам легко использовать API Timeweb Cloud в вашем приложении на Python.

[Документация API](https://timeweb.cloud/api-docs)

[![OpenAPI etag: 63e3c467-b194f](https://img.shields.io/badge/OpenAPI%20etag-63e3c467--b194f-blue)](https://github.com/LulzLoL231/timeweb-cloud/wiki/1.bundle.json) [Как определяется etag?](#etag)

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
> **Warning**
> В планах добавить все методы API, но на текущий момент доступны только некоторые из них.

 - [x] Аккаунт
 - [ ] Базы данных
 - [ ] Балансировщики
 - [ ] Выделенные серверы
 - [ ] Домены
 - [ ] Облачные серверы
 - [x] Образы
 - [ ] Проекты
 - [x] Токены API
 - [ ] Kubernetes
 - [x] S3-хранилище
 - [x] SSH-ключи

## Etag
Etag - это уникальный идентификатор, который используется для проверки изменений в API. Он будет использоваться чтобы определять текущею версию API, т.к. сейчас API Timeweb Cloud не имеет версионности. Получается он из запроса к спецификации OpenAPI по ссылке https://timeweb.cloud/api-docs-data/bundle.json. Сервер сам его возвращает и мы пока операемся на него. В будущем, когда/если API Timeweb Cloud будет иметь версионность, будем опираться на их версию API.