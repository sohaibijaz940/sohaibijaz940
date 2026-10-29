import unittest
from datetime import date
from activity import streaks
class ActivityTests(unittest.TestCase):
 def days(self,values):return [{'date':f'2026-10-{n:02}','contributionCount':v} for n,v in values]
 def test_streak_continues_through_yesterday(self):self.assertEqual(streaks(self.days([(26,2),(27,1),(28,3),(29,0)]),date(2026,10,29)),(3,3,'2026-10-28'))
 def test_today_extends_streak(self):self.assertEqual(streaks(self.days([(27,1),(28,1),(29,1)]),date(2026,10,29)),(3,3,'2026-10-29'))
 def test_a_gap_breaks_the_run(self):self.assertEqual(streaks(self.days([(25,1),(26,1),(27,0),(28,0),(29,0)]),date(2026,10,29)),(0,2,None))
 def test_missing_dates_and_future_data_do_not_inflate(self):self.assertEqual(streaks(self.days([(25,1),(27,1),(29,1),(30,8)]),date(2026,10,29)),(1,1,'2026-10-29'))
if __name__=='__main__':unittest.main()
