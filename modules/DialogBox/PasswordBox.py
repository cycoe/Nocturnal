import re
from getpass import getpass

from modules.DialogBox.BaseBox import BaseBox


class PasswordBox(BaseBox):

    def __init__(self, title=None):
        super(PasswordBox, self).__init__(title)

    def input(self):
        """
        處理輸入的匹配問題
        :return: 輸入結果
        """
        while True:
            result = getpass(self.prompt)
            # 當輸入爲空但缺省輸入非空時，直接返回缺省值，對應不對缺省值進行修改的情況
            if result == '' and self.default_output != '':
                return self.default_output

            # 此處使用 re.fullmatch 函數進行完全匹配
            if re.fullmatch(self.pattern, result):
                break
            else:
                print(self.warning)

        return result
