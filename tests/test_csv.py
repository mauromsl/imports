from django.test import TestCase

from plugins.imports.csv import fields, CSVMeta, CSV


class TestCSVModel():
    pass


class TestCSVFields(TestCase):

    def test_valid_string_field(self):
        field = fields.StringField(max_length=255)
        field.value = "This is my string"
        self.assertEqual(field.validate(), None,
                         msg="%s not a valid StringField value" % field.value)

    def test_invalid_string(self):
        field = fields.StringField(max_length=255)
        field.value = object()
        self.assertNotEqual(field.validate(), None,
                            msg="%s should not validate as a StringField value"
                            "" % field.value)

    def test_invalid_string_too_long(self):
        field = fields.StringField(max_length=1)
        field.value = "12"
        self.assertNotEqual(field.validate(), None,
                            msg="%s should not validate as a StringField value"
                            "" % field.value)

    def test_valid_integer_field(self):
        field = fields.IntegerField()
        field.value = 1
        self.assertEqual(field.validate(), None,
                         msg="%s not a valid IntegerField value" % field.value)

    def test_invalid_integer(self):
        field = fields.IntegerField()
        field.value = object()
        self.assertNotEqual(field.validate(), None,
                            msg="%s should not validate as a StringField value"
                            "" % field.value)

    def test_valid_email(self):
        field = fields.EmailField()
        field.value = "email@dummy.org"
        self.assertEqual(field.validate(), None,
                         msg="%s not a valid EmailField value" % field.value)

    def test_invalid_email(self):
        field = fields.IntegerField()
        field.value = "invalidemail"
        self.assertNotEqual(field.validate(), None,
                            msg="%s should not validate as an EmailField value"
                            "" % field.value)

class TestCSVMeta(TestCase):

    def test_row_type(self):
        class TestCSV(metaclass=CSVMeta):
            test_field = fields.Field()

        test_csv = TestCSV()
        self.assertTrue(hasattr(test_csv, "row_type"))

    def test_row_slots(self):
        class TestCSV(metaclass=CSVMeta):
            test_field = fields.Field()

        test_csv = TestCSV()
        row = test_csv.row_type()
        self.assertTupleEqual(("test_field",), row.__slots__)


class TestCSV(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        class CSVTest(CSV):
            field = fields.IntegerField()

        cls.csv_class = CSVTest

    def test_create_csv(self):
        row = 1,
        csv_obj = self.csv_class(row)
        expected = [self.csv_class.row_type(*row)]
        self.assertEqual(expected[0], csv_obj._rows[0])
        self.assertListEqual(expected, csv_obj._rows)
