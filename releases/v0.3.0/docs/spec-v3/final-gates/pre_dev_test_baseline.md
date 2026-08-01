# PRE-DEV-FINAL-GATE-001 — 当前测试基线

- Python：3.12.10
- 标准命令：`.venv\Scripts\python.exe -m pytest -q`（pytest.ini的testpaths=tests）
- 当前全仓：437 passed，0 failed，0 skipped，162.69s。
- 定向合同/参数/config/game_id/RNG/PlayerView/隐藏信息/MODEL-001生成器与标签/数据分离/审计回放：69 passed，0 failed，0 skipped，27.91s。
- 历史基线：387 passed；当前新增50个通过项，无新增skip。
- collect范围由pytest.ini和当前tests目录确定；全仓输出到100%，未见收集错误或永久skip掩盖。
- 测试通过不解除B1-B规格设计门禁，也不自动升级任何单元为AUDITED。

