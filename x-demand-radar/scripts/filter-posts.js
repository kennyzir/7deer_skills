#!/usr/bin/env node

/**
 * X Demand Radar - Post Filter & Ranker
 * 解析 browser snapshot 输出，过滤特征帖，输出 Top 10
 */

const READLINE = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  crlfDelay: Infinity
});

let rawInput = '';
rl.on('line', line => rawInput += line + '\n');
rl.on('close', () => {
  try {
    const snapshot = JSON.parse(rawInput);
    const posts = extractPosts(snapshot);
    const filtered = filterAndRank(posts);
    console.log(JSON.stringify(filtered, null, 2));
  } catch (e) {
    console.error('Parse error:', e.message);
    process.exit(1);
  }
});

/**
 * 从 snapshot 中提取帖子数据
 * 支持多种 snapshot 格式
 */
function extractPosts(snapshot) {
  const posts = [];
  
  // 尝试从 snapshot 结构中提取文章列表
  // snapshot 结构: { data: [...], refs: {...} } 或直接是数组
  const articles = findArticles(snapshot);
  
  for (const article of articles) {
    const post = parseArticle(article);
    if (post) posts.push(post);
  }
  
  return posts;
}

function findArticles(obj) {
  if (!obj || typeof obj !== 'object') return [];
  
  // 直接是数组
  if (Array.isArray(obj)) return obj;
  
  // 查找 articles 或 statuses 字段
  if (obj.articles) return obj.articles;
  if (obj.statuses) return obj.statuses;
  if (obj.data) return findArticles(obj.data);
  
  // 递归搜索
  for (const key of Object.keys(obj)) {
    const val = obj[key];
    if (Array.isArray(val) && val.length > 0) {
      // 检查是否像帖子数组
      if (val[0] && (val[0].text || val[0].full_text || val[0].content)) {
        return val;
      }
      const nested = findArticles(val);
      if (nested.length > 0) return nested;
    }
  }
  
  return [];
}

function parseArticle(article) {
  if (!article) return null;
  
  // 提取文本 (支持多种字段名)
  const text = article.text || article.full_text || article.content || article.description || '';
  
  // 跳过太短的
  if (text.length < 30) return null;
  
  // 提取用户信息
  const user = article.user || article.author || {};
  const screenName = user.screen_name || user.username || user.handle || 'unknown';
  
  // 提取 engagement
  const favorites = parseInt(article.favorite_count || article.favorites || article.likes || 0);
  const retweets = parseInt(article.retweet_count || article.retweets || article.reposts || 0);
  const replies = parseInt(article.reply_count || article.replies || 0);
  
  // 提取时间和 ID
  const createdAt = article.created_at || article.timestamp || article.date || '';
  const id = article.id_str || article.id || '';
  
  return {
    text,
    author: screenName,
    favorites,
    retweets,
    replies,
    createdAt,
    id,
    url: screenName !== 'unknown' ? `https://x.com/${screenName}/status/${id}` : ''
  };
}

function filterAndRank(posts) {
  // 排除词
  const excludePatterns = [
    'already exists', 'already built', 'try it at',
    'check this out', 'here is the tool', 'i built this',
    'we built', 'launched:', 'show hn', 'github.com',
    'product hunt', 'beta.access'
  ];
  
  return posts
    // 基础过滤
    .filter(p => p.favorites >= 30)
    .filter(p => p.replies <= 100) // 还没被刷屏
    .filter(p => p.text.length >= 80)
    
    // 排除已有解决方案
    .filter(p => !excludePatterns.some(w => p.text.toLowerCase().includes(w)))
    
    // 排序：优先点赞，其次转发
    .sort((a, b) => {
      const scoreA = a.favorites * 1 + a.retweets * 0.5;
      const scoreB = b.favorites * 1 + b.retweets * 0.5;
      return scoreB - scoreA;
    })
    
    // Top 10
    .slice(0, 10)
    
    // 添加排名
    .map((p, i) => ({
      rank: i + 1,
      ...p,
      engagementScore: p.favorites * 1 + p.retweets * 0.5
    }));
}
