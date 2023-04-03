# repo-autoindex

Generate static HTML indexes of various repository types

![Build Status](https://github.com/release-engineering/repo-autoindex/actions/workflows/ci.yml/badge.svg?branch=main)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
[![Docs](https://img.shields.io/website?label=docs&url=https%3A%2F%2Frelease-engineering.github.io%2Frepo-autoindex%2F)](https://release-engineering.github.io/repo-autoindex/)
[![PyPI](https://img.shields.io/pypi/v/repo-autoindex)](https://pypi.org/project/repo-autoindex/)

## Overview

`repo-autoindex` provides a minimal CLI and Python library to generate static HTML indexes
for certain types of content, such as yum repositories.

```
pip install repo-autoindex
REPO_URL=$(curl -s 'https://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f36&arch=x86_64' | egrep '^http' | head -n1)
repo-autoindex $REPO_URL
xdg-open index.html
```

See [the manual](https://release-engineering.github.io/repo-autoindex/) for more
information about the usage of `repo-autoindex`.

## Changelog

### v1.1.0 - 2023-04-04

- Added limited support for kickstart repositories.

### v1.0.2 - 2022-10-21

- Reduced memory usage when handling large yum repositories.

### v1.0.1 - 2022-08-15

- Use correct SPDX license identifier in package metadata.

### v1.0.0 - 2022-08-15

- Initial stable release.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
