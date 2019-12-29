# Khan Academy management helpers

## Environment

This repository rely on python language.
All dependant packages can be installed using `requirements.txt` 

## Init the repository
In order to all features work you need to following.

First run the `init.bash` file. This file will update `PYTHONPATH` variable such that all imports inside the repo will be possible. Together with it `KA_MANAGE_REPO` variable will be also created. It will contain path to the root of the repository. By this variable one can access custom files which are not tracked by git, such as `env.yaml`.

This scrip will also create `env.ide` file. This file will contain variables to be included in IDE such as PyCharm 

## Crowdin

Inside crowdin directory you can find scripts and notebooks for monitoring activities on crowdin.

## Notes
The discovery script was test on python 3.5.2
