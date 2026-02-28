"""
自定义密码验证器，提供中文错误消息
"""

from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator
)

class ChineseUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    """中文用户属性相似性验证器"""
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except Exception as e:
            # 将英文错误消息转换为中文
            if "too similar" in str(e).lower():
                raise Exception("密码与用户名或邮箱过于相似，请选择更复杂的密码")
            raise

class ChineseMinimumLengthValidator(MinimumLengthValidator):
    """中文最小长度验证器"""
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except Exception as e:
            if "too short" in str(e).lower():
                raise Exception(f"密码长度至少需要{self.min_length}个字符")
            raise

class ChineseCommonPasswordValidator(CommonPasswordValidator):
    """中文常用密码验证器"""
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except Exception as e:
            if "common" in str(e).lower():
                raise Exception("密码过于常见，请选择更复杂的密码")
            raise

class ChineseNumericPasswordValidator(NumericPasswordValidator):
    """中文纯数字密码验证器"""
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except Exception as e:
            if "numeric" in str(e).lower():
                raise Exception("密码不能全是数字，请包含字母或其他字符")
            raise