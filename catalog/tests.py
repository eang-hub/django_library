from django.test import TestCase

# Create your tests here.
from django.test import TestCase

class YourTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        # 注释：setUpTestData: 只运行一次，用于为所有类方法设置不会被修改的数据。
        # 此方法只被调用一次，用于创建测试用例中需要重复使用但不修改的数据。
        pass

    def setUp(self):
        # 注释：setUp: 对每个测试方法运行一次，用于设置干净的数据。
        # 在每个测试方法执行前被调用，用于设置或重置测试环境的状态，确保数据的独立性。
        pass

    def test_false_is_false(self):
        # 注释：方法：test_false_is_false。
        # 测试False是否被评估为False，这是一个应该通过的测试。
        self.assertFalse(False)

    def test_false_is_true(self):
        # 注释：方法：test_false_is_true。
        # 测试False是否被评估为True，这是一个故意设计为失败的测试，用于演示测试断言如何工作。
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        # 注释：方法：test_one_plus_one_equals_two。
        # 测试1加1是否等于2，这也是一个应该通过的测试。
        self.assertEqual(1 + 1, 2)