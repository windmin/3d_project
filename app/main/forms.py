from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired

# from ..models import CaizhixishuTable,PumpPriceTable,MifengjiageTable,BaojialiebiaoTable,MotorTable,GroupTable,DianjijiageTable,OtherTable
from flask_login import current_user



# #泵选型报价列表 - 表单
# class BengxuanxingListbiao(FlaskForm):
#     add_baojialiebiao = SubmitField('新建报价')
#     export_baojialiebiao = SubmitField('导出报价')
