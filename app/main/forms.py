from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired

from ..models import ShebeiTable

# 新增设备 - 表单
class CreateShebeiForm(FlaskForm):
    shebei_name = StringField('机架名', validators=[DataRequired()]) #设备1

    front_slotNums = IntegerField('96芯设备单元数', default=9) #front_96_slotNums=range(1,10) #9
    front_slot_rows = IntegerField('每个96芯设备单元有几排', default=4) #96芯4排
    front_slot_cols = IntegerField('每个96芯设备单元有几列', default=24) #96芯24列

    back_slotNums = IntegerField('72芯配线单元数', default=12) #96芯12块
    back_slot_rows = IntegerField('每个72芯配线单元有几排', default=6) #96芯4排
    back_slot_cols = IntegerField('每个72芯配线单元有几列', default=12) #96芯4排

    submit = SubmitField('新增机架')

# 选择设备 - 表单
class SelectShebeiForm(FlaskForm):
    jiechushebei = SelectField('1. 请选择此次跳纤的接出机架', coerce=str)
    jiechushebei_side = SelectField('请选择从机架的「96芯设备单元」还是「72芯配线单元」接出', choices=[('96芯设备单元','96芯设备单元'),('72芯配线单元','72芯配线单元')])
    jierushebei = SelectField('2. 请选择此次跳纤的接入机架', coerce=str)
    jierushebei_side = SelectField('请选择从机架的「96芯设备单元」还是「72芯配线单元」接出', choices=[('96芯设备单元','96芯设备单元'),('72芯配线单元','72芯配线单元')])
    # submit = SubmitField('开始计算')
    # reset = SubmitField('重新选择')
    # step = SubmitField('跳纤步骤')
    submit = SubmitField('下一步')

    def __init__(self, *args, **kwargs):
        super(SelectShebeiForm, self).__init__(*args, **kwargs)
        self.jiechushebei.choices = [(shebei.shebei_name,shebei.shebei_name) for shebei in ShebeiTable.query.all()]
        self.jierushebei.choices = [(shebei.shebei_name,shebei.shebei_name) for shebei in ShebeiTable.query.all()]
