# This script should be sourced before using this repo (for development).
# If you want to use this in your project install it as a package.

if type python27 > /dev/null 2>/dev/null ; then
	PYTHONEXEC=python27
else
	PYTHONEXEC=python
fi

if [ -d ".env" ]; then
   # Virtual Env exists
   true
else
   echo "**> creatinv virtualenv"
   virtualenv .env --python=$PYTHONEXEC --prompt "(filecacher) " --extra-search-dir=$PWD \
			--distribute
fi

source .env/bin/active

# readline must be come before everything else
if [[ `uname` == 'Darwin' ]]; then
   easy_install -q readline==6.2.2
fi
pip install -r dev-requirements.txt

echo Ready to work!
