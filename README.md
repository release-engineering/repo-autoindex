# repo-autoindex-prototype
Generate static HTML indexes of various repository types

## Usage example

```
pip install repo-autoindex
REPO_URL=$(curl -s 'https://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f36&arch=x86_64' | egrep '^http' | head -n1)
repo-autoindex $REPO_URL
xdg-open index.html
```
