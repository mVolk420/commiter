import os
import subprocess
import unittest
from unittest.mock import patch
import sys
import types
from pathlib import Path

# Provide fake modules for missing dependencies
fake_dotenv = types.ModuleType('dotenv')
fake_dotenv.load_dotenv = lambda: None
sys.modules['dotenv'] = fake_dotenv

fake_openai = types.ModuleType('openai')
class FakeOpenAI:
    pass
fake_openai.OpenAI = FakeOpenAI
sys.modules['openai'] = fake_openai

# Ensure the repository root is in the path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Ensure PROJECT_BASE_PATH is set so importing main doesn't raise
os.environ.setdefault('PROJECT_BASE_PATH', '/tmp')

from main import push_changes

class PushChangesTest(unittest.TestCase):
    @patch('subprocess.run')
    def test_push_failure_does_not_raise(self, mock_run):
        mock_run.side_effect = [subprocess.CalledProcessError(1, ['git']), None]
        push_changes('/tmp/repo1')
        push_changes('/tmp/repo2')
        self.assertEqual(mock_run.call_count, 2)

if __name__ == '__main__':
    unittest.main()
