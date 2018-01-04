#!/usr/bin/python
# -*- coding: utf-8 -*-

import re


class ClassTable(object):

    class_table = [[[None] * 13] * 7] * 30
    week_pattern = re.compile('第(\d{1,2})-(\d{1,2})周')
    day_hour_pattern = re.compile('星期.*')
    hour_pattern = re.compile('\d{1,2}')

    day_map = {
        '星期一': 0,
        '星期二': 1,
        '星期三': 2,
        '星期四': 3,
        '星期五': 4,
        '星期六': 5,
        '星期日': 6,
    }

    @staticmethod
    def init_table():
        ClassTable.class_table = [[[None] * 13] * 7] * 30

    @staticmethod
    def create_table(table):
        for line in table:
            time_string = line[4]

            # deal with the weeks for class
            week_string = re.findall(ClassTable.week_pattern, time_string)[0] if re.search(ClassTable.week_pattern, time_string) else (0, 0)
            try:
                week_start = int(week_string[0]) - 1
                week_end = int(week_string[1]) - 1
            except ValueError:
                week_start = 0
                week_end = 0

            # deal with the days and hours for class
            day_hour_string = re.findall(ClassTable.day_hour_pattern, time_string)[0] if re.search(ClassTable.day_hour_pattern, time_string) else ''
            day_hour_string = day_hour_string.split(',')
            day_hour_string = [item.split('-') for item in day_hour_string]

            day = 0
            for item in day_hour_string:
                if len(item) == 2:
                    day = ClassTable.day_map[item[0]]
                    hour = re.findall(ClassTable.hour_pattern, item[1])[0] if re.search(ClassTable.hour_pattern, item[1]) else 0
                else:
                    hour = re.findall(ClassTable.hour_pattern, item[0])[0] if re.search(ClassTable.hour_pattern, item[0]) else 0

                try:
                    hour = int(hour) - 1
                except ValueError:
                    hour = 0

                for week in range(week_start, week_end + 1):
                    ClassTable.class_table[week][day][hour] = line[2]

                # print(week_start, week_end, day, hour)
        print(ClassTable.class_table)
        print(len(ClassTable.class_table))