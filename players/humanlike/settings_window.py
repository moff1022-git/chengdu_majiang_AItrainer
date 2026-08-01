"""Chinese form editor for every Humanlike v2 configuration field."""
from __future__ import annotations
import argparse, copy, json, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from players.humanlike.settings_service import default_config_path, read_raw, save_raw, validate_raw
from players.humanlike.personality_presets import PRESET_IDS, apply_personality_preset, detect_personality_preset, personality_preset_diff
from players.humanlike.rp_archive import dual_view, load_envelopes

GP_TITLES = {
  1:"版本锁定",2:"成都麻将规则集",3:"局制与初始分",4:"牌组定义",5:"换三张",6:"定缺",7:"允许动作",8:"响应优先级",9:"过胡规则",10:"牌墙与终局",
  11:"番型开关",12:"番型关系",13:"基础计分",14:"自摸计分",15:"杠分",16:"呼叫转移",17:"花猪",18:"查叫",19:"退税",20:"庄家",
  21:"信息可见性",22:"思考与超时",23:"玩家画像数量",24:"记忆",25:"情绪与随机误差",26:"搜索与决策",27:"全局目标"}
ZH = {"seed":"随机种子","player_id":"座位编号","profile":"人格参数","cognitive_parameters":"认知与目标参数","name":"名称","level":"水平","style":"风格","enabled":"启用","weights":"权重","decision_weights":"决策权重",
"peng_preference":"碰牌偏好","gang_preference":"杠牌偏好","big_hand_preference":"大牌偏好","defense_awareness":"防守意识","plan_persistence":"计划坚持度","thinking_speed":"思考速度",
"initial_strength":"初始记忆强度","forget_rate":"遗忘率","salience_boost":"显著事件增强","cross_round_history":"跨局记忆局数","learn_hidden_information":"学习隐藏信息",
"emotional_stability":"情绪稳定度","habit_strength":"习惯强度","max_error_probability":"最大失误概率","near_equal_randomness":"近似选择随机度","random_seed":"策略随机种子",
"min_candidates":"最少候选数","max_candidates":"最多候选数","search_depth":"搜索深度","attention_capacity":"注意容量","satisfaction_threshold":"满意停止阈值","research_threshold":"重新搜索阈值",
"rule_version":"规则版本","parameter_version":"参数版本","implementation_version":"实现版本","ruleset":"规则集","total_rounds":"总局数","starting_score":"起始分","base_score":"基础分","fan_cap":"封顶番数",
"discard_timeout_ms":"出牌超时（毫秒）","response_timeout_ms":"响应超时（毫秒）","max_performance_delay_ms":"最大模拟思考延迟（毫秒）"}
ENUMS={
"level":["novice","normal","skilled","expert"],"style":["conservative","balanced","aggressive"],"direction":["left","right","opposite","dice","random"],"ranking":["total_score","rank_points","custom"],
"priority_mode":["hu_gang_peng_pass","hu_seat_peng_gang_pass"],"seat_priority":["nearest_from_discarder","platform_deterministic"],"pass_hu_mode":["none","until_self_draw","until_value_increase","platform_custom"],
"gang_draw_source":["wall_tail","platform_position"],"mode":["add_base","add_fan","fixed_bonus","none"],"payers":["all_active_opponents","platform_set"],"payment":["discarder_only","all_active_opponents","custom"],
"settlement":["immediate","round_end"],"multi_hu_mode":["copy_to_each_winner","split","custom"],"payees":["all_non_hu_non_huazhu","all_eligible","custom"],"dead_wait":["valid","invalid"],
"valuation":["actual_live_wait","maximum_possible_fan","custom"],"dealer_mode":["dice","rotate","winner","custom"],"timeout_action":["auto_pass","auto_hu","safe_discard","platform_default"]}
SCOPE_ENUMS={"GP-016":["latest_gang_only","all_related_gang_score","custom"],"GP-019":["all_gang_income","untransferred_gang_income","selected_events","custom"]}
RANGES={"total_rounds":"1–10000","starting_score":"-1,000,000,000–1,000,000,000","early_end_score":"留空或 -1,000,000,000–1,000,000,000","forced_hu_wall_threshold":"0–4","tail_reserved":"0–16","base_score":"1–1,000,000","fan_cap":"0–64","bonus_fan":"0–16","fixed_bonus":"0–1,000,000","ming_gang_score":"0–1,000,000","an_gang_score":"0–1,000,000","bu_gang_score":"0–1,000,000","penalty_fan":"0–64","fixed_score":"0–1,000,000","dealer_bonus_fan":"0–16","dealer_fixed_bonus":"0–1,000,000","continuations":"0–10000","discard_timeout_ms":"250–600000 毫秒","response_timeout_ms":"250–600000 毫秒","max_performance_delay_ms":"0–出牌超时的 80%","cross_round_history":"0–10000","random_seed":"0–18,446,744,073,709,551,615","min_candidates":"1–14，且不大于最多候选数","max_candidates":"1–14，且不小于最少候选数","search_depth":"0–8","attention_capacity":"1–64","target_rank":"1–4","lead_gap":"0–1,000,000,000","trail_gap":"0–1,000,000,000","seed":"0–18,446,744,073,709,551,615"}

def _label(key): return ZH.get(key, key.replace("_"," "))
def _help(key,value,path=()):
    if isinstance(value,bool): return "控制该功能是否启用；范围：开启 / 关闭。"
    choices=SCOPE_ENUMS.get(next((p for p in path if isinstance(p,str) and p.startswith("GP-")),"")) if key=="scope" else ENUMS.get(key)
    if choices: return "选择该参数的工作模式；可选："+" / ".join(choices)
    if "GP-021" in path: return "控制该公开信息的可见程度；可选：hidden / public_partial / public_exact。"
    if isinstance(value,float): return "调节该行为的相对强度；范围：0.0–1.0"+("，同组权重总和须为 1。" if "weights" in path or "decision_weights" in path else "。")
    if isinstance(value,int):
        return "整数参数；范围："+RANGES.get(key,"固定值（只读）。")
    if isinstance(value,(list,dict)): return "结构化列表；逐行填写 JSON 数组，保存时执行完整规范校验。"
    if value is None and key in RANGES: return "可选整数参数；范围："+RANGES[key]
    if key=="platform_ruleset_id": return "平台规则集标识；长度范围：1–128 个字符。"
    if key=="name": return "玩家画像名称；必须为非空文本。"
    return "规范标识文本；当前字段为锁定值，不可修改。"

class SettingsWindow:
    def __init__(self,path:Path):
        self.path=path; self.data=read_raw(path); self.vars={}; self.root=tk.Tk(); self.root.title("Humanlike AI v2 — 中文参数设置"); self.root.geometry("1080x780")
        self.root.configure(bg="#0d2818"); tk.Label(self.root,text="Humanlike AI v2 中文参数设置",bg="#0d2818",fg="#fff3c4",font=("TkDefaultFont",16,"bold")).pack(fill="x",padx=12,pady=8)
        self.book=ttk.Notebook(self.root); self.book.pack(fill="both",expand=True,padx=10,pady=4)
        self._build_tab("基础设置",[(k,self.data[k]) for k in ("rule_version","parameter_version","implementation_version","ruleset","seed")],())
        gp=self.data["global_parameters"]
        for start,end,title in ((1,10,"规则与牌局"),(11,20,"番型与结算"),(21,23,"全局行为")):
            self._build_tab(title,[(f"GP-{i:03d}",gp[f"GP-{i:03d}"]) for i in range(start,end+1)],("global_parameters",))
        player_groups=[(f"座位 S{i}",p) for i,p in enumerate(self.data["players"])]
        self._build_tab("逐玩家设置",player_groups,("players",))
        self._build_personality_presets_tab()
        self._build_rp_view_tab()
        bar=tk.Frame(self.root,bg="#0d2818"); bar.pack(fill="x",padx=12,pady=8)
        for label,fn in (("重新载入",self.reload),("校验全部",self.validate),("保存（下局生效）",self.save),("导入…",self.import_file),("导出…",self.export_file)): tk.Button(bar,text=label,command=fn,bg="#e8f5e9",fg="#102019",activeforeground="#102019",padx=10).pack(side="left",padx=3)
        tk.Button(bar,text="关闭",command=self.root.destroy,bg="#ffe0b2",fg="#3e2723",activeforeground="#3e2723").pack(side="right")
        self.status=tk.StringVar(value=str(path)); tk.Label(self.root,textvariable=self.status,bg="#0d2818",fg="#b0bec5",anchor="w").pack(fill="x",padx=12,pady=(0,8))

    def _build_tab(self,title,groups,prefix):
        outer=tk.Frame(self.book,bg="#102019"); self.book.add(outer,text=title); canvas=tk.Canvas(outer,bg="#102019",highlightthickness=0); sb=ttk.Scrollbar(outer,orient="vertical",command=canvas.yview); body=tk.Frame(canvas,bg="#102019")
        body.bind("<Configure>",lambda e,c=canvas:c.configure(scrollregion=c.bbox("all"))); canvas.create_window((0,0),window=body,anchor="nw"); canvas.configure(yscrollcommand=sb.set); canvas.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y")
        for name,value in groups:
            section=tk.LabelFrame(body,text=GP_TITLES.get(int(name[-3:]),name) if name.startswith("GP-") else name,bg="#12261c",fg="#ffe082",padx=8,pady=6); section.pack(fill="x",padx=8,pady=6)
            if isinstance(value,dict):
                base=prefix+(name,) if name.startswith("GP-") else (prefix+(int(name[-1]),) if name.startswith("座位") else (name,))
                self._fields(section,value,base)
            else:
                self._fields(section,{name:value},())

    def _fields(self,parent,obj,path):
        for key,value in obj.items():
            p=path+(key,); row=tk.Frame(parent,bg="#12261c"); row.pack(fill="x",pady=3); tk.Label(row,text=_label(key),width=24,anchor="w",bg="#12261c",fg="#e8f5e9").pack(side="left")
            locked=("GP-001" in p or "GP-004" in p or key in {"rule_version","parameter_version","implementation_version","ruleset","player_id"})
            if isinstance(value,dict):
                tk.Label(row,text="分组",bg="#12261c",fg="#80cbc4").pack(side="left"); self._fields(parent,value,p); continue
            if isinstance(value,bool): var=tk.BooleanVar(value=value); widget=tk.Checkbutton(row,variable=var,text="开启",bg="#12261c",fg="#e8f5e9",selectcolor="#256d45")
            elif key in ENUMS or key=="scope" or "GP-021" in p:
                choices=(SCOPE_ENUMS.get(next((x for x in p if isinstance(x,str) and x.startswith("GP-")),""),[]) if key=="scope" else (["hidden","public_partial","public_exact"] if "GP-021" in p else ENUMS[key]))
                var=tk.StringVar(value=str(value)); widget=ttk.Combobox(row,textvariable=var,values=choices,state="readonly",width=28)
            else: var=tk.StringVar(value=json.dumps(value,ensure_ascii=False) if isinstance(value,list) else ("" if value is None else str(value))); widget=tk.Entry(row,textvariable=var,width=30)
            if locked:
                try: widget.configure(state="disabled")
                except tk.TclError: pass
            widget.pack(side="left",padx=5); tk.Label(row,text=("🔒 " if locked else "")+_help(key,value,p),anchor="w",justify="left",wraplength=560,bg="#12261c",fg="#9fb8aa").pack(side="left",fill="x",expand=True); self.vars[p]=(var,value)

    def _collect(self):
        out=copy.deepcopy(self.data)
        for path,(var,old) in self.vars.items():
            raw=var.get()
            if isinstance(old,bool): value=bool(raw)
            elif isinstance(old,int): value=int(raw)
            elif isinstance(old,float): value=float(raw)
            elif isinstance(old,list): value=json.loads(raw)
            elif old is None: value=None if str(raw).strip()=="" else raw
            else: value=str(raw)
            target=out
            for part in path[:-1]: target=target[part]
            target[path[-1]]=value
        return out
    def _build_personality_presets_tab(self):
        frame=tk.Frame(self.book,bg="#102019"); self.book.add(frame,text="人格预设")
        tk.Label(frame,text="选择后原子覆盖该座位的人格、GP-025 行为字段和 GP-026 认知字段；名称、seed、记忆和比赛目标保持不变。",bg="#102019",fg="#e8f5e9",wraplength=900,justify="left").pack(fill="x",padx=12,pady=10)
        self.preset_vars={}
        for seat in range(4):
            row=tk.Frame(frame,bg="#12261c"); row.pack(fill="x",padx=12,pady=6)
            tk.Label(row,text=f"座位 S{seat}",width=12,bg="#12261c",fg="#ffe082").pack(side="left")
            current=detect_personality_preset(self.data["players"][seat]); var=tk.StringVar(value=current); self.preset_vars[seat]=var
            box=ttk.Combobox(row,textvariable=var,values=PRESET_IDS,state="readonly",width=28); box.pack(side="left",padx=6)
            tk.Button(row,text="应用预设",command=lambda s=seat:self.apply_preset(s),bg="#e8f5e9",fg="#102019").pack(side="left",padx=4)
            tk.Label(row,text=f"当前：{current}",bg="#12261c",fg="#9fb8aa").pack(side="left",padx=8)
    def apply_preset(self,seat):
        try:
            current=self._collect(); preset_id=self.preset_vars[seat].get(); diffs=personality_preset_diff(current["players"][seat],preset_id)
            preview="\n".join(f"{d.path}: {d.before} → {d.after}" for d in diffs[:10])
            if len(diffs)>10: preview+=f"\n…另有 {len(diffs)-10} 项"
            if diffs and not messagebox.askyesno("确认应用人格预设",f"将覆盖座位 S{seat} 的 {len(diffs)} 个字段：\n\n{preview}",parent=self.root): return
            updated=apply_personality_preset(current["players"][seat],preset_id)
            for path,(var,old) in self.vars.items():
                if len(path)<2 or path[0]!="players" or path[1]!=seat: continue
                value=updated
                for part in path[2:]: value=value[part]
                var.set(json.dumps(value,ensure_ascii=False) if isinstance(value,list) else ("" if value is None else value))
            self.status.set(f"已应用 {preset_id} 到 S{seat}；点击保存后下局生效")
        except Exception as exc: messagebox.showerror("应用预设失败",str(exc),parent=self.root)
    def _build_rp_view_tab(self):
        frame=tk.Frame(self.book,bg="#102019"); self.book.add(frame,text="RP 双视图")
        tk.Label(frame,text="选择 RP envelope 存档后，可切换 envelope 元数据视图与 payload 兼容视图；audit_only 默认隐藏。",bg="#102019",fg="#e8f5e9",wraplength=900,justify="left").pack(fill="x",padx=12,pady=8)
        bar=tk.Frame(frame,bg="#102019"); bar.pack(fill="x",padx=12)
        path_var=tk.StringVar(value=""); include_var=tk.BooleanVar(value=False)
        tk.Entry(bar,textvariable=path_var,width=72).pack(side="left",padx=4)
        def open_archive():
            try:
                data=dual_view(load_envelopes(path_var.get()),include_audit=include_var.get())
                text.delete("1.0","end"); text.insert("end",json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True))
            except Exception as exc: messagebox.showerror("RP 存档读取失败",str(exc),parent=self.root)
        tk.Button(bar,text="打开",command=open_archive,bg="#e8f5e9",fg="#102019").pack(side="left",padx=4)
        tk.Checkbutton(bar,text="显示 audit_only",variable=include_var,bg="#102019",fg="#e8f5e9",selectcolor="#256d45").pack(side="left",padx=4)
        text=tk.Text(frame,bg="#0d1812",fg="#d7ffd9",wrap="none"); text.pack(fill="both",expand=True,padx=12,pady=8)
    def validate(self):
        try: cfg=validate_raw(self._collect(),target=self.path); self.status.set(f"全部参数校验通过 · hash {cfg.config_hash[:12]}"); return True
        except Exception as exc: messagebox.showerror("参数校验失败",str(exc),parent=self.root); self.status.set(str(exc)); return False
    def save(self):
        try: cfg=save_raw(self._collect(),self.path); self.status.set(f"保存成功，下局生效 · hash {cfg.config_hash[:12]}")
        except Exception as exc: messagebox.showerror("保存失败",str(exc),parent=self.root)
    def reload(self): self.root.destroy(); SettingsWindow(self.path).run()
    def import_file(self):
        name=filedialog.askopenfilename(filetypes=[("JSON","*.json")],parent=self.root)
        if name:
            imported=read_raw(name); validate_raw(imported,target=self.path)
            for path,(var,old) in self.vars.items():
                value=imported
                for part in path: value=value[part]
                var.set(json.dumps(value,ensure_ascii=False) if isinstance(value,list) else ("" if value is None else value))
            self.status.set("导入内容校验通过；检查后点击保存")
    def export_file(self):
        name=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("JSON","*.json")],parent=self.root)
        if name: Path(name).write_text(json.dumps(self._collect(),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    def run(self): self.root.mainloop()

def main():
    p=argparse.ArgumentParser(); p.add_argument("--config"); a=p.parse_args(); SettingsWindow(Path(a.config) if a.config else default_config_path()).run(); return 0
if __name__=="__main__": raise SystemExit(main())
