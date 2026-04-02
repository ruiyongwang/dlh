#!/usr/bin/env node
/**
 * 度量衡工程咨询 - 合同审查脚本
 * 自动化合同风险识别与报告生成
 */

const fs = require('fs');
const path = require('path');

// 高风险关键词库
const HIGH_RISK_PATTERNS = [
    { pattern: /付款.*(不明确|模糊|视情况而定)/i, risk: '付款节点不明确', level: 'high' },
    { pattern: /变更.*(未约定|无程序|口头)/i, risk: '变更程序不完善', level: 'high' },
    { pattern: /索赔.*(过期|失权|放弃)/i, risk: '索赔时限过短', level: 'high' },
    { pattern: /违约金.*(过高|超过|上限)/i, risk: '违约金过高', level: 'medium' },
    { pattern: /担保.*(无|未约定|不足)/i, risk: '担保措施不足', level: 'medium' },
    { pattern: /争议解决.*(不明确|单一)/i, risk: '争议解决机制不完善', level: 'medium' },
];

// 合同审查主函数
function reviewContract(contractText) {
    const findings = [];
    
    // 风险扫描
    HIGH_RISK_PATTERNS.forEach(({ pattern, risk, level }) => {
        if (pattern.test(contractText)) {
            findings.push({ risk, level, context: extractContext(contractText, pattern) });
        }
    });
    
    // 生成报告
    return generateReport(findings);
}

// 提取上下文
function extractContext(text, pattern) {
    const match = text.match(pattern);
    if (!match) return '';
    
    const index = match.index;
    const start = Math.max(0, index - 50);
    const end = Math.min(text.length, index + 100);
    return text.substring(start, end).replace(/\s+/g, ' ');
}

// 生成审查报告
function generateReport(findings) {
    const highRisks = findings.filter(f => f.level === 'high');
    const mediumRisks = findings.filter(f => f.level === 'medium');
    
    let report = `# 合同风险审查报告\n\n`;
    report += `生成时间：${new Date().toLocaleString()}\n\n`;
    
    // 风险摘要
    report += `## 风险摘要\n\n`;
    report += `- 高风险：${highRisks.length} 项\n`;
    report += `- 中风险：${mediumRisks.length} 项\n`;
    report += `- 总体评级：${highRisks.length > 2 ? '⚠️ 高风险' : (highRisks.length > 0 ? '⚡ 中等风险' : '✅ 低风险')}\n\n`;
    
    // 高风险详情
    if (highRisks.length > 0) {
        report += `## 高风险条款\n\n`;
        highRisks.forEach((finding, index) => {
            report += `${index + 1}. **${finding.risk}**\n`;
            report += `   - 上下文：...${finding.context}...\n\n`;
        });
    }
    
    // 中风险详情
    if (mediumRisks.length > 0) {
        report += `## 中风险条款\n\n`;
        mediumRisks.forEach((finding, index) => {
            report += `${index + 1}. **${finding.risk}**\n`;
            report += `   - 上下文：...${finding.context}...\n\n`;
        });
    }
    
    // 建议
    report += `## 修改建议\n\n`;
    if (highRisks.length > 0) {
        report += `### 必须修改\n`;
        highRisks.forEach(finding => {
            report += `- [ ] ${finding.risk}\n`;
        });
        report += `\n`;
    }
    
    report += `### 建议优化\n`;
    report += `- [ ] 完善合同定义和解释条款\n`;
    report += `- [ ] 明确各方联系人及通知方式\n`;
    report += `- [ ] 增加保密和知识产权条款\n`;
    report += `- [ ] 完善不可抗力条款\n\n`;
    
    return report;
}

// CLI入口
if (require.main === module) {
    const contractFile = process.argv[2];
    
    if (!contractFile) {
        console.log('用法：node contract-review.js <合同文件路径>');
        process.exit(1);
    }
    
    try {
        const contractText = fs.readFileSync(contractFile, 'utf-8');
        const report = reviewContract(contractText);
        
        // 输出报告
        console.log(report);
        
        // 保存报告
        const reportPath = contractFile.replace(/\.\w+$/, '') + '-审查报告.md';
        fs.writeFileSync(reportPath, report);
        console.log(`\n✅ 报告已保存至：${reportPath}`);
        
    } catch (error) {
        console.error('❌ 错误：', error.message);
        process.exit(1);
    }
}

module.exports = { reviewContract, generateReport };
