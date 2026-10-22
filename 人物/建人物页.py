#!/usr/bin/env python3
"""人物廊样稿生成器（卡 361）。

输入：人物/人物.json（唯一数据源：肖像、站位、一句话、故事、出自第几计）
输出：
  1. people/<id>/index.html        每个人的静态页（首屏整屏大图＋超大名字，往下故事、出自第几计）
  2. index.html 里两行标记之间的卡片墙 HTML（首页"一墙人物卡片"）

用法：python3 人物/建人物页.py
规矩：只吃现有人物图，不新出图；生成物别手改，改 JSON 再跑。
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DATA = os.path.join(HERE, '人物.json')
MARK_A = '<!-- 人物廊:开始（人物/建人物页.py 生成，别手改） -->'
MARK_B = '<!-- 人物廊:结束 -->'


def esc(s):
    return html.escape(s, quote=True)


def load():
    with open(DATA, encoding='utf-8') as f:
        return json.load(f)


# ---------- 首页卡片墙 ----------
def wall_html(data):
    out = [MARK_A, '<div class="wall">']
    for i, p in enumerate(data['人物']):
        col, row = p['cell']
        cs, rs = p['span']
        cls = 'card' + (' lead' if i == 0 else '') + (' narrow' if cs == 1 else '')
        out.append(
            '<a class="{cls}" href="people/{id}/" style="grid-column:{col}/span {cs};grid-row:{row}/span {rs}">'
            '<img src="{img}" alt="{zh} {en}" loading="lazy" style="object-position:{pos}">'
            '<span class="nm"><span class="zh">{zh}</span><span class="en">{en}</span></span>'
            '</a>'.format(cls=cls, id=esc(p['id']), col=col, cs=cs, row=row, rs=rs,
                          img=esc(p['img']), zh=esc(p['zh']), en=esc(p['en']), pos=p['pos']))
    out.append('</div>')
    out.append(MARK_B)
    return '\n'.join(out)


# ---------- 人物页 ----------
PAGE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{zh} {en} · The 36 Stratagems with Yoko</title>
<meta name="description" content="{line}">
<link rel="icon" type="image/png" sizes="32x32" href="../../favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="../../favicon-192.png">
<link rel="apple-touch-icon" href="../../apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:title" content="{zh} {en} · 博弈 Bóyì">
<meta property="og:description" content="{line}">
<meta property="og:image" content="../../{img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../person.css">
</head>
<body>

<header class="hero">
  <img class="pic" src="../../{img}" alt="{zh} {en}" style="object-position:{pos}">
  <div class="veil"></div>
  <div class="heroIn">
    <span class="kicker">{kicker}</span>
    <h1>{zh}<span class="en">{en}</span></h1>
    <p class="line">{line}</p>
    <p class="lineZh">{lineZh}</p>
  </div>
  <a class="down" href="#story" aria-label="Read on">↓</a>
</header>

<main class="wrap">
{story}
{episode}
{others}
</main>

<footer class="foot">
  <div class="wrap row">
    <a class="back" href="../../">← All stratagems</a>
    <span class="meta">© 2026 博弈 Bóyì · The 36 Stratagems with Yoko</span>
  </div>
</footer>

</body>
</html>
'''

STORY = '''<section class="sec" id="story">
  <span class="seclabel"><span class="no">Story</span><span class="ln"></span></span>
  <div class="story">
{paras}
  </div>
</section>
'''

PARA = '''    <p>{en}<span class="zh">{zh}</span></p>
'''

EPISODE = '''<section class="sec" id="appears">
  <span class="seclabel"><span class="no">Appears in</span><span class="ln"></span></span>
  <div class="eps">
{eps}
  </div>
</section>
'''

EP = '''    <article class="ep">
      <div class="epNo">No. {no:02d}</div>
      <h2>{zh}</h2>
      <div class="epEn">{en}</div>
      <div class="epActs">
        <a class="btn red" href="https://www.youtube.com/watch?v={video}" target="_blank" rel="noopener">Watch the video</a>
        <a class="btn ghost" href="../../{pdf}">Free PDF</a>
      </div>
    </article>
'''

OTHERS = '''<section class="sec" id="others">
  <span class="seclabel"><span class="no">Also in {epno:02d}</span><span class="ln"></span></span>
  <div class="strip">
{cards}
  </div>
</section>
'''

OTHERCARD = '''    <a class="mini" href="../{id}/">
      <img src="../../{img}" alt="{zh} {en}" loading="lazy" style="object-position:{pos}">
      <span class="nm"><span class="zh">{zh}</span><span class="en">{en}</span></span>
    </a>
'''


def person_page(data, p):
    eps = p.get('episodes') or []
    first = eps[0] if eps else None
    kicker = ('No. %02d · People' % first['no']) if first else 'People'

    story = ''
    if p.get('story'):
        paras = ''.join(PARA.format(en=esc(s['en']), zh=esc(s.get('zh', ''))) for s in p['story'])
        story = STORY.format(paras=paras)

    episode = ''
    others = ''
    if first:
        episode = EPISODE.format(eps=''.join(EP.format(no=e['no'], zh=esc(e['zh']), en=esc(e['en']),
                                                     video=esc(e['video']), pdf=esc(e['pdf']))
                                              for e in eps))
        mates = [q for q in data['人物'] if q['id'] != p['id'] and any(e['no'] == first['no'] for e in (q.get('episodes') or []))]
        if mates:
            cards = ''.join(OTHERCARD.format(id=esc(q['id']), img=esc(q['img']), zh=esc(q['zh']),
                                             en=esc(q['en']), pos=q['pos']) for q in mates)
            others = OTHERS.format(epno=first['no'], cards=cards)

    return PAGE.format(zh=esc(p['zh']), en=esc(p['en']), id=esc(p['id']), img=esc(p['img']), pos=p['pos'],
                       line=esc(p['line']), lineZh=esc(p.get('lineZh', '')), kicker=esc(kicker),
                       story=story, episode=episode, others=others)


def main():
    data = load()
    ids = [p['id'] for p in data['人物']]
    assert len(ids) == len(set(ids)), 'id 有重复：%r' % ids
    for p in data['人物']:
        d = os.path.join(SITE, 'people', p['id'])
        os.makedirs(d, exist_ok=True)
        out = os.path.join(d, 'index.html')
        with open(out, 'w', encoding='utf-8') as f:
            f.write(person_page(data, p))
        print('人物页', os.path.relpath(out, SITE))

    idx = os.path.join(SITE, 'index.html')
    with open(idx, encoding='utf-8') as f:
        page = f.read()
    if MARK_A not in page or MARK_B not in page:
        sys.exit('index.html 里找不到人物廊标记，先在首页放好标记再来跑')
    new = re.sub(re.escape(MARK_A) + r'.*?' + re.escape(MARK_B), lambda m: wall_html(data), page, flags=re.S)
    with open(idx, 'w', encoding='utf-8') as f:
        f.write(new)
    print('首页卡片墙已写入 index.html（%d 张卡）' % len(data['人物']))


if __name__ == '__main__':
    main()
