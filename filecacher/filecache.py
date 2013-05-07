# ===========================================================================
#
#  COPYRIGHT 2013 Brain Corporation.
#  All rights reserved. Brain Corporation proprietary and confidential.
#
#  The party receiving this software directly from Brain Corporation
#  (the "Recipient" ) may use this software and make copies thereof as
#  reasonably necessary solely for the purposes set forth in the agreement
#  between the Recipient and Brain Corporation ( the "Agreement" ). The
#  software may be used in source code form
#  solely by the Recipient's employees. The Recipient shall have no right to
#  sublicense, assign, transfer or otherwise provide the source code to any
#  third party. Subject to the terms and conditions set forth in the Agreement,
#  this software, in binary form only, may be distributed by the Recipient to
#  its customers. Brain Corporation retains all ownership rights in and to
#  the software.
#
#  This notice shall supercede any other notices contained within the software.
# =============================================================================

import os
import shutil


class FileCache(object):
	def __init__(self, cache_folder, cache_size=1024*1024*1024):
		"""Create a file cache, utilizing cache_folder to store the cached files
		and utilizing a maximum of cache_size.

		Note the actual cache size may increase by +/- 10% of the specified
		cache size.

		Keys must be strings which do not contain slashes and are valid filenames.
		"""
		self._cache_folder = os.path.abspath(cache_folder)
		self._cache_size = cache_size

		self._init_cache()

	def _init_cache(self):
		if not os.path.exists(self._cache_folder):
			os.makedirs(self._cache_folder)
		assert os.path.isdir(self._cache_folder)

	def _key_path(self, key):
		"""Key path from key."""
		return os.path.join(self._cache_folder, key)

	def __getitem__(self, key):
		"""Lookup item and return the full path to the file."""
		key_path = self._key_path(key)
		if os.path.exists(key_path):
			return key_path
		else:
			raise KeyError(key + ' not in cache')

	def __setitem__(self, key, filename):
		"""Insert filename into the dictionary under the keyname."""
		shutil.copyfile(filename, self._key_path(key))
