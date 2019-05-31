import unittest

from ..base import Model


class TestModelsBase(unittest.TestCase):
    def test_simple(self):
        m = Model(schema={
            "a": ("str", Model.OPTIONAL)
        })
        assert isinstance(m, Model)

    def test_raises_exception_empty_schema(self):
        self.assertRaises(KeyError, Model)

    def test_empty_dump(self):
        m = Model(schema={
            "a": ("str", Model.OPTIONAL)
        })
        self.assertEqual(m.dump(), {})

    def test_flat_dump(self):
        m = Model(schema={
            "a": ("int", Model.OPTIONAL),
            "b": ("str", Model.REQUIRED)
        })
        m._setup(a=1, b="123")

        dump = m.dump()
        self.assertEqual(len(dump), 2)
        self.assertIsInstance(dump, dict)
        self.assertEqual(dump["a"], 1)
        self.assertEqual(dump["b"], "123")

    def test_nested_dump(self):
        m_nested = Model(schema={
            "d": ("int", Model.REQUIRED)
        })

        m = Model(schema={
            "a": ("int", Model.OPTIONAL),
            "b": ("str", Model.REQUIRED),
            "e": (m_nested, Model.REQUIRED)
        })

        m._setup(
            a=1,
            b=2,
            c="NOT_IN_DUMP",
            e=m_nested._setup(d=22)
        )

        dump = m.dump()
        self.assertEqual(len(dump), 3)
        self.assertIsInstance(dump, dict)
        self.assertIsInstance(dump["e"], dict)

        self.assertEqual(dump["e"]["d"], 22)
        self.assertEqual(dump["a"], 1)
        self.assertEqual(dump["b"], 2)

    def test_model_field_type(self):
        m = Model({
            "a": ("str", Model.REQUIRED),
            "b": ("str", Model.OPTIONAL)
        })

        self.assertIsInstance(m.SCHEMA["a"][1], Model._REQ)
        self.assertIsInstance(m.SCHEMA["b"][1], Model._OPT)

    def test_load_valid_flat_schema(self):
        m = Model(schema={
            "a": ("int", Model.OPTIONAL),
            "b": ("int", Model.REQUIRED)
        }).load({"b": 3})

        self.assertEqual(len(m.__dict__), 1)
        self.assertEqual(m.b, 3)

    def test_load_nested_schema(self):
        m_nested = Model({"nested": Model.OPTIONAL})

        m = Model(schema={
            "a": (m_nested, Model.OPTIONAL),
            "b": ("str", Model.REQUIRED)
        }).load({
            "a": {"c": 1},
            "b": 3,
            "d": "NOT_IN_SCHEMA"
        })

        self.assertEqual(len(m.__dict__), 3)
        self.assertEqual(len(m.a.__dict__), 1)

        self.assertEqual(m.a.c, 1)
        self.assertEqual(m.b, 3)
        self.assertEqual(m.d, "NOT_IN_SCHEMA")

    def test_assert_setup_raises_key_error(self):
        m = Model(schema={
            "b": ("str", Model.REQUIRED)
        })
        self.assertRaises(KeyError, m._setup, c=1)

    def test_model_setup(self):
        m = Model(schema={
            "a": ("str", Model.OPTIONAL),
            "b": ("str", Model.OPTIONAL)
        })

        m._setup(a=1, b=2)

        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 2)

    def test_model_setup_optional_field(self):
        m = Model(schema={
            "a": ("str", Model.OPTIONAL),
            "b": ("str", Model.OPTIONAL),
            "c": ("int", Model.REQUIRED)
        },
            c=12
        )

        d = m.dump(skip_none=False)

        self.assertEqual(len(d), 3)
        self.assertIsNone(d["a"])
        self.assertIsNone(d["b"])
        self.assertEqual(d["c"], 12)

    def test_inherited_class(self):
        class m(Model):
            _SCHEMA_ = {
                "a": ("str", Model.OPTIONAL),
                "b": ("int", Model.REQUIRED)
            }

        m1 = m(b=1).dump()
        m2 = m(b=2).dump()
        self.assertNotEqual(m1, m2)

        self.assertEqual(m1["b"], 1)
        self.assertEqual(m2["b"], 2)


if __name__ == '__main__':
    unittest.main()

