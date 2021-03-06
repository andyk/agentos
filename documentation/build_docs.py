"""
Build the AgentOS documentation.

To use::

  $ cd documentation
  $ pip install -r requirements.txt
  $ python build_docs.py
"""   

from importlib.machinery import SourceFileLoader
import os
import pip
from subprocess import Popen

docs_dir = os.path.dirname(os.path.abspath(__file__))

# Use pip to install dev-requirements.txt.
if hasattr(pip, 'main'):
    pip.main(['install', '-r', docs_dir + '/../dev-requirements.txt'])
else:
    pip._internal.main(['install', '-r', docs_dir + '/../dev-requirements.txt'])

version = SourceFileLoader(
    'agentos.version', os.path.join(docs_dir, '..', 'agentos', 'version.py')).load_module().VERSION
Popen(["sphinx-build", docs_dir, f"{docs_dir}/../docs/{version}"]).wait()

os.chdir(f"{docs_dir}/../docs")
os.remove(f"latest")
os.symlink(version, "latest", target_is_directory=True)
print(f"Created symbolic link docs/latest pointing to docs/{version}")
