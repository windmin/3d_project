from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired

from ..models import ShebeiTable

# 新增设备 - 表单
class CreateShebeiForm(FlaskForm):
    shebei_name = StringField('机架名') #设备1

    front_slotNums = IntegerField('96芯设备单元数', default=9) #front_96_slotNums=range(1,10) #9
    front_slot_rows = IntegerField('每个96芯设备单元有几排', default=4) #96芯4排
    front_slot_cols = IntegerField('每个96芯设备单元有几列', default=24) #96芯24列

    back_slotNums = IntegerField('72芯配线单元数', default=12) #72芯12块
    back_slot_rows = IntegerField('每个72芯配线单元有几排', default=6) #72芯6排
    back_slot_cols = IntegerField('每个72芯配线单元有几列', default=12) #72芯12列

    shebei_place = IntegerField('机架放置位置（第几排）')

    submit = SubmitField('添加机架')

# 选择设备 - 表单
class SelectShebeiForm(FlaskForm):
    shebei_count = SelectField('请选择需要跳纤的机架数', coerce=int)
    jiechushebei = SelectField('请选择此次跳纤的接出机架', coerce=str)
    # jiechushebei_side = SelectField('请选择接出单元', choices=[('96芯设备单元','96芯设备单元'),('72芯配线单元','72芯配线单元')])
    jierushebei = SelectField('请选择此次跳纤的接入机架', coerce=str)
    # jierushebei_side = SelectField('请选择接入单元', choices=[('96芯设备单元','96芯设备单元'),('72芯配线单元','72芯配线单元')])
    submit = SubmitField('下一步 >')

    def __init__(self, *args, **kwargs):
        super(SelectShebeiForm, self).__init__(*args, **kwargs)
        self.jiechushebei.choices = [(shebei.shebei_name,shebei.shebei_name) for shebei in ShebeiTable.query.all()]
        self.jierushebei.choices = [(shebei.shebei_name,shebei.shebei_name) for shebei in ShebeiTable.query.all()]
        self.shebei_count.choices = [(count,count) for count in range(1,ShebeiTable.query.count()+1)]
