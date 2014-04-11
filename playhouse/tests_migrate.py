import datetime
import psycopg2
import unittest

from peewee import *
from playhouse.migrate import *


pg_db = PostgresqlDatabase('peewee_test')

class Tag(Model):
    tag = CharField()

    class Meta:
        database = pg_db


class PostgresqlMigrateTestCase(unittest.TestCase):
    integrity_error = IntegrityError

    def setUp(self):
        Tag.drop_table(True)
        Tag.create_table()

        self.migrator = PostgresqlMigrator(pg_db)

    def test_add_column(self):
        df = DateTimeField(null=True)
        df_def = DateTimeField(default=datetime.datetime(2012, 1, 1))
        cf = CharField(max_length=200, default='')
        bf = BooleanField(default=True)
        ff = FloatField(default=0)

        t1 = Tag.create(tag='t1')
        t2 = Tag.create(tag='t2')

        migration = Migration(
            pg_db,
            self.migrator.add_column('tag', 'pub_date', df),
            self.migrator.add_column('tag', 'modified_date', df_def),
            self.migrator.add_column('tag', 'comment', cf),
            self.migrator.add_column('tag', 'is_public', bf),
            self.migrator.add_column('tag', 'popularity', ff),
        )
        migration.run()

        curs = pg_db.execute_sql('select id, tag, pub_date, modified_date, comment, is_public, popularity from tag order by tag asc')
        rows = curs.fetchall()

        self.assertEqual(rows, [
            (t1.id, 't1', None, datetime.datetime(2012, 1, 1), '', True, 0.0),
            (t2.id, 't2', None, datetime.datetime(2012, 1, 1), '', True, 0.0),
        ])

    """
    def test_rename_column(self):
        t1 = Tag.create(tag='t1')

        with db.transaction():
            self.migrator.rename_column(Tag, 'tag', 'foo')

        curs = db.execute_sql('select foo from tag')
        rows = curs.fetchall()

        self.assertEqual(rows, [
            ('t1',),
        ])

    def test_drop_column(self):
        t1 = Tag.create(tag='t1')

        with db.transaction():
            self.migrator.drop_column(Tag, 'tag')

        curs = db.execute_sql('select * from tag')
        rows = curs.fetchall()

        self.assertEqual(rows, [
            (t1.id,),
        ])

    def test_set_nullable(self):
        t1 = Tag.create(tag='t1')

        with db.transaction():
            self.migrator.set_nullable(Tag, Tag.tag, True)

        t2 = Tag.create(tag=None)
        tags = [t.tag for t in Tag.select().order_by(Tag.id)]
        self.assertEqual(tags, ['t1', None])

        t2.delete_instance()

        with db.transaction():
            self.migrator.set_nullable(Tag, Tag.tag, False)

        with db.transaction():
            self.assertRaises(self.integrity_error, Tag.create, tag=None)

    def test_rename_table(self):
        t1 = Tag.create(tag='t1')

        self.migrator.rename_table(Tag, 'tagzz')
        curs = db.execute_sql('select * from tagzz')
        res = curs.fetchall()

        self.assertEqual(res, [
            (t1.id, 't1'),
        ])

        self.migrator.rename_table(Tag, 'tag')
    """
