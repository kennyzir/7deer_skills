"""
Trello 看板数据抓取器

从 Roblox 游戏的官方 Trello 看板抓取结构化数据
"""

import requests
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class TrelloCard:
    """Trello 卡片数据结构"""
    id: str
    name: str
    desc: str
    list_name: str
    labels: List[str]
    url: str

@dataclass
class GameItem:
    """游戏物品数据结构"""
    name: str
    category: str
    rarity: Optional[str]
    drop_rate: Optional[float]
    stats: Dict[str, any]
    obtain_method: List[str]
    description: str

class TrelloScraper:
    """Trello 看板抓取器"""
    
    def __init__(self, api_key: str = None, token: str = None):
        """
        初始化抓取器
        
        Args:
            api_key: Trello API Key (可选，公开看板不需要)
            token: Trello Token (可选，公开看板不需要)
        """
        self.api_key = api_key
        self.token = token
        self.base_url = "https://api.trello.com/1"
    
    def get_board_data(self, board_id: str) -> Dict:
        """
        获取看板的所有数据
        
        Args:
            board_id: Trello 看板 ID (从 URL 提取)
            
        Returns:
            包含所有列表和卡片的字典
        """
        # 构建 API URL
        url = f"{self.base_url}/boards/{board_id}"
        params = {
            'lists': 'all',
            'cards': 'all',
            'card_fields': 'name,desc,labels,idList',
            'list_fields': 'name'
        }
        
        if self.api_key and self.token:
            params['key'] = self.api_key
            params['token'] = self.token
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def extract_items(self, board_data: Dict) -> List[GameItem]:
        """
        从看板数据中提取游戏物品
        
        Args:
            board_data: get_board_data() 返回的数据
            
        Returns:
            游戏物品列表
        """
        items = []
        
        # 查找 "Items" 或 "Weapons" 列表
        item_lists = [
            lst for lst in board_data.get('lists', [])
            if any(keyword in lst['name'].lower() 
                   for keyword in ['item', 'weapon', 'accessory', 'equipment'])
        ]
        
        for lst in item_lists:
            list_name = lst['name']
            list_id = lst['id']
            
            # 获取该列表的所有卡片
            cards = [
                card for card in board_data.get('cards', [])
                if card['idList'] == list_id
            ]
            
            for card in cards:
                item = self._parse_item_card(card, list_name)
                if item:
                    items.append(item)
        
        return items
    
    def _parse_item_card(self, card: Dict, category: str) -> Optional[GameItem]:
        """
        解析单个物品卡片
        
        Args:
            card: Trello 卡片数据
            category: 物品类别 (从列表名推断)
            
        Returns:
            GameItem 对象或 None
        """
        name = card['name']
        desc = card.get('desc', '')
        
        # 提取稀有度
        rarity = self._extract_rarity(desc, card.get('labels', []))
        
        # 提取掉落率
        drop_rate = self._extract_drop_rate(desc)
        
        # 提取属性
        stats = self._extract_stats(desc)
        
        # 提取获取方法
        obtain_method = self._extract_obtain_method(desc)
        
        return GameItem(
            name=name,
            category=category,
            rarity=rarity,
            drop_rate=drop_rate,
            stats=stats,
            obtain_method=obtain_method,
            description=desc
        )
    
    def _extract_rarity(self, desc: str, labels: List[Dict]) -> Optional[str]:
        """从描述或标签中提取稀有度"""
        # 从标签提取
        rarity_labels = ['Common', 'Rare', 'Legendary', 'Mythical', 'Special Grade']
        for label in labels:
            label_name = label.get('name', '')
            if label_name in rarity_labels:
                return label_name
        
        # 从描述提取
        rarity_pattern = r'Rarity:\s*(\w+)'
        match = re.search(rarity_pattern, desc, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return None
    
    def _extract_drop_rate(self, desc: str) -> Optional[float]:
        """从描述中提取掉落率"""
        # 匹配 "0.25%", "2.5%", "Drop Rate: 0.1%" 等格式
        patterns = [
            r'(\d+\.?\d*)\s*%\s*drop',
            r'drop\s*rate:\s*(\d+\.?\d*)\s*%',
            r'chance:\s*(\d+\.?\d*)\s*%',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, desc, re.IGNORECASE)
            if match:
                return float(match.group(1))
        
        return None
    
    def _extract_stats(self, desc: str) -> Dict[str, any]:
        """从描述中提取属性数值"""
        stats = {}
        
        # 匹配 "Damage: 150", "Speed: 1.2", "+25% Crit" 等格式
        stat_patterns = [
            (r'Damage:\s*(\d+)', 'damage'),
            (r'Speed:\s*(\d+\.?\d*)', 'speed'),
            (r'Range:\s*(\d+)', 'range'),
            (r'\+(\d+)%\s*Crit', 'crit_bonus'),
            (r'\+(\d+)%\s*Attack\s*Speed', 'attack_speed_bonus'),
        ]
        
        for pattern, stat_name in stat_patterns:
            match = re.search(pattern, desc, re.IGNORECASE)
            if match:
                value = match.group(1)
                stats[stat_name] = float(value) if '.' in value else int(value)
        
        return stats
    
    def _extract_obtain_method(self, desc: str) -> List[str]:
        """从描述中提取获取方法"""
        methods = []
        
        # 常见获取方法关键词
        method_keywords = {
            'boss': 'Boss Drop',
            'raid': 'Raid',
            'craft': 'Crafting',
            'quest': 'Quest Reward',
            'shop': 'Shop Purchase',
            'trade': 'Trading',
            'chest': 'Chest Drop',
        }
        
        desc_lower = desc.lower()
        for keyword, method in method_keywords.items():
            if keyword in desc_lower:
                methods.append(method)
        
        return methods if methods else ['Unknown']
    
    def extract_codes(self, board_data: Dict) -> List[Dict]:
        """
        从看板中提取游戏代码
        
        Returns:
            代码列表，格式:
            [
                {
                    'code': 'LUNAR_FAREWELL',
                    'reward': '50 Spins',
                    'status': 'Active',
                    'notes': '...'
                }
            ]
        """
        codes = []
        
        # 查找 "Codes" 列表
        code_lists = [
            lst for lst in board_data.get('lists', [])
            if 'code' in lst['name'].lower()
        ]
        
        for lst in code_lists:
            list_name = lst['name']
            list_id = lst['id']
            
            # 判断是 Active 还是 Expired
            status = 'Expired' if 'expired' in list_name.lower() else 'Active'
            
            cards = [
                card for card in board_data.get('cards', [])
                if card['idList'] == list_id
            ]
            
            for card in cards:
                code_data = self._parse_code_card(card, status)
                if code_data:
                    codes.append(code_data)
        
        return codes
    
    def _parse_code_card(self, card: Dict, status: str) -> Optional[Dict]:
        """解析代码卡片"""
        name = card['name']
        desc = card.get('desc', '')
        
        # 代码通常在标题中
        code = name.strip()
        
        # 奖励通常在描述中
        reward = self._extract_reward(desc) or 'Unknown Reward'
        
        return {
            'code': code,
            'reward': reward,
            'status': status,
            'notes': desc[:200] if desc else ''
        }
    
    def _extract_reward(self, desc: str) -> Optional[str]:
        """从描述中提取奖励"""
        # 匹配 "50 Spins", "100 Cash", "5 Demon Fingers" 等
        reward_pattern = r'(\d+)\s*(Spins?|Cash|Yen|Fingers?|Resets?)'
        match = re.search(reward_pattern, desc, re.IGNORECASE)
        if match:
            return f"{match.group(1)} {match.group(2)}"
        
        return None


# 示例用法
if __name__ == '__main__':
    # Jujutsu Infinite 的 Trello 看板 ID
    board_id = 'mV6sSwXY'  # 从 URL 提取
    
    scraper = TrelloScraper()
    
    try:
        print("正在抓取 Trello 看板...")
        board_data = scraper.get_board_data(board_id)
        
        print("\n提取游戏物品...")
        items = scraper.extract_items(board_data)
        print(f"找到 {len(items)} 个物品")
        
        print("\n提取游戏代码...")
        codes = scraper.extract_codes(board_data)
        print(f"找到 {len(codes)} 个代码")
        
        # 保存为 JSON
        output = {
            'items': [vars(item) for item in items],
            'codes': codes
        }
        
        with open('trello_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print("\n数据已保存到 trello_data.json")
        
    except Exception as e:
        print(f"错误: {e}")
