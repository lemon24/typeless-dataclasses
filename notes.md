## 2021-03-29


### github repo

* readme: yes, .gitignore: python: license: unlicense, default branch: master, no wiki, no projects

14:20/14:30


### to do

* [x] repo
* [x] reserve pypi name
* [ ] pre-commit: black etc.
* [ ] code
* [ ] tests
* [ ] (maybe) tox
* [ ] CI
* [ ] readme
  * [ ] badges
  * [ ] docs
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

16:29/16:47
