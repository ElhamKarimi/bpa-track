# -*- coding: utf-8 -*-

"""
Utility functions to fetch data from web server
"""

import os
import glob
import requests
from bs4 import BeautifulSoup
import logging

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)

class Fetcher():
    """ facilitates fetching data from webserver """

    def __init__(self, target_folder, metadata_source_url, auth=None):
        self.target_folder = target_folder
        self.metadata_source_url = metadata_source_url
        self.auth = auth

        self._ensure_target_folder_exists()

    def _ensure_target_folder_exists(self):
        if not os.path.exists(self.target_folder):
            from distutils.dir_util import mkpath

            mkpath(self.target_folder)

    def clean(self):
        """ Clean up existing contents """

        files = glob.glob(self.target_folder + "/*")
        for f in files:
            os.remove(f)

    def fetch(self, name):
        """ fetch file from server """

        logger.info("Fetching {0} from {1}".format(name, self.metadata_source_url))
        r = requests.get(self.metadata_source_url + "/" + name, stream=True, auth=self.auth, verify=False)
        with open(self.target_folder + "/" + name, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

    def fetch_metadata_from_folder(self):
        """ downloads metadata from archive """

        response = requests.get(self.metadata_source_url, stream=True, auth=self.auth, verify=False)
        for link in BeautifulSoup(response.content).find_all("a"):
            metadata_filename = link.get("href")
            if metadata_filename.endswith(".xlsx") or \
                    metadata_filename.endswith(".txt") or \
                    metadata_filename.endswith(".csv") or \
                    metadata_filename.endswith(".zip") or \
                    metadata_filename.endswith(".gz") or \
                    metadata_filename.endswith(".md5"):
                self.fetch(metadata_filename)
