from bs4 import BeautifulSoup
import re
import ch2num
import os
import sys
# -*- coding: utf-8 -*

def fuzzyfinder(user_input, collection):  #公司简称模糊匹配
    if collection == None:
        return 0
    if len(re.findall(r'\(|\)|\）|\（',user_input))>0 or len(re.findall(r'“|”',user_input)) > 0 or len(re.findall(r'\*',user_input)) > 0:
        return 0
    is_match = 0
    pattern = '.*'.join(user_input) # Converts 'djm' to 'd.*j.*m'
    try:
        regex = re.compile(pattern)     # Compiles a regex.
        match = regex.search(collection)  # Checks if the current item matches the regex.
        if match:
            is_match = 1
    except(Exception) as ex:
        print('error:',ex)
    finally:
        return is_match

def find_previous_div(current_div):  #该函数特别用于寻找表格标题，其他地方不适用
    div_previous = None
    div_previous_set = current_div.find_previous_siblings('div')
    div_temp = current_div
    div_previous_bool = 0
    while len(div_previous_set) == 0:
        div_temp = div_temp.find_parent('div')
        if (div_temp['class'])[0] == 'pc' or (div_temp['class'])[0] == 'pf':
            div_previous_bool = 1
            break
        else:
            div_previous_set = div_temp.find_previous_siblings('div')

    if len(div_previous_set)>0 and div_previous_bool == 0 :
        div_previous = div_previous_set[0]

    return div_previous





def find_next_div(current_div):  # 由于每一个内容项div都包括在外层的page div里，此函数可在到达页面底部时跳到下一个页面，并且自动略过页眉页脚div
    next_div = current_div.find_next_sibling('div')
    div_temp = current_div
    while next_div is None:
        next_div = div_temp.find_parent('div').find_next_sibling('div')
        div_temp = div_temp.find_parent('div')
    # if not next_div:
    #     if ((current_div.find_parent('div').find_next_sibling('div'))['class'])[0] == 'pi':
    #         next_page = current_div.find_parent('div', class_='pf').find_next_sibling('div', class_='pf')
    #         if next_page:
    #             next_div_pc = next_page.find('div')
    #             next_div_set = next_div_pc.find_all('div')
    #             if not next_div_set[2].find_next_sibling('div'):
    #                 next_div = next_div_set[2].find_parent('div').find_next_sibling('div')
    #             else:
    #                 next_div = next_div_set[2]
    #     else:
    #         next_div = current_div.find_parent('div').find_next_sibling('div')

    if (next_div['class'])[0] == 'pi':
        next_page = current_div.find_parent('div', class_='pf').find_next_sibling('div', class_='pf')
        if next_page:
            next_div_pc = next_page.find('div')
            next_div_set = next_div_pc.find_all('div')
            if not next_div_set[1].find_next_sibling('div'):
                next_div = next_div_set[1].find_parent('div').find_next_sibling('div')
            else:
                next_div = next_div_set[1]

    # next_div = current_div.find_next_sibling('div')
    # if not next_div:
    #     next_page = current_div.find_parent('div', class_='pf').find_next_sibling('div', class_='pf')
    #     if next_page:
    #         next_div_pc = next_page.find('div')
    #         next_div_set = next_div_pc.find_all('div')
    #         if not next_div_set[2].find_next_sibling('div'):
    #             next_div = next_div_set[2].find_parent('div').find_next_sibling('div')
    #         else:
    #             next_div = next_div_set[2]
    #         # next_div = next_page.find('div', class_='t').find_next_sibling('div').find_next_sibling('div')

    return next_div

def build_original_table(current_td_div): #根据当前找到的表格的第一项，搜索出整个表格并输出
    original_table = ''

    begin_tag = 0

    paging_tag = 0

    refinish_tag = 0

    passed_tag = 0

    # try:
    #     while current_td_div:
    #
    #         if (refinish_tag == 1 and len(re.findall(r'[\u4e00-\u9fa5]+', current_td_div.get_text())) > 0) or \
    #                 (begin_tag == 1 and len(
    #                     re.findall(r'\d\d.{1,4}[\u4e00-\u9fa5]{4,}', current_td_div.get_text())) > 0):
    #             break
    #         else:
    #             begin_tag = 1
    #
    #             if refinish_tag == 0 and len(re.findall(r'合\s*计', current_td_div.get_text())) > 0:
    #                 refinish_tag = 1
    #             if (paging_tag == 1 and len(re.findall(r'[\u4e00-\u9fa5]{2,15}', current_td_div.get_text())) > 0) or \
    #                     (paging_tag == 0):
    #                 if (paging_tag == 1):
    #                     original_table += '<div class="paging"></div>'
    #                     paging_tag = 0
    #                 original_table += str(current_td_div)
    #
    #         current_td_div = find_next_div(current_td_div)
    # except Exception as ex:
    #     print(ex)
    #     print(sys.exc_info())
    # finally:
    #     original_table = 'error'
    while current_td_div:

        if (refinish_tag == 1 and len(re.findall(r'[\u4e00-\u9fa5]+',current_td_div.get_text())) > 0) or \
                (begin_tag == 1 and len(re.findall(r'\d\d.{1,4}[\u4e00-\u9fa5]{4,}', current_td_div.get_text())) > 0 and len(re.findall(r'[年发生额度]', current_td_div.get_text())) == 0) or (begin_tag == 1 and len(re.findall(r'(\b管\s*理\s*费\s*用\b)|(财\s*务\s*报\s*表\s*附\s*注)|(\b财\s*务\s*费\s*用\b)|(\b说\s*明\s*：?)|(\b其\s*他\s*说\s*明\s*：?)|(\b其\s*它\s*说\s*明\s*：?)', current_td_div.get_text())) == 1):
            # if(len(re.findall(r'管\s*理\s*费\s*用', current_td_div.get_text())) == 1) and len(re.findall(r'\d|[一二三四五六七八九]', current_td_div.get_text())) == 0:
            #     original_table -= str(find_previous_div(current_td_div))
            break
        else:
            begin_tag = 1

            if refinish_tag == 0 and len(re.findall(r'合\s*计', current_td_div.get_text())) > 0:
                refinish_tag = 1
            if (paging_tag == 1 and len(re.findall(r'[\u4e00-\u9fa5]{2,15}', current_td_div.get_text())) > 0) or\
                    (paging_tag == 0):
                if paging_tag == 1:
                    original_table += '<div class="paging"></div>'
                    paging_tag = 0
                original_table += str(current_td_div)

        # current_td_div = find_next_div(current_td_div)
        next_div = current_td_div.find_next_sibling('div')
        div_temp = current_td_div
        while next_div is None:
            next_div = div_temp.find_parent('div').find_next_sibling('div')
            div_temp = div_temp.find_parent('div')

        if (next_div['class'])[0] == 'pi' and passed_tag == 0:
            next_page = current_td_div.find_parent('div', class_='pf').find_next_sibling('div', class_='pf')
            if next_page:
                passed_tag = 1
                paging_tag = 1
                next_div_pc = next_page.find('div')
                next_div_set = next_div_pc.find_all('div')
                if not next_div_set[2].find_next_sibling('div'):
                    next_div = next_div_set[2].find_parent('div').find_next_sibling('div')
                else:
                    next_div = next_div_set[2]

        if (next_div['class'])[0] == 'pi' and passed_tag == 1:
            break

        current_td_div = next_div
        # print(current_td_div)
    return original_table


def information_extract(html_filename):
    soup = BeautifulSoup(open(html_filename,'rb'), "lxml", from_encoding="utf-8")
    pf = soup.findAll(class_='pf')
    def else_inEX_else(): #未读到表格的处理
        #先找到利润表或合并利润表的大标题
        find_bool = 0
        startpf = -1
        for i in range(10, int(len(pf))):
            if find_bool == 1:
                break
            page_temp_pc = pf[i].find('div')
            page_temp = page_temp_pc.find_all('div')
            for div_temp in page_temp:
                div_temp_cursor_str = re.findall(r'\b合\s*并\s*利\s*润\s*表\b', div_temp.get_text())
                div_temp_cursor_str1 = re.findall(r'\b利\s*润\s*表\b', div_temp.get_text())
                div_temp_cursor_str2 = re.findall(r'\b[^、]*合\s*并\s*利\s*润\s*表\b', div_temp.get_text())
                div_temp_cursor_str3 = re.findall(r'\b[^、]*利\s*润\s*表\b', div_temp.get_text())
                div_temp_cursor_str4 = re.findall(r'\b[^、]*利\s*润\s*分\s*配\s*表\b', div_temp.get_text())
                countlen = len(div_temp_cursor_str)
                countlen1 = len(div_temp_cursor_str1)
                countlen2 = len(div_temp_cursor_str2)
                countlen3 = len(div_temp_cursor_str3)
                countlen4 = len(div_temp_cursor_str4)
                if countlen > 0:
                    div_temp_cursor = (div_temp.get_text()).find(div_temp_cursor_str[0])
                    div_temp_str = (div_temp.get_text())[0:div_temp_cursor]
                    div_temp_str2 = (div_temp.get_text())[div_temp_cursor:]
                    if (len(re.findall(r'[^\s]', div_temp_str2)) - len(re.findall(r'[\u4e00-\u9fa5]',div_temp_cursor_str[0]))) == 0 and (len(re.findall(r'[^\s]', div_temp_str)) == 0):
                       startpf = i
                       find_bool = 1
                       break
                if countlen1 > 0:
                    div_temp_cursor = (div_temp.get_text()).find(div_temp_cursor_str1[0])
                    div_temp_str = (div_temp.get_text())[0:div_temp_cursor]
                    div_temp_str2 = (div_temp.get_text())[div_temp_cursor:]
                    if (len(re.findall(r'[^\s]', div_temp_str2)) - len(re.findall(r'[\u4e00-\u9fa5]',div_temp_cursor_str1[0]))) == 0 and (len(re.findall(r'[^\s]', div_temp_str)) == 0):
                       startpf = i
                       find_bool = 1
                       break
                if countlen2 > 0:
                    div_temp_cursor = (div_temp.get_text()).find(div_temp_cursor_str2[0])
                    div_temp_str = (div_temp.get_text())[0:div_temp_cursor]
                    div_temp_str2 = (div_temp.get_text())[div_temp_cursor:]
                    if (len(re.findall(r'[^\s]', div_temp_str2)) - len(re.findall(r'[\u4e00-\u9fa5]', div_temp_cursor_str2[0]))) == 0 and (len(re.findall(r'[^\s]', div_temp_str)) == 0):
                        startpf = i
                        find_bool = 1
                        break
                if countlen3 > 0:
                    div_temp_cursor = (div_temp.get_text()).find(div_temp_cursor_str3[0])
                    div_temp_str = (div_temp.get_text())[0:div_temp_cursor]
                    div_temp_str2 = (div_temp.get_text())[div_temp_cursor:]
                    if (len(re.findall(r'[^\s]', div_temp_str2)) - len(re.findall(r'[\u4e00-\u9fa5]', div_temp_cursor_str3[0]))) == 0 and (len(re.findall(r'[^\s]', div_temp_str)) == 0):
                        startpf = i
                        find_bool = 1
                        break
                if countlen4 > 0:
                    div_temp_cursor = (div_temp.get_text()).find(div_temp_cursor_str4[0])
                    div_temp_str = (div_temp.get_text())[0:div_temp_cursor]
                    div_temp_str2 = (div_temp.get_text())[div_temp_cursor:]
                    if (len(re.findall(r'[^\s]', div_temp_str2)) - len(re.findall(r'[\u4e00-\u9fa5]', div_temp_cursor_str4[0]))) == 0 and (len(re.findall(r'[^\s]', div_temp_str)) == 0):
                        startpf = i
                        find_bool = 1
                        break

        # print(startpf)

        #如果找到了大标题，向下搜索4页
        current_div = None
        if startpf != -1:
            is_end = 0
            for i in range(startpf, min(startpf+5,len(pf))):
                if is_end == 1:
                    break
                page_temp_pc = pf[i].find('div')
                page_temp = page_temp_pc.find_all('div')
                for div_temp in page_temp:
                    div_temp_cursor_str = re.findall(r'\b销售费用\b', div_temp.get_text())
                    countlen = len(div_temp_cursor_str)
                    if countlen > 0:
                        div_temp_cursor = (div_temp.get_text()).find(div_temp_cursor_str[0])
                        div_temp_str = (div_temp.get_text())[:div_temp_cursor]
                        div_temp_str2 = (div_temp.get_text())[div_temp_cursor:]
                        previous_div_str = ''
                        if find_previous_div(div_temp) is not None:
                            previous_div_str = find_previous_div(div_temp).get_text()
                        # print(div_temp)
                        # print(previous_div_str)
                        # print(div_temp.get_text())
                        # 匹配条件找入口
                        if len(re.findall(r'[^\s]', div_temp_str)) == 0 and ((len(
                                re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) - len(
                                re.findall(r'[一二三四五六七八九十]', div_temp_str2))) < 8) and (
                                len(re.findall(r'\d', previous_div_str)) > 3 or len(
                                re.findall(r'\d', previous_div_str)) == 0):
                            if (len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) == 4) and ((len(
                                    re.findall(r'[\u4e00-\u9fa5]', find_next_div(div_temp).get_text())) - len(
                                    re.findall(r'[一二三四五六七八九十]', find_next_div(div_temp).get_text()))) < 3) and (
                                len(re.findall(r'\d', div_temp_str2)) == 0):
                                current_div = div_temp;
                                is_end = 1
                                break
                            else:
                                if ((len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) > 4) and (
                                    len(re.findall(r'\d|[一二三四五六七八九十]', div_temp_str2)) > 0)) or (
                                    (len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) == 4) and (
                                    len(re.findall(r'\d', div_temp_str2)) > 0)):
                                    current_div = div_temp;
                                    is_end = 1
                                    break
        table2str = ''
        max_search_range = 5  # 最大查找范围，如果超过这个数仍然找不到结束标志，则可以结束查找
        while (current_div != None) and (len(re.findall(r'\b管\s*理\s*费\s*用\b',current_div.get_text())) == 0 )and (len(re.findall(r'(\b财\s*务\s*费\s*用\b)|(\b投\s*资\s*收\s*益\b)',current_div.get_text())) == 0) and (max_search_range != 0):
            table2str += str(current_div)
            current_div = find_next_div(current_div)
            max_search_range -= 1
        # return str(table2str)

        current_div2 = None
        if table2str == '':
            is_end = 0

            for i in range(10, int(len(pf))):
                if is_end == 1:
                    break
                page_temp_pc = pf[i].find('div')
                page_temp = page_temp_pc.find_all('div')
                for div_temp in page_temp:
                    div_temp_cursor_str = re.findall(r'\b销售费用\b', div_temp.get_text())
                    countlen = len(div_temp_cursor_str)
                    if countlen > 0:
                        div_temp_cursor = (div_temp.get_text()).find(div_temp_cursor_str[0])
                        div_temp_str = (div_temp.get_text())[:div_temp_cursor]
                        div_temp_str2 = (div_temp.get_text())[div_temp_cursor:]
                        previous_div_str = ''
                        if find_previous_div(div_temp) is not None:
                            previous_div_str = find_previous_div(div_temp).get_text()
                        # 匹配条件找入口
                        if len(re.findall(r'[^\s]', div_temp_str)) == 0 and ((len(
                                re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) - len(
                                re.findall(r'[一二三四五六七八九十]', div_temp_str2))) < 8) and (
                                len(re.findall(r'\d', previous_div_str)) > 3 or len(
                                re.findall(r'\d', previous_div_str)) == 0):
                            if (len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) == 4) and ((len(
                                    re.findall(r'[\u4e00-\u9fa5]', find_next_div(div_temp).get_text())) - len(
                                    re.findall(r'[一二三四五六七八九十]', find_next_div(div_temp).get_text()))) < 3) and (len(re.findall(r'\d', div_temp_str2)) == 0):
                                current_div2 = div_temp;
                                is_end = 1
                                break
                            else:
                                if ((len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) > 4) and (len(re.findall(r'\d', div_temp_str2)) > 2)) or ((len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) == 4) and (len(re.findall(r'\d', div_temp_str2)) > 3)):
                                    current_div2 = div_temp;
                                    is_end = 1
                                    break

        max_search_range2 = 4  # 最大查找范围，如果超过这个数仍然找不到结束标志，则可以结束查找
        while (current_div2 != None) and (len(re.findall(r'\b管\s*理\s*费\s*用\b', current_div2.get_text())) == 0) and (len(re.findall(r'(\b财\s*务\s*费\s*用\b)|(\b投\s*资\s*收\s*益\b)', current_div2.get_text())) == 0) and (max_search_range2 != 0):
            table2str += str(current_div2)
            current_div2 = find_next_div(current_div2)
            max_search_range2 -= 1

        return str(table2str)


    def else_inEX():#未读到目录或目录中没有“销售费用”索引
        current_div = None

        for i in range(len(pf) - 2, int(len(pf) * 0.5), -1):
            # page_temp = pf[i].find_all('div', class_='t')
            page_temp_pc = pf[i].find('div')
            page_temp = page_temp_pc.find_all('div')
            for div_temp in page_temp:
                div_temp_cursor_str = re.findall(r'\b销售费用\b', div_temp.get_text())
                countlen = len(div_temp_cursor_str)
                if countlen > 0:
                    # print(div_temp)
                    # print(div_temp_cursor_str)
                    div_temp_cursor = (div_temp.get_text()).find(div_temp_cursor_str[0])
                    div_temp_str = (div_temp.get_text())[:div_temp_cursor]
                    # print(div_temp_str)
                    div_temp_str2 = (div_temp.get_text())[div_temp_cursor:]
                    # print(div_temp_str2)
                    previous_div_str = ''
                    if find_previous_div(div_temp) is not None:
                        previous_div_str = find_previous_div(div_temp).get_text()
                        previous_div_0 = re.findall('\s*0\s*', previous_div_str)
                        if len(previous_div_0) == 1:
                            if previous_div_str == previous_div_0[0]:
                                previous_div_str = ''

                    if ((len(re.findall(r'\d|[一二三四五六七八九]', div_temp_str)) > 0) and (len(re.findall(r'\d|[一二三四五六七八九]', div_temp_str)) < 3) and (len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str)) < 4) and (len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) < 10)) or\
                            ((len(re.findall(r'\d|[一二三四五六七八九]', div_temp_str)) == 0)and (len(re.findall(r'\d|[一二三四五六七八九]', previous_div_str)) > 0) and (len(re.findall(r'\d|[一二三四五六七八九]', previous_div_str)) < 3) \
                                     and (len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str)) < 4)and (len(re.findall(r'[\u4e00-\u9fa5]', previous_div_str)) < 4) and (len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) < 10)):
                        if len(re.findall(r'\d', div_temp_str)) == 1:
                            if ((re.findall(r'\d', div_temp_str))[0] != '1') and (
                                        (re.findall(r'\d', div_temp_str))[0] != '2') and (
                                (re.findall(r'\d', div_temp_str))[0] != '3'):
                                current_div = div_temp
                                break
                        else:
                            if (len(re.findall(r'\d', div_temp_str)) == 0) and (
                                        len(re.findall(r'\d', previous_div_str)) == 1):
                                if ((re.findall(r'\d', previous_div_str))[0] != '1') and (
                                            (re.findall(r'\d', previous_div_str))[0] != '2') and (
                                    (re.findall(r'\d', previous_div_str))[0] != '3'):
                                    current_div = div_temp
                                    break
                            else:
                                current_div = div_temp
                                break
            if current_div is not None:
                break

        return current_div

    #会计期间
    fiscal_period = None
    year = None
    report_type_temp = None

    for i in range(5):
        str_temp = str(ch2num.chinese2digits(pf[i].get_text())).replace(' ', '')
        year_temp = re.findall(r'2\d*?年度报告|2\d*?年年度报告|2\d*?半年度报告|2\d*?第1季度报告|2\d*?第3季度报告', str_temp)
        if len(year_temp) > 0:
            report_type_temp = re.findall(r'(?:[半]? *年 *度 *报 *告|第 *(?:1|3) *季 *度 *报 *告)', str_temp)
            year = year_temp[0].replace("年年度报告", '')
            year = year.replace("年度报告", '')
            year = year.replace("半年度报告", '')
            year = year.replace("第1季度报告", '')
            year = year.replace("第3季度报告", '')
            year = year[-4:]
            fiscal_period_map = {"年度报告": str(year) + "-12-31", "半年度报告": str(year) + "-06-31",
                                 "第1季度报告": str(year) + "-03-31", \
                                 "第3季度报告": str(year) + "-09-31"}
            report_type_temp2 = report_type_temp[0]
            fiscal_period = fiscal_period_map[report_type_temp2]
            break
    #公司名称
    company = None
    for i in range(10):
        company_temp = re.findall(r'[\u4e00-\u9fa5]{2,}?股份有限公司|[\u4e00-\u9fa5]{2,}?（集团）股份有限公司', str(pf[i].get_text()))
        # company_temp = re.findall(r'[\u4e00-\u9fa5]{1,}[^ ]*[\u4e00-\u9fa5]{1,}有限公司', str(pf[i].get_text()))
        if len(company_temp) > 0:
            company = company_temp[0];
            break
    #股票简称
    short_name = None
    for i in range(10):
        pfTemp_text = str(pf[i].get_text())
        front = re.findall(r'股\s*票?\s*简\s*称|股\s*票?\s*名\s*称',pfTemp_text)
        if len(front) > 0:
            str_cursor = pfTemp_text.find(front[0])
            searchText_temp = pfTemp_text[str_cursor+4:str_cursor+80]
            if len(searchText_temp) < 76:
                searchText_temp = searchText_temp+str(pf[i+1].get_text())
            searchText_temp = searchText_temp.replace('：', ' ')
            searchText_temp = searchText_temp.replace(':', ' ')
            searchText_temp = searchText_temp.replace(':', ' ')
            searchText_temp = searchText_temp.replace('、', ' ')
            searchText_temp = searchText_temp.replace('股票代码', ' ')
            each_text = re.findall(r'[^\s]+',searchText_temp)
            for j in range(len(each_text) - 2):
                if each_text[j] == "股" or each_text[j+1][0] == '*':
                    continue
                if len(re.findall(r'.*ST',each_text[j])) > 0 and len(each_text[j]) > 3:
                    short_name = each_text[j]
                    break
                if len(re.findall(r'.*S',each_text[j])) > 0:
                    if fuzzyfinder(each_text[j+1], company):
                        short_name = each_text[j]+each_text[j+1]
                    else:
                        short_name = each_text[j]
                    break
                if fuzzyfinder(each_text[j+1], 'AB') and each_text[j+2] != '股' and fuzzyfinder(each_text[j][-2:], company):
                    short_name = each_text[j]+each_text[j+1]
                    break
                if fuzzyfinder(each_text[j], company):
                    short_name = each_text[j]
                    if fuzzyfinder(each_text[j+1], company):
                        short_name = short_name+each_text[j+1]
                    break
            if len(each_text) < 3:
                for n in range(len(each_text)):
                    if fuzzyfinder(each_text[n], company):
                        short_name = each_text[n]
                        break
            if short_name == None:
                for k in range(len(each_text) - 2):
                    half =int((len(each_text[k])+1)/2)
                    text_two = each_text[k][:half]
                    if fuzzyfinder(text_two, company):
                        short_name = each_text[k]
                        break
            if short_name == None:
                for m in range(len(each_text) - 2):
                    half =int((len(each_text[m])+1)/2)
                    text_two = each_text[m][-half:]
                    if fuzzyfinder(text_two, company) and each_text[m] != 'A股':
                        short_name = each_text[m]
                        break
            break

    #股票代码
    searchText_temp = None
    share_code = None
    ishave_bool = 0
    for i in range(10):
        pfTemp_text = str(pf[i].get_text())
        pfTemp_text0 = pfTemp_text.replace(' ', '')
        str_cursor = pfTemp_text0.find("代码")
        if str_cursor > 0:
            local_str = pfTemp_text[:str_cursor]
            empty = local_str.count(" ")
            searchText_temp = pfTemp_text[str_cursor + empty:] + str(pf[i + 1].get_text());
            ishave_bool = 1;
            break
    if ishave_bool == 1:
        share_code_temp = re.findall(r"\b\d{6}\b", searchText_temp)
        if len(share_code_temp) > 0:
            share_code = share_code_temp[0]

    #销售费用表格提取
    current_div = None  # 从此处开始查找目标表格
    index_div = soup.find('div', id='outline')  # 目录。如果没有这部分，则直接在页面中查找
    if index_div:
        selling_expenses_page = None
        selling_expenses_a = index_div.find('a', text=re.compile(r'.*销售费用\b'))
        if selling_expenses_a:
            selling_expenses_page = selling_expenses_a['href'].replace('#', '')
            if selling_expenses_page:
                selling_expenses_page_pc = (soup.find('div', id=str(selling_expenses_page))).find('div')
                selling_expenses_page_content = selling_expenses_page_pc.find_all('div')

                for div_temp in selling_expenses_page_content:
                    div_temp_cursor_str = re.findall(r'\b销售费用\b', div_temp.get_text())
                    countlen = len(div_temp_cursor_str)
                    if countlen > 0:
                        div_temp_cursor = (div_temp.get_text()).find(div_temp_cursor_str[0])
                        div_temp_str = (div_temp.get_text())[:div_temp_cursor]
                        div_temp_str2 = (div_temp.get_text())[div_temp_cursor:]

                        #存在上一个标签是页数的情况，待解决
                        previous_div_str = ''
                        if find_previous_div(div_temp) is not None:
                            previous_div_str = find_previous_div(div_temp).get_text()
                            previous_div_0 = re.findall('\s*0\s*', previous_div_str)
                            if len(previous_div_0) == 1:
                                if previous_div_str == previous_div_0[0]:
                                    previous_div_str = ''
                        if (len(re.findall(r'\d|[一二三四五六七八九]', div_temp_str)) > 0 and (len(re.findall(r'\d|[一二三四五六七八九]' \
                                , div_temp_str)) < 3)and (len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str)) < 4) and (len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) < 10)) or ((len(re.findall(r'\d|[一二三四五六七八九]', div_temp_str)) == 0) and \
                                                                                                                                                         (len(re.findall(r'\d|[一二三四五六七八九]',
                                                                                     previous_div_str)) > 0 ) and (len(
                            re.findall(r'\d|[一二三四五六七八九]', previous_div_str)) < 3 )and (len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str)) < 4)and (len(re.findall(r'[\u4e00-\u9fa5]', previous_div_str)) < 4) and (len(re.findall(r'[\u4e00-\u9fa5]', div_temp_str2)) < 10)):
                            if len(re.findall(r'\d', div_temp_str)) == 1:
                                if ((re.findall(r'\d', div_temp_str))[0] != '1') and (
                                    (re.findall(r'\d', div_temp_str))[0] != '2') and ((re.findall(r'\d', div_temp_str))[0] != '3'):
                                    current_div = div_temp
                                    break
                            else:
                                if (len(re.findall(r'\d', div_temp_str)) == 0) and (
                                    len(re.findall(r'\d', previous_div_str)) == 1):
                                    if ((re.findall(r'\d', previous_div_str))[0] != '1') and (
                                        (re.findall(r'\d', previous_div_str))[0] != '2') and ((re.findall(r'\d', previous_div_str))[0] != '3'):
                                        current_div = div_temp
                                        break
                                else:
                                    current_div = div_temp
                                    break
                    # while countlen > 0:
                    #     countlen = countlen - 1
                    #     div_temp_cursor = (div_temp.get_text()).find(div_temp_cursor_str[countlen])
                    #     div_temp_str = (div_temp.get_text())[:div_temp_cursor]
                    #     if len(re.findall(r'\d|[一二三四五六七八九]', div_temp_str)) > 0:
                    #         current_div = div_temp;
                    #         break
                # selling_expenses_page_content = soup.find('div', id=str(selling_expenses_page)).find_all('div',
                #                                                                                          class_='t')
                # for temp_div in selling_expenses_page_content:
                #     if len(re.findall(r'\b销售费用\b', temp_div.get_text())) > 0:
                #         current_div = temp_div
                #         break
        else:  # 进入目录但没找到“销售费用”标签
            current_div = else_inEX()

    else:  # 没有目录的处理
        current_div = else_inEX()

    first_td_div = None  # 表格第一项的位置
    max_search_range = 20  # 最大查找范围，如果超过这个数仍然找不到表格，则可以认为待查表格不在附近

    div_bool = 0   #判断表格标题是否为‘c’标签
    if current_div != None:
        if (current_div['class'])[0] == 'c':
            div_bool = 1
    title_div = current_div
    # print(title_div)

    while current_div and max_search_range != 0:
        # print(current_div.get_text() + "//")
        current_div_class = current_div['class']
        if (current_div != title_div and (len(re.findall(r'\d\d.{1,4}[\u4e00-\u9fa5]{4,}', current_div.get_text())) == 1) and (len(re.findall(r'[年发生额度]',current_div.get_text())) == 0)) or len(re.findall(r'\b管理费用\b',current_div.get_text())) > 0 :
            break
        if (current_div_class[0] == 'c' and div_bool == 0 and len(re.findall(r'(全\s*文)|(报\s*告)|(有\s*限\s*公\s*司)',current_div.get_text())) == 0) or \
                (len(re.findall(r'(项\s*目)|(费\s*用\s*性\s*质)|(\d\s*年\s*度)|(本\s*期\s*发\s*生\s*额)|(期\s*末\s*余\s*额)|(本\s*年\s*发\s*生\s*额)|(\d\s*\d\s*\d\s*\d\s*年)',current_div.get_text())) > 0 and len(re.findall(r'(全\s*文)|(报\s*告)',current_div.get_text())) == 0) or len(re.findall(r'单/s*位.*',current_div.get_text())) == 1:
            first_td_div = current_div
            break
        current_div = find_next_div(current_div)
        max_search_range -= 1
        div_bool = 0

    table2str = None
    # print(first_td_div)
    if not first_td_div:
        print('查找不到表格！')
        '''

        待补充代码：


        '''
        else_inEX_else_str = else_inEX_else()
        if else_inEX_else_str != '':
            table2str_temp1P = re.compile(r'<[^>]*span[^>]*>', re.S)
            table2str_temp1 = table2str_temp1P.sub('', else_inEX_else_str)
            table2str_tempP = re.compile(r'<[^>]+>', re.S)
            table2str = table2str_tempP.sub(' ', table2str_temp1)
    else:
        print('查找到表格！')
        '''

        待补充代码：
        未查找计价货币

        '''
        if build_original_table(first_td_div)=='':
            else_inEX_else_str = else_inEX_else()
            if else_inEX_else_str != '':
                table2str_temp1P = re.compile(r'<[^>]*span[^>]*>', re.S)
                table2str_temp1 = table2str_temp1P.sub('', else_inEX_else_str)
                table2str_tempP = re.compile(r'<[^>]+>', re.S)
                table2str = table2str_tempP.sub(' ', table2str_temp1)
        else:
        #大标签替换成空格，小标签去掉
            table2str_temp1P = re.compile(r'<[^>]*span[^>]*>', re.S)
            table2str_temp1 = table2str_temp1P.sub('', build_original_table(first_td_div))
            table2str_tempP = re.compile(r'<[^>]+>', re.S)
            table2str = table2str_tempP.sub(' ', table2str_temp1)
        # table2str_temp = re.compile(r'<[^>]+>', re.S)
        # table2str = table2str_temp.sub('', build_original_table(first_td_div))
        #大标签替换成空格，小标签去掉
        # table2str_temp1P = re.compile(r'<[^>]*span[^>]*>', re.S)
        # table2str_temp1 = table2str_temp1P.sub('', build_original_table(first_td_div))
        # table2str_tempP = re.compile(r'<[^>]+>', re.S)
        # table2str = table2str_tempP.sub(' ', table2str_temp1)

    #基本信息总结输出
    # print("公司简称：" + str(short_name) + "\n")
    # print("会计期间：" + str(fiscal_period) + "\n")
    # print("股票代码：" + str(share_code) + "\n")
    # print("销售费用表格:" + str(table2str) + "\n")
    # print("------------------------------------------")
    return str(short_name),str(fiscal_period),str(share_code),str(table2str),str(company)

# path = "html/2013/YEAR/"
# inFile = input("读取文件：")
# information_extract(path+inFile)


path = ["2010/YEAR/"]
fiscal_period_dict = {"2012/YEAR/":"2012-12-31","2013/YEAR/":"2013-12-31","2011/YEAR/":"2011-12-31", \
                      "2010/YEAR/":"2010-12-31"}

for i in range(len(path)):
    files = os.listdir(path[i])
    if os.path.exists(path[i] + 'saleEx.txt'):
        os.remove(path[i] + 'saleEx.txt')
    fileflow = open(path[i] + 'saleEx.txt','a+',encoding='utf-8')
    for filename in files:
        pos = filename.find(".")
        if filename[pos + 1:] == "html":
            print(path[i] + filename + "正在提取...")
            short_name,fiscal_period,share_code,table2str,company = information_extract(path[i] + filename)
            # if share_code == 'None' or share_code != filename[0:pos]:
            share_code = filename[0:pos]
            fiscal_period = fiscal_period_dict[path[i]]
            fileflow.write(share_code+"\n"+short_name+"\n"+fiscal_period+"\n"+company+"\n"+table2str+"\n")
            fileflow.write("---------------------------------\n")
            print(path[i] + filename + "已提取完成！")
    print(path[i]+"已提取完成！")
    fileflow.close()


