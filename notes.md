## 2021-03-29


### github repo

* readme: yes, .gitignore: python: license: unlicense, no wiki, no projects

14:20/14:30


### to do

* [x] repo
* [x] reserve pypi name
* [x] pre-commit: black etc.
* [x] code
* [x] tests
* [x] packaging
* [x] coverage
* [x] (maybe) tox
* [x] makefile
* [x] (maybe) check coverage 100%
* [x] CI
* [x] codecov
* [x] readme
  * [x] badges
  * [x] docs
* [x] docstrings
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

19:29/20:01


### tox

* https://tox.readthedocs.io/en/latest/example/basic.html#a-simple-tox-ini-default-environments
* src/typeless_dataclasses.py showing up with 0 coverage
  * https://pytest-cov.readthedocs.io/en/latest/tox.html this didn't help 100%, but its useful
  * https://stackoverflow.com/questions/58696476/tox-0-coverage kinda didnt help (tests missing)
  * also need to set coverage:paths in setup.cfg
  * https://github.com/pytest-dev/pytest-cov/blob/master/examples/src-layout/ helped everything in result
    * except "No data to combine"
  * https://gist.github.com/dnozay/5b9b818ff0dc857d1358 did help, also no need to add --parallel


20:01/21:01



## 2021-03-31

### docstrings

* must look nice with help()
* to test docstring examples: pytest --doctest-modules
  * "addopts = --doctest-modules" in setup.cfg to always have them
    * https://docs.pytest.org/en/stable/reference.html#ini-options-ref

10:02/10:34


### check coverage 100%

* "if not hasattr(cls, '__annotations__'):" is missing branch coverage
  * need empty class
* while we're here, let's also test the __annotations__ for the main ones are the same
* pytest --cov --cov-context=test --cov-fail-under=100

10:34/10:58


### readme (docs)

* also changelog

13:01/14:20


### Makefile

* also added to manifest
* added --fail-under to tox.ini as well
* originally inspired from flask, now inspired from reader

14:22/14:58



### CI

* inspired from reader
* https://docs.github.com/en/actions/guides/building-and-testing-python
* https://docs.github.com/en/actions/guides/building-and-testing-python#testing-your-code could have used the tox thing, like flask does; won't, because reasons
* https://docs.github.com/en/actions/guides/building-and-testing-python#publishing-to-package-registries could upload to pypi as well, don't wanna do this for now


15:17/15:30


### codecov

* can't use reader, since we're only using codecov with travis
* https://docs.codecov.io/docs/supported-languages
  * https://github.com/codecov/example-python

15:30/15:42


### badges

* build: github -> actions -> build -> ... -> create status badge
* codecov: settings -> badge
* pypi: https://shields.io/ -> version -> pypi
* black: https://github.com/psf/black -> show your style

15:42/15:55


### type checking

* https://mypy.readthedocs.io/en/stable/
* from reader we know it doesn't work on pypy; it's OK
* want this to run on CI and on tox, and badge

```
$ mypy --strict src
src/typeless_dataclasses.py:14: error: Function is missing a return type annotation
src/typeless_dataclasses.py:59: error: Call to untyped function "_isattribute" in typed context
src/typeless_dataclasses.py:72: error: Function is missing a type annotation
Found 3 errors in 1 file (checked 1 source file)
```

* making it pass is easy, just add annotations to signatures `def typeless(cls: type) -> type:

```python
from dataclasses import dataclass, field

@dataclass
@typeless
class Data:
    one = field()
    two = field(default=2)

d = Data(1, '')

reveal_type(d)
reveal_type(d.one)
reveal_type(d.two)
```

```
src/typeless_dataclasses.py:94: error: Too many arguments for "Data"
src/typeless_dataclasses.py:96: note: Revealed type is 'typeless_dataclasses.Data'
src/typeless_dataclasses.py:97: note: Revealed type is 'Any'
src/typeless_dataclasses.py:98: note: Revealed type is 'builtins.int*'
Found 1 error in 1 file (checked 1 source file)
```

* `def typeless(cls: T) -> T:` does not help either

* looks like fancy dataclass stuff is not supported: https://mypy.readthedocs.io/en/stable/additional_features.html#dataclasses

* tried to do some wrapping and stuff, maybe trick mypy; most likely a plugin is needed,
  * after looking at the dataclasses mypy plugin, i'm way in over my head
  * giving up

15:55/16:55

* trying again, found https://mypy.readthedocs.io/en/stable/extending_mypy.html#configuring-mypy-to-use-plugins

16:55/17:14

* still nothing; use this to run:
  `MYPYPATH=../src mypy --strict --config-file mypyconf.ini mypyex.py --show-traceback`

* tests are failing like this: * https://github.com/lemon24/typeless-dataclasses/runs/2239074261
  * I don't understand why pytest is looking there in the first place; "works on my machine"
  * made a new mypy branch and removing them from here

17:25/20:15
