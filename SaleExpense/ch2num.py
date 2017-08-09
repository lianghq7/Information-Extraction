# -*- coding: utf-8 -*

common_used_numerals_tmp ={u'零':u'0',u'〇':u'0',u'○':u'0',u'一':u'1', u'二':u'2', u'两':u'2', u'三':u'3', u'四':u'4', u'五':u'5', \
                           u'六':u'6', u'七':u'7', u'八':u'8', u'九':u'9',u'十':u'1'}
# common_used_numerals_tmp ={'零':'0','〇':'0', '一':'1', '二':'2', '两':'2', '三':'3', '四':'4', '五':'5', \
#                            '六':'6', '七':'7', '八':'8', '九':'9','十':'1'}

def chinese2digits(uStr):
    for i in range(len(uStr)-1):
        if uStr[i] in common_used_numerals_tmp.keys():
            uStr = uStr.replace(uStr[i],common_used_numerals_tmp[uStr[i]],5)
    return uStr

# print(chinese2digits('二○○七年年度报告'))
