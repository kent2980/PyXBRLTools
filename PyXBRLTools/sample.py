from datetimejp import JDate
jd = JDate.strptime('2023年10月3日', '%g%e年%m月%d日')
result = jd.strftime('%Y-%m-%d')
print(result)