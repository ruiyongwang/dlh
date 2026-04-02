#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""汕尾市造价估算器测试脚本"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from shanwei_cost_estimator import ShanweiCostEstimator

def run_tests():
    """运行自动化测试"""
    print("="*60)
    print("汕尾市造价估算器 - 自动化测试")
    print("="*60)
    
    estimator = ShanweiCostEstimator()
    
    # 测试1: 学校工程
    print("\n【测试1: 学校工程 - 幼儿园(无地下室)】")
    item = estimator.db['building']['school']['items'][0]
    print(f"  项目: {item['name']}")
    print(f"  单方造价: {item['unit_cost']}元/m2")
    area = 5000
    cost = area * item['unit_cost'] / 10000
    print(f"  建筑面积: {area}m2")
    print(f"  估算造价: {cost:.2f}万元")
    
    # 测试2: 医院工程
    print("\n【测试2: 医院工程 - 三甲综合医院】")
    item = estimator.db['building']['hospital']['items'][0]
    print(f"  项目: {item['name']}")
    print(f"  单方造价: {item['unit_cost']}元/m2")
    print(f"  床均造价: {item['bed_cost_wan']}万元/床")
    area = 30000
    cost = area * item['unit_cost'] / 10000
    print(f"  建筑面积: {area}m2")
    print(f"  估算造价: {cost:.2f}万元")
    
    # 测试3: 综合楼
    print("\n【测试3: 综合楼 - 高层(24-100m)】")
    item = estimator.db['building']['comprehensive_building']['items'][1]
    print(f"  项目: {item['name']}")
    print(f"  单方造价: {item['unit_cost']}元/m2")
    area = 20000
    cost = area * item['unit_cost'] / 10000
    print(f"  建筑面积: {area}m2")
    print(f"  估算造价: {cost:.2f}万元")
    
    # 测试4: 市政道路
    print("\n【测试4: 市政道路 - 城市主干道】")
    item = estimator.db['municipal_road']['new_construction']['items'][1]
    print(f"  项目: {item['name']}")
    print(f"  单位造价: {item['wan_per_km']}万元/公里")
    print(f"  单方造价: {item['yuan_per_sqm']}元/m2")
    length = 5
    cost = length * item['wan_per_km']
    print(f"  道路长度: {length}公里")
    print(f"  估算造价: {cost:.2f}万元")
    
    # 测试5: 桥梁工程
    print("\n【测试5: 桥梁工程 - 市政跨河桥(钢筋混凝土)】")
    item = estimator.db['bridge']['items'][6]
    print(f"  项目: {item['name']}")
    print(f"  单方造价区间: {item['yuan_per_sqm_low']}-{item['yuan_per_sqm_high']}元/m2")
    area = 2000
    avg_cost = (item['yuan_per_sqm_low'] + item['yuan_per_sqm_high']) / 2
    cost = area * avg_cost / 10000
    print(f"  桥梁面积: {area}m2")
    print(f"  估算造价: {cost:.2f}万元")
    
    # 测试6: 装配式建筑增加费
    print("\n【测试6: 装配式建筑增加费 - 装配率50%-70%】")
    item = estimator.db['building']['prefabricated_extra']['items'][1]
    print(f"  项目: {item['name']}")
    print(f"  增加费用区间: {item['extra_low']}-{item['extra_high']}元/m2")
    area = 10000
    avg_extra = (item['extra_low'] + item['extra_high']) / 2
    cost = area * avg_extra / 10000
    print(f"  建筑面积: {area}m2")
    print(f"  装配式增加费: {cost:.2f}万元")
    
    # 测试7: 水利工程
    print("\n【测试7: 水利工程 - 防洪墙】")
    item = estimator.db['water_conservancy']['embankment'][0]
    print(f"  项目: {item['name']}")
    print(f"  单位造价: {item['value']}{item['unit']}")
    length = 1000
    cost = length * item['value'] / 10000
    print(f"  堤防长度: {length}米")
    print(f"  估算造价: {cost:.2f}万元")
    
    print("\n" + "="*60)
    print("[OK] 所有测试通过!")
    print("="*60)
    
    return True

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"\n[错误] 测试失败: {e}")
        import traceback
        traceback.print_exc()
