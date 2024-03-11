#!/usr/bin/env python

import os
import sys
import json
import subprocess


if __name__ == "__main__":
    if not os.environ['PRE_COMMIT_LOCAL_BRANCH'].startswith('refs/tags/'):
        sys.exit(0)

    # get github run status
    result = subprocess.run(
        ['gh', 'run', 'list', '--commit', os.environ['PRE_COMMIT_TO_REF'],
         '--json', 'status,event,conclusion'],
        capture_output=True, check=True
    )

    runs = json.loads(result.stdout)
    if len(runs) == 0:
        print('no CI runs found, please invoke CI first')
        sys.exit(1)

    if not all('conclusion' in run for run in runs):
        print('not all CI runs are done, please wait')
        sys.exit(1)

    if not all(run['conclusion'] == 'success' for run in runs):
        print('at least one CI run has failed, tag rejected')
        sys.exit(1)
