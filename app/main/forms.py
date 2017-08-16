from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired

from ..models import ShebeiTable

# 新增设备 - 表单
class CreateShebeiForm(FlaskForm):
    shebei_name = StringField('设备名', validators=[DataRequired()]) #设备1

    front_slotNums = IntegerField('正面Slot数量', default=9) #front_96_slotNums=range(1,10) #9
    front_slot_rows = IntegerField('正面每块Slot有几排', default=4) #96芯4排
    front_slot_cols = IntegerField('正面每块Slot有几列', default=24) #96芯24列

    back_slotNums = IntegerField('背面Slot数量', default=12) #96芯12块
    back_slot_rows = IntegerField('背面面每块Slot有几排', default=6) #96芯4排
    back_slot_cols = IntegerField('背面面每块Slot有几列', default=12) #96芯4排

    submit = SubmitField('新增设备')

# 选择设备 - 表单
class SelectShebeiForm(FlaskForm):
    jiechushebei = SelectField('1. 请选择此次跳纤的接出设备', coerce=str)
    jiechushebei_side = SelectField('请选择正面（96芯）端口还是背面（72芯）端口', choices=[('正面','正面'),('背面','背面')])
    jierushebei = SelectField('2. 请选择此次跳纤的接入设备', coerce=str)
    jierushebei_side = SelectField('请选择正面（96芯）端口还是背面（72芯）端口', choices=[('正面','正面'),('背面','背面')])
    # submit = SubmitField('开始计算')
    # reset = SubmitField('重新选择')
    # step = SubmitField('跳纤步骤')
    submit = SubmitField('下一步')

    def __init__(self, *args, **kwargs):
        super(SelectShebeiForm, self).__init__(*args, **kwargs)
        self.jiechushebei.choices = [(shebei.shebei_name,shebei.shebei_name) for shebei in ShebeiTable.query.all()]
        self.jierushebei.choices = [(shebei.shebei_name,shebei.shebei_name) for shebei in ShebeiTable.query.all()]
