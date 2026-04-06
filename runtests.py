#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.test_settings")
    django.setup()
    runner = get_runner(settings)(verbosity=2, interactive=False)
    failures = runner.run_tests(["tests"])
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
