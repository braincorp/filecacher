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

from filecache import FileCache
import pytest


@pytest.fixture
def filecache(tmpdir, **optional_args):
	"""Create an empty file cache as helper for some tests."""
	return FileCache(str(tmpdir.mkdir('filecache')), **optional_args)


def test_get_set(filecache, tmpdir):
	bar_path = tmpdir.join('bar')
	bar_path.write('hello')
	filecache['foo'] = str(bar_path)

	assert open(filecache['foo']).read() == 'hello'


def test_missing_key(filecache):
	with pytest.raises(KeyError):
		filecache['missing_key']


def _create_file(tmpdir, length):
	file = tmpdir.tempfile().open()
	file.write('a'*length)


def test_remove_old_files(tmpdir):
	fc = filecache(tmpdir, cache_size=128)
	fc['a'] = _create_file(tmpdir, 32)
	fc['b'] = _create_file(tmpdir, 64)
	fc['a']  # Force a get to preserve a
	fc['c'] = _create_file(tmpdir, 48)
	fc['a']  # Force a get to preserve a
	fc['d'] = _create_file(tmpdir, 48)

	fc['a']
	fc['d']

	with pytest.raises(KeyError):
		# 'b' should have been flushed out by now
		fc['b']
