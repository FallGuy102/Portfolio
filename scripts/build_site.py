"""Generate static HTML from reviewed public project content. No private sources copied."""
from pathlib import Path
from html import escape as e
from hashlib import sha256

ROOT = Path(__file__).resolve().parents[1]
A = 'assets/portfolio/'

def s(title, text, images=(), steps=()):
    return dict(title=title, text=text, images=images, steps=steps)

PROJECTS = [
dict(slug='memorizer', title='Memorizer', en='RECORD. REPLAY. RETHINK.', category='2D 平台解谜', tag='GAMEPLAY / SYSTEMS', date='2024.01 — 2024.03', engine='Unity / C#', team='个人项目', role='核心机制、关卡设计、程序实现、UI 与测试迭代', cover='page-12-07.webp', intro='记录一段动作，在新的位置重放。将移动、跳跃与机关操作重新组合，抵达原本无法到达的地方。', links=[('观看玩法演示','https://www.bilibili.com/video/BV1aV5Dz2EM1/')], sections=[
s('先尝试，再用操作理解能力。','录制一段动作，换一个位置播放。同一段移动因此能跨过原本无法通过的地形。首关用无法直接跳过的深渊制造需求，并在附近设置存档点，支持反复尝试。', [('page-12-08.webp','首关：先面对普通跳跃无法通过的障碍，再尝试录制与播放。')], [('测试发现','获得能力，却不知道怎么用','试玩中，玩家初次获得能力后无从下手。'),('教学调整','录制 → 移动 → 播放','先允许自主尝试；死亡后出现 UI，提示在一处录制、走到另一处播放，亲自观察结果。新的流程仍需后续测试验证。')]),
s('只改高度，就需要新的解法。','梯子谜题先让玩家录制爬梯，再利用播放抵达高台。下一道谜题保留相似结构，却抬高目标：照搬旧解法不再有效，录制中必须增加跳跃。之后再引入录制下落，打破“只记录向上移动”的惯性。', [('memorizer-ladder-a.webp','基础谜题：录制爬梯，在新的起点播放并抵达高台。'),('memorizer-ladder-b.webp','变化谜题：高度差让原解法失效，需要在录制中补上跳跃。')]),
s('主线教规则，紫星考验复用。','黄色星星引导主路线；紫色星星留给额外探索。图中黄色星星位于中间高台，紫色星星则放在更高的平台：完成主要路线后，还可以继续尝试录制与播放的组合，挑战额外收集。', [('memorizer-purple-star.png','梯子谜题的难度分层：中间高台上的黄星与更高处的可选紫星。')]),
s('有了解法，不代表谜题就成立。','曾先设想“录下短暂停留和按钮操作，再站到移动平台上播放”的解法，却难以构建匹配的关卡条件。最终放弃部分设想，改为相近的谜题。这次尝试暴露了从预期解法倒推关卡时的限制。', [('page-17-02.webp','未采用方案 / 录制：红圈表示按下按钮，箭头表示移动。'),('page-17-03.webp','未采用方案 / 播放：预想通过重放操作启动平台，抵达另一端。')])
]),
dict(slug='beneath-the-ice', title='冰面之下', en='BENEATH THE ICE', category='3D 关卡白盒', tag='LEVEL DESIGN / SPATIAL PUZZLE', date='2026.05.18 — 2026.05.25 · 7 天', engine='Unity / 3D', team='个人作品', role='关卡规则、空间布局、能力教学与镜像区域设计', cover='ice-cover.webp', intro='冰既能铺出道路，也能打开空间。在水上工厂中逐步掌握冰冻与破冰，再从熟悉场景的另一面寻找出口。', video=True, links=[], sections=[
s('两个阀门，串起两次能力教学。','中央装置需要两个阀门，左右支路分别引入冰枪与破冰锤。能力先用于敌人，再用于地形：冻结水面铺路，或击碎冰面让敌人落水，再重新冻结通过。取得阀门后返回中心，开启下一段路线。', [('ice-03.webp','双阀门区域：两条支路承载能力教学，完成后回到中央装置。')], [('冰枪','从冻结敌人到冻结水面','将同一能力从战斗对象迁移到通行问题。'),('破冰锤','破坏冰面，再重建通路','通过观察孔预览水域与敌人，先破冰清除障碍，再冻结水面前进。')]),
s('先补全一个洞口，再翻转整座工厂。','高能水让普通冰枪失效，引导玩家寻找寒冰核心。升级后的冰面映出半圆洞口，补全它的形状；真正打碎冰面后，镜像通路才打开。玩家先在局部理解规则，再回到祭坛，将它应用于更大的水面。', [('ice-04.webp','升级与镜像教学路线：先解决局部通路，再将新规则迁移到大水面。')], [('观察','倒影补全形状','镜面提示空间关系，但倒影本身不是可通行区域。'),('行动','破冰打开镜像','从小尺度的洞口验证，过渡到整片区域的空间翻转。')]),
s('旧空间，新的可达关系。','镜像后，原来的天花板成为地面，管道成为方向参照和落脚点。先前看得到却到不了的黄色光房间变得可达；双阀门谜题不必重做，挑战转向辨认熟悉场景中的新路线。', [('ice-05.webp','镜像后的入口：沿熟悉的管道和桥梁，重新判断可以落脚的位置。')]),
s('白盒范围','当前 Demo 在抵达黄色光房间并拾取终点道具后结束。重点是能力教学、路径组织与空间翻转；现实和镜像之间的往返仍是后续设想。控制器基于 Unity Starter Assets，部分模型与音效来自 Sketchfab、Pixabay，不作为个人美术成果。')
]),
dict(slug='lost-realm', title='Lost Realm', en='READ THE SPACE.', category='3D 潜行解谜', tag='LEVEL DESIGN / BLUEPRINT', date='2024.04 — 2024.07', engine='Unreal Engine / Blueprint', team='个人项目', role='三层箱庭布局、潜行解谜、交互蓝图与流程迭代', cover='page-19-02.webp', intro='通过潜行、机关与空间变化，探索三层箱庭。让玩家在学习规则的同时，逐步建立对整张地图的理解。', links=[('观看关卡演示','https://www.bilibili.com/video/BV1aV5Dz2EGF/')], sections=[
s('用转折控制视线，用掩体改变节奏。','Z 形走廊不让玩家一眼看到目的地。矮掩体、巡逻朝向与转角共同决定移动时机：蹲伏隐藏，等待守卫转身，再接近背刺。这里也将前段的解谜节奏切换为潜行。', [('page-24-01.webp','Z 形路线与矮掩体：先观察巡逻，再选择通过时机。')]),
s('先看见谜题，再找到入口。','玩家隔着玻璃预览暂时无法进入的画廊，再寻找另一条路线。进入后，通过旋转地面改变与炮台射线的相对位置，逐步关闭炮台并解锁中央水晶。空间既预告目标，也构成解法。', [('page-26-01.webp','二层路线：餐厅潜行之后进入画廊解谜，随后开启返回大厅的捷径。')]),
s('让地标参与整个流程。','大厅中央圆盘在迭代中改为巨型雕像：先帮助定位，再作为机关打开下层，随后成为 Boss，倒下后形成通路。同一对象反复出现，但承担不同任务。', [('page-29-01.webp','白盒迭代：中央圆盘改为雕像，同时调整餐厅布局与区域连接。')], [('目标可见','出口从二楼移到一楼','扩大出口尺度，使玩家进入大厅时就能看到宝藏室，尽早建立长期目标。'),('重访空间','回收并重新分配电池','返回已探索区域，把已有道具用于退出路径，而不是不断引入新规则。')])
]),
dict(slug='divine-deception', title='Divine Deception', en='TRUST IS A CHOICE.', category='多人策略桌游', tag='BOARD GAME / SOCIAL DEDUCTION', date='2023.09 — 2023.11', engine='实体卡牌 / 5、7、9、11 人', team='个人项目', role='合作与欺骗机制、卡牌系统、数值平衡、卡牌视觉制作', cover='page-01-01.webp', intro='每轮私聊后秘密选择阵营：全员一致可以共同得分，足够少的少数派却能赢得更多。围绕承诺与人数预判，争取个人胜利。', links=[], sections=[
s('同意合作，还是成为唯一的背叛者？','基础计分取决于两边的人数：全员同阵营时每人 1 分；若出现少数派，5／7 人局中少数方仅 1 人、9／11 人局中少数方不超过 2 人时，少数方每人 3 分；否则多数方每人 1 分。其余玩家本轮不获分，卡牌可能改变结果。下面用五人局说明：', steps=[('5 : 0','全员各得 1 分','一致选择，所有人共同获益。'),('3 : 2','多数方各得 1 分','少数方人数不够少，无法获得高收益。'),('4 : 1','唯一少数派得 3 分','单独行动收益更高，但多人同时背叛就可能落空。')]),
s('卡牌改变信息，也提供应对机会。','不只增加效果数量，而是改变玩家作决定时掌握的信息与资源。', steps=[('事件示例','公开选择后，允许再选','Change of Heart 让玩家看到原本的阵营分布后重新选择，使先前承诺面临新的判断。'),('失利补偿','下一轮获得能力牌','从第二轮起，上轮失利者抽取能力牌，手牌上限为一张，为后续回合提供应对资源。')]),
s('测试后，留下需要解决的问题。','实体原型支持 5、7、9、11 人。达到 7 分且领先第二名至少 2 分时获胜。测试记录指出部分事件卡影响较弱或不明显；下一步应检验它们是否真正改变选择，而不是继续增加卡牌数量。', [('page-07-01.webp','实体卡牌原型与测试记录中的桌面照片。')])
]),
dict(slug='1000-action', title='1000, Action!', en='EDIT THE TIMELINE.', category='时间编辑解谜', tag='GAME JAM / LEVEL DESIGN', date='2026.01.31 — 2026.02.02 · 48 小时', engine='Unity / C#', team='团队项目', role='关卡设计；参与时间控制与局部冻结机制实现', cover='action-cover.png', intro='像剪辑视频一样解谜。利用时间轴与遮罩改变事件的发生关系，在有限时间里构建因果推演的挑战。', award='GGJ 2026 哥德堡 · 最佳游戏设计奖 / 最佳创新奖', links=[('前往 itch.io 试玩','https://zzoonng.itch.io/1000action')], sections=[
s('改变顺序，改变结果。','通过调整时间轴与遮罩，改变事件发生顺序和局部冻结状态。解谜的关键是看清各对象的动作如何相互影响，再编辑它们的时间关系。', [('action-gameplay.png','关卡与时间轴同屏呈现，便于对照操作和运行结果。')]),
s('48 小时内的个人贡献。','负责关卡设计，并参与时间控制与局部冻结机制实现。项目在 Global Game Jam 2026 哥德堡站完成，获得最佳游戏设计奖与最佳创新奖；其他成员及可玩版本见项目主页。')
]),
dict(slug='peng-win', title='Peng-Win!', en='ONE KICK. MANY POSSIBILITIES.', category='2.5D 网格解谜', tag='GAME JAM / PUZZLE DESIGN', date='2025.12.12 — 2025.12.14 · 48 小时', engine='Unity / C#', team='团队项目', role='核心玩法、递进式关卡、箱子路径控制与设计迭代', cover='peng-cover.png', intro='踢动企鹅，预测滑行终点。利用冰面、水面和箱子改变路径，将企鹅送进雪橇。', award='Xmas Game Jam · 最佳游戏设计奖', links=[('前往 itch.io 试玩','https://scariett77.itch.io/peng-win')], sections=[
s('预测滑行终点，再决定从哪里踢。','玩家在网格中调整位置，踢动企鹅，利用滑行惯性抵达雪橇。箱子用于阻挡、填补间隙或改变路径，让挑战集中在方向与终点的预判。', [('peng-gameplay.png','网格关卡：观察企鹅、箱子与终点的位置，再布置滑行路线。')]),
s('围绕一个动作构建关卡。','负责“踢动 + 滑行”的核心玩法、递进式关卡与箱子路径系统设计。作品由团队在 48 小时内完成，获得 Xmas Game Jam 最佳游戏设计奖；成员与可玩版本见项目主页。')
])
]

# Explain the player's goal and actions before discussing design decisions.
GAMEPLAY = {
    'memorizer': (
        '一款以动作录制与播放为核心的单人 2D 平台解谜游戏。玩家操控蘑菇角色穿过平台与机关，抵达关卡终点；紫色星星是可选挑战。',
        [('录制动作', '记录移动、跳跃、爬梯或机关操作。键鼠左键录制，手柄使用 LB。'),
         ('换一个起点', '移动到新的位置，考虑同一段动作从这里执行，会把角色带到哪里。'),
         ('播放并修正', '右键或 RB 播放记录，让角色执行先前的动作。这不是时间倒流，也不是生成分身；失败后调整记录或起点。')]),
    'beneath-the-ice': (
        '一款在水上工厂中探索的单人 3D 空间解谜白盒。玩家利用冰枪、破冰锤和阀门改变通路，最终抵达先前无法到达的黄色光房间。',
        [('冻结水面', '水域阻挡通行；冰枪可冻结普通水面铺路，也可冻结敌人。'),
         ('破冰与开路', '用锤子击碎冰面或冻结的敌人，结合阀门改变水位，进入下一区域。'),
         ('进入镜像空间', '获取寒冰核心后，冻结高能水形成二级冰；击碎它打开上下翻转的空间，重新寻找路线。')]),
    'lost-realm': (
        '一款结合潜行与机关解谜的单人 3D 探索游戏。玩家扮演寻宝者进入三层地下宫殿，避开或消灭守卫，解开机关并寻找宝藏。',
        [('观察与潜行', '观察巡逻方向，利用蹲伏和掩体躲避视线，等待接近守卫背后的时机。'),
         ('操作机关', '使用杠杆、旋转平台和电池供电改变空间，打开原本无法通过的路径。'),
         ('重访与推进', '沿新通路探索，再回到熟悉区域，利用获得的道具和空间变化推进到宝藏与退出路径。')]),
    'divine-deception': (
        '一款面向 5、7、9 或 11 人的协商与欺骗桌游。每人持有天使、恶魔两种阵营卡，每轮都能重新选择立场。没有固定队伍：通过谈判影响他人的选择，再凭阵营人数和卡牌效果争取个人得分。先达到 7 分且领先第二名至少 2 分者获胜。',
        [('揭示事件，私下协商', '事件卡改变本轮条件。玩家用 3–4 分钟私聊，可以约定一起选哪边，也可以误导对手。'),
         ('秘密选择阵营', '各自选择天使或恶魔，在揭晓前不知道其他人最终选了哪边。承诺不强制约束选择。'),
         ('使用能力，结算分数', '选择是否激活能力牌，按阵营人数及卡牌效果得分，再进入下一轮。每轮都可以重新合作或改变立场。')]),
    '1000-action': (
        '一款把视频剪辑变成操作方式的单人解谜游戏。玩家扮演剪辑师，通过安排场景对象的行动时机，帮助主角通过障碍、抵达终点，而不是直接控制主角移动。',
        [('编辑时间轴', '拖动轨道上的片段，调整角色、落石等对象开始和结束行动的时间。'),
         ('使用遮罩', '遮罩是让选定区域时间冻结的工具，用它改变局部对象与其他事件的配合。'),
         ('播放并重试', '按空格开始或重新运行，观察结果，再调整片段顺序和时机。具体操作以游戏内提示为准。')]),
    'peng-win': (
        '一款单人网格解谜游戏。玩家调整踢击位置，让企鹅沿冰面和水面滑行，目标是将它送进雪橇。滑动会持续到遇到障碍或抵达目标，因此需要先规划停靠点。',
        [('观察路线', '确认企鹅、雪橇、水面和障碍的位置，预测一次踢击会让企鹅停在哪里。'),
         ('移动箱子', '利用可推动箱子阻挡滑行、填补间隙或改变可用路径。'),
         ('踢击并验证', '从合适的方向踢动企鹅；根据滑行结果重新安排位置与路径。')]),
}

# Reading guides point to evidence already present in each case study.
CASE_GUIDES = {
    'memorizer': ('录制、播放与谜题变式', '让同一段动作，成为不同谜题的解法。', [('教学调整', 1), ('谜题变式', 2), ('设计取舍', 4)], '四关个人原型 · 核心玩法、关卡与程序实现'),
    'beneath-the-ice': ('能力教学与镜像空间', '从改变水面，到重新理解整座工厂。', [('双阀门教学', 1), ('镜像规则', 2), ('空间回收', 3)], '个人 3D 关卡白盒 · 路径、能力教学与空间设计'),
    'lost-realm': ('视线、路线与地标', '让空间决定玩家何时观察、行动与重访。', [('潜行视线', 1), ('目标预告', 2), ('布局迭代', 3)], '个人 Unreal Engine 项目 · 潜行解谜与交互蓝图'),
    'divine-deception': ('协商与秘密选择', '合作有收益，背叛也有风险。', [('五人局示例', 1), ('卡牌决策', 2), ('测试反思', 3)], '个人桌游原型 · 规则、卡牌与实体测试'),
    '1000-action': ('时间编辑解谜', '把事件顺序变成可以操作的谜题。', [('核心玩法', 1), ('个人贡献', 2)], '48 小时团队作品 · 关卡设计与部分机制实现'),
    'peng-win': ('滑行与路径控制', '用简单的踢击，构建空间推演。', [('玩法与箱子', 1), ('个人贡献', 2)], '48 小时团队作品 · 核心玩法与关卡设计'),
}

# Display only the evidence region; the lightbox preserves the original source page.
IMAGE_REGIONS = {
    'page-24-01.webp': (4, 14, 65, 75, 2500 / 1407),
    'page-26-01.webp': (6.8, 13.8, 39, 77, 2500 / 1407),
    'page-29-01.webp': (3.5, 9.6, 93, 44, 2500 / 1407),
    'page-07-01.webp': (1, 60.5, 53, 32.5, 2560 / 1392),
}

PROJECT_VIDEOS = {
    'memorizer': 'vh6fNjEnm2g',
    'lost-realm': 'yDFRsF5Ki6g',
    'beneath-the-ice': 'bwX1CtxmgSg',
}

def arrow_icon(direction="up-right"):
    paths = {
        "up-right": "M6 18 18 6M6 6h12v12",
        "down": "M12 4v16m-7-7 7 7 7-7",
        "up": "M12 20V4m-7 7 7-7 7 7",
        "left": "M20 12H4m7-7-7 7 7 7",
    }
    return f'<svg class="arrow-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="{paths[direction]}"/></svg>'

def youtube_video(video_id, title):
    return f'''<figure class="video-figure"><iframe class="youtube-player" src="https://www.youtube-nocookie.com/embed/{e(video_id)}?rel=0&amp;playsinline=1" title="{e(title)}：玩法与关卡演示（YouTube）" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe><figcaption>{e(title)} · 玩法与关卡演示</figcaption></figure><div class="video-actions"><a class="text-link" href="https://www.youtube.com/watch?v={e(video_id)}" target="_blank" rel="noopener noreferrer">在 YouTube 观看 {arrow_icon()}</a></div>'''

def picture(file, caption, eager=False):
    img = f'<img src="{A}{file}" alt="{e(caption)}" loading="{"eager" if eager else "lazy"}" decoding="async">'
    hint = '点击查看大图 +'
    if file in IMAGE_REGIONS:
        x, y, w, h, ratio = IMAGE_REGIONS[file]
        style = f'--region-ratio:{ratio*w/h:.5f};--image-width:{10000/w:.5f}%;--image-left:{-x/w*100:.5f}%;--image-top:{-y/h*100:.5f}%'
        img = f'<span class="image-region" style="{style}">{img}</span>'
        hint = '查看原始设计页 +'
    return f'<figure class="figure"><a class="image-link" href="{A}{file}" data-lightbox aria-label="{hint[:-2]}：{e(caption)}">{img}</a><figcaption>{e(caption)} <span>{hint}</span></figcaption></figure>'

def shell(title, desc, content):
    css_version = sha256((ROOT / 'portfolio.css').read_bytes()).hexdigest()[:12]
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#0a0a0a"><title>{e(title)} | 陈品元</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="styles.css"></head>
<body><a class="skip" href="#main">跳转到内容</a><header class="site-header"><a class="brand" href="index.html" aria-label="陈品元，返回首页">CP<span>Y.</span></a><span class="header-name">CHEN PINYUAN / 陈品元</span><nav aria-label="主导航"><a href="index.html#work">作品 <span>06</span></a><a href="index.html#about">关于</a><a href="mailto:1027997849@qq.com">联系 <span aria-hidden="true">{arrow_icon()}</span></a></nav></header>
<main id="main">{content}</main>
<footer id="contact" class="container footer"><p class="eyebrow">LET’S MAKE SOMETHING PLAYABLE.</p><h2>一起创造值得探索的体验。</h2><a class="email" href="mailto:1027997849@qq.com">1027997849@qq.com <span aria-hidden="true">{arrow_icon()}</span></a><div class="footer-bottom"><span>陈品元 · GAME & LEVEL DESIGN</span><a href="#main">回到顶部 {arrow_icon("up")}</a></div></footer>
<dialog id="image-viewer" aria-label="图片大图"><button class="viewer-close" aria-label="关闭大图">关闭 ×</button><button class="viewer-zoom" aria-pressed="false">原尺寸查看</button><div class="viewer-scroll"><img alt=""></div><p></p></dialog><script src="portfolio.js" defer></script></body></html>'''.replace('href="styles.css"', f'href="portfolio.css?v={css_version}"')

def build_home():
    rows=''
    for i,p in enumerate(PROJECTS):
        rows+=f'<a class="work-row" href="{p["slug"]}.html"><div class="work-image"><img src="{A}{p["cover"]}" alt="{e(p["title"])} 游戏画面与作品设计" loading="lazy" decoding="async"><span class="work-number">0{i+1}</span></div><div class="work-copy"><p class="eyebrow">{p["tag"]}</p><h3>{p["title"]}</h3><p>{p["intro"]}</p><div class="work-meta"><span>{p["team"]}</span><span>{p["category"]}</span></div><span class="row-link">查看项目 <span aria-hidden="true">{arrow_icon()}</span></span></div></a>'
    body=f'''<section class="container home-hero"><div class="hero-top"><p class="eyebrow">LEVEL DESIGN / PLAYER GUIDANCE / PUZZLES</p><span class="edition">PORTFOLIO / 2026</span></div><h1>DESIGN<br><span>FOR PLAY.</span></h1><div class="hero-bottom"><p class="intro-name">陈品元<span>关卡策划 / Level Designer</span></p><p>围绕玩法组织空间与挑战，<br>关注玩家如何找到路线、理解能力并完成解谜。</p><a class="text-link" href="#work">探索作品 {arrow_icon("down")}</a></div><a class="hero-feature" href="beneath-the-ice.html"><img src="{A}ice-cover.webp" alt="冰面之下：水上工厂的 3D 关卡白盒" fetchpriority="high"><span class="feature-label">SPATIAL STUDY / 3D BLOCKOUT</span><span class="feature-title">冰面之下 <span aria-hidden="true">{arrow_icon()}</span></span></a></section>
<section class="container work-section" id="work"><div class="section-heading"><div><p class="eyebrow">SELECTED WORK / 01—06</p><h2>玩法，落在作品里。</h2></div><p>个人项目与团队创作<br>从桌面规则到三维空间</p></div>{rows}</section>
<section id="about" class="about-section"><div class="container about-grid"><div><p class="eyebrow">ABOUT / 陈品元</p><h2>关注规则，<br>也关注规则<br><span>如何被理解。</span></h2></div><div class="about-copy"><p class="lead">游戏设计与技术背景，关注玩法机制、解谜设计与关卡空间。</p><p>在哥德堡大学攻读 Game Design and Technology 硕士。以计算机科学为基础，将设计想法转化为可运行的原型，再通过测试调整玩家的学习过程与挑战节奏。</p><dl class="profile"><div><dt>2025—2027</dt><dd>哥德堡大学<br>Game Design and Technology · 硕士在读</dd></div><div><dt>2020—2024</dt><dd>北师香港浸会大学<br>计算机科学与技术 · 荣誉理学学士</dd></div><div><dt>TOOLS</dt><dd>Unity / Unreal Engine / C# / Blueprint<br>Git / Photoshop / Spine</dd></div></dl></div></div></section>'''
    (ROOT/'index.html').write_text(shell('游戏与关卡设计作品集','陈品元的游戏设计作品集：六个玩法与关卡项目，包含个人原型、桌游和团队 GameJam。',body).replace('><', '>\n<'),encoding='utf-8')

def build_project(p,i):
    focus, question, highlights, scope = CASE_GUIDES[p['slug']]
    guide_links = ''.join(f'<a href="#section-{section}">{e(label)} <span aria-hidden="true">{arrow_icon("down")}</span></a>' for label, section in highlights)
    overview = f'<section class="case-overview" aria-label="项目阅读重点"><p class="eyebrow">DESIGN FOCUS / {e(focus)}</p><h2>{e(question)}</h2><p>{e(scope)}</p><nav aria-label="重点内容">{guide_links}</nav></section>'
    nav='<a href="#gameplay"><span>00</span>游戏介绍与玩法</a>'+''.join(f'<a href="#section-{j+1}"><span>0{j+1}</span>{e(s["title"])}</a>' for j,s in enumerate(p['sections']))
    body=''
    for j,s in enumerate(p['sections']):
        steps='<div class="steps">'+''.join(f'<article><p class="eyebrow">{e(n)}</p><h3>{e(t)}</h3><p>{e(d)}</p></article>' for n,t,d in s['steps'])+'</div>' if s['steps'] else ''
        pics=''.join(picture(f,c) for f,c in s['images'])
        body+=f'<section class="case-section" id="section-{j+1}"><p class="eyebrow">0{j+1} / DESIGN NOTES</p><h2>{e(s["title"])}</h2><p class="section-lead">{e(s["text"])}</p>{steps}<div class="gallery">{pics}</div></section>'
    video_id = PROJECT_VIDEOS.get(p['slug'])
    media = youtube_video(video_id, p['title']) if video_id else ''
    if p.get('video'):
        media += f'''<details class="video-fallback"><summary>YouTube 无法播放？使用本地备用视频</summary><video controls playsinline preload="none" poster="{A}ice-cover.webp" aria-label="冰面之下本地备用演示"><source src="{A}beneath-the-ice.mp4" type="video/mp4"></video><p>备用视频为较小的 720p 版本。</p></details>'''
    nxt=PROJECTS[(i+1)%len(PROJECTS)]
    description, actions = GAMEPLAY[p['slug']]
    action_html = ''.join(f'<li><h3>{e(title)}</h3><p>{e(text)}</p></li>' for title, text in actions)
    gameplay = f'<section class="gameplay-intro" id="gameplay" aria-labelledby="gameplay-title"><p class="eyebrow">HOW TO PLAY / 游戏介绍</p><h2 id="gameplay-title">这是什么游戏，怎么玩？</h2><p class="section-lead">{e(description)}</p><ol class="gameplay-loop">{action_html}</ol></section>'
    if p['slug'] == '1000-action':
        media += f'''<section class="playable" aria-labelledby="playable-title"><p class="eyebrow">PLAY IN BROWSER / 网页试玩</p><h2 id="playable-title">直接试一关。</h2><p>建议使用电脑键鼠。点击后从 itch.io 加载游戏，可能需要等待；先点击游戏画面，再按空格运行或重试。</p><div class="game-stage" id="action-game" data-game-src="https://itch.io/embed-upload/16338738?color=0a0a0a"><button class="game-launch" type="button" aria-controls="action-game">加载并开始游戏</button></div><div class="game-controls"><button class="game-fullscreen" type="button" disabled>全屏游玩</button><button class="game-stop" type="button" hidden>关闭游戏</button><a class="text-link" href="https://zzoonng.itch.io/1000action" target="_blank" rel="noopener noreferrer">无法加载？前往 itch.io {arrow_icon()}</a></div><p class="game-status" role="status" aria-live="polite">尚未加载，不会自动播放声音。</p><noscript><p>当前浏览器未启用 JavaScript，请通过上方 itch.io 链接游玩。</p></noscript></section>'''
    media = gameplay + media + overview
    award=f'<p class="award">{p["award"]}</p>' if p.get('award') else ''
    links=''.join(f'<a class="text-link" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)} {arrow_icon()}</a>' for label,url in p['links'])
    content=f'''<div class="container"><section class="project-hero"><a class="back-link" href="index.html#work">{arrow_icon("left")} 全部作品</a><p class="eyebrow">0{i+1} / {p['tag']}</p><h1>{p['title']}</h1><p class="project-english">{p['en']}</p><p class="project-intro">{p['intro']}</p>{award}<dl class="project-facts"><div><dt>TYPE / 类型</dt><dd>{p['category']} · {p['team']}</dd></div><div><dt>PERIOD / 周期</dt><dd>{p['date']}</dd></div><div><dt>TOOLS / 工具</dt><dd>{p['engine']}</dd></div><div><dt>CONTRIBUTION / 职责</dt><dd>{p['role']}</dd></div></dl><div class="project-links">{links}</div>{media}</section><div class="case-layout"><aside class="case-nav" aria-label="项目内容导航"><p class="eyebrow">IN THIS PROJECT</p>{nav}</aside><div>{body}</div></div><a class="next-project" href="{nxt['slug']}.html"><span class="eyebrow">NEXT PROJECT</span><strong>{nxt['title']} <span aria-hidden="true">{arrow_icon()}</span></strong></a></div>'''
    (ROOT/(p['slug']+'.html')).write_text(shell(p['title'],p['intro'],content).replace('><', '>\n<'),encoding='utf-8')

if __name__=='__main__':
    build_home()
    for i,p in enumerate(PROJECTS):
        build_project(p,i)
    print('Built homepage and 6 project pages.')
