#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from django.core.management import BaseCommand


class ModuleCommand(BaseCommand):
    help = 'fuyck you'

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('modules', nargs='+', type=str)
        parser.add_argument('--drf')
