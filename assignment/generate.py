from pathlib import Path
from random import choice, choices, randint, random
from datetime import datetime as dt
from datetime import timedelta
import sqlite3

class DataGenerator():
    DATETIME_FMT = '%Y-%m-%dT%H:%M:%S'
    def __init__(self, abnormal_threshold: float=0.90):
        with Path('names.txt').open('r') as file:
            self.names = [name.strip().lower() for name in file.readlines()]
        self.names_dict = {n: (abs(hash(n)) // 1e17) < 10 for n in self.names}
        self.abnormal_threshold = abnormal_threshold
        self._reset_normal_cnt()

    def _reset_normal_cnt(self):
        self._count = 0
        self._abnormal_count_thres = randint(35, 40)

    def _update_normal_cnt(self):
        self._count += 1
    
    def _check_abnormal_count_thres(self):
        if self._count == self._abnormal_count_thres:
            self._reset_normal_cnt()
            return True
        return False

    def generate_amount(self, name):
        if self.names_dict[name]:
            abnormal = choices([False, True], weights=[0.7, 0.3])[0]
        else:
            prob = random()
            abnormal = prob >= self.abnormal_threshold

        if self._check_abnormal_count_thres() or abnormal:
            self._reset_normal_cnt()
            return random() * 1e10
        else:
            self._update_normal_cnt()
            amount = random() * choices([10, 100, 1000, 1e4, 1e5], weights=[0.35, 0.4, 0.1, 0.1, 0.05])[0]
            if amount < 1:
                amount += 1
            return amount

    def generate(self, i: int, timestamp: dt):
        name = choice(self.names)
        email_address = name+'@card.com'
        card_number = '-'.join([str(randint(1000, 9999)) for _ in range(4)])
        amount = self.generate_amount(name)
        return {
            'timestamp': timestamp.strftime(self.DATETIME_FMT), 
            'email_address': email_address,
            'card_number': card_number,
            'amount': amount
        }

if __name__ == '__main__':
    con = sqlite3.connect('./trans.db')
    con.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            timestamp TEXT,
            email_address TEXT,
            card_number TEXT,
            amount DOUBLE
        );""")
    cur = con.cursor()
    generator = DataGenerator()

    timestamp = dt.now()
    n = 1000
    for i in range(1, n+1):
        random_wait = choice([2, 3, 5, 10])
        timestamp = timestamp + timedelta(seconds=random_wait)
        data = generator.generate(i, timestamp)
        cur.execute(
            """INSERT INTO transactions(timestamp, email_address, card_number, amount) 
            VALUES(:timestamp, :email_address, :card_number, :amount);""",
            data
        )
    con.commit()  # since it is not auto-commit
    con.close()