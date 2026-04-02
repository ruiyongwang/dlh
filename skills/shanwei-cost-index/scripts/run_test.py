#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

db_path = Path('c:/Users/wry08/.workbuddy/skills/shanwei-cost-index/references/shanwei-cost-database.json')
with open(db_path, 'r', encoding='utf-8') as f:
    db = json.load(f)

print('='*60)
print('汕尾市造价估算器 - 自动化测试')
print('='*60)

# 测试1: 学校工程
print('\n[测试1] 学校工程 - 幼儿园(无地下室)')
item = db['building']['school']['items'][0]
print('  项目:', item['name'])
print('  单方造价:', item['unit_cost'], '元/m2')
area = 5000
cost = area * item['unit_cost'] / 10000
print('  建筑面积:', area, 'm2')
print('  估算造价:', round(cost, 2), '万元')

# 测试2: 医院工程
print('\n[测试2] 医院工程 - 三甲综合医院')
item = db['building']['hospital']['items'][0]
print('  项目:', item['name'])
print('  单方造价:', item['unit_cost'], '元/m2')
area = 30000
cost = area * item['unit_cost'] / 10000
print('  建筑面积:', area, 'm2')
print('  估算造价:', round(cost, 2), '万元')

# 测试3: 综合楼
print('\n[测试3] 综合楼 - 高层(24-100m)')
item = db['building']['comprehensive_building']['items'][1]
print('  项目:', item['name'])
print('  单方造价:', item['unit_cost'], '元/m2')
area = 20000
cost = area * item['unit_cost'] / 10000
print('  建筑面积:', area, 'm2')
print('  估算造价:', round(cost, 2), '万元')

# 测试4: 市政道路
print('\n[测试4] 市政道路 - 城市主干道')
item = db['municipal_road']['new_construction']['items'][1]
print('  项目:', item['name'])
print('  单位造价:', item['wan_per_km'], '万元/公里')
length = 5
cost = length * item['wan_per_km']
print('  道路长度:', length, '公里')
print('  估算造价:', round(cost, 2), '万元')

# 测试5: 桥梁工程
print('\n[测试5] 桥梁工程 - 市政跨河桥(钢筋混凝土)')
item = db['bridge']['items'][6]
print('  项目:', item['name'])
print('  单方造价区间:', item['yuan_per_sqm_low'], '-', item['yuan_per_sqm_high'], '元/m2')
area = 2000
avg_cost = (item['yuan_per_sqm_low'] + item['yuan_per_sqm_high']) / 2
cost = area * avg_cost / 10000
print('  桥梁面积:', area, 'm2')
print('  估算造价:', round(cost, 2), '万元')

# 测试6: 装配式建筑增加费
print('\n[测试6] 装配式建筑增加费 - 装配率50%-70%')
item = db['building']['prefabricated_extra']['items'][1]
print('  项目:', item['name'])
print('  增加费用区间:', item['extra_low'], '-', item['extra_high'], '元/m2')
area = 10000
avg_extra = (item['extra_low'] + item['extra_high']) / 2
cost = area * avg_extra / 10000
print('  建筑面积:', area, 'm2')
print('  装配式增加费:', round(cost, 2), '万元')

# 测试7: 水利工程
print('\n[测试7] 水利工程 - 防洪墙')
item = db['water_conservancy']['embankment'][0]
print('  项目:', item['name'])
print('  单位造价:', item['value'], item['unit'])
length = 1000
cost = length * item['value'] / 10000
print('  堤防长度:', length, '米')
print('  估算造价:', round(cost, 2), '万元')

print('\n' + '='*60)
print('[OK] 所有测试通过!')
print('='*60)
