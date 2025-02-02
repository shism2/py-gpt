#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2025.02.02 02:00:00                  #
# ================================================== #

import requests

class Ollama:
    def __init__(self, window=None):
        """
        Ollama core

        :param window: Window instance
        """
        self.window = window
        self.available_models = []

    def get_status(self) -> dict:
        """
        Check Ollama status

        :return: dict
        """
        url = "http://localhost:11434/api/tags"
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': True,
                    'models': data.get('models', [])
                }
            else:
                return {
                    'status': False,
                    'models': []
                }
        except requests.exceptions.RequestException:
            return {
                'status': False,
                'models': []
            }

    def check_model(self, model: str) -> dict:
        """
        Check if model is available

        :param model: model ID
        :return: dict
        """
        result = {
            'is_installed': False,
            'is_model': False,
        }
        if model in self.available_models:
            return {
                'is_installed': True,
                'is_model': True,
            }
        status = self.get_status()
        if not status.get('status'):
            return result
        if "models" not in status:
            return result
        for item in status.get('models', []):
            model_id = item.get('name').replace(":latest", "")
            if model_id not in self.available_models:
                self.available_models.append(model_id)
            if model_id == model:
                return {
                    'is_installed': True,
                    'is_model': True,
                }
        return {
            'is_installed': True,
            'is_model': False,
        }
