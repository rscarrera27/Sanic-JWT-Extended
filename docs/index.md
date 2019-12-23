---
layout: default
title: Index
nav_order: 1
description: "Sanic-JWT-Extended is an open source Sanic extension that provides JWT support"
permalink: /
---

Note
{: .label .label-yellow }

**This is documentation for pre `1.0` version. `1.0` release does not support backward compatibility to 0.x version.**

[Visit legacy version(v0.4.4)](https://sanic-jwt-extended.readthedocs.io/en/latest/){: .btn .btn-purple }

---

# Provides **extended** JWT support that comply with RFC 7519
{: .fs-9 }

Sanic-JWT-Extended not only adds support for using JWT to Sanic for protecting views, but also many helpful (and optional) features built in to make working with JWT easier.
{: .fs-6 .fw-300 }

* Support for adding public claims with [namespacing](https://auth0.com/docs/tokens/concepts/claims-namespacing)
* Support for adding private claims
* [Refresh tokens](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)
* Token freshness and separate view decorators to only allow fresh tokens
* Access control
* blacklist support with some built-in blacklist
* Provides Token object for easier jwt manifulation

---

## Installation

```bash
$ pip install sanic-jwt-extended --pre
```
```bash
$ poetry add sanic-jwt-extended --git https://github.com/NovemberOscar/Sanic-JWT-Extended.git
```
```bash
$ pipenv install sanic-jwt-extended --pre
```

---

## About the project

Sanic-JWT-Extended is &copy; 2018-2019 by [Seonghyeon Kim](https://github.com/NovemberOscar)

### License

Sanic-JWT-Extended is distributed by an [MIT license](https://github.com/NovemberOscar/sanic-jwt-extended/tree/master/LICENSE).

### Contribution

When contributing to this repository, please first discuss the change you wish to make via issue. Read more about [becoming a contributor]() in our GitHub repo.

#### Thank you to the contributors of Sanic-JWT-Extended!

<ul class="list-style-none">
{% for contributor in site.github.contributors %}
  <li class="d-inline-block mr-1">
     <a href="{{ contributor.html_url }}"><img src="{{ contributor.avatar_url }}" width="32" height="32" alt="{{ contributor.login }}"/></a>
  </li>
{% endfor %}
</ul>

