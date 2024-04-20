import os
import csv
from datetime import datetime
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_count = defaultdict(int)
        self.total = 0

    def process_item(self, item, spider):
        self.status_count[item['status']] += 1
        self.total += 1
        return item

    def close_spider(self, spider):
        filename = (
            os.path.join(
                os.path.join(BASE_DIR, 'results'), 'status_summary_'
                f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
            ))
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Статус', 'Количество']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for status, count in self.status_count.items():
                writer.writerow({'Статус': status, 'Количество': count})
            writer.writerow({'Статус': 'Total', 'Количество': self.total})
