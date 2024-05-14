from django.test import TestCase
from catalog.models import Author

# python manage.py test catalog.tests.test_models
class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # 初始化公共数据，此方法会在测试开始前只运行一次
        # 创建一个名为'Big Bob'的作者对象，被全体测试方法共享
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        # 测试模型的 first_name 字段标签是否为 "first name"
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label,'first name')

    def test_date_of_death_label(self):
        # 测试模型的 date_of_death 字段标签是否为 "died"
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label,'died')

    def test_first_name_max_length(self):
        # 测试模型的 first_name 字段的最大长度是否为100
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        # 测试对象的字符串表示形式是否为 "姓, 名"
        author = Author.objects.get(id=1)
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        self.assertEquals(expected_object_name,str(author))

    def test_get_absolute_url(self):
        # 测试 get_absolute_url 方法返回的URL是否正确
        # 如果urlconf未定义，则测试将会失败。
        author = Author.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(),'/catalog/author/1')



    def test_object_name_is_last_name_comma_first_name(self):
        # 于验证Author模型对象转换为字符串时是否是姓, 名的格式
        # 获取id为1的作者对象
        author = Author.objects.get(id=1)
        # 将期望的对象名设置为 "姓, 名" 的格式
        expected_object_name = '%s, %s' % (author.last_name, author.first_name)
        # 检查获取的作者对象转为字符串后是否与期望的对象名匹配
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        # 验证get_absolute_url方法返回的URL是否正确
        # 获取id为1的作者对象
        author = Author.objects.get(id=1)
        # 检查获取的作者对象的get_absolute_url方法返回的url是否与期望的url匹配
        # 如果urlconf未定义，这个测试将会失败。
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')