#!/usr/bin/env node
/**
 * 度量衡工程咨询 - 造价分析脚本
 * 工程变更索赔分析与合理性评估
 */

// 造价分析主函数
function analyzeCostChange(changeData) {
    const {
        projectType,      // 项目类型
        contractAmount,   // 合同金额
        changeItems,      // 变更项目清单
        marketRates       // 市场参考价格
    } = changeData;
    
    // 分析各项变更
    const analyzedItems = changeItems.map(item => {
        const marketRate = marketRates[item.category] || 1;
        const reasonableQty = validateQuantity(item.quantity, item.category);
        const reasonableUnitPrice = validateUnitPrice(item.unitPrice, marketRate);
        
        return {
            ...item,
            reasonableQty,
            reasonableUnitPrice,
            claimedAmount: item.quantity * item.unitPrice,
            reasonableAmount: reasonableQty * reasonableUnitPrice,
            variance: (item.quantity * item.unitPrice) - (reasonableQty * reasonableUnitPrice)
        };
    });
    
    // 生成报告
    return generateCostReport(analyzedItems, contractAmount);
}

// 验证工程量合理性
function validateQuantity(qty, category) {
    // 根据工程类型和行业标准验证工程量
    const wasteRates = {
        '混凝土': 1.015,  // 1.5%损耗
        '钢筋': 1.03,     // 3%损耗
        '模板': 1.05,     // 5%损耗
        '砌筑': 1.02,     // 2%损耗
        'default': 1.03
    };
    
    const rate = wasteRates[category] || wasteRates.default;
    return Math.round(qty / rate * 100) / 100;  // 扣除合理损耗
}

// 验证单价合理性
function validateUnitPrice(price, marketRate) {
    // 单价应在市场价的±15%范围内
    const minPrice = marketRate * 0.85;
    const maxPrice = marketRate * 1.15;
    
    if (price < minPrice) return minPrice;
    if (price > maxPrice) return maxPrice;
    return price;
}

// 生成造价分析报告
function generateCostReport(items, contractAmount) {
    const totalClaimed = items.reduce((sum, item) => sum + item.claimedAmount, 0);
    const totalReasonable = items.reduce((sum, item) => sum + item.reasonableAmount, 0);
    const totalVariance = items.reduce((sum, item) => sum + item.variance, 0);
    
    let report = `# 工程变更索赔分析报告\n\n`;
    report += `生成时间：${new Date().toLocaleString()}\n`;
    report += `合同金额：${formatMoney(contractAmount)}\n\n`;
    
    // 汇总表
    report += `## 索赔汇总\n\n`;
    report += `| 项目 | 申报金额 | 审核金额 | 差异 |\n`;
    report += `|:-----|:---------|:---------|:-----|\n`;
    
    items.forEach(item => {
        report += `| ${item.name} | ${formatMoney(item.claimedAmount)} | ${formatMoney(item.reasonableAmount)} | ${formatMoney(item.variance)} |\n`;
    });
    
    report += `| **合计** | **${formatMoney(totalClaimed)}** | **${formatMoney(totalReasonable)}** | **${formatMoney(totalVariance)}** |\n\n`;
    
    // 差异分析
    report += `## 差异分析\n\n`;
    
    const highVarianceItems = items.filter(item => item.variance > totalClaimed * 0.1);
    if (highVarianceItems.length > 0) {
        report += `### 重大差异项（差异>10%）\n\n`;
        highVarianceItems.forEach(item => {
            report += `**${item.name}**\n`;
            report += `- 申报：${formatMoney(item.claimedAmount)}\n`;
            report += `- 审核：${formatMoney(item.reasonableAmount)}\n`;
            report += `- 差异原因：${analyzeVarianceReason(item)}\n\n`;
        });
    }
    
    // 结论与建议
    report += `## 结论与建议\n\n`;
    report += `### 审核结论\n`;
    report += `- 申报总额：${formatMoney(totalClaimed)}\n`;
    report += `- 合理金额：${formatMoney(totalReasonable)}（${(totalReasonable/totalClaimed*100).toFixed(1)}%）\n`;
    report += `- 审减金额：${formatMoney(totalVariance)}（${(totalVariance/totalClaimed*100).toFixed(1)}%）\n\n`;
    
    report += `### 谈判建议\n`;
    report += `1. **合理区间**：${formatMoney(totalReasonable * 0.95)} - ${formatMoney(totalReasonable * 1.05)}\n`;
    report += `2. **谈判策略**：重点核实${highVarianceItems.map(i => i.name).join('、')}\n`;
    report += `3. **让步空间**：可在管理费、利润方面适度让步\n`;
    report += `4. **底线金额**：${formatMoney(totalReasonable * 0.9)}\n\n`;
    
    return report;
}

// 分析差异原因
function analyzeVarianceReason(item) {
    const qtyDiff = item.quantity - item.reasonableQty;
    const priceDiff = item.unitPrice - item.reasonableUnitPrice;
    
    if (qtyDiff > 0 && priceDiff > 0) {
        return '工程量偏高且单价高于市场价';
    } else if (qtyDiff > 0) {
        return '工程量计算偏高（含不合理损耗）';
    } else if (priceDiff > 0) {
        return '单价高于市场参考价15%以上';
    }
    return '综合因素';
}

// 格式化金额
function formatMoney(amount) {
    return '¥' + amount.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// CLI入口
if (require.main === module) {
    // 示例数据
    const exampleData = {
        projectType: '商业综合体',
        contractAmount: 150000000,
        changeItems: [
            { name: '基础加深', category: '混凝土', quantity: 1200, unitPrice: 850 },
            { name: '钢筋增量', category: '钢筋', quantity: 180, unitPrice: 5200 },
            { name: '模板增加', category: '模板', quantity: 3200, unitPrice: 65 }
        ],
        marketRates: {
            '混凝土': 800,
            '钢筋': 4800,
            '模板': 60
        }
    };
    
    const report = analyzeCostChange(exampleData);
    console.log(report);
    
    // 保存示例报告
    const fs = require('fs');
    fs.writeFileSync('cost-analysis-example.md', report);
    console.log('\n✅ 示例报告已保存至：cost-analysis-example.md');
}

module.exports = { analyzeCostChange, generateCostReport };
