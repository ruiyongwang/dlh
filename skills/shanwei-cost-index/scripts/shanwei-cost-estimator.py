#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汕尾市政府投资项目估算造价计算器
基于《汕尾市政府投资项目估算造价指标》(2021-12)

使用方法:
    python shanwei-cost-estimator.py
    
交互式填写项目参数，自动计算投资估算
"""

import json
import os
from pathlib import Path
from datetime import datetime

# 加载造价指标数据库
SCRIPT_DIR = Path(__file__).parent
DATABASE_PATH = SCRIPT_DIR.parent / "references" / "shanwei-cost-database.json"

def load_database():
    """加载造价指标数据库"""
    with open(DATABASE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

class ShanweiCostEstimator:
    """汕尾市造价估算器"""
    
    def __init__(self):
        self.db = load_database()
        self.project_info = {}
        self.cost_breakdown = {}
        
    def select_building_type(self):
        """选择建筑类型"""
        print("\n" + "="*60)
        print("【房屋建筑类造价估算】")
        print("="*60)
        print("\n请选择建筑类型:")
        
        building_types = {
            "1": ("school", "学校工程（幼儿园、小学、中学、大学）"),
            "2": ("hospital", "医院工程（综合医院、专科医院）"),
            "3": ("comprehensive_building", "综合楼（办公、商业等）"),
            "4": ("public_rental", "公租房"),
            "5": ("garage", "车库（地下车库、立体车库）"),
            "6": ("office_renovation", "办公室装修"),
            "7": ("outdoor_works", "室外及其他配套工程"),
        }
        
        for key, (_, desc) in building_types.items():
            print(f"  {key}. {desc}")
        
        choice = input("\n请输入选项(1-7): ").strip()
        return building_types.get(choice, (None, None))[0]
    
    def select_municipal_type(self):
        """选择市政工程类型"""
        print("\n" + "="*60)
        print("【市政工程类造价估算】")
        print("="*60)
        print("\n请选择市政工程类型:")
        
        municipal_types = {
            "1": "municipal_road",      # 市政道路
            "2": "bridge",              # 桥梁工程
            "3": "water_conservancy",   # 水利工程
        }
        
        print("  1. 市政道路工程（新建道路、道路改造、软基处理）")
        print("  2. 桥梁工程（跨线桥、跨河桥、景观桥、人行天桥）")
        print("  3. 水利工程（堤防、清淤、泵站、水闸）")
        
        choice = input("\n请输入选项(1-3): ").strip()
        return municipal_types.get(choice)
    
    def select_school_item(self):
        """选择学校工程细项"""
        print("\n【学校工程】")
        items = self.db["building"]["school"]["items"]
        
        for i, item in enumerate(items, 1):
            unit_cost = item.get('unit_cost', '-')
            student_cost = item.get('student_cost_wan', '-')
            print(f"  {i}. {item['name']}")
            print(f"     单方造价: {unit_cost}元/㎡ | 生均造价: {student_cost}万元")
        
        choice = int(input("\n请选择序号: ").strip())
        return items[choice - 1] if 1 <= choice <= len(items) else None
    
    def select_hospital_item(self):
        """选择医院工程细项"""
        print("\n【医院工程】")
        items = self.db["building"]["hospital"]["items"]
        
        for i, item in enumerate(items, 1):
            unit_cost = item.get('unit_cost', '-')
            bed_cost = item.get('bed_cost_wan', '-')
            print(f"  {i}. {item['name']}")
            print(f"     单方造价: {unit_cost}元/㎡ | 床均造价: {bed_cost}万元")
        
        choice = int(input("\n请选择序号: ").strip())
        return items[choice - 1] if 1 <= choice <= len(items) else None
    
    def select_comprehensive_building_item(self):
        """选择综合楼细项"""
        print("\n【综合楼】")
        items = self.db["building"]["comprehensive_building"]["items"]
        
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item['name']} - 单方造价: {item['unit_cost']}元/㎡")
        
        choice = int(input("\n请选择序号: ").strip())
        return items[choice - 1] if 1 <= choice <= len(items) else None
    
    def select_garage_item(self):
        """选择车库细项"""
        print("\n【车库工程】")
        items = self.db["building"]["garage"]["items"]
        
        for i, item in enumerate(items, 1):
            unit_cost = item.get('unit_cost')
            car_cost = item.get('car_cost_wan')
            if unit_cost:
                print(f"  {i}. {item['name']} - 单方造价: {unit_cost}元/㎡")
            elif car_cost:
                print(f"  {i}. {item['name']} - 车位造价: {car_cost}万元/车位")
        
        choice = int(input("\n请选择序号: ").strip())
        return items[choice - 1] if 1 <= choice <= len(items) else None
    
    def select_road_item(self):
        """选择道路工程细项"""
        print("\n【市政道路工程】")
        print("  1. 新建道路")
        print("  2. 道路改造")
        print("  3. 软基处理")
        
        sub_choice = input("\n请选择子类(1-3): ").strip()
        
        if sub_choice == "1":
            items = self.db["municipal_road"]["new_construction"]["items"]
            print("\n【新建道路】")
            for i, item in enumerate(items, 1):
                print(f"  {i}. {item['name']}")
                print(f"     {item['wan_per_km']}万元/km | {item['yuan_per_sqm']}元/㎡ | 参考宽度{item['reference_width_m']}m")
            
            choice = int(input("\n请选择序号: ").strip())
            return items[choice - 1] if 1 <= choice <= len(items) else None
            
        elif sub_choice == "2":
            items = self.db["municipal_road"]["reconstruction"]["items"]
            print("\n【道路改造】")
            for i, item in enumerate(items, 1):
                print(f"  {i}. {item['name']}")
                print(f"     {item['wan_per_km']}万元/km | {item['yuan_per_sqm']}元/㎡")
            
            choice = int(input("\n请选择序号: ").strip())
            return items[choice - 1] if 1 <= choice <= len(items) else None
            
        elif sub_choice == "3":
            items = self.db["municipal_road"]["soft_ground"]["items"]
            print("\n【软基处理】")
            for i, item in enumerate(items, 1):
                low = item.get('yuan_per_sqm_low', '')
                high = item.get('yuan_per_sqm_high', '')
                print(f"  {i}. {item['name']} - {low}-{high}元/㎡")
            
            choice = int(input("\n请选择序号: ").strip())
            return items[choice - 1] if 1 <= choice <= len(items) else None
        
        return None
    
    def select_bridge_item(self):
        """选择桥梁工程细项"""
        print("\n【桥梁工程】")
        items = self.db["bridge"]["items"]
        
        for i, item in enumerate(items, 1):
            low = item.get('yuan_per_sqm_low', '')
            high = item.get('yuan_per_sqm_high', '')
            print(f"  {i}. {item['name']} - {low}-{high}元/㎡")
        
        choice = int(input("\n请选择序号: ").strip())
        return items[choice - 1] if 1 <= choice <= len(items) else None
    
    def select_water_conservancy_item(self):
        """选择水利工程细项"""
        print("\n【水利工程】")
        print("  1. 堤防工程")
        print("  2. 河道清淤")
        print("  3. 排涝泵站")
        print("  4. 水闸")
        
        sub_choice = input("\n请选择子类(1-4): ").strip()
        
        types_map = {
            "1": "embankment",
            "2": "river_dredging",
            "3": "drainage_station",
            "4": "sluice"
        }
        
        type_key = types_map.get(sub_choice)
        if not type_key:
            return None
        
        items = self.db["water_conservancy"][type_key]
        
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item['name']} - {item['value']}{item['unit']}")
        
        choice = int(input("\n请选择序号: ").strip())
        return items[choice - 1] if 1 <= choice <= len(items) else None
    
    def calculate_building_cost(self, item, category):
        """计算房屋建筑造价"""
        print("\n" + "="*60)
        print("【项目参数输入】")
        print("="*60)
        
        # 建筑面积
        area = float(input("请输入建筑面积(㎡): ").strip())
        
        # 是否装配式建筑
        prefab_rate = None
        prefab_choice = input("是否装配式建筑? (y/n): ").strip().lower()
        if prefab_choice == 'y':
            print("\n装配率选择:")
            print("  1. 30%-50%")
            print("  2. 50%-70%")
            print("  3. >70%")
            prefab_choice = input("请选择(1-3): ").strip()
            
            prefab_rates = {
                "1": (30, 50, 150, 250),
                "2": (50, 70, 250, 400),
                "3": (70, 100, 400, 600)
            }
            if prefab_choice in prefab_rates:
                prefab_rate = prefab_rates[prefab_choice]
        
        # 地下室层数（针对车库）
        basement_levels = 1
        if category == "garage" and "地下车库" in item.get('name', ''):
            basement_levels = int(input("地下室层数(默认1): ").strip() or "1")
        
        # 计算基础造价
        unit_cost = item.get('unit_cost', 0)
        
        if not unit_cost:
            # 立体车库按车位计算
            car_count = int(input("请输入车位数量: ").strip())
            car_cost_wan = item.get('car_cost_wan', 0)
            base_cost_wan = car_count * car_cost_wan
            unit_cost = None
        else:
            base_cost_wan = area * unit_cost / 10000
        
        # 装配式增加费
        prefab_cost_wan = 0
        if prefab_rate:
            extra_low, extra_high = prefab_rate[2], prefab_rate[3]
            extra_avg = (extra_low + extra_high) / 2
            prefab_cost_wan = area * extra_avg / 10000
            print(f"\n装配式增加费: {prefab_cost_wan:.2f}万元")
        
        # 地下室层数调整（车库）
        basement_adjust = 0
        if basement_levels > 1:
            basement_adjust = base_cost_wan * (1.1 ** (basement_levels - 1) - 1)
            print(f"地下室加深调整: {basement_adjust:.2f}万元")
        
        # 合计
        total_cost_wan = base_cost_wan + prefab_cost_wan + basement_adjust
        
        self.cost_breakdown = {
            "建筑类型": item['name'],
            "建筑面积": f"{area}㎡",
            "单方造价": f"{unit_cost}元/㎡" if unit_cost else f"{item.get('car_cost_wan')}万元/车位",
            "基础造价": f"{base_cost_wan:.2f}万元",
            "装配式增加费": f"{prefab_cost_wan:.2f}万元" if prefab_cost_wan > 0 else "不适用",
            "地下室调整": f"{basement_adjust:.2f}万元" if basement_adjust > 0 else "不适用",
            "投资估算": f"{total_cost_wan:.2f}万元"
        }
        
        return total_cost_wan
    
    def calculate_road_cost(self, item):
        """计算道路工程造价"""
        print("\n" + "="*60)
        print("【项目参数输入】")
        print("="*60)
        
        # 计算方式选择
        print("\n计算方式:")
        print("  1. 按长度计算(公里)")
        print("  2. 按面积计算(平方米)")
        calc_choice = input("请选择(1-2): ").strip()
        
        if calc_choice == "1":
            length_km = float(input("请输入道路长度(公里): ").strip())
            cost_per_km = item.get('wan_per_km', 0)
            total_cost_wan = length_km * cost_per_km
            width = item.get('reference_width_m', 0)
            area = length_km * 1000 * width
        else:
            area = float(input("请输入道路面积(㎡): ").strip())
            cost_per_sqm = item.get('yuan_per_sqm', 0)
            if not cost_per_sqm:
                low = item.get('yuan_per_sqm_low', 0)
                high = item.get('yuan_per_sqm_high', 0)
                cost_per_sqm = (low + high) / 2
            total_cost_wan = area * cost_per_sqm / 10000
            length_km = None
        
        self.cost_breakdown = {
            "工程类型": item['name'],
            "道路长度": f"{length_km}公里" if length_km else "按面积计算",
            "道路面积": f"{area}㎡",
            "单位造价": f"{item.get('wan_per_km')}万元/公里" if item.get('wan_per_km') else f"{cost_per_sqm}元/㎡",
            "投资估算": f"{total_cost_wan:.2f}万元"
        }
        
        return total_cost_wan
    
    def calculate_bridge_cost(self, item):
        """计算桥梁工程造价"""
        print("\n" + "="*60)
        print("【项目参数输入】")
        print("="*60)
        
        area = float(input("请输入桥梁面积(㎡): ").strip())
        
        low = item.get('yuan_per_sqm_low', 0)
        high = item.get('yuan_per_sqm_high', 0)
        avg_cost = (low + high) / 2
        
        total_cost_wan = area * avg_cost / 10000
        
        self.cost_breakdown = {
            "工程类型": item['name'],
            "桥梁面积": f"{area}㎡",
            "单方造价区间": f"{low}-{high}元/㎡",
            "平均单方造价": f"{avg_cost:.0f}元/㎡",
            "投资估算": f"{total_cost_wan:.2f}万元"
        }
        
        return total_cost_wan
    
    def calculate_water_conservancy_cost(self, item):
        """计算水利工程造价"""
        print("\n" + "="*60)
        print("【项目参数输入】")
        print("="*60)
        
        unit = item.get('unit', '')
        value = item.get('value', 0)
        
        if '延米' in unit:
            length = float(input("请输入堤防长度(米): ").strip())
            total_cost_wan = length * value / 10000
            quantity_desc = f"{length}米"
        elif 'm³' in unit:
            volume = float(input("请输入清淤方量(m³): ").strip())
            total_cost_wan = volume * value / 10000
            quantity_desc = f"{volume}m³"
        elif 'KW' in unit:
            power = float(input("请输入装机容量(KW): ").strip())
            total_cost_wan = power * value
            quantity_desc = f"{power}KW"
        elif '净宽' in unit:
            width = float(input("请输入水闸净宽(米): ").strip())
            total_cost_wan = width * value
            quantity_desc = f"{width}米"
        else:
            quantity = float(input(f"请输入工程量({unit}): ").strip())
            total_cost_wan = quantity * value
            quantity_desc = f"{quantity}{unit}"
        
        self.cost_breakdown = {
            "工程类型": item['name'],
            "工程量": quantity_desc,
            "单位造价": f"{value}{unit}",
            "投资估算": f"{total_cost_wan:.2f}万元"
        }
        
        return total_cost_wan
    
    def generate_report(self):
        """生成估算报告"""
        print("\n" + "="*60)
        print("【汕尾市政府投资项目估算造价报告】")
        print("="*60)
        
        for key, value in self.cost_breakdown.items():
            print(f"  {key}: {value}")
        
        print("\n" + "="*60)
        print("说明:")
        print("  1. 本估算基于《汕尾市政府投资项目估算造价指标》(2021-12)")
        print("  2. 指标包含建安工程费、工程建设其他费用、预备费")
        print("  3. 不含建设用地费、建设期利息、流动资金")
        print("  4. 实际造价需根据具体设计方案调整")
        print("="*60)
        
        # 保存报告
        save_choice = input("\n是否保存报告到文件? (y/n): ").strip().lower()
        if save_choice == 'y':
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shanwei_cost_estimate_{timestamp}.txt"
            filepath = SCRIPT_DIR / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("汕尾市政府投资项目估算造价报告\n")
                f.write("="*60 + "\n\n")
                for key, value in self.cost_breakdown.items():
                    f.write(f"{key}: {value}\n")
                f.write("\n" + "="*60 + "\n")
                f.write("说明:\n")
                f.write("  1. 本估算基于《汕尾市政府投资项目估算造价指标》(2021-12)\n")
                f.write("  2. 指标包含建安工程费、工程建设其他费用、预备费\n")
                f.write("  3. 不含建设用地费、建设期利息、流动资金\n")
                f.write("  4. 实际造价需根据具体设计方案调整\n")
                f.write("="*60 + "\n")
                f.write(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            print(f"\n[OK] 报告已保存: {filepath}")
    
    def run(self):
        """运行估算器"""
        print("\n" + "="*60)
        print("  汕尾市政府投资项目估算造价计算器")
        print("  基于《汕尾市政府投资项目估算造价指标》(2021-12)")
        print("="*60)
        
        print("\n请选择工程类型:")
        print("  1. 房屋建筑类")
        print("  2. 市政工程类")
        
        main_choice = input("\n请输入选项(1-2): ").strip()
        
        if main_choice == "1":
            # 房屋建筑
            category = self.select_building_type()
            if not category:
                print("[错误] 无效的选择")
                return
            
            item = None
            if category == "school":
                item = self.select_school_item()
            elif category == "hospital":
                item = self.select_hospital_item()
            elif category == "comprehensive_building":
                item = self.select_comprehensive_building_item()
            elif category == "public_rental":
                item = self.db["building"]["public_rental"]["items"][0]
                print(f"\n已选择: {item['name']} - {item['unit_cost']}元/㎡")
            elif category == "garage":
                item = self.select_garage_item()
            elif category == "office_renovation":
                items = self.db["building"]["office_renovation"]["items"]
                print("\n【办公室装修】")
                for i, it in enumerate(items, 1):
                    print(f"  {i}. {it['name']} - {it['unit_cost']}元/㎡")
                choice = int(input("\n请选择序号: ").strip())
                item = items[choice - 1] if 1 <= choice <= len(items) else None
            elif category == "outdoor_works":
                items = self.db["building"]["outdoor_works"]["items"]
                print("\n【室外及其他配套工程】")
                for i, it in enumerate(items, 1):
                    print(f"  {i}. {it['name']} - {it['unit_cost']}元/㎡")
                choice = int(input("\n请选择序号: ").strip())
                item = items[choice - 1] if 1 <= choice <= len(items) else None
            
            if item:
                self.calculate_building_cost(item, category)
                
        elif main_choice == "2":
            # 市政工程
            category = self.select_municipal_type()
            if not category:
                print("[错误] 无效的选择")
                return
            
            item = None
            if category == "municipal_road":
                item = self.select_road_item()
                if item:
                    self.calculate_road_cost(item)
            elif category == "bridge":
                item = self.select_bridge_item()
                if item:
                    self.calculate_bridge_cost(item)
            elif category == "water_conservancy":
                item = self.select_water_conservancy_item()
                if item:
                    self.calculate_water_conservancy_cost(item)
            
            if not item:
                print("[错误] 无效的选择")
                return
        else:
            print("[错误] 无效的选择")
            return
        
        # 生成报告
        self.generate_report()


def main():
    """主函数"""
    try:
        estimator = ShanweiCostEstimator()
        estimator.run()
    except KeyboardInterrupt:
        print("\n\n[INFO] 用户取消操作")
    except Exception as e:
        print(f"\n[错误] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
