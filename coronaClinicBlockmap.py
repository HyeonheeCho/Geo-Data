import pandas as pd
import os
from blockMap import draw_blockMap
from matplotlib import rcParams, style
from matplotlib import font_manager, rc
from matplotlib import pyplot as plt

printLog = True

data = pd.read_csv('./resources/clinicList.csv',
            index_col=0,
            encoding='CP949',
            engine='python')

addr = pd.DataFrame(data['address2'].apply(lambda v:v.split()[:2]).tolist(),
                    columns=('시도', '군구'))

addr['시도군구'] = addr.apply(lambda r:r['시도'] + ' ' + r['군구'], axis=1)

addr['count'] = 0

address_group = pd.DataFrame(addr.groupby(['시도', '군구', '시도군구'],
                                            as_index=False).count())
if printLog:
    print(address_group.head())

# # 시도군구로 인덱스 설정
address_group = address_group.set_index("시도군구")
if printLog:
    print(address_group.head())


# ##### 행정구역별 인구수 데이터 ######

population = pd.read_excel('./resources/행정구역_시군구_별__성별_인구수_2.xlsx')

population = population.rename(columns={'행정구역(시군구)별(1)':'시도', '행정구역(시군구)별(2)':'군구'})


for element in range(0, len(population)):
    population['군구'][element] = population['군구'][element].strip()

population['시도군구'] = population.apply(lambda r:r['시도'] + ' ' + r['군구'], axis = 1)

population = population[population.군구 != '소계']
population = population.set_index('시도군구')


# address_group & population 결합

addr_population_merge = pd.merge(address_group, population,
                                 how='inner',
                                 left_index= True,
                                 right_index= True)

if printLog:
    print(f'addr_population_merge : \n {addr_population_merge.head()}')

clinic_population = addr_population_merge[['시도_x', '군구_x',
                                          'count', '총인구수 (명)']]

# # 컬럼 변경
clinic_population = clinic_population.rename(columns= {'시도_x':'시도',
                                                       '군구_x':'군구',
                                                       '총인구수 (명)':'인구수'})
clinic_count = clinic_population['count']

clinic_population['clinic_ratie'] = clinic_count.div(clinic_population['인구수'], axis=0)*100000

if printLog:
    print(f'clinic_population : \n {clinic_population.head()}')

# 시각화
style.use('ggplot')
font_name = font_manager.FontProperties(fname="C:/Windows/Fonts/malgun.ttf").get_name()


rc('font', family = font_name)
# 공공보건의료기관 수
MC_ratio = clinic_population[['count']]
MC_ratio = MC_ratio.sort_values('count', ascending=False)
plt.rcParams['figure.figsize'] = (25, 5)
MC_ratio.plot(kind = 'bar', rot =90)

MC_ratio = clinic_population[['clinic_ratie']]
MC_ratio = MC_ratio.sort_values('clinic_ratie', ascending=False)
plt.rcParams['figure.figsize'] = (25, 5)
MC_ratio.plot(kind = 'bar', rot =90)
# ## 블록맵으로 시각화 하기 ##

path = os.getcwd()

data_draw_korea = pd.read_csv(path+'./resources/data_draw_korea.csv',
                              index_col=0,
                              encoding='UTF-8',
                              engine='python')

# # 행정구역 이름 매핑하기

data_draw_korea['시도군구'] = data_draw_korea.apply(lambda r:r['광역시도'] + ' ' + r['행정구역'], axis=1)

data_draw_korea = data_draw_korea.set_index("시도군구")

data_draw_korea_clinic_population_all = pd.merge(data_draw_korea, clinic_population,
                                                 how='outer',
                                                 left_index=True,
                                                 right_index=True)

if printLog:
    print(f'data_draw_korea_clinic_population_all : \n {data_draw_korea_clinic_population_all.head()}')



print(f'data_draw_korea : \n {data_draw_korea}' )



# # 블록맵의 블록에 데이터 매핑하고 색 표시

draw_blockMap(data_draw_korea_clinic_population_all,
              'count',
              '행정구역별 코로나 선별진료소 수',
              'Blues')

draw_blockMap(data_draw_korea_clinic_population_all,
              'clinic_ratie',
              '행정구역별 인구수 대비 코로나 선별진료소 비율',
              'Reds')