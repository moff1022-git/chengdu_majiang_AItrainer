# 四川成都麻将 · 图形资源使用说明

> 适用于 AI 编程辅助工具（Grok Build / Cursor / Copilot 等）快速理解并调用本项目全部图形资源。
> 资源总数：432 张 PNG · 全部使用 `@resvg/resvg-js` 渲染
> **本仓库本地运行根目录：`assets/`**（Pygame `AssetManager` 从此加载；文档中的 `/src/assets/`、`/public/assets/` 仅为设计侧路径别名）
> Web 服务访问路径示例：`/assets/`
> 字体风格：华文琥珀浮雕风格（多层描边 + 渐变填充 + 投影）
> 生成脚本：`scripts/generate-all-v3.mjs`（主资源）/ `scripts/gen-palette.mjs`（色板卡）

---

## 一、目录结构总览

```
assets/   # 本仓库实际目录（等同设计稿 /src/assets/）
├── tiles/
│   ├── wan/          万子牌面（一万～九万）× 2主题
│   ├── tong/         筒子牌面（一筒～九筒）× 2主题
│   ├── tiao/         条子牌面（一条～九条）× 2主题
│   └── backs/        牌背 + 占位透明框
├── buttons/          操作按钮（碰/杠/胡/过/确认/取消）× 2主题
├── backgrounds/      背景图（桌面/大厅/结算弹窗）× 2主题
├── players/          头像、座位标、庄家角标 × 2主题
├── dice/             骰子点数 1～6 × 2主题
├── icons/            UI 通用图标 × 2主题
├── effects/          特效横幅（胡/杠/碰/流局/金币）× 2主题
├── inference/        牌形推理 HUD 元素 × 2主题
├── strategy/         出牌策略 HUD 元素 × 2主题
├── palettes/         完整设计色板卡（翠玉青云 / 碧海朗月）
└── fonts/
    ├── numbers/      数字字形（0～9 + 负号）× 尺寸 × 色彩
    └── chars/        汉字字形 + 组合排版
```

---

## 二、主题命名规则

所有需要区分主题的文件，文件名末尾带 `_green` 或 `_blue` 后缀：

| 后缀 | 主题名 | 桌面主色 | 牌背主色 |
|------|--------|----------|----------|
| `_green` | 翠玉青云（传统绿色系） | `#1A3D2B` | `#2E7D4F` |
| `_blue`  | 碧海朗月（蓝色系）     | `#0D2744` | `#1565C0` |

**调用示例（React/TypeScript）：**
```ts
const theme = 'green'; // 或 'blue'
const tileBack = `/assets/tiles/backs/tile_back_${theme}.png`;
const huBtn    = `/assets/buttons/btn_hu_${theme}.png`;
```

---

## 三、麻将牌面

### 3.1 命名规则
```
/assets/tiles/{suit}/tile_{suit}_{n}_{theme}.png
```
- `{suit}`：`wan`（万）| `tong`（筒）| `tiao`（条）
- `{n}`：`1` ～ `9`
- `{theme}`：`green` | `blue`

### 3.2 尺寸
- **宽 × 高：270 × 378 px**（3× 高清，比例 1 : 1.4，标准麻将牌比例）
- 适配 4K 桌面端，按 display ratio 缩放使用（建议显示宽度 90–180 CSS px）

### 3.3 文件列表
```
tiles/wan/tile_wan_1_green.png  ...  tile_wan_9_blue.png   （18张）
tiles/tong/tile_tong_1_green.png  ...  tile_tong_9_blue.png  （18张）
tiles/tiao/tile_tiao_1_green.png  ...  tile_tiao_9_blue.png  （18张）
```

### 3.4 特殊说明
- **一条**（`tile_tiao_1`）：图案为传统麻雀鸟，非竹节排列
- 万字颜色：朱砂红 `#C62828`（两套主题统一）
- 筒子颜色：各圈颜色按牌号轮转（蓝/红/绿/紫）
- 条子颜色：竹节深绿 `#2E7D32`

### 3.5 调用示例
```ts
// 获取任意牌面路径
function getTilePath(suit: 'wan'|'tong'|'tiao', n: number, theme: string) {
  return `/assets/tiles/${suit}/tile_${suit}_${n}_${theme}.png`;
}

// 牌背（正面朝下时显示）
const backPath = `/assets/tiles/backs/tile_back_${theme}.png`;

// 占位透明框（手牌区空槽）
const placeholder = `/assets/tiles/backs/tile_placeholder.png`; // 主题无关
```

---

## 四、操作按钮

### 4.1 命名规则
```
/assets/buttons/btn_{key}_{theme}.png
```

### 4.2 按钮列表

| key | 中文 | 宽 × 高 | 触发条件 |
|-----|------|---------|----------|
| `hu` | 胡 | 480 × 192 px（3×） | 可和牌时显示，最高优先级 |
| `pong` | 碰 | 480 × 192 px（3×） | 其他玩家出牌可碰时 |
| `gang_ming` | 明杠 | 480 × 192 px（3×） | 碰后可明杠时 |
| `gang_an` | 暗杠 | 480 × 192 px（3×） | 手中有4张同牌时 |
| `gang_jia` | 补杠 | 480 × 192 px（3×） | 已碰的牌摸到第4张时 |
| `pass` | 过 | 480 × 192 px（3×） | 跳过当前操作 |
| `confirm` | 确认 | 480 × 192 px（3×） | 通用弹窗确认 |
| `cancel` | 取消 | 480 × 192 px（3×） | 通用弹窗取消 |

> **注意**：四川麻将无「吃」操作，无对应按钮资源。

### 4.3 调用示例
```ts
// 按钮组渲染
const ACTIONS = ['hu','pong','gang_ming','gang_an','gang_jia','pass'] as const;
type Action = typeof ACTIONS[number];

function getButtonPath(action: Action, theme: string) {
  return `/assets/buttons/btn_${action}_${theme}.png`;
}
```

---

## 五、背景图

| 文件名 | 尺寸 | 用途 |
|--------|------|------|
| `bg_table_{theme}.png` | 3840 × 2160 px（4K） | 游戏主桌面（含桌框和席面纹理） |
| `bg_lobby_{theme}.png` | 3840 × 2160 px（4K） | 主菜单 / 房间大厅背景 |
| `bg_result_{theme}.png` | 3840 × 2880 px（3×）| 局结算弹窗底图 |

---

## 六、玩家区域

### 6.1 头像
```
/assets/players/avatar_{n}_{theme}.png   （240 × 240 px（3×，圆形））
```
- `{n}`：1（东）| 2（南）| 3（西）| 4（北）
- 头像内含对应方位汉字

### 6.2 座位标识
```
/assets/players/seat_{dir}_{theme}.png   （64 × 64 px，圆角方形）
```
- `{dir}`：`east`（东）| `south`（南）| `west`（西）| `north`（北）

### 6.3 庄家角标
```
/assets/players/dealer_badge_{theme}.png  （36 × 36 px，五角星形）
```
叠加于庄家头像右上角。

### 6.4 调用示例
```ts
const DIRS = ['east','south','west','north'] as const;

// 根据玩家座位索引（0=东,1=南,2=西,3=北）获取资源
function getPlayerAssets(seatIndex: number, theme: string) {
  const dir = DIRS[seatIndex];
  return {
    avatar:  `/assets/players/avatar_${seatIndex + 1}_${theme}.png`,
    seat:    `/assets/players/seat_${dir}_${theme}.png`,
    dealer:  `/assets/players/dealer_badge_${theme}.png`,
  };
}
```

---

## 七、骰子

```
/assets/dice/dice_{n}_{theme}.png   （64 × 64 px，圆角正方形白底）
```
- `{n}`：`1` ～ `6`
- 一点为红色（`#EF5350`），其余点为黑色
- 用途：开局掷骰确定庄家/座位方向

---

## 八、UI 通用图标

| 文件名 | 尺寸 | 用途 |
|--------|------|------|
| `logo_{theme}.png` | 480 × 120 px | 游戏标题「成都麻将」金字 |
| `icon_settings_{theme}.png` | 64 × 64 px | 设置入口 |
| `icon_sound_on_{theme}.png` | 64 × 64 px | 音效开启状态 |
| `icon_sound_off_{theme}.png` | 64 × 64 px | 音效关闭状态 |
| `icon_exit_{theme}.png` | 64 × 64 px | 退出/返回 |
| `icon_score_{theme}.png` | 64 × 64 px | 分数/金币入口 |
| `icon_remain_{theme}.png` | 64 × 64 px | 剩余牌堆计数显示 |

---

## 九、特效横幅

```
/assets/effects/fx_{key}_{theme}.png   （400 × 130 px，透明底横幅）
```

| key | 中文 | 触发时机 |
|-----|------|----------|
| `hu` | 胡 | 有玩家和牌 |
| `gang` | 杠 | 有玩家杠牌 |
| `pong` | 碰 | 有玩家碰牌 |
| `liuju` | 流局 | 牌墙摸完无人胡牌 |
| `coin` | 金币 | 分数结算飞出动画 |

> 横幅设计为透明底，可直接居中叠加于桌面之上。

---

## 十、牌形推理 HUD（AI 辅助功能）

### 10.1 危险度标记
```
/assets/inference/danger_{level}_{theme}.png   （36 × 36 px，圆形角标）
```
叠加于手牌右上角，指示打出该牌的放炮风险：

| level | 颜色 | 含义 |
|-------|------|------|
| `critical` | 烈红 `#B71C1C` | 极高风险，对方极可能胡此牌 |
| `high` | 橙红 `#E64A19` | 高风险 |
| `medium` | 琥珀 `#F9A825` | 中等风险 |
| `low` | 暗绿/深蓝 | 较安全 |
| `safe` | 深绿/深蓝 | 已确认安全 |
| `unknown` | 灰色 | 无法判断 |

### 10.2 对手状态面板元素

| 文件名 | 尺寸 | 用途 |
|--------|------|------|
| `infer_panel_{theme}.png` | 280 × 200 px | 对手分析卡底图 |
| `tenpai_active_{theme}.png` | 40 × 40 px | 听牌警示灯·激活（金黄闪烁） |
| `tenpai_unknown_{theme}.png` | 40 × 40 px | 听牌警示灯·未知（灰暗） |
| `remain_bar_{theme}.png` | 240 × 24 px | 剩余牌分布热力条（绿→红渐变） |
| `discarded_bg_{theme}.png` | 320 × 180 px | 出牌记录区域底图 |
| `key_tile_frame_{theme}.png` | 270 × 378 px（3×）| 关键推理牌高亮描边框（叠加于牌面） |

### 10.3 调用示例
```ts
// 根据危险等级获取标记图
type DangerLevel = 'critical'|'high'|'medium'|'low'|'safe'|'unknown';

function getDangerMarker(level: DangerLevel, theme: string) {
  return `/assets/inference/danger_${level}_${theme}.png`;
}

// 叠加到牌面右上角（CSS 绝对定位）
// <img src={getTilePath(...)} />
// <img src={getDangerMarker(level, theme)} style={{position:'absolute', top:2, right:2}} />
```

---

## 十一、出牌策略 HUD（AI 胜率计算）

| 文件名 | 尺寸 | 用途 |
|--------|------|------|
| `strategy_panel_{theme}.png` | 400 × 120 px | 策略 HUD 整体底图，置于手牌上方 |
| `winrate_ring_{theme}.png` | 140 × 140 px | 环形胜率表盘（示例值 65%，运行时替换数字） |
| `mark_best_{theme}.png` | 32 × 32 px | 最优出牌角标（★），叠加于推荐弃牌左上角 |
| `mark_second_{theme}.png` | 32 × 32 px | 次优出牌角标（▲） |
| `mark_avoid_{theme}.png` | 32 × 32 px | 不建议出牌角标（✕），橙色警示 |
| `shanten_badge_{theme}.png` | 72 × 28 px | 向听数标签（示例「1向听」） |
| `draw_tile_glow_{theme}.png` | 270 × 378 px（3×）| 有效进张牌光晕框（叠加于可进张牌） |
| `deal_in_bar_{theme}.png` | 300 × 28 px | 放炮风险横向进度条（示例 35%） |
| `expectation_label_{theme}.png` | 80 × 24 px | 摸牌期望值标签（示例「期望 3.2」） |

> **注意**：`winrate_ring`、`shanten_badge`、`deal_in_bar`、`expectation_label` 中的数值为示例图，
> 实际游戏中建议用 Canvas 或 SVG 动态绘制数值，以这些 PNG 作为底图样式参考。

---

## 十二、字体资源

### 12.1 数字字形
```
/assets/fonts/numbers/digit_{char}_{color}_{size}.png
```

**参数说明：**

| 参数 | 取值 | 说明 |
|------|------|------|
| `{char}` | `0`~`9`，`minus` | `minus` 为负号「−」 |
| `{color}` | `gold` / `neg` / `neutral` / `accent_green` / `accent_blue` | 色彩变体 |
| `{size}` | `lg` / `md` / `sm` | 大/中/小三档尺寸 |

**尺寸规格：**

| size | 像素宽 × 高 | 使用场景 |
|------|------------|----------|
| `lg` | 54 × 76 px | 结算弹窗主分数 |
| `md` | 40 × 56 px | 各家实时分数显示 |
| `sm` | 28 × 40 px | 向听数 / 进张数标注 |

**色彩说明：**

| color | HEX | 使用场景 |
|-------|-----|----------|
| `gold` | `#FFD700` | 正分、得分 |
| `neg` | `#EF5350` | 负分、扣分 |
| `neutral` | `#A5C9A8` | 中性信息 |
| `accent_green` | `#4CAF78` | 绿色主题高亮值 |
| `accent_blue` | `#42A5F5` | 蓝色主题高亮值 |

**调用示例：**
```ts
// 拼接分数显示（如 -3200 分）
function getScoreDigits(score: number, theme: string, size: 'lg'|'md'|'sm') {
  const color = score >= 0 ? 'gold' : 'neg';
  const digits = Math.abs(score).toString().split('');
  const paths: string[] = [];
  if (score < 0) paths.push(`/assets/fonts/numbers/digit_minus_${color}_${size}.png`);
  digits.forEach(d => paths.push(`/assets/fonts/numbers/digit_${d}_${color}_${size}.png`));
  return paths;
}
```

### 12.2 汉字字形
```
/assets/fonts/chars/char_{key}_{size}_{theme}.png
```

**字符索引表：**

| key | 字 | 分类 | 大号尺寸 | 中号尺寸 |
|-----|----|------|----------|----------|
| `east` | 东 | 方位 | 64×64 | 40×40 |
| `south` | 南 | 方位 | 64×64 | 40×40 |
| `west` | 西 | 方位 | 64×64 | 40×40 |
| `north` | 北 | 方位 | 64×64 | 40×40 |
| `pong` | 碰 | 操作 | 64×64 | 40×40 |
| `gang` | 杠 | 操作 | 64×64 | 40×40 |
| `hu` | 胡 | 操作 | 64×64 | 40×40 |
| `pass` | 过 | 操作 | 64×64 | 40×40 |
| `ting` | 听 | 状态 | 64×64 | 40×40 |
| `rong` | 荣 | 状态 | 64×64 | 40×40 |
| `zi` | 自 | 状态 | 64×64 | 40×40 |
| `mo` | 摸 | 状态 | 64×64 | 40×40 |
| `fen` | 分 | 计分 | 64×64 | 40×40 |
| `fan` | 番 | 计分 | 64×64 | 40×40 |
| `ju` | 局 | 计分 | 64×64 | 40×40 |
| `zhuang` | 庄 | 计分 | 64×64 | 40×40 |
| `di` | 第 | 计分 | 64×64 | 40×40 |
| `liu` | 流 | 结果 | 64×64 | 40×40 |
| `ying` | 赢 | 结果 | 64×64 | 40×40 |
| `shu` | 输 | 结果 | 64×64 | 40×40 |
| `he` | 和 | 结果 | 64×64 | 40×40 |

### 12.3 组合排版
```
/assets/fonts/chars/combo_{key}_{theme}.png
```

| key | 内容示例 | 尺寸 | 用途 |
|-----|----------|------|------|
| `score` | 「3200分」 | 160 × 56 px | 结算分数组合 |
| `fan` | 「三番」 | 120 × 56 px | 番数组合 |
| `ju` | 「第8局」 | 160 × 56 px | 局数组合（「第」「局」用汉字字体，「8」用数字字体） |

---

## 十三、完整路径速查表（TypeScript 常量）

```ts
// assets-map.ts — 可直接复制到项目中使用

const THEME = 'green'; // 切换主题修改此处

export const ASSETS = {
  // 牌面
  tile: (suit: 'wan'|'tong'|'tiao', n: number) =>
    `/assets/tiles/${suit}/tile_${suit}_${n}_${THEME}.png`,
  tileBack: `/assets/tiles/backs/tile_back_${THEME}.png`,
  tilePlaceholder: `/assets/tiles/backs/tile_placeholder.png`,

  // 按钮
  btn: (key: 'hu'|'pong'|'gang_ming'|'gang_an'|'gang_jia'|'pass'|'confirm'|'cancel') =>
    `/assets/buttons/btn_${key}_${THEME}.png`,

  // 背景
  bg: {
    table:  `/assets/backgrounds/bg_table_${THEME}.png`,
    lobby:  `/assets/backgrounds/bg_lobby_${THEME}.png`,
    result: `/assets/backgrounds/bg_result_${THEME}.png`,
  },

  // 玩家
  player: (n: 1|2|3|4) => ({
    avatar: `/assets/players/avatar_${n}_${THEME}.png`,
    seat:   `/assets/players/seat_${(['east','south','west','north'])[n-1]}_${THEME}.png`,
    dealer: `/assets/players/dealer_badge_${THEME}.png`,
  }),

  // 骰子
  dice: (n: 1|2|3|4|5|6) => `/assets/dice/dice_${n}_${THEME}.png`,

  // 图标
  icon: {
    logo:     `/assets/icons/logo_${THEME}.png`,
    settings: `/assets/icons/icon_settings_${THEME}.png`,
    soundOn:  `/assets/icons/icon_sound_on_${THEME}.png`,
    soundOff: `/assets/icons/icon_sound_off_${THEME}.png`,
    exit:     `/assets/icons/icon_exit_${THEME}.png`,
    score:    `/assets/icons/icon_score_${THEME}.png`,
    remain:   `/assets/icons/icon_remain_${THEME}.png`,
  },

  // 特效
  fx: {
    hu:    `/assets/effects/fx_hu_${THEME}.png`,
    gang:  `/assets/effects/fx_gang_${THEME}.png`,
    pong:  `/assets/effects/fx_pong_${THEME}.png`,
    liuju: `/assets/effects/fx_liuju_${THEME}.png`,
    coin:  `/assets/effects/fx_coin_${THEME}.png`,
  },

  // 推理 HUD
  inference: {
    danger: (level: 'critical'|'high'|'medium'|'low'|'safe'|'unknown') =>
      `/assets/inference/danger_${level}_${THEME}.png`,
    panel:        `/assets/inference/infer_panel_${THEME}.png`,
    tenpaiOn:     `/assets/inference/tenpai_active_${THEME}.png`,
    tenpaiOff:    `/assets/inference/tenpai_unknown_${THEME}.png`,
    remainBar:    `/assets/inference/remain_bar_${THEME}.png`,
    discardedBg:  `/assets/inference/discarded_bg_${THEME}.png`,
    keyTileFrame: `/assets/inference/key_tile_frame_${THEME}.png`,
  },

  // 策略 HUD
  strategy: {
    panel:       `/assets/strategy/strategy_panel_${THEME}.png`,
    winrateRing: `/assets/strategy/winrate_ring_${THEME}.png`,
    markBest:    `/assets/strategy/mark_best_${THEME}.png`,
    markSecond:  `/assets/strategy/mark_second_${THEME}.png`,
    markAvoid:   `/assets/strategy/mark_avoid_${THEME}.png`,
    shanten:     `/assets/strategy/shanten_badge_${THEME}.png`,
    drawGlow:    `/assets/strategy/draw_tile_glow_${THEME}.png`,
    dealInBar:   `/assets/strategy/deal_in_bar_${THEME}.png`,
    expectation: `/assets/strategy/expectation_label_${THEME}.png`,
  },

  // 数字字形
  digit: (
    n: 0|1|2|3|4|5|6|7|8|9|'minus',
    color: 'gold'|'neg'|'neutral'|'accent_green'|'accent_blue',
    size: 'lg'|'md'|'sm'
  ) => `/assets/fonts/numbers/digit_${n}_${color}_${size}.png`,

  // 汉字字形
  char: (
    key: 'east'|'south'|'west'|'north'|'pong'|'gang'|'hu'|'pass'|
         'ting'|'rong'|'zi'|'mo'|'fen'|'fan'|'ju'|'zhuang'|'di'|
         'liu'|'ying'|'shu'|'he',
    size: 'lg'|'md',
  ) => `/assets/fonts/chars/char_${key}_${size}_${THEME}.png`,

  // 组合排版
  combo: (key: 'score'|'fan'|'ju') =>
    `/assets/fonts/chars/combo_${key}_${THEME}.png`,
};
```

---

## 十四、重新生成资源

若需修改设计后重新生成全部 PNG：

```bash
node scripts/generate-assets.mjs
```

生成脚本位于 `scripts/generate-assets.mjs`，所有 SVG 模板内联定义，修改对应函数后重跑即可覆盖输出。

---

## 十五、注意事项

1. **CJK 字体**：本环境无系统 CJK 字体，万字/汉字 PNG 文字区透明。在有 Noto CJK 字体的环境（Docker / macOS）重跑脚本可得完整文字渲染。
2. **叠加层资源**：危险标记、关键牌高亮框、进张光晕框、操作横幅均为透明底 PNG，设计为绝对定位叠加于牌面之上，不含背景色。
3. **HUD 数值图**：胜率环、向听数标签、放炮风险条、期望值标签中的数值为示例静态图。生产环境建议以这些 PNG 为视觉参考，用 Canvas/SVG 动态渲染实际计算值。
4. **主题切换**：仅需改变路径中 `_green` / `_blue` 后缀即可完整切换主题，无需修改任何游戏逻辑。

---

## 十六、设计色板卡

### 16.1 说明

两张完整设计色板 PNG，供设计师和开发者参考全部设计 Token。每张 1440×960 px，38色，含：牌面色 / 牌背色 / 桌面色 / 文字色 / 功能色 / 按钮色 / 危险色 / 特效色，共 8 大类别。

生成脚本：`scripts/gen-palette.mjs`

### 16.2 文件列表

| 文件路径 | 尺寸 | 色彩数 | 说明 |
|---------|------|--------|------|
| `/assets/palettes/palette_green.png` | 1440×960 | 38色 | 翠玉青云 · 传统绿色系 |
| `/assets/palettes/palette_blue.png`  | 1440×960 | 38色 | 碧海朗月 · 蓝色系 |

### 16.3 色板分类

| 类别 | 色数 | 内容 |
|------|------|------|
| 牌面 | 5   | 牌面光高、底色、暗影、边框、侧边厚度 |
| 牌背 | 4   | 背面主色、暗色、图案、边框 |
| 桌面 | 5   | 毯面主色、暗色、外框、面板主色、面板边框 |
| 文字 | 4   | 主/副文字色、主题强调色、亮色 |
| 功能 | 5   | 得分金色、金色暗调、正值、负值、中性色 |
| 按钮 | 4   | 胡/碰/杠/过四个操作按钮色 |
| 危险 | 6   | 极高/高/中/低危险、安全牌、未知牌 |
| 特效 | 5   | 胜率高/中/低、特效光晕、杠特效、听牌警示 |

### 16.4 调用示例

```ts
// 色板图片（仅用于展示参考，不用于运行时）
const paletteGreen = `${import.meta.env.BASE_URL}assets/palettes/palette_green.png`;
const paletteBlue  = `${import.meta.env.BASE_URL}assets/palettes/palette_blue.png`;
```
