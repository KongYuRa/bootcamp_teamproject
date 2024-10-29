import pandas as pd

dp = pd.read_excel('/Users/ur/Desktop/sparta data/관서별 5대범죄 발생 및 검거.xlsx')
pop_kor = pd.read_csv('/Users/ur/Desktop/sparta data/pop_kor.csv')



mapping = {'서대문서': '서대문구', '수서서': '강남구', '강서서': '강서구', '서초서': '서초구','서부서': '은평구', '중부서': '중구', '종로서': '종로구', '남대문서': '중구','혜화서': '종로구', '용산서': '용산구', 
        '성북서': '성북구', '동대문서': '동대문구','마포서': '마포구', '영등포서': '영등포구', '성동서': '성동구', '동작서': '동작구','광진서': '광진구', '강북서': '강북구', '금천서': '금천구', '중랑서': '중랑구',
        '강남서': '강남구', '관악서': '관악구', '강동서': '강동구', '종암서': '성북구', '구로서': '구로구', '양천서': '양천구', '송파서': '송파구', '노원서': '노원구', '방배서': '서초구', '은평서': '은평구', '도봉서': '도봉구'}


temp = pd.Series(name='구별')
for office_name in dp['관서명']:
        if office_name in mapping:
                temp = pd.concat([temp, pd.Series([mapping[office_name]],name='구별')], ignore_index=True)
        else: 
                temp = pd.concat([temp, pd.Series([None],name='구별')], ignore_index=True)

dp = pd.concat([dp, temp], axis=1)
dp['구별'] = dp['구별'].fillna('구 없음')

print(dp)


dp.set_index('구별', inplace=True)
dp.drop(columns='관서명', inplace=True)

dp = pd.pivot_table(dp, index='구별', aggfunc='sum')

dp.drop(['구 없음'], inplace=True)

print(dp)



x = ['강간', '강도', '살인', '절도', '폭력']

for name in x:
        dp[name+' 검거율'] = dp[name+'(검거)'] / dp[name+'(발생)'] * 100
dp['검거율'] = dp['소계(검거)'] / dp['소계(발생)'] * 100

#dp['강간검거율'] = dp['강간(검거)'] / dp['강간(발생)'] * 100
#dp['강도검거율'] = dp['강도(검거)'] / dp['강도(발생)'] * 100
#dp['살인검거율'] = dp['살인(검거)'] / dp['살인(발생)'] * 100
#dp['검거율'] = dp['소계(검거)'] / dp['소계(발생)'] * 100
#dp['절도검거율'] = dp['절도(검거)'] / dp['절도(발생)'] * 100
#dp['폭력검거율'] = dp['폭력(검거)'] / dp['폭력(발생)'] * 100

print(dp)

del dp['강간(검거)']
del dp['강도(검거)']
del dp['살인(검거)']
del dp['절도(검거)']
del dp['폭력(검거)']
del dp['소계(검거)']
del dp['소계(발생)']

print(dp)

for name in x:
#       dp.rename(columns = {name+'강간(발생)':'강간', name+'강도(발생)':'강도', name+'살인(발생)':'살인', name+'소게(발생)':'절도', name+'(발생)':'폭력'}, inplace=True)
        dp.rename(columns = {name+'(발생)' : name}, inplace=True)

#dp.rename(dic, inplace=True, axis=1)

print(dp)
