# function testing module

import unittest
from func.func_time import check_year, check_day, check_month, check_hour, check_minutes, check_second
from func.func_weather import get_weather
from bot import add_data_schedule, add_data_queries, get_user_schedule, delete_one_schedule, all_id_record


class Test_function(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_city = 'Минск'
        self.invalid_city = 'cvxvxv'
        self.wind = 'м/с'
        self.id = 12345678
        self.invalid_num_record = 999


    def test_check_time(self):
        self.assertEqual(type(check_year()), int), 'test type no passed'
        self.assertEqual(type(check_month()), int), 'test type no passed'
        self.assertEqual(type(check_day()), int), 'test type no passed'
        self.assertEqual(type(check_hour()), int), 'test type no passed'
        self.assertEqual(type(check_minutes()), int), 'test type no passed'
        self.assertEqual(type(check_second()), int), 'test type no passed'


    def test_get_weather(self):
        self.assertEqual(type(get_weather(self.valid_city)), str), 'test type no passed'
        self.assertEqual(get_weather(self.invalid_city), 'Город не найден'), 'test invalid_city no passed'
        self.assertIn(self.wind, get_weather(self.valid_city)), 'test string_wind no passed'
        self.assertNotIn(self.wind, get_weather(self.invalid_city)), 'test string_wind no passed'


    def test_add_data_schedule(self):
        id = 12345678
        city = 'Test'
        time_hour = 12
        time_minutes = 50
        data = {}
        data.setdefault(id, []).extend([id, city, time_hour, time_minutes])
        self.assertEqual(add_data_schedule(data, id), True), 'test added data schedule no passed'


    def test_add_data_queries(self):
        id = 777
        city = 'Test'
        result = 'test'
        year = 2021
        month = 12
        day = 12
        hour = 12
        min = 12
        sec = 12
        data = {}
        data.setdefault(id, []).extend([id, city, result, year, month, day, hour, min, sec])
        self.assertEqual(add_data_queries(data, id), True), 'test added data queries no passed'


    def test_get_user_schedule(self):
        self.assertEqual(type(get_user_schedule(self.id)), str), 'test user_schedule no passed'


    def test_delete_one_schedule(self):
        self.assertEqual(delete_one_schedule(self.invalid_num_record),False), 'test delete_one_schedule no passed'


    def test_all_id_record(self):
        self.assertEqual(type(all_id_record()), list), 'test all_id_record no passed'



if __name__ == '__main__':
    unittest.main()