#!/usr/bin/python
# -*- coding: utf-8 -*-


emoji = {
    'thanks': ' (｡◕ˇ∀ˇ◕）',
    'cannot_help': ' ㄟ( ▔, ▔ )ㄏ',
    'dozing': ' _(:3 」∠)_',
}


String = {
    'wrong_argument': '无效的命令' + emoji['cannot_help'],
    'thanks_to_donate': '帮 Cycoe 买一杯咖啡吧',
    'failed_fetch_login': '抓取登录页面数据失败' + emoji['cannot_help'],
    'max_attempts': '达到最大重试次数' + emoji['cannot_help'],
    'server_unreachable': '可能是远程服务器不可用' + emoji['cannot_help'],
    'username': '学号: ',
    'password': '密码: ',
    'failed_fetch_vertify_code': '抓取验证码失败' + emoji['cannot_help'],
    'retrying': '正在重试...' + emoji['dozing'],
    'no_such_a_user': '用户名不存在' + emoji['cannot_help'],
    'wrong_password': '密码错误' + emoji['cannot_help'],
    'wrong_vertify_code': '验证码错误' + emoji['cannot_help'],
    'clean_password': '正在清理错误的密码文件...' + emoji['dozing'],
    'empty_vertify_code': '请输入验证码' + emoji['cannot_help'],
    'login_successfully': '登录成功' + emoji['thanks'],
    'failed_fetch_report': '抓取报告列表失败' + emoji['cannot_help'],
    're-login': '可能需要重新登录' + emoji['cannot_help'],
    'failed_post_report': '提交抢报告请求失败' + emoji['cannot_help'],
    'login_first': '请先登录' + emoji['cannot_help'],
    'sending_a_test_mail': '正在向你的邮箱发送测试邮件...' + emoji['dozing'],
    'check_in_trash_box': '如果没有收到测试邮件，请检查一下垃圾箱中的邮件' + emoji['cannot_help'],
    'sender_mail_address': '发送者邮箱地址: ',
    'nickname': '发送者昵称: ',
    'just_test_connection': '邮箱连接测试',
    'test_connection': '测试 class_robber 与邮箱之间的连接，无需回复。',
    'robbing_report': '检测到报告，开抢...',
    'dozing': '没有报告可抢，开始休眠...' + emoji['dozing'],
    'robbed_new_reports': '抢到新报告' + emoji['thanks'],
    'site_cleaning': '清理现场...',
    'exiting': '正在退出...',
    'have_send_a_mail': '已向你的邮箱中发送通知邮件',
    'to_mail': '目标邮箱: ',
    'failed_send_email': '邮件发送失败' + emoji['cannot_help'],
    'check_your_email_address': '请检查你的邮箱地址是否正确: ',
    'cannot_handle_decode': '无法对邮件的编码进行解析' + emoji['cannot_help'],
    'check_your_computer_name': '请将你的电脑主机名设为英文' + emoji['cannot_help'],
    'alipay': '支付宝' + emoji['thanks'],
    'wechat': '微信' + emoji['thanks'],
    'not_now': '先用用看' + emoji['dozing'],
    'remember_to_donate': '觉得好用别忘了赏我一杯咖啡钱哦' + emoji['thanks'],
    'thanks_to_support': '感谢支持！' + emoji['thanks'],
}
