"""Chinese form editor for every Humanlike v2 configuration field."""
from __future__ import annotations
import argparse, copy, json, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from players.humanlike.settings_service import default_config_path, read_raw, save_raw, validate_raw

GP_TITLES = {
  1:"版本锁定",2:"成都麻将规则集",3:"局制与初始分",4:"牌组定义",5:"换三张",6:"定缺",7:"允许动作",8:"响应优先级",9:"过胡规则",10:"牌墙与终局",
  11:"番型开关",12:"番型关系",13:"基础计分",14:"自摸计分",15:"杠分",16:"呼叫转移",17:"花猪",18:"查叫",19:"退税",20:"庄家",
  21:"信息可见性",22:"思考与超时",23:"玩家画像数量",24:"记忆",25:"情绪与随机误差",26:"搜索与决策",27:"全局目标"}
ZH = {"seed":"随机种子","name":"名称","level":"水平","style":"风格","enabled":"启用","weights":"权重","decision_weights":"决策权重",
"peng_preference":"碰牌偏好","gang_preference":"杠牌偏好","big_hand_preference":"大牌偏好","defense_awareness":"防守意识","plan_persistence":"计划坚持度","thinking_speed":"思考速度",
"initial_strength":"初始记忆强度","forget_rate":"遗忘率","salience_boost":"显著事件增强","cross_round_history":"跨局记忆局数","learn_hidden_information":"学习隐藏信息",
"emotional_stability":"情绪稳定度","habit_strength":"习惯强度","max_error_probability":"最大失误概率","near_equal_randomness":"近似选择随机度","random_seed":"策略随机种子",
"min_candidates":"最少候选数","max_candidates":"最多候选数","search_depth":"搜索深度","attention_capacity":"注意容量","satisfaction_threshold":"满意停止阈值","research_threshold":"重新搜索阈值",
"rule_version":"规则版本","parameter_version":"参数版本","implementation_version":"实现版本","ruleset":"规则集","total_rounds":"总局数","starting_score":"起始分","base_score":"基础分","fan_cap":"封顶番数",
"discard_timeout_ms":"出牌超时（毫秒）","response_timeout_ms":"响应超时（毫秒）","max_performance_delay_ms":"最大模拟思考延迟（毫秒）"}
ENUMS={"level":["novice","normal","skilled","expert"],"style":["conservative","balanced","aggressive"],"direction":["left","right","opposite","dice","random"],"ranking":["total_score","rank_points","custom"]}

def _label(key): return ZH.get(key, key.replace("_"," "))
def _help(key,value):
    if isinstance(value,bool): return "控制该功能是否启用；范围：开启 / 关闭。"
    if key in ENUMS: return "选择该参数的工作模式；范围："+" / ".join(ENUMS[key])
    if isinstance(value,float): return "调节该行为的相对强度；范围：0.0–1.0（权重组总和须为 1）。"
    if isinstance(value,int):
        if key.endswith("_ms"): return "控制等待时间；范围：0–600000 毫秒，具体上限由规范校验。"
        return "整数参数；合法范围由成都麻将参数规范校验，越界不能保存。"
    if isinstance(value,(list,dict)): return "结构化列表；逐行填写 JSON 数组，保存时执行完整规范校验。"
    return "文本标识或模式名称；可选值和长度由参数规范校验。"

class SettingsWindow:
    def __init__(self,path:Path):
        self.path=path; self.data=read_raw(path); self.vars={}; self.root=tk.Tk(); self.root.title("Humanlike AI v2 — 中文参数设置"); self.root.geometry("1080x780")
        self.root.configure(bg="#0d2818"); tk.Label(self.root,text="Humanlike AI v2 中文参数设置",bg="#0d2818",fg="#fff3c4",font=("TkDefaultFont",16,"bold")).pack(fill="x",padx=12,pady=8)
        self.book=ttk.Notebook(self.root); self.book.pack(fill="both",expand=True,padx=10,pady=4)
        self._build_tab("基础设置",[(k,self.data[k]) for k in ("rule_version","parameter_version","implementation_version","ruleset","seed")],())
        gp=self.data["global_parameters"]
        for start,end,title in ((1,10,"规则与牌局"),(11,20,"番型与结算"),(21,27,"认知与目标")):
            self._build_tab(title,[(f"GP-{i:03d}",gp[f"GP-{i:03d}"]) for i in range(start,end+1)],("global_parameters",))
        self._build_tab("玩家画像",[(f"座位 S{i}",p["profile"]) for i,p in enumerate(self.data["players"])],("players",))
        bar=tk.Frame(self.root,bg="#0d2818"); bar.pack(fill="x",padx=12,pady=8)
        for label,fn in (("重新载入",self.reload),("校验全部",self.validate),("保存（下局生效）",self.save),("导入…",self.import_file),("导出…",self.export_file)): tk.Button(bar,text=label,command=fn,bg="#256d45",fg="white",padx=10).pack(side="left",padx=3)
        tk.Button(bar,text="关闭",command=self.root.destroy,bg="#5b4030",fg="white").pack(side="right")
        self.status=tk.StringVar(value=str(path)); tk.Label(self.root,textvariable=self.status,bg="#0d2818",fg="#b0bec5",anchor="w").pack(fill="x",padx=12,pady=(0,8))

    def _build_tab(self,title,groups,prefix):
        outer=tk.Frame(self.book,bg="#102019"); self.book.add(outer,text=title); canvas=tk.Canvas(outer,bg="#102019",highlightthickness=0); sb=ttk.Scrollbar(outer,orient="vertical",command=canvas.yview); body=tk.Frame(canvas,bg="#102019")
        body.bind("<Configure>",lambda e,c=canvas:c.configure(scrollregion=c.bbox("all"))); canvas.create_window((0,0),window=body,anchor="nw"); canvas.configure(yscrollcommand=sb.set); canvas.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y")
        for name,value in groups:
            section=tk.LabelFrame(body,text=GP_TITLES.get(int(name[-3:]),name) if name.startswith("GP-") else name,bg="#12261c",fg="#ffe082",padx=8,pady=6); section.pack(fill="x",padx=8,pady=6)
            if isinstance(value,dict):
                base=prefix+(name,) if name.startswith("GP-") else (prefix+(int(name[-1]),"profile") if name.startswith("座位") else (name,))
                self._fields(section,value,base)
            else:
                self._fields(section,{name:value},())

    def _fields(self,parent,obj,path):
        for key,value in obj.items():
            p=path+(key,); row=tk.Frame(parent,bg="#12261c"); row.pack(fill="x",pady=3); tk.Label(row,text=_label(key),width=24,anchor="w",bg="#12261c",fg="#e8f5e9").pack(side="left")
            locked=("GP-001" in p or "GP-004" in p or key in {"rule_version","parameter_version","implementation_version","ruleset"})
            if isinstance(value,dict):
                tk.Label(row,text="分组",bg="#12261c",fg="#80cbc4").pack(side="left"); self._fields(parent,value,p); continue
            if isinstance(value,bool): var=tk.BooleanVar(value=value); widget=tk.Checkbutton(row,variable=var,text="开启",bg="#12261c",fg="#e8f5e9",selectcolor="#256d45")
            elif key in ENUMS: var=tk.StringVar(value=str(value)); widget=ttk.Combobox(row,textvariable=var,values=ENUMS[key],state="readonly",width=24)
            else: var=tk.StringVar(value=json.dumps(value,ensure_ascii=False) if isinstance(value,list) else ("" if value is None else str(value))); widget=tk.Entry(row,textvariable=var,width=30)
            if locked:
                try: widget.configure(state="disabled")
                except tk.TclError: pass
            widget.pack(side="left",padx=5); tk.Label(row,text=("🔒 " if locked else "")+_help(key,value),anchor="w",justify="left",wraplength=560,bg="#12261c",fg="#9fb8aa").pack(side="left",fill="x",expand=True); self.vars[p]=(var,value)

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
