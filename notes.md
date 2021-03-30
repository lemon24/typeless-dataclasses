## 2021-03-29


### github repo

* readme: yes, .gitignore: python: license: unlicense, default branch: master, no wiki, no projects

14:20/14:30


### to do

* [x] repo
* [x] reserve pypi name
* [x] pre-commit: black etc.
* [x] code
* [x] tests
* [x] packaging
* [x] coverage
* [ ] (maybe) tox
* [ ] CI
* [ ] readme
  * [ ] badges
  * [ ] docs
* [ ] docstrings
* [ ] (maybe) set up type checking
* [ ] release
  * [ ] bump version
  * [ ] update changelog
  * [ ] push to github
  * [ ] upload to pypi
  * [ ] tag release

14:30/14:45


### envrc

```console
$ echo "layout python-venv python3.9" > .envrc
direnv: error ~/code/typeless-dataclasses/.envrc is blocked. Run `direnv allow` to approve its content
$ direnv allow
direnv: loading ~/code/typeless-dataclasses/.envrc
Collecting pip
  Using cached pip-21.0.1-py3-none-any.whl (1.5 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 20.2.3
    Uninstalling pip-20.2.3:
      Successfully uninstalled pip-20.2.3
Successfully installed pip-21.0.1
direnv: export +PYTEST_ADDOPTS +VIRTUAL_ENV ~PATH
```

15:28/15:31


### reserve pypi name

* google "python packaging"; first result: https://packaging.python.org/
* https://packaging.python.org/tutorials/packaging-projects/ looks good
  * eh, nothing on registering package name without upload
  * twine is used for upload
* pip install twine
  * https://twine.readthedocs.io/en/latest/
  * TOC -> Commands -> twine register
  * "register" no longer supported
* backtrack: upload empty package
* pyproject.toml
* setup.cfg
  * version = 0.1.dev0

* pip install build
  * python -m build
    * error: error in 'egg_base' option: 'src' does not exist or is not a directory
      * mkdir src
  * worked the second time
    * note: directory won't appear in the repo because it has no files

* python -m twine upload dist/*
  * yay: https://pypi.org/project/typeless-dataclasses/0.1.dev0/

    ```console
    $ pip install typeless-dataclasses
    Collecting typeless-dataclasses
      Downloading typeless_dataclasses-0.1.dev0-py3-none-any.whl (2.2 kB)
    Installing collected packages: typeless-dataclasses
    Successfully installed typeless-dataclasses-0.1.dev0
    $ pip show typeless-dataclasses
    Name: typeless-dataclasses
    Version: 0.1.dev0
    Summary: Use dataclasses without variable annotations.
    Home-page: https://github.com/lemon24/typeless-dataclasses
    Author: lemon24
    Author-email: None
    License: UNKNOWN
    Location: /Users/lemon/code/typeless-dataclasses/.venv/lib/python3.9/site-packages
    Requires:
    Required-by:
    $ pip uninstall typeless-dataclasses
    Found existing installation: typeless-dataclasses 0.1.dev0
    Uninstalling typeless-dataclasses-0.1.dev0:
      Would remove:
        /Users/lemon/code/typeless-dataclasses/.venv/lib/python3.9/site-packages/typeless_dataclasses-0.1.dev0.dist-info/*
    Proceed (y/n)? y
      Successfully uninstalled typeless-dataclasses-0.1.dev0
    ```

15:32/16:00


### pre-commit

* https://pre-commit.com/
  * pip install pre-commit
  * .pre-commit-config.yaml
    * mostly what's in the example, plus black (with pyproject.toml settings), flake8 and bugbear, and reorder imports
  * pre-commit autoupdate
  * pre-commit install

16:29/16:48


### code + tests

* module: copy from article
* tests: already had them, kinda
  * add simple import test
  * pip install pytest
  * pytest
    * ModuleNotFoundError: No module named 'typeless_dataclasses'
  * pip install -e .
    * ERROR: File "setup.py" not found. Directory cannot be installed in editable mode: /Users/lemon/code/typeless-dataclasses (A "pyproject.toml" file was found, but editable mode currently requires a setup.py based build.)
    * add setup.py with empty setup() call
    * works on the second try

16:48/17:31

---

* E501 line too long (87 > 79 characters); B950 line too long (87 > 79 characters)
  * had to add ignores to setup.cfg

17:31/17:49



## 2021-03-30


### packaging

* (started with tox, but realized this would be needed first)

* things we want
  * version from file
  * tests etc in tarball

* let's go through all the options from https://packaging.python.org/guides/distributing-packages-using-setuptools/ (linked from https://packaging.python.org/tutorials/packaging-projects/)
  * version (nice guidelines on versionning, btw)
  * project_urls
    * the list in distributing-packages-using-setuptools differs from the one in packaging-projects; it does say it can be arbitrary, but...
    * look at reader (inspired from flask a long time ago)
    * look at flask
    * go with flask (they must know something)
      * kept documentation, source code, and issue tracker
      * for docs we use the same link, readme will be docs enough
  * for license we'll use classifiers,
  * classifiers
    * from https://pypi.org/classifiers/
    * if we add mypy support, add Typing :: Typed
  * keywords
  * what goes where? options vs metadata
    * the distributing-packages-using-setuptools example stup.cfg is almost empty
    * better https://setuptools.readthedocs.io/en/latest/userguide/declarative_config.html
  * no dependencies; 3.6 users should install datacalsses themselves
    * we'd put them in setup.py like flask does: https://github.com/pallets/flask/blob/ecb3450f19d3d817b4b857bb5831b309131b37e1/setup.py (presumably github will eventually know to use setup.cfg)
  * extras_require
    * don't appear in github, so we'll use setup.cfg
    * tests, dev; still want dataclasses for test
    * https://setuptools.readthedocs.io/en/latest/userguide/dependency_management.html#declaring-dependencies is nice, has both setup.cfg and setup.py versions

    * pip install -e '.[tests,dev]'; python -m build
  * ended at 16:09

* files

  ```console
  $ unzip -l dist/typeless_dataclasses-0.1.dev1-py3-none-any.whl
  Archive:  dist/typeless_dataclasses-0.1.dev1-py3-none-any.whl
    Length      Date    Time    Name
  ---------  ---------- -----   ----
      1211  03-30-2021 13:09   typeless_dataclasses-0.1.dev1.dist-info/LICENSE
      1591  03-30-2021 13:09   typeless_dataclasses-0.1.dev1.dist-info/METADATA
        92  03-30-2021 13:09   typeless_dataclasses-0.1.dev1.dist-info/WHEEL
          1  03-30-2021 13:09   typeless_dataclasses-0.1.dev1.dist-info/top_level.txt
        465  03-30-2021 13:09   typeless_dataclasses-0.1.dev1.dist-info/RECORD
  ---------                     -------
      3360                     5 files
  $ tar -tvf dist/typeless-dataclasses-0.1.dev1.tar.gz
  drwxr-xr-x  0 lemon  staff       0 Mar 30 16:14 typeless-dataclasses-0.1.dev1/
  -rw-r--r--  0 lemon  staff    1334 Mar 30 16:14 typeless-dataclasses-0.1.dev1/PKG-INFO
  -rw-r--r--  0 lemon  staff      69 Mar 29 14:29 typeless-dataclasses-0.1.dev1/README.md
  -rw-r--r--  0 lemon  staff     193 Mar 29 17:34 typeless-dataclasses-0.1.dev1/pyproject.toml
  -rw-r--r--  0 lemon  staff    1390 Mar 30 16:14 typeless-dataclasses-0.1.dev1/setup.cfg
  -rw-r--r--  0 lemon  staff      38 Mar 29 17:01 typeless-dataclasses-0.1.dev1/setup.py
  drwxr-xr-x  0 lemon  staff       0 Mar 30 16:14 typeless-dataclasses-0.1.dev1/src/
  drwxr-xr-x  0 lemon  staff       0 Mar 30 16:14 typeless-dataclasses-0.1.dev1/src/typeless_dataclasses.egg-info/
  -rw-r--r--  0 lemon  staff    1334 Mar 30 16:14 typeless-dataclasses-0.1.dev1/src/typeless_dataclasses.egg-info/PKG-INFO
  -rw-r--r--  0 lemon  staff     282 Mar 30 16:14 typeless-dataclasses-0.1.dev1/src/typeless_dataclasses.egg-info/SOURCES.txt
  -rw-r--r--  0 lemon  staff       1 Mar 30 16:14 typeless-dataclasses-0.1.dev1/src/typeless_dataclasses.egg-info/dependency_links.txt
  -rw-r--r--  0 lemon  staff      70 Mar 30 16:14 typeless-dataclasses-0.1.dev1/src/typeless_dataclasses.egg-info/requires.txt
  -rw-r--r--  0 lemon  staff       1 Mar 30 16:14 typeless-dataclasses-0.1.dev1/src/typeless_dataclasses.egg-info/top_level.txt
  ```

  * file is missing from wheel and tar; tar should also have tests and license
  * py_modules for modules fixes the module, but we need to spell it out (according to distributing-packages-using-setuptools, there's no find:)
  * MANIFEST.in for the rest
    * using LICENSE, recursive-include tests (pyproject, setup, readme seem to be already included)
    * uh oh, we're also including tests/__pycache__/
      * global-exclude to the rescue

15:15/16:36


### coverage

* need pytest-cov (and coverage)
* pytest --cov && coverage html
  * 100% coverage, but... .venv/* included
  * https://coverage.readthedocs.io
  * where to add options? "configuration reference" -> also reads from setup.cfg
  * "specifying source files" source
    * both src and tests
  * without branch, 100%, with branch, 97%

* would be nice to know what code runs what
  * "measurement context"
  * https://pytest-cov.readthedocs.io/en/latest/contexts.html
  * pytest --cov --cov-context=test && coverage html --show-contexts
    * hmm, says (empty)
    * [paths] didn't fix it
    * ok, seems to be because our code does not run in a test function; rather, it runs at the module level
      * fixed

16:54/17:16

19:29/20:00
