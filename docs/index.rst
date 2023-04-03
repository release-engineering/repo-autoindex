repo-autoindex
==============

Minimal generator for HTML indexes of content repositories.

.. contents:: Contents
   :depth: 1
   :local:

Overview
--------

``repo-autoindex`` is a minimal Python library and CLI for generating
static HTML indexes for content repositories of various types.
It supports:

- yum repositories (``repodata/repomd.xml``)
- pulp file repositories (``PULP_MANIFEST``)
- kickstart tree repositories\* (``treeinfo``, ``repodata/repomd.xml``, ``extra_files.json``)

``repo-autoindex`` provides similar functionality to traditional server-generated
directory indexes such as httpd's
`mod_autoindex <https://httpd.apache.org/docs/2.4/mod/mod_autoindex.html>`_, with
a few key differences:

- The generated indexes are intentionally limited to show only the content present
  in repository metadata, rather than all content within a directory.
- The method of obtaining the content for indexing can be customized, allowing the
  library to integrate with exotic scenarios such as repositories generated on demand
  or not stored within a traditional filesystem.

\* ``repo-autoindex`` supports kickstart tree repositories satisfying certain conditions:

- The kickstart repo contains exactly one yum repo
- The yum repo is located in the root of the kickstart tree repo, at exactly ``.``

Reference: CLI
--------------

.. argparse::
   :module: repo_autoindex._impl.cmd
   :func: argparser
   :prog: repo-autoindex

Example
.......

In the following example we generate indexes for a single Fedora
yum repository. Note that the command generates multiple HTML files,
reproducing the directory structure found in the repo.

.. code-block::

   REPO_URL=$(curl -s 'https://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f36&arch=x86_64' | egrep '^http' | head -n1)
   repo-autoindex $REPO_URL
   Fetching: https://fedora.mirror.digitalpacific.com.au/linux/updates/36/Everything/x86_64/repodata/repomd.xml
   Fetching: https://fedora.mirror.digitalpacific.com.au/linux/updates/36/Everything/x86_64/repodata/32cf6191e4ef86045c9f34589d98f6378069359746b50def80a66e15fe5a906f-primary.xml.gz
   Wrote ./index.html
   Wrote repodata/index.html
   Wrote Packages/index.html
   Wrote Packages/z/index.html
   Wrote Packages/y/index.html
   Wrote Packages/x/index.html
   Wrote Packages/w/index.html
   Wrote Packages/v/index.html
   Wrote Packages/u/index.html
   Wrote Packages/t/index.html
   Wrote Packages/s/index.html
   Wrote Packages/r/index.html
   Wrote Packages/q/index.html
   Wrote Packages/p/index.html
   Wrote Packages/o/index.html
   Wrote Packages/n/index.html
   Wrote Packages/m/index.html
   Wrote Packages/l/index.html
   Wrote Packages/k/index.html
   Wrote Packages/j/index.html
   Wrote Packages/i/index.html
   Wrote Packages/h/index.html
   Wrote Packages/g/index.html
   Wrote Packages/f/index.html
   Wrote Packages/e/index.html
   Wrote Packages/d/index.html
   Wrote Packages/c/index.html
   Wrote Packages/b/index.html
   Wrote Packages/a/index.html
   Wrote Packages/3/index.html


Reference: API
--------------

.. automodule:: repo_autoindex
   :members:
