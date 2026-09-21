import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def test_member_id_and_total_owed_are_initialized(self):
        fine = DuckFine("member-42")

        self.assertEqual(fine.member_id, "member-42")
        self.assertEqual(fine.total_owed, 0.0)

    def test_fine_is_zero_until_the_grace_period_is_exhausted(self):
        fine = DuckFine("member-1")

        charged = fine.charge(2)

        self.assertEqual(charged, 0.0)
        self.assertEqual(fine.total_owed, 0.0)

    def test_fine_is_zero_while_within_the_two_day_grace_period(self):
        fine = DuckFine("member-1a")

        charged = fine.charge(1)

        self.assertEqual(charged, 0.0)
        self.assertEqual(fine.total_owed, 0.0)

    def test_fine_is_50_cents_per_day_after_two_grace_days(self):
        fine = DuckFine("member-2")

        charged = fine.charge(5)

        self.assertEqual(charged, 1.50)
        self.assertEqual(fine.total_owed, 1.50)

    def test_negative_days_late_are_rejected(self):
        fine = DuckFine("member-3")

        with self.assertRaisesRegex(ValueError, "days_late must not be negative"):
            fine.charge(-1)

    def test_deluxe_fine_is_double_the_regular_fine(self):
        fine = DuckFine("member-4")

        charged = fine.charge(5, deluxe=True)

        self.assertEqual(charged, 3.00)
        self.assertEqual(fine.total_owed, 3.00)

    def test_fine_is_capped_at_five_dollars(self):
        fine = DuckFine("member-5")

        charged = fine.charge(20)

        self.assertEqual(charged, 5.00)
        self.assertEqual(fine.total_owed, 5.00)

    def test_total_owed_accumulates_across_charges(self):
        fine = DuckFine("member-6")

        first = fine.charge(3)
        second = fine.charge(7)

        self.assertEqual(first, 0.50)
        self.assertEqual(second, 2.50)
        self.assertEqual(fine.total_owed, 3.00)


if __name__ == "__main__":
    unittest.main()
