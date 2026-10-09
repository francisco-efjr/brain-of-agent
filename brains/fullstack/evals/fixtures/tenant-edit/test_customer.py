import sqlite3
import unittest
import tempfile
from pathlib import Path
from customer import edit_customer, CustomerNotFound

class CustomerTests(unittest.TestCase):
    def setUp(self):
        self.db=sqlite3.connect(':memory:')
        self.db.execute('CREATE TABLE customers(id INTEGER PRIMARY KEY, tenant_id TEXT, name TEXT)')
        self.db.executemany('INSERT INTO customers VALUES (?,?,?)',[(1,'a','Alice'),(2,'b','Bob')])
        self.db.commit()
        self.addCleanup(self.db.close)
    def snapshot(self):
        return self.db.execute('SELECT * FROM customers ORDER BY id').fetchall()
    def test_cross_tenant_no_mutation(self):
        before=self.snapshot()
        with self.assertRaises(CustomerNotFound): edit_customer(self.db,'a',2,'Stolen')
        self.assertEqual(self.snapshot(),before)
    def test_missing_and_foreign_same_public_error(self):
        errors=[]
        for ident in (999,2):
            with self.assertRaises(CustomerNotFound) as caught: edit_customer(self.db,'a',ident,'Valid')
            errors.append((type(caught.exception),str(caught.exception)))
        self.assertEqual(errors[0],errors[1])
    def test_valid_trim_persist_other_untouched(self):
        edit_customer(self.db,'a',1,'  Ana  ')
        self.assertEqual(self.snapshot(),[(1,'a','Ana'),(2,'b','Bob')])
        self.assertFalse(self.db.in_transaction)
    def test_invalid_name_no_mutation(self):
        for value in (None,123,True,b'Name','',' \t\n ','x'*101):
            with self.subTest(value=repr(value)):
                before=self.snapshot()
                with self.assertRaises(ValueError): edit_customer(self.db,'a',1,value)
                self.assertEqual(self.snapshot(),before)
    def test_length_boundaries_after_trim(self):
        for length in (1,99,100):
            with self.subTest(length=length):
                edit_customer(self.db,'a',1,'  '+'é'*length+'  ')
                self.assertEqual(self.snapshot()[0][2],'é'*length)
    def test_parameterized_input(self):
        payload="x', tenant_id='b' --"
        edit_customer(self.db,'a',1,payload)
        self.assertEqual(self.snapshot(),[(1,'a',payload),(2,'b','Bob')])
    def test_tenant_none_no_authority(self):
        before=self.snapshot()
        with self.assertRaises(CustomerNotFound): edit_customer(self.db,None,1,'Name')
        self.assertEqual(self.snapshot(),before)
    def test_persistence_after_reconnect(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'fixture.sqlite'
            with sqlite3.connect(path) as db:
                db.execute('CREATE TABLE customers(id INTEGER PRIMARY KEY, tenant_id TEXT, name TEXT)')
                db.execute('INSERT INTO customers VALUES (1, ?, ?)',('a','Before'))
            db=sqlite3.connect(path)
            try:
                edit_customer(db,'a',1,'  Persisted  ')
            finally:
                db.close()
            with sqlite3.connect(path) as db:
                self.assertEqual(db.execute('SELECT name FROM customers WHERE id=1').fetchone(),('Persisted',))

    def test_repeated_valid_edit(self):
        edit_customer(self.db,'a',1,'Ana')
        edit_customer(self.db,'a',1,'Ana')
        self.assertEqual(self.snapshot(),[(1,'a','Ana'),(2,'b','Bob')])
if __name__=='__main__': unittest.main()
