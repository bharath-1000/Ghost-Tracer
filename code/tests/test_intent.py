"""
Unit tests for multilingual intent detection.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.intent import classify_intent

class TestIntentClassification(unittest.TestCase):
    def test_direct_deletion_english(self):
        res = classify_intent("Please delete all my personal records and close my account.")
        self.assertTrue(res["is_deletion"])
        self.assertEqual(res["intent_type"], "DELETION")

    def test_direct_deletion_spanish(self):
        res = classify_intent("Por favor, borren todos mis datos personales y cancelen mi cuenta.")
        self.assertTrue(res["is_deletion"])
        self.assertEqual(res["language"], "es")

    def test_direct_deletion_french(self):
        res = classify_intent("Supprimez définitivement mon compte et toutes mes données personnelles.")
        self.assertTrue(res["is_deletion"])
        self.assertEqual(res["language"], "fr")

    def test_direct_deletion_korean(self):
        res = classify_intent("제 계정과 관련된 모든 정보를 완전히 삭제해 주시기 바랍니다.")
        self.assertTrue(res["is_deletion"])
        self.assertEqual(res["language"], "ko")

    def test_direct_deletion_japanese(self):
        res = classify_intent("個人情報保護法に基づき、私のアカウントおよび個人データをすべて削除してください。")
        self.assertTrue(res["is_deletion"])
        self.assertEqual(res["language"], "ja")

    def test_negation_intent(self):
        res = classify_intent("Please do not delete my account. I made a mistake.")
        self.assertFalse(res["is_deletion"])
        self.assertEqual(res["intent_type"], "NEGATION")

    def test_withdrawal_intent(self):
        res = classify_intent("I withdrew my earlier deletion request. Keep profile active.")
        self.assertFalse(res["is_deletion"])
        self.assertEqual(res["intent_type"], "NEGATION")

    def test_data_access_intent(self):
        res = classify_intent("Send me a copy of all my purchase history.")
        self.assertFalse(res["is_deletion"])
        self.assertEqual(res["intent_type"], "NON_DELETION")

    def test_newsletter_opt_out_intent(self):
        res = classify_intent("Unsubscribe me from the weekly newsletter.")
        self.assertFalse(res["is_deletion"])
        self.assertEqual(res["intent_type"], "NON_DELETION")

    def test_address_correction_intent(self):
        res = classify_intent("Update my shipping address for the next shipment.")
        self.assertFalse(res["is_deletion"])
        self.assertEqual(res["intent_type"], "NON_DELETION")

if __name__ == "__main__":
    unittest.main()
