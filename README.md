# python-jerasoft

This package covers basic Jerasoft VCS API functions to integrate it with external services.

## Table of Contents

- [Settings](#settings)
- [Client API](#client-api)
   - [Getting client info](#getting-client-info)
   - [Client removal](#client-removal)
   - [Client archiving](#client-archiving)
   - [Client info update](#client-info-update)
   - [Making an client](#making-an-client)
   - [Add package to client](#add-package-to-client)
- [Account API](#account-api)
   - [Making an account](#making-an-account)
   - [Getting account info](#getting-account-info)
   - [Account removal](#account-removal)
   - [Account info update](#account-info-update)
- [Rates API](#rates-api)
   - [Getting raw rate info](#getting-raw-rate-info)
   - [Getting rate codes](#getting-rate-codes)
   - [Getting rate by service id](#getting-rate-by-service-id)
- [Getting charges report](#getting-charges-report)
- [Getting list of transactions](#getting-list-of-transactions)
- [Links](#links)

## Settings

In `settings.py` under `default` section one can setup some sane defaults that would be
used when not set explicitly. The `token` and `endpoint` parameters should be set to actual 
Jerasoft VCS API token and full API url respectfully.

Fill those values in `settings.py` and then just import `jerasoft`  package with:

```python
import jerasoft
```

to start working.

## Client API
### Getting client info

Print an Client object with id 68:
```python
>>> jerasoft.Clients(68)
<Clients: 68 CF: Тестеренко А.Пи. 0.0>
```

Print client name:
```python
>>> print(jerasoft.Clients(68).name)
CF: Тестеренко А.Пи.
```

Get client balance:
```python
>>> jerasoft.Clients(68).balance()
0.0
```

Get client status:
```python
>>> jerasoft.Clients(68).status
u'active'
```

Get credit balance:
```python
>>> jerasoft.Clients(68).credit
0.0
```

Get client email:
```python
>>> jerasoft.Clients(68).c_email_billing
u'chop@chop.ch'
```

All the fields of Client entity returned by Jerasoft VCS may be requested this way. There is 
also possibility to request raw data for custom interactions:
```python
>>> jerasoft.Clients(68).get()
{u'balance_accountant': 0.0, u'low_balance_capacity': None, u'autoinvoice_enabled': False,
u'invoice_no_tpl': u'invoice-%N-%X', u'orig_capacity': ............ }
```

### Client removal
```python
>>> client = jerasoft.Clients(68)
>>> client.delete()
(True, '')
```

### Client archiving
```python
>>> client = jerasoft.Clients(68)
>>> client.archive()
(True, '')
```

### Client info update
```python
>>> params = {"name": "Тестеренко А.Пи. 47"}
>>> client = jerasoft.Clients(68)
>>> client.update(**params)
(True, '')
>>> client.name
u'\u0422\u0435\u0441\u0442\u0435\u0440\u0435\u043d\u043a\u043e \u0410.\u041f\u0438. 47'
>>> print(client.name)
Тестеренко А.Пи. 47
```

or just

```python
>>> client = jerasoft.Clients(68)
>>> client.update(name="Тестеренко А.Пи. 47")
(True, '')
>>> print(client.name)
Тестеренко А.Пи. 47
```

Multiple attributes may be updated in single `client.update()` call.


### Making an client
```python
>>> params = {"name": u"Тестеренко А.Пи. Esq", "c_company": "Defaults", "c_email_billing":
"chop@chop.ch"}
>>> client = jerasoft.Clients()
>>> client.create(**params)
(True, 69)
>>> client.id
69
>>> print(client.name)
CF: Тестеренко А.Пи. Esq
```

Other Client entity attributes (like rate id, currency id, start balance etc) may be passed in `params` too, sane defaults from `settings.py` would be used if they are not set.

### Add package to client
```python
>>> client = jerasoft.Clients(69)
>>> params = {"stop_days": 30, "packages_id": 6}
>>> client.add_package(**params)
(True, '')
```

If one wants to set the default package to Client, passing params to `client.add_package()` may be skipped:

```python
>>> client = jerasoft.Clients(69)
>>> client.add_package()
(True, '')
```

## Account API
### Making an account
```python
>>> import jerasoft, uuid
>>> params = {"clients_id": 69, "ipaddr": "127.0.0.69", "ani": uuid.uuid4().hex, "name": "my-server"}
>>> account = jerasoft.Accounts()
>>> account.create(**params)
(True, 242)
>>> account.id
242
>>> account.name
u'127.0.0.69 my-server'
>>> account.clients_id
69
>>> print(account.clients_name)
CF: Тестеренко А.Пи. Esq
```

Other Account entity attributes (like rate id, authentication type etc) may be passed in `params` too, sane defaults from `settings.py` would be used if they are not set.

### Getting account info
Print an Account object with id 242:
```python
>>> jerasoft.Accounts(242)
<Accounts: 242 127.0.0.69 my-server>
```

Print account name:
```python
>>> jerasoft.Accounts(242).name
u'127.0.0.69 my-server'
```

Print account rate id:
```python
>>> jerasoft.Accounts(242).orig_rate_table
19
```

Print client name and id, associated with this account:
```python
>>> jerasoft.Accounts(242).clients_id
69
>>> print(jerasoft.Accounts(242).clients_name)
CF: Тестеренко А.Пи. Esq
```

All the fields of Account entity returned by Jerasoft VCS may be requested this way. There is 
also possibility to request raw data for custom interactions:
```python
>>> jerasoft.Accounts(242).get()
{u'auth_type': u'ani', u'protocol': None, u'dr_plans_id': None, u'ani':
u'52add16b1d4f4ee987fc9c2b05c64a7f', u'orig_capacity': None, u'ips': [], u'term_tags': [],
u'term_capacity': None, u'id': 242, u'orig_enabled': True, u'clients_id': 69, u' ............ }
```

### Account removal
```python
>>> jerasoft.Accounts(242).delete()
(True, '')
```

### Account info update
```python
>>> jerasoft.Accounts(242).ani
u'52add16b1d4f4ee987fc9c2b05c64a7f'
>>> params = {"ani": uuid.uuid4().hex}
>>> jerasoft.Accounts(242).update(**params)
(True, '')
>>> jerasoft.Accounts(242).ani
u'f086a5a04a534ac58b4ffb2621b71c49'
```

or 

```python
>>> jerasoft.Accounts(242).update(ani=uuid.uuid4().hex)
(True, '')
>>> print(account.ani)
u'f086a5a04a534ac58b4ffb2621b71c49'
```

Multiple attributes may be updated in single Accounts `update()` call.

## Rates API
### Getting raw rate info
```python
>>> jerasoft.Rates(19).get()
[{u'status': u'active', u'effective_till': u'9999-12-31 23:59:59', u'code': u'cpu_fix', u'rate_tables_id': 19,
u'end_date': None, u'currencies_id': 27, ............ }
```

### Getting rate codes
```python
>>> jerasoft.Rates(19).codes()
[u'cpu_fix', u'cpu_scale', u'ram_fix', u'ram_scale', u'hdd_150', u'hdd_1500', u'cpu_fix_off',
u'cpu_scale_off', u'ram_fix_off', u'ram_scale_off', u'hdd_150_off', u'hdd_1500_off', u'ip_setup',
u'ip_usage', u'network', u'internet']
```

### Getting rate by service id
```python
>>> from pprint import pprint
>>> pprint(jerasoft.Rates(19).by_code("cpu_fix"))
{u'code': u'cpu_fix',
u'code_name': u'CPU utilization',
u'currencies_id': 27,
u'effective_from': u'2017-07-14 00:00:00+0300',
u'effective_till': u'9999-12-31 23:59:59',
u'end_date': None,
u'grace_volume': 0,
u'id': 1122989,
u'min_volume': 3600,
u'notes': None,
u'pay_interval': 3600,
u'pay_setup': 0.0,
u'policy': u'regular',
u'rate_tables_id': 19,
u'services_id': 1,
u'status': u'active',
u'tag': u'@',
u'time_profiles_id': 1,
u'value': 0.406090902}
```

For example, selecting the service unit cost for service with code `cpu_fix`:
```python
>>> jerasoft.Rates(19).by_code("cpu_fix").get("value")
0.406090902
```

## Getting charges report

Example of getting charges list for account id 242 using date interval:
```python
>>> report = jerasoft.Reports(242)
>>> report
<Reports: 242>
>>> report.get("2017-10-16", "2017-10-16")
[]
```

Calling `report.get()` without arguments will select charges at current date:
```python
>>> report = jerasoft.Reports(242)
>>> report.get()
[]
```

## Getting list of transactions

Example of getting transactions for client id 69:
```python
>>> trans = jerasoft.Transactions(69)
```

Get the sum of all transactions:
```python
>>> trans.counted
-200.0
```

Get the list of transactions:
```python
>>> trans.charges
[{'date': u'2017-10-17 16:48:50+0300', 'comment': u'Package pending payment: test', 'amount':
-100.0}, {'date': u'2017-10-17 16:51:42+0300', 'comment': u'Package pending payment: test',
'amount': -100.0}]
```

Raw response from Jerasoft VCS:
```python
>>> trans.raw_charges
[{u'status': u'pending', u'c_dt': u'2017-10-17 16:48:50+0300', u'companies_id': 24, u'clients_id': 69,
u'currencies_id': 27, u'type': u'charge', u'notes': u'P ............... }
```

## Links
[Jerasoft VCS vendor web-site](https://www.jerasoft.net/) all the product info and documentation

[python-digitalocean](https://github.com/koalalorenzo/python-digitalocean) was a package design influence.
