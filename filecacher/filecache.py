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
import logging


class FileCache(object):
	def __init__(self, cache_folder, cache_size=1024*1024*1024):
		"""Create a file cache, utilizing cache_folder to store the cached files
		and utilizing a maximum of cache_size.

		Keys must be strings which do not contain slashes and are valid filenames.

		Maximum size is a soft limit - it is tracked per process - so if multiple
		processes are writing to the cache it may go oversize.
		"""
		self._logger = logging.getLogger(__name__)

		self._cache_folder = os.path.abspath(cache_folder)
		self._maximum_cache_size = cache_size

		self._init_cache()

	def _init_cache(self):
		if not os.path.exists(self._cache_folder):
			os.makedirs(self._cache_folder)
		assert os.path.isdir(self._cache_folder)
		self._calculate_cache_size()

	def _calculate_cache_size(self):
		files = os.listdir(self._cache_folder)
		self._cache_size = 0
		for f in files:
			self._cache_size += os.stat(os.path.join(self._cache_folder, f)).st_size
		self._logger.info('Initial cache size in %s is %d' % (self._cache_folder,
													self._cache_size))
		self._trim_cache()

	def _key_path(self, key):
		"""Key path from key."""
		return os.path.join(self._cache_folder, key)

	def __getitem__(self, key):
		"""Lookup item and return the full path to the file."""
		key_path = self._key_path(key)
		if os.path.exists(key_path):
			# Update the access time
			os.utime(key_path, None)
			return key_path
		else:
			raise KeyError(key + ' not in cache')

	def _trim_cache(self):
		"""Check if the cache is oversized - if it is trim it."""
		if self._cache_size <= self._maximum_cache_size:
			return
		oversize = self._cache_size - self._maximum_cache_size
		logging.info('Cache oversize by %d' % oversize)
		files = os.listdir(self._cache_folder)
		# add path to each file
		files = [os.path.join(self._cache_folder, f) for f in files]
		files.sort(key=lambda x: os.path.getmtime(x))

		for f in files:
			f_size = os.stat(f).st_size
			self._cache_size -= f_size
			self._logger.info('Removing %s with size %d to make room' % (f, f_size))
			os.remove(f)
			if self._cache_size < 0.9*self._maximum_cache_size:
				return

	def __setitem__(self, key, filename):
		"""Insert filename into the dictionary under the keyname."""
		self._trim_cache()
		shutil.copyfile(filename, self._key_path(key))
		self._cache_size += os.stat(self._key_path(key)).st_size
