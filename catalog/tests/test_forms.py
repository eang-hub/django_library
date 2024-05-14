from django.test import TestCase
import datetime
from django.utils import timezone
from catalog.forms import RenewBookForm


class RenewBookFormTest(TestCase):
    # 定义一个测试类，用来对RenewBookForm表单进行测试

    def test_renew_form_date_field_label(self):
        # 测试renewal_date字段的标签是否符合预期（为空或者为'renewal date'）
        form = RenewBookForm()
        self.assertTrue(
            form.fields['renewal_date'].label == None or form.fields['renewal_date'].label == 'renewal date')

    def test_renew_form_date_field_help_text(self):
        # 测试renewal_date字段的帮助文本是否符合预期
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        # 测试当输入过去的日期时，表单的验证结果应该为无效
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        # 测试当输入超出未来四周的日期时，表单的验证结果应该为无效
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        # 测试当输入今天的日期时，表单的验证结果应该为有效
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        # 测试当输入最多四周后的日期时，表单的验证结果应该为有效
        date = timezone.now() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())