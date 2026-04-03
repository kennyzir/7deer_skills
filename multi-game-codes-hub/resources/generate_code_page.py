"""
代码页面生成器

快速为任何 Roblox 游戏生成完整的代码页面
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict

def load_template(template_path: str) -> str:
    """加载页面模板"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_code_page(
    game_name: str,
    game_slug: str,
    active_codes: List[Dict],
    expired_codes: List[Dict],
    template_path: str,
    output_path: str
):
    """
    生成代码页面
    
    Args:
        game_name: 游戏全名 (如 "Your Bizarre Adventure")
        game_slug: URL slug (如 "yba")
        active_codes: 有效代码列表
        expired_codes: 过期代码列表
        template_path: 模板文件路径
        output_path: 输出文件路径
    """
    # 加载模板
    template = load_template(template_path)
    
    # 提取奖励类型 (用于 meta description)
    rewards = set()
    for code in active_codes:
        reward = code.get('reward', '')
        if 'Spin' in reward:
            rewards.add('Spins')
        if 'Cash' in reward or 'Yen' in reward:
            rewards.add('Cash')
        if 'Arrow' in reward:
            rewards.add('Arrows')
    rewards_text = ', '.join(rewards) or 'rewards'
    
    # 生成 TypeScript 数据
    active_codes_ts = json.dumps(active_codes, indent=2)
    expired_codes_ts = json.dumps(expired_codes, indent=2)
    
    # 生成 FAQ Schema
    faq_schema = generate_faq_schema(game_name)
    faq_schema_json = json.dumps(faq_schema, indent=2)
    
    # 替换模板变量
    content = template
    content = content.replace('{{gameName}}', game_name)
    content = content.replace('{{gameSlug}}', game_slug)
    content = content.replace('{{rewards}}', rewards_text)
    content = content.replace('{{activeCodesData}}', active_codes_ts)
    content = content.replace('{{expiredCodesData}}', expired_codes_ts)
    content = content.replace('{{faqSchema}}', faq_schema_json)
    content = content.replace('{{lastUpdated}}', datetime.now().strftime('%Y-%m-%d'))
    
    # 确保输出目录存在
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'✅ 代码页面已生成: {output_path}')
    print(f'   游戏: {game_name}')
    print(f'   有效代码: {len(active_codes)}')
    print(f'   过期代码: {len(expired_codes)}')

def generate_faq_schema(game_name: str) -> Dict:
    """生成 FAQ Schema"""
    return {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name': f'How do I redeem {game_name} codes?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': f'Open {game_name}, click the Settings icon, find the "Codes" or "Redeem" button, enter the code exactly as shown (case-sensitive), and click Submit.'
                }
            },
            {
                '@type': 'Question',
                'name': f'Why isn\'t my {game_name} code working?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'Codes are case-sensitive and may have expired. Check the expiration date in the table above and ensure you\'re typing it correctly without extra spaces.'
                }
            },
            {
                '@type': 'Question',
                'name': f'How often are new {game_name} codes released?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': f'New codes are typically released during game updates, milestones (like 1M likes), special events, and holidays. Follow the official {game_name} Discord and Twitter for instant notifications!'
                }
            },
            {
                '@type': 'Question',
                'name': f'Do {game_name} codes expire?',
                'acceptedAnswer': {
                    '@type': 'Answer',
                    'text': 'Yes, most codes expire after a few weeks or when the next update is released. We update this page daily to mark expired codes, so check back regularly!'
                }
            }
        ]
    }

def main():
    parser = argparse.ArgumentParser(description='生成 Roblox 游戏代码页面')
    parser.add_argument('--input', required=True, help='输入 JSON 文件路径')
    parser.add_argument('--output', required=True, help='输出 TSX 文件路径')
    parser.add_argument('--template', default='resources/templates/codes_page.tsx', 
                       help='模板文件路径')
    
    args = parser.parse_args()
    
    # 加载输入数据
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 生成页面
    generate_code_page(
        game_name=data['gameName'],
        game_slug=data['gameSlug'],
        active_codes=data.get('activeCodes', []),
        expired_codes=data.get('expiredCodes', []),
        template_path=args.template,
        output_path=args.output
    )

if __name__ == '__main__':
    main()
