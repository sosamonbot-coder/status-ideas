#!/usr/bin/env python3
import re
from datetime import datetime

# Read the markdown file
with open('STATUS-IDEAS.md', 'r') as f:
    content = f.read()

# Parse ideas from markdown
ideas = []
current_category = None
current_section = None

lines = content.split('\n')
idea_counter = 0

for line in lines:
    line = line.strip()
    
    # Skip empty lines and header
    if not line or line.startswith('#') and 'Status Ideas' in line:
        continue
        
    # Category headers (## Revenue Streams, ## Partnership Plays, etc.)
    if line.startswith('## ') and not line.startswith('## 💰') and not line.startswith('## 🤝'):
        current_category = line[3:].strip()
        current_section = current_category
        continue
    
    # Section headers with emojis (### Immediate, ### Short-term, etc.)
    if line.startswith('### '):
        current_section = line[4:].strip()
        continue
        
    # Numbered ideas
    if re.match(r'^\d+\.', line):
        idea_counter += 1
        match = re.match(r'^(\d+)\.\s*\*\*(.*?)\*\*\s*—\s*(.*)', line)
        if match:
            num, title, desc = match.groups()
            
            # Determine tag based on section
            tag = 'feature'
            tag_color = 'tag-feature'
            
            if current_category:
                if 'Revenue' in current_category:
                    if 'Immediate' in current_section:
                        tag = 'immediate'
                        tag_color = 'tag-immediate'
                    elif 'Short-term' in current_section:
                        tag = 'short'
                        tag_color = 'tag-short'
                    elif 'Medium-term' in current_section:
                        tag = 'medium'
                        tag_color = 'tag-medium'
                    elif 'Long-term' in current_section:
                        tag = 'long'
                        tag_color = 'tag-long'
                    else:
                        tag = 'revenue'
                        tag_color = 'tag-immediate'
                elif 'Partnership' in current_category:
                    tag = 'partnership'
                    tag_color = 'tag-partnership'
                elif 'Growth' in current_category:
                    tag = 'growth'
                    tag_color = 'tag-growth'
                elif 'Feature' in current_category:
                    tag = 'feature'
                    tag_color = 'tag-feature'
                elif 'Data' in current_category:
                    tag = 'data'
                    tag_color = 'tag-data'
                elif 'City' in current_category:
                    tag = 'city'
                    tag_color = 'tag-city'
                elif 'Quick' in current_category:
                    tag = 'quick win'
                    tag_color = 'tag-quick'
                elif 'Latest' in current_category or 'Sosa' in current_category:
                    tag = 'new'
                    tag_color = 'tag-quick'
            
            ideas.append({
                'num': int(num),
                'title': title.strip(),
                'desc': desc.strip(),
                'category': current_category or 'Other',
                'section': current_section or current_category or 'Other',
                'tag': tag,
                'tag_color': tag_color
            })

# Build HTML
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Status Ideas Engine</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#000;color:#fff;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display',system-ui,sans-serif;padding:16px;padding-bottom:100px}}
h1{{font-size:28px;font-weight:700;margin-bottom:4px}}
.subtitle{{color:#888;font-size:14px;margin-bottom:24px}}
.category{{margin-bottom:32px}}
.cat-header{{display:flex;align-items:center;gap:10px;margin-bottom:16px;cursor:pointer;-webkit-tap-highlight-color:transparent}}
.cat-icon{{font-size:24px}}
.cat-title{{font-size:20px;font-weight:600}}
.cat-count{{background:#1a1a1a;color:#888;font-size:12px;padding:2px 8px;border-radius:10px}}
.idea{{background:#111;border-radius:12px;padding:14px 16px;margin-bottom:8px;transition:all 0.2s}}
.idea:active{{background:#1a1a1a;transform:scale(0.98)}}
.idea-num{{color:#555;font-size:12px;font-weight:600;margin-bottom:4px}}
.idea-title{{font-size:15px;font-weight:600;margin-bottom:4px}}
.idea-desc{{color:#999;font-size:13px;line-height:1.4}}
.tag{{display:inline-block;font-size:11px;padding:2px 8px;border-radius:8px;margin-right:6px;margin-top:6px;font-weight:500}}
.tag-immediate{{background:#0a2a0a;color:#4ade80}}
.tag-short{{background:#1a1a00;color:#facc15}}
.tag-medium{{background:#1a0a00;color:#fb923c}}
.tag-long{{background:#1a0015;color:#c084fc}}
.tag-partnership{{background:#001a1a;color:#22d3ee}}
.tag-growth{{background:#0a001a;color:#818cf8}}
.tag-feature{{background:#1a0a1a;color:#f472b6}}
.tag-data{{background:#0a1a0a;color:#34d399}}
.tag-city{{background:#0a0a1a;color:#60a5fa}}
.tag-quick{{background:#2a0a0a;color:#f87171}}
.tag-new{{background:#2a1a00;color:#fbbf24}}
.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:24px}}
.stat{{background:#111;border-radius:12px;padding:14px;text-align:center}}
.stat-num{{font-size:28px;font-weight:700}}
.stat-label{{color:#888;font-size:11px;margin-top:2px}}
.filter-bar{{display:flex;gap:8px;overflow-x:auto;margin-bottom:20px;padding-bottom:8px;-webkit-overflow-scrolling:touch}}
.filter-bar::-webkit-scrollbar{{display:none}}
.filter{{background:#1a1a1a;color:#888;border:none;padding:8px 16px;border-radius:20px;font-size:13px;white-space:nowrap;cursor:pointer;-webkit-tap-highlight-color:transparent}}
.filter.active{{background:#fff;color:#000;font-weight:600}}
.hidden{{display:none}}
.search{{width:100%;background:#111;border:none;color:#fff;padding:12px 16px;border-radius:12px;font-size:15px;margin-bottom:16px;outline:none}}
.search::placeholder{{color:#555}}
</style>
</head>
<body>

<h1>Status Ideas Engine 🏆</h1>
<p class="subtitle">Living document · Updated {datetime.now().strftime("%B %d, %Y")}</p>

<div class="stats">
  <div class="stat">
    <div class="stat-num">{len(ideas)}</div>
    <div class="stat-label">Total Ideas</div>
  </div>
  <div class="stat">
    <div class="stat-num">{len([i for i in ideas if i['tag'] in ['immediate', 'new']])}</div>
    <div class="stat-label">Ready Now</div>
  </div>
  <div class="stat">
    <div class="stat-num">{len([i for i in ideas if 'Revenue' in i['category']])}</div>
    <div class="stat-label">Revenue Streams</div>
  </div>
</div>

<input type="text" class="search" placeholder="Search ideas..." id="search">

<div class="filter-bar">
  <button class="filter active" data-filter="all">All</button>
  <button class="filter" data-filter="new">New</button>
  <button class="filter" data-filter="immediate">Ready</button>
  <button class="filter" data-filter="partnership">Partnerships</button>
  <button class="filter" data-filter="growth">Growth</button>
  <button class="filter" data-filter="feature">Features</button>
  <button class="filter" data-filter="data">Data</button>
</div>

<div id="ideas-container">
"""

# Group ideas by category
categories = {}
for idea in ideas:
    cat = idea['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(idea)

# Add categories to HTML
for cat_name, cat_ideas in categories.items():
    # Get emoji for category
    emoji = '💰' if 'Revenue' in cat_name else '🤝' if 'Partnership' in cat_name else '🚀' if 'Growth' in cat_name else '🧠' if 'Feature' in cat_name else '📊' if 'Data' in cat_name else '🏙️' if 'City' in cat_name else '🎯' if 'Quick' in cat_name else '🧪' if 'Sosa' in cat_name else '💡'
    
    html += f"""
<div class="category" data-category="{cat_name}">
  <div class="cat-header">
    <span class="cat-icon">{emoji}</span>
    <span class="cat-title">{cat_name}</span>
    <span class="cat-count">{len(cat_ideas)}</span>
  </div>
"""
    
    for idea in sorted(cat_ideas, key=lambda x: x['num']):
        html += f"""
  <div class="idea" data-tags="{idea['tag']}" data-category="{idea['category']}">
    <div class="idea-num">#{idea['num']}</div>
    <div class="idea-title">{idea['title']}</div>
    <div class="idea-desc">{idea['desc']}</div>
    <span class="tag {idea['tag_color']}">{idea['tag']}</span>
  </div>
"""
    
    html += "</div>"

html += """
</div>

<script>
// Search functionality
document.getElementById('search').addEventListener('input', function() {
  const query = this.value.toLowerCase();
  const ideas = document.querySelectorAll('.idea');
  
  ideas.forEach(idea => {
    const title = idea.querySelector('.idea-title').textContent.toLowerCase();
    const desc = idea.querySelector('.idea-desc').textContent.toLowerCase();
    const matches = title.includes(query) || desc.includes(query);
    idea.style.display = matches ? 'block' : 'none';
  });
  
  // Hide empty categories
  document.querySelectorAll('.category').forEach(cat => {
    const visibleIdeas = cat.querySelectorAll('.idea[style*="block"], .idea:not([style*="none"])').length;
    cat.style.display = visibleIdeas > 0 ? 'block' : 'none';
  });
});

// Filter functionality
document.querySelectorAll('.filter').forEach(filter => {
  filter.addEventListener('click', function() {
    // Update active filter
    document.querySelectorAll('.filter').forEach(f => f.classList.remove('active'));
    this.classList.add('active');
    
    const filterValue = this.getAttribute('data-filter');
    const ideas = document.querySelectorAll('.idea');
    
    ideas.forEach(idea => {
      const tags = idea.getAttribute('data-tags');
      const matches = filterValue === 'all' || tags.includes(filterValue);
      idea.style.display = matches ? 'block' : 'none';
    });
    
    // Hide empty categories
    document.querySelectorAll('.category').forEach(cat => {
      const visibleIdeas = cat.querySelectorAll('.idea[style*="block"], .idea:not([style*="none"])').length;
      cat.style.display = visibleIdeas > 0 ? 'block' : 'none';
    });
  });
});

// Category toggle
document.querySelectorAll('.cat-header').forEach(header => {
  header.addEventListener('click', function() {
    const category = this.parentElement;
    const ideas = category.querySelectorAll('.idea');
    const isHidden = ideas[0].style.display === 'none';
    
    ideas.forEach(idea => {
      idea.style.display = isHidden ? 'block' : 'none';
    });
  });
});
</script>

</body>
</html>
"""

# Write the HTML file
with open('index.html', 'w') as f:
    f.write(html)

print(f"Dashboard built with {len(ideas)} ideas!")