import unittest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.cathedral_engine import DialetheicBuffer, SpectrumConstant
from src.vector_mapper import VectorMapper, AshArchiveMapper


class TestDialetheicCoreModule(unittest.TestCase):

    def setUp(self):
        self.archive_mapper = AshArchiveMapper()

    def test_stratum_1_codex_ingestion(self):
        codex_path = os.path.join(os.path.dirname(__file__), '../codex/inner_mandala_stratum_1.json')
        with open(codex_path, 'r') as f:
            data = json.load(f)

        verses = data.get('verses', [])
        self.assertGreater(len(verses), 0)

        for v in verses:
            record = self.archive_mapper.ingest_verse_pair(
                verse_claim=v['claim'],
                verse_counter_claim=v['counter_claim'],
                verse_id=v['verse_id']
            )
            self.assertIn('paradox_load', record)
            self.assertIn('evaluation', record)

        self.assertEqual(len(self.archive_mapper.ingested_verses), len(verses))


if __name__ == '__main__':
    unittest.main()
