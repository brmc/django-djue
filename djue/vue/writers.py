#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from djue.utils import get_output_path, log


class SimpleWriter:
    def __init__(self, relative_path):
        path = get_output_path()
        self.path = os.path.join(path, relative_path)

    def write(self, payload):
        file_path = self.path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w+') as file:
            log('writing to ' + file_path)
            file.write(payload)