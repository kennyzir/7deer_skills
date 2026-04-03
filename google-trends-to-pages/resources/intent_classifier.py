"""
Google Trends 关键词搜索意图分类器

根据关键词特征自动判断搜索意图，用于选择合适的页面模板。
"""

import re
from typing import Literal

IntentType = Literal['Transactional', 'Informational', 'Navigational', 'Commercial']

# 意图识别规则
INTENT_PATTERNS = {
    'Transactional': [
        r'\bcodes?\b',
        r'\bfree\b',
        r'\bredeem\b',
        r'\bdownload\b',
        r'\bget\b.*\bfree\b',
        r'\bclaim\b',
        r'\bunlock\b',
    ],
    'Informational': [
        r'\bhow to\b',
        r'\bwhat is\b',
        r'\bwhy\b',
        r'\bguide\b',
        r'\btutorial\b',
        r'\bexplain\b',
        r'\blearn\b',
        r'\bstep by step\b',
    ],
    'Commercial': [
        r'\bbest\b',
        r'\btop\b',
        r'\bvs\b',
        r'\bcompare\b',
        r'\breview\b',
        r'\btier list\b',
        r'\branking\b',
    ],
    'Navigational': [
        r'\bwiki\b',
        r'\blist\b',
        r'\ball\b',
        r'\bdiscord\b',
        r'\btrello\b',
        r'\bofficial\b',
    ]
}

def classify_intent(keyword: str) -> IntentType:
    """
    分类关键词的搜索意图
    
    Args:
        keyword: 搜索关键词
        
    Returns:
        IntentType: 'Transactional', 'Informational', 'Navigational', 或 'Commercial'
    """
    keyword_lower = keyword.lower()
    
    # 计算每种意图的匹配分数
    scores = {intent: 0 for intent in INTENT_PATTERNS.keys()}
    
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, keyword_lower):
                scores[intent] += 1
    
    # 返回得分最高的意图
    max_intent = max(scores, key=scores.get)
    
    # 如果没有匹配，默认为 Informational
    if scores[max_intent] == 0:
        return 'Informational'
    
    return max_intent


def get_page_template(intent: IntentType) -> str:
    """
    根据意图返回推荐的页面模板
    
    Args:
        intent: 搜索意图类型
        
    Returns:
        str: 模板文件路径
    """
    template_map = {
        'Transactional': 'resources/templates/codes_page.tsx',
        'Informational': 'resources/templates/guide_page.tsx',
        'Navigational': 'resources/templates/hub_page.tsx',
        'Commercial': 'resources/templates/comparison_page.tsx',
    }
    return template_map[intent]


def analyze_keyword(keyword: str, search_volume: int, growth_rate: str) -> dict:
    """
    完整分析关键词并返回页面生成建议
    
    Args:
        keyword: 搜索关键词
        search_volume: 搜索量 (0-100)
        growth_rate: 增长率 (如 "+90%")
        
    Returns:
        dict: 包含意图、模板、优先级等信息
    """
    intent = classify_intent(keyword)
    template = get_page_template(intent)
    
    # 计算优先级
    growth_value = int(growth_rate.replace('%', '').replace('+', ''))
    priority_score = search_volume * (1 + growth_value / 100)
    
    if priority_score > 150:
        priority = 'P0'
    elif priority_score > 50:
        priority = 'P1'
    else:
        priority = 'P2'
    
    # 推荐字数
    word_count_map = {
        'Transactional': 800,   # 代码页简洁
        'Informational': 2000,  # 指南页详细
        'Navigational': 1200,   # 聚合页中等
        'Commercial': 1500,     # 对比页较详细
    }
    
    return {
        'keyword': keyword,
        'intent': intent,
        'template': template,
        'priority': priority,
        'priority_score': priority_score,
        'suggested_word_count': word_count_map[intent],
        'schema_type': get_schema_type(intent),
    }


def get_schema_type(intent: IntentType) -> str:
    """
    根据意图返回推荐的 Schema 类型
    """
    schema_map = {
        'Transactional': 'FAQPage',
        'Informational': 'HowTo',
        'Navigational': 'ItemList',
        'Commercial': 'ItemList',
    }
    return schema_map[intent]


# 示例用法
if __name__ == '__main__':
    test_keywords = [
        ("yba codes", 100, "+400%"),
        ("how to get fuga in jujutsu infinite", 25, "+90%"),
        ("jujutsu infinite tier list", 11, "+20%"),
        ("jujutsu infinite wiki", 6, "+10%"),
    ]
    
    print("关键词意图分析结果:\n")
    for keyword, volume, growth in test_keywords:
        result = analyze_keyword(keyword, volume, growth)
        print(f"关键词: {result['keyword']}")
        print(f"  意图: {result['intent']}")
        print(f"  优先级: {result['priority']} (分数: {result['priority_score']:.1f})")
        print(f"  推荐模板: {result['template']}")
        print(f"  推荐字数: {result['suggested_word_count']}")
        print(f"  Schema 类型: {result['schema_type']}")
        print()
