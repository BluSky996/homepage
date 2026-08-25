import unittest
from pathlib import Path


HTML = (Path(__file__).parents[1] / "product-intelligence-report.html").read_text(encoding="utf-8")


class MarketFeedbackViewerContractTests(unittest.TestCase):
    def test_positive_and_negative_professional_reviews_have_distinct_labels(self):
        self.assertIn('row.evidence_type==="professional_or_media_review"', HTML)
        self.assertIn('row.opinion_direction==="positive"', HTML)
        self.assertIn('row.opinion_direction==="negative"', HTML)
        self.assertIn("正面信号", HTML)
        self.assertIn("负面 / 痛点信号", HTML)

    def test_consumer_voice_is_separate_and_requires_qualification(self):
        self.assertIn("row.consumer_voice_qualified===true", HTML)
        self.assertIn("消费者评论", HTML)
        self.assertIn("暂无足够消费者评论证据", HTML)

    def test_unknown_direction_is_not_presented_as_positive_or_negative(self):
        self.assertIn('["positive","negative"].includes(row.opinion_direction)', HTML)
        self.assertNotIn('row.opinion_direction==="unknown"', HTML)

    def test_empty_feedback_has_explicit_fallback(self):
        self.assertIn("暂无足够市场评价证据", HTML)

    def test_feedback_requires_product_association_and_evidence_id(self):
        self.assertIn("row.product_entity_id===productId", HTML)
        self.assertIn("row.qualified_product_mention===true", HTML)
        self.assertIn("asArray(row.evidence_ids).length>0", HTML)


if __name__ == "__main__":
    unittest.main()
