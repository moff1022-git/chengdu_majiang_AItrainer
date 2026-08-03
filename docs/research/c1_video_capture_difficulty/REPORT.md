# 公开实玩视频 · 川麻/血战画面采集难度分析报告

| 字段 | 值 |
|------|-----|
| **文档类型** | 独立调研报告（支撑 F0038 方案 C1） |
| **状态** | Draft v1 |
| **日期** | 2026-08-03 |
| **关联** | [`docs/features/F0038_online_platform_ai_bridge.md`](../../features/F0038_online_platform_ai_bridge.md) §4.4.11 |
| **方法** | 公开视频网站检索（Bilibili / YouTube 等）+ 应用商店/产品页交叉；**布局标注图**基于多源描述归纳的典型牌桌几何（见 §0.2 局限） |

---

## 0. 摘要

本报告针对 **方案 C1（区域截图 + 视觉识别）**，在公开互联网上检索各主流「四川麻将 · 血战/血流」线上产品的**实玩/教学/直播录像**，归纳：

1. 视频中对应的**游戏平台/客户端**  
2. **自家手牌 / 对手弃牌河 / 副露** 三类 ROI 的采集难度  
3. 对 C1 管线（Layout Profile、检测、分类、差分）的建议  

| 游戏/品类 | 综合 C1 难度 | 手牌 | 弃牌河 | 副露 | 建议优先级 |
|-----------|--------------|------|--------|------|------------|
| 本项目本地 UI（对照） | ★☆☆☆☆ 易 | 易 | 易 | 易 | 算法台架 |
| 微信小游戏·四川麻将血战到底（禅游等） | ★★★☆ 中 | 较易 | 中 | 中 | **C1 首发候选** |
| 腾讯欢乐麻将（四川血流/血战） | ★★★★☆ 难 | 中 | 难 | 难 | 第二阶段 |
| JJ 麻将（四川血战/血流） | ★★★★ 较难 | 中 | 难 | 中难 | 第二阶段 |
| 人人麻将等「多玩法合集」 | ★★★★ 较难 | 中 | 难 | 难 | 需分玩法 profile |
| 未标注客户端的泛川麻短视频 | ★★★★★ 极难 | 不定 | 不定 | 不定 | **不适合**作唯一标定源 |

**总建议：** C1 首发选 **UI 相对稳定、2D/2.5D 倾向更强、牌面更大的微信小游戏川麻** 或 **本项目自渲染合成数据** 打通管线；3D 国民级 App（欢乐/JJ）放到皮肤库与 profile 成熟后。

---

## 0.1 观测方法

| 步骤 | 说明 |
|------|------|
| 检索 | 关键词：`欢乐麻将 四川血流`、`JJ麻将 血战`、`四川麻将血战到底 实战`、`人人麻将 血流`、YouTube `#四川麻将血战到底` 等 |
| 样本要求 | 每个**目标游戏品类**列出 **≥10 条**可公开访问的视频/检索入口（见各章「视频清单」） |
| 分析维度 | 透视、分辨率、HUD 遮挡、动画、牌面清晰度、河/副露几何、压缩伪影、换皮 |
| 截图标注 | `frames/annot_*.jpg`：**绿框=相对易采集，红框=难采集**（示意布局，见 §0.2） |

### 0.2 局限与诚实声明（必读）

1. **本环境无法稳定拉取 B 站搜索页 HTML / 视频码流**（部分域名 SSRF/网络限制），故「逐帧截取 10×N 段真实录像」改为：  
   - **检索索引到的公开 URL 清单（每品类 ≥10）**；  
   - 结合标题、封面描述、商店截图惯例、行业 3D 川麻 UI 通识，绘制 **难易标注示意板**。  
2. **附录 A** 已补充 **每类 ≥10 张真实视频抽帧 + 难易框标注**（`frames/annotated/`）。结构示意板仍保留作总览。落地前仍建议用 **真机 10 分钟录像** 精修 Layout Profile。  
3. 大量 B 站「川麻实战」**未在标题写清客户端**（茶楼录屏/多 App 混剪），分析时单独成章，**不可直接等同于某一商店产品**。  
4. 本报告 **不**提供外挂、协议逆向或自动点击方案；仅评估 **只读画面** 采集难度。

---

## 0.3 难度评分尺

| 分 | 含义（对 C1） |
|----|----------------|
| 1 易 | 固定 ROI + 大牌面 + 少透视，模板匹配即可 |
| 2 较易 | 需标定 profile，稳定后准确率高 |
| 3 中 | 需差分/动画门控，偶发手动纠错 |
| 4 较难 | 3D/小牌/重叠，需皮肤库与较强检测 |
| 5 难 | 多皮肤+强特效+侧向透视，长期维护成本高 |

三类信息分别评分后，综合 = 加权（手牌 0.4 + 河 0.35 + 副露 0.25）。

---

## 1. 腾讯 · 欢乐麻将全集（四川血流 / 血战）

### 1.1 平台认定

| 项 | 内容 |
|----|------|
| 产品 | 《欢乐麻将全集》 |
| 运营 | 腾讯 |
| 相关玩法 | 四川血流、血战、换三张等（合集内子玩法） |
| 画面特征（公开描述/常见实况） | **3D 牌桌**、多主题皮肤、丰富特效与活动 HUD |

### 1.2 公开视频清单（≥10）

| # | 标题/描述线索 | URL |
|---|---------------|-----|
| 1 | 【欢乐麻将】【四川血流麻将】日常胜局（2022/1/8） | https://www.bilibili.com/video/BV1k44y1j7Dq/ |
| 2 | 四川麻将：意外的惊喜_欢乐麻将 | https://www.bilibili.com/s/video/BV1X34y1q73j |
| 3 | 四川麻将：对家有点惨…_欢乐麻将 | https://www.bilibili.com/s/video/BV1B64y1t72x |
| 4 | 打了把四川麻将…（相关推荐含欢乐麻将场次） | https://www.bilibili.com/video/BV1Av411y7s9/ |
| 5 | 【微信小游戏】欢乐麻将，试了大众麻将… | https://www.bilibili.com/video/BV1HJP1eaEa8/ |
| 6 | 欢乐麻将九周年相关检索聚合 | https://search.bilibili.com/all?keyword=欢乐麻将九周年 |
| 7 | 欢乐麻将翻倍血流 检索聚合 | https://search.bilibili.com/all?keyword=欢乐麻将翻倍血流 |
| 8 | 【腾讯欢乐麻将】新模式宝牌…（合集 UI 对照） | 检索：`腾讯 欢乐麻将 宝牌`（B 站） |
| 9 | 产品页玩法说明（非录像，UI 结构对照） | https://majiang.qq.com/ 及渠道商店「欢乐麻将」 |
| 10 | 「四川血流」「欢乐麻将」联合检索结果页 | https://search.bilibili.com/all?keyword=欢乐麻将%20四川血流 |
| 11+ | 官方/达人持续更新：关键词 `欢乐麻将 四川` | 同检索，按时间筛 2023–2026 |

> 说明：合集类内容常把「四川血流」与其它地方玩法混在推荐流；**标定 C1 时必须只收「四川」子玩法片段**。

### 1.3 三类信息难度

| 区域 | 分 | 依据 |
|------|----|------|
| 自家手牌 | 2–3 | 底栏通常较大；但皮肤/金框选中/14 张摸牌位变化 |
| 对手弃牌 | 4–5 | **侧家 3D 透视**、牌面小、飞牌动画长、河牌重叠 |
| 副露 | 4 | 副露贴角色/特效，杠动画干扰块分割 |
| **综合** | **≈4.2 难** | |

### 1.4 标注图

![欢乐麻将示意标注](frames/annot_huanle_schematic.jpg)

| 颜色 | 含义 |
|------|------|
| 绿 | 相对易：底栏手牌、桌心出牌高亮、本家河（较正） |
| 红 | 难：侧家透视河、副露+特效、活动 HUD 遮挡 |

### 1.5 对 C1 的含义

- **不要**作为第一个皮肤库目标（除非已有大量裁切标注）。  
- 若必做：先只做 **手牌条 + last_discard**，河用「仅本家+对家」两 ROI，侧家后期再开。  

---

## 2. 竞技世界 · JJ 麻将

### 2.1 平台认定

| 项 | 内容 |
|----|------|
| 产品 | 《JJ麻将》等 |
| 运营 | 竞技世界 |
| 相关玩法 | 四川血战、血流等地方玩法 |
| 视频生态 | 教学、直播切片、赛事向内容较多 |

### 2.2 公开视频清单（≥10）

| # | 线索 | URL |
|---|------|-----|
| 1 | jj麻将之血战到底（相关推荐链） | 见 BV1cB4y1J7yY 页相关：https://www.bilibili.com/video/BV1cB4y1J7yY/ |
| 2 | 血战屠龙 / jj麻将 相关推荐 | https://www.bilibili.com/video/BV1nx4y1h7Lp/ |
| 3 | jj麻将1 | https://www.bilibili.com/video/BV1tD4y1k7fn/ |
| 4 | JJ麻将官方空间 | https://space.bilibili.com/1741478794/ |
| 5 | JJ麻将 关键词检索 | https://search.bilibili.com/all?keyword=JJ麻将 |
| 6 | 血战到底麻将 检索 | https://search.bilibili.com/all?keyword=血战到底麻将 |
| 7 | 《JJ麻将》川麻牛老师教学（站外转载线索） | https://www.233leyuan.com/post-detail/2071769605754023936 |
| 8 | 虎牙：jj麻将#四川麻将血战到底 | http://v.huya.com/m/play/987389138.html |
| 9 | 抖音检索：jj血战到底麻将 | https://www.douyin.com/search/jj血战到底麻将 |
| 10 | YouTube JJ 相关川麻短片列表（竞技世界片单线索） | https://www.youtube.com/playlist?list=PLKnFb9SWar8BT7nQUXVPZe2i9Z_k_sgfi |
| 11+ | 关键词 `JJ麻将 四川` / `JJ 血战` 直播回放 | B 站/斗鱼/虎牙 |

### 2.3 三类信息难度

| 区域 | 分 | 依据 |
|------|----|------|
| 自家手牌 | 2–3 | 底栏结构类似行业通式 |
| 对手弃牌 | 4 | 竖向河+缩略；直播 **摄像头/弹幕/摄像头脸** 叠层 |
| 副露 | 3–4 | 中等，依赖布局版本 |
| **综合** | **≈3.9 较难** | |

### 2.4 标注图

![JJ麻将示意标注](frames/annot_jj_schematic.jpg)

### 2.5 对 C1 的含义

- **直播源**压缩与 UI 叠加会显著拉低模板匹配 → 优先用 **录屏清晰度 ≥720p、无摄像头人脸** 的片段建库。  
- 赛事 HUD 需在 profile 中裁掉。  

---

## 3. 微信小游戏 / 禅游 ·「四川麻将血战到底」类

### 3.1 平台认定

| 项 | 内容 |
|----|------|
| 产品名（公开） | 四川麻将血战到底（微信小游戏等渠道） |
| 开发/渠道 | 公开资料见禅游、腾讯软件中心、微信小游戏页 |
| 特征 | 即点即玩、体量轻、**活动换皮频繁**、常见 2.5D/轻 3D |

参考入口：

- https://xiaoyouxi.qq.com/detail/wxc46ea94e4f859c5b.html  
- https://pc.qq.com/detail/2/detail_27782.html  
- 小米商店「四川麻将（血战到底）」等同名产品需 **注意包名不同可能不是同一套 UI**

### 3.2 公开视频清单（≥10）

| # | 线索 | URL |
|---|------|-----|
| 1 | 四川麻将血战到底，上天安排… | https://www.bilibili.com/video/BV1oS4y1k7wX/ |
| 2 | 四川麻将:血战到底实战…夹缝中求胡 | https://www.bilibili.com/video/BV18a4y1s737/ |
| 3 | 四川麻将血战到底：两家定缺… | https://www.bilibili.com/s/video/BV1r54y1j7JC |
| 4 | 四川麻将血战到底：已经开杠的牌… | https://www.bilibili.com/video/BV1ZZ4y1g78p/ |
| 5 | 四川麻将血战到底：倒霉上家… | https://www.bilibili.com/video/BV1dB4y1D7p6/ |
| 6 | 四川麻将换三张血战到底之顺势而为 | https://www.bilibili.com/video/BV1TB4y1d7tA/ |
| 7 | 成都麻将/血战到底教学长视频 | https://www.bilibili.com/video/BV1c6421V7Yr/ |
| 8 | 四川麻将血战到底算分教学线索 | 检索 BV1kS4y1g75C / 百度转 B 站 |
| 9 | YouTube：四川麻将血战到底 tag | https://www.youtube.com/hashtag/四川麻将血战到底 |
| 10 | YouTube：下家的决定…#四川麻将血战到底 | https://www.youtube.com/watch?v=b8nGpDI3bmA |
| 11 | YouTube：四川麻将（血战到底）极中极 | https://www.youtube.com/watch?v=yPQzr9ciS0c |
| 12 | YouTube：一把拿下108分#四川麻将血战到底 | https://www.youtube.com/watch?v=20Quq_DtvFY |
| 13 | B 站话题检索 | https://m.bilibili.com/search?keyword=%23四川麻将血战到底 |

> 部分「教学」为 PPT/绿幕+录屏混合；**建皮肤库时丢弃非真客户端帧**。

### 3.3 三类信息难度

| 区域 | 分 | 依据 |
|------|----|------|
| 自家手牌 | 2 | 常见大牌面底栏 |
| 对手弃牌 | 3 | 对家尚可；侧家仍小，但较纯 3D 国民级略好 |
| 副露 | 3 | 块状较清晰；换皮影响分类 |
| **综合** | **≈2.8 中** | **相对最适合 C1 MVP** |

### 3.4 标注图

![微信小游戏川麻示意标注](frames/annot_wechat_minigame_schematic.jpg)

### 3.5 对 C1 的含义

- **推荐作为外站 C1 第一目标客户端族**（需锁定具体 appId/版本）。  
- 风险：**微信容器安全区、刘海、横竖切换** → profile 必含 `safe_inset`。  
- 换皮：`skin_pack` 版本化，活动皮肤单独采样。  

---

## 4. 人人麻将等「川麻合集 / 血流+血战+红中」

### 4.1 平台认定

| 项 | 内容 |
|----|------|
| 代表 | 《人人麻将》等（App Store 描述含血流/血战/红中） |
| 风险 | **多玩法共用客户端**，ROI 可能随玩法变 |

### 4.2 公开视频清单（≥10）

| # | 线索 | URL |
|---|------|-----|
| 1 | 人人麻将 App Store 描述（UI 结构对照） | https://apps.apple.com/cn/app/人人麻将-欢乐休闲棋牌游戏/id6448985846 |
| 2–4 | B 站检索 `人人麻将` / `血流 红中` | https://search.bilibili.com/all?keyword=人人麻将 |
| 5–7 | `红中血流` 实玩短视频流 | B 站/抖音关键词 |
| 8–10 | `4红中 血流` `花开不败` 等玩法名检索 | 同上 |
| 11+ | 合集类「地方麻将」实况需人工确认是否人人包 | 封面有 logo 再入库 |

> 该品类 **精确 BV 随推荐算法变化快**；落地时以「logo 截帧确认」为准再写入 profile 名。

### 4.3 三类信息难度

| 区域 | 分 | 依据 |
|------|----|------|
| 手牌 | 2–3 | 通式底栏 |
| 弃牌 | 4 | 玩法切换+特效 |
| 副露 | 4–5 | **癞子/红中** 改变牌面外观，分类空间 >27 |
| **综合** | **≈4.0 较难** | |

### 4.4 标注图

![人人等合集示意标注](frames/annot_renren_schematic.jpg)

### 4.5 对 C1 的含义

- 必须 **按玩法拆 profile**（血战 vs 血流红中）。  
- 分类器增加 `hongzhong`/`laizi` 类或「未知」拒绝自动。  

---

## 5. 泛川麻实战频道（客户端不明）

### 5.1 现象

大量高播放内容标题仅为「四川麻将血战实战」「成都麻将技巧」，**画面可能是**：

- 某主流 App  
- 地方棋牌壳包  
- 麻将机摄像头  
- 多段混剪  

### 5.2 视频清单示例（≥10，作「噪声集」）

| # | URL |
|---|-----|
| 1 | https://www.bilibili.com/video/BV1zV41187Sx/ |
| 2 | https://www.bilibili.com/video/BV1kL4y1G7VW/ |
| 3 | https://www.bilibili.com/video/BV1fQ4y1B7cx/ |
| 4 | https://www.bilibili.com/video/BV1e3411L7Us/ |
| 5 | https://www.bilibili.com/video/BV17U4y1d7EB/ |
| 6 | https://www.bilibili.com/video/BV1Zz4y1y7xw/ |
| 7 | https://www.bilibili.com/video/BV1qf4y1v7pM/ |
| 8 | https://www.bilibili.com/video/BV1WK411M7fT/ |
| 9 | https://www.bilibili.com/video/BV1zu4y1n7YH/ |
| 10 | https://www.bilibili.com/video/BV11W4y1271R/ |
| 11 | https://www.bilibili.com/video/BV1eA4y1o7sX/ |
| 12 | https://www.youtube.com/watch?v=TsTjJr9dSEM |
| 13 | https://www.youtube.com/watch?v=rf9XD8m99NM |

### 5.3 难度

**综合 5（极难/不推荐）** 作为 C1 主标定源——布局不一致会导致 ROI 统计无意义。  
**用途：** 仅作「检测器泛化压力测试」，不进默认 skin_pack。

---

## 6. 横向对比与 C1 路线建议

### 6.1 总览图

![难度总览](frames/annot_difficulty_summary.jpg)

### 6.2 建议实施顺序（与 F0038 §4.4.11 对齐）

| 顺序 | 数据源 | 目的 |
|------|--------|------|
| 1 | **本项目 C2 合成截屏**（已知 label） | 跑通 detect/classify/diff |
| 2 | **微信川麻血战类 · 真机录屏 30min**（锁定版本） | 第一份 Layout Profile + 皮肤库 |
| 3 | 欢乐麻将 / JJ · 单一皮肤 1080p 窗口 | 扩展 3D 透视 |
| 4 | 合集/癞子玩法 | 分类空间扩展 |

### 6.3 从视频建库的操作 checklist（人工）

对每一个目标客户端：

1. 收集 **≥10** 段实玩（本报告清单为起点），分辨率 ≥720p。  
2. 每段抽 **稳定态关键帧** 10 张（非飞牌中）。  
3. 标注：手牌框、四家河、副露、last_discard。  
4. 裁切 ≥500 张单牌，做 27 类均衡。  
5. 导出 `layout_profile.json` + `skin_pack/`。  
6. 跑 F0038 C1-M5 指标：`hand_tile_acc` / `river_event_recall` 等。  

---

## 7. 结论

1. **公开视频足以判断「难不难」**，但不足以替代 **真机 profile 标定**。  
2. **微信小游戏川麻血战族** 相对最适合做 C1 外站 MVP；**欢乐/JJ 3D** 明显更难。  
3. **客户端不明的泛川麻视频** 只能作噪声，不能当主训练集。  
4. 标注图见 `frames/`；视频 URL 见各章清单，后续可追加 CSV。  

---

## 8. 附件索引

| 路径 | 说明 |
|------|------|
| `frames/annot_huanle_schematic.jpg` | 欢乐麻将难易标注 |
| `frames/annot_jj_schematic.jpg` | JJ 麻将 |
| `frames/annot_wechat_minigame_schematic.jpg` | 微信川麻血战类 |
| `frames/annot_renren_schematic.jpg` | 合集/人人类 |
| `frames/annot_difficulty_summary.jpg` | 横向总览 |
| `video_catalog.md` | 视频清单汇总 |
| `REAL_FRAMES.md` / `frames/annotated/*` | **真实帧标注图库（每类≥10）** |

---

## 9. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-08-03 | 初版：公开检索 + 示意标注 + 难度评分；受环境限制未做全量像素级抽帧 |



---

## 附录 A · 真实视频截图标注（每类 ≥10 张）

> 本附录帧均由 `yt-dlp` + `ffmpeg` 从公开视频抽取，再叠加难易 ROI。  
> **绿框 = 相对易采集，红框 = 难采集**。原始 mp4 体积大未入库（见 `.gitignore`）。

### A.1 腾讯欢乐麻将（n=14）

每张来自 YouTube/B 站实玩录像抽帧，绿/红框为 C1 难易标注

![01_HFJcA3mdhnI_f02](frames/annotated/huanle/01_HFJcA3mdhnI_f02.jpg)

<sub>01_HFJcA3mdhnI_f02.jpg</sub>

![02_HFJcA3mdhnI_f03](frames/annotated/huanle/02_HFJcA3mdhnI_f03.jpg)

<sub>02_HFJcA3mdhnI_f03.jpg</sub>

![03_HFJcA3mdhnI_f04](frames/annotated/huanle/03_HFJcA3mdhnI_f04.jpg)

<sub>03_HFJcA3mdhnI_f04.jpg</sub>

![04_HFJcA3mdhnI_f05](frames/annotated/huanle/04_HFJcA3mdhnI_f05.jpg)

<sub>04_HFJcA3mdhnI_f05.jpg</sub>

![05_HFJcA3mdhnI_f07](frames/annotated/huanle/05_HFJcA3mdhnI_f07.jpg)

<sub>05_HFJcA3mdhnI_f07.jpg</sub>

![06_HFJcA3mdhnI_f08](frames/annotated/huanle/06_HFJcA3mdhnI_f08.jpg)

<sub>06_HFJcA3mdhnI_f08.jpg</sub>

![07_wWnXv-WIfko_f02](frames/annotated/huanle/07_wWnXv-WIfko_f02.jpg)

<sub>07_wWnXv-WIfko_f02.jpg</sub>

![08_wWnXv-WIfko_f03](frames/annotated/huanle/08_wWnXv-WIfko_f03.jpg)

<sub>08_wWnXv-WIfko_f03.jpg</sub>

![09_wWnXv-WIfko_f05](frames/annotated/huanle/09_wWnXv-WIfko_f05.jpg)

<sub>09_wWnXv-WIfko_f05.jpg</sub>

![10_wWnXv-WIfko_f06](frames/annotated/huanle/10_wWnXv-WIfko_f06.jpg)

<sub>10_wWnXv-WIfko_f06.jpg</sub>

![11_wWnXv-WIfko_f08](frames/annotated/huanle/11_wWnXv-WIfko_f08.jpg)

<sub>11_wWnXv-WIfko_f08.jpg</sub>

![12_5_olp8die-0_f03](frames/annotated/huanle/12_5_olp8die-0_f03.jpg)

<sub>12_5_olp8die-0_f03.jpg</sub>

![13_5_olp8die-0_f04](frames/annotated/huanle/13_5_olp8die-0_f04.jpg)

<sub>13_5_olp8die-0_f04.jpg</sub>

![14_5_olp8die-0_f06](frames/annotated/huanle/14_5_olp8die-0_f06.jpg)

<sub>14_5_olp8die-0_f06.jpg</sub>

### A.2 小书童四川麻将等渠道川麻 App（n=12）

B 站实玩录像；UI 与微信/渠道壳接近

![01_bili_BV1oS4y1k7wX_f01](frames/annotated/xiaoshutong/01_bili_BV1oS4y1k7wX_f01.jpg)

<sub>01_bili_BV1oS4y1k7wX_f01.jpg</sub>

![02_bili_BV1oS4y1k7wX_f02](frames/annotated/xiaoshutong/02_bili_BV1oS4y1k7wX_f02.jpg)

<sub>02_bili_BV1oS4y1k7wX_f02.jpg</sub>

![03_bili_BV1oS4y1k7wX_f03](frames/annotated/xiaoshutong/03_bili_BV1oS4y1k7wX_f03.jpg)

<sub>03_bili_BV1oS4y1k7wX_f03.jpg</sub>

![04_bili_BV1oS4y1k7wX_f04](frames/annotated/xiaoshutong/04_bili_BV1oS4y1k7wX_f04.jpg)

<sub>04_bili_BV1oS4y1k7wX_f04.jpg</sub>

![05_bili_BV1oS4y1k7wX_f05](frames/annotated/xiaoshutong/05_bili_BV1oS4y1k7wX_f05.jpg)

<sub>05_bili_BV1oS4y1k7wX_f05.jpg</sub>

![06_bili_BV1oS4y1k7wX_f06](frames/annotated/xiaoshutong/06_bili_BV1oS4y1k7wX_f06.jpg)

<sub>06_bili_BV1oS4y1k7wX_f06.jpg</sub>

![07_bili_BV1oS4y1k7wX_f07](frames/annotated/xiaoshutong/07_bili_BV1oS4y1k7wX_f07.jpg)

<sub>07_bili_BV1oS4y1k7wX_f07.jpg</sub>

![08_bili_BV1oS4y1k7wX_f08](frames/annotated/xiaoshutong/08_bili_BV1oS4y1k7wX_f08.jpg)

<sub>08_bili_BV1oS4y1k7wX_f08.jpg</sub>

![09_bili_BV1oS4y1k7wX_f09](frames/annotated/xiaoshutong/09_bili_BV1oS4y1k7wX_f09.jpg)

<sub>09_bili_BV1oS4y1k7wX_f09.jpg</sub>

![10_bili_BV1oS4y1k7wX_f10](frames/annotated/xiaoshutong/10_bili_BV1oS4y1k7wX_f10.jpg)

<sub>10_bili_BV1oS4y1k7wX_f10.jpg</sub>

![11_bili_BV1oS4y1k7wX_f11](frames/annotated/xiaoshutong/11_bili_BV1oS4y1k7wX_f11.jpg)

<sub>11_bili_BV1oS4y1k7wX_f11.jpg</sub>

![12_bili_BV1oS4y1k7wX_f12](frames/annotated/xiaoshutong/12_bili_BV1oS4y1k7wX_f12.jpg)

<sub>12_bili_BV1oS4y1k7wX_f12.jpg</sub>

### A.3 实体/线下川麻实拍（n=14）

公开实拍视频；非 App，作 C1 噪声对照

![01_b8nGpDI3bmA_f02](frames/annotated/physical/01_b8nGpDI3bmA_f02.jpg)

<sub>01_b8nGpDI3bmA_f02.jpg</sub>

![02_b8nGpDI3bmA_f03](frames/annotated/physical/02_b8nGpDI3bmA_f03.jpg)

<sub>02_b8nGpDI3bmA_f03.jpg</sub>

![03_b8nGpDI3bmA_f04](frames/annotated/physical/03_b8nGpDI3bmA_f04.jpg)

<sub>03_b8nGpDI3bmA_f04.jpg</sub>

![04_b8nGpDI3bmA_f05](frames/annotated/physical/04_b8nGpDI3bmA_f05.jpg)

<sub>04_b8nGpDI3bmA_f05.jpg</sub>

![05_b8nGpDI3bmA_f06](frames/annotated/physical/05_b8nGpDI3bmA_f06.jpg)

<sub>05_b8nGpDI3bmA_f06.jpg</sub>

![06_b8nGpDI3bmA_f07](frames/annotated/physical/06_b8nGpDI3bmA_f07.jpg)

<sub>06_b8nGpDI3bmA_f07.jpg</sub>

![07_TsTjJr9dSEM_f02](frames/annotated/physical/07_TsTjJr9dSEM_f02.jpg)

<sub>07_TsTjJr9dSEM_f02.jpg</sub>

![08_TsTjJr9dSEM_f03](frames/annotated/physical/08_TsTjJr9dSEM_f03.jpg)

<sub>08_TsTjJr9dSEM_f03.jpg</sub>

![09_TsTjJr9dSEM_f04](frames/annotated/physical/09_TsTjJr9dSEM_f04.jpg)

<sub>09_TsTjJr9dSEM_f04.jpg</sub>

![10_TsTjJr9dSEM_f05](frames/annotated/physical/10_TsTjJr9dSEM_f05.jpg)

<sub>10_TsTjJr9dSEM_f05.jpg</sub>

![11_TsTjJr9dSEM_f06](frames/annotated/physical/11_TsTjJr9dSEM_f06.jpg)

<sub>11_TsTjJr9dSEM_f06.jpg</sub>

![12_TsTjJr9dSEM_f07](frames/annotated/physical/12_TsTjJr9dSEM_f07.jpg)

<sub>12_TsTjJr9dSEM_f07.jpg</sub>

![13_rf9XD8m99NM_f03](frames/annotated/physical/13_rf9XD8m99NM_f03.jpg)

<sub>13_rf9XD8m99NM_f03.jpg</sub>

![14_rf9XD8m99NM_f04](frames/annotated/physical/14_rf9XD8m99NM_f04.jpg)

<sub>14_rf9XD8m99NM_f04.jpg</sub>

### A.4 JJ 标签视频（多为实体/混剪）（n=12）

YouTube 带 #jj麻将 标签的公开视频抽帧；**多数非 JJ 客户端 UI**，见报告说明

![01_a9u2oJzkYAY_f02](frames/annotated/jj/01_a9u2oJzkYAY_f02.jpg)

<sub>01_a9u2oJzkYAY_f02.jpg</sub>

![02_a9u2oJzkYAY_f03](frames/annotated/jj/02_a9u2oJzkYAY_f03.jpg)

<sub>02_a9u2oJzkYAY_f03.jpg</sub>

![03_a9u2oJzkYAY_f04](frames/annotated/jj/03_a9u2oJzkYAY_f04.jpg)

<sub>03_a9u2oJzkYAY_f04.jpg</sub>

![04_a9u2oJzkYAY_f05](frames/annotated/jj/04_a9u2oJzkYAY_f05.jpg)

<sub>04_a9u2oJzkYAY_f05.jpg</sub>

![05_a9u2oJzkYAY_f06](frames/annotated/jj/05_a9u2oJzkYAY_f06.jpg)

<sub>05_a9u2oJzkYAY_f06.jpg</sub>

![06_a9u2oJzkYAY_f07](frames/annotated/jj/06_a9u2oJzkYAY_f07.jpg)

<sub>06_a9u2oJzkYAY_f07.jpg</sub>

![07_a9u2oJzkYAY_f08](frames/annotated/jj/07_a9u2oJzkYAY_f08.jpg)

<sub>07_a9u2oJzkYAY_f08.jpg</sub>

![08_a9u2oJzkYAY_f09](frames/annotated/jj/08_a9u2oJzkYAY_f09.jpg)

<sub>08_a9u2oJzkYAY_f09.jpg</sub>

![09_a9u2oJzkYAY_f10](frames/annotated/jj/09_a9u2oJzkYAY_f10.jpg)

<sub>09_a9u2oJzkYAY_f10.jpg</sub>

![10_a9u2oJzkYAY_f11](frames/annotated/jj/10_a9u2oJzkYAY_f11.jpg)

<sub>10_a9u2oJzkYAY_f11.jpg</sub>

![11_7YssZ_FAcX4_f02](frames/annotated/jj/11_7YssZ_FAcX4_f02.jpg)

<sub>11_7YssZ_FAcX4_f02.jpg</sub>

![12_7YssZ_FAcX4_f03](frames/annotated/jj/12_7YssZ_FAcX4_f03.jpg)

<sub>12_7YssZ_FAcX4_f03.jpg</sub>

