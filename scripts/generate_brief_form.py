#!/usr/bin/env python3
"""
生成展览策划项目信息收集表单（HTML）。

用法:
    python3 generate_brief_form.py <type> [output_dir]

参数:
    type        项目类型: a (企业展厅) | b (博物馆/文化馆) | c (文旅/主题展馆)
    output_dir  输出目录，默认当前目录

输出:
    在 output_dir 下生成 brief-form.html
    用户填写后点击「生成填写结果」按钮，复制文本框内容回传给策划助手。
"""

import sys
import os

# 三类项目的表单字段定义： (字段名, 提示语, 输入类型)
# 输入类型: text(单行) / textarea(多行) / select(下拉，选项用|分隔写在提示里)
FIELDS = {
    "a": {
        "title": "企业展厅 · 项目信息收集表",
        "sections": [
            ("基本信息", [
                ("企业名称", "公司全称", "text"),
                ("项目名称", "如：XX企业品牌展厅", "text"),
                ("展厅面积", "总面积，分多层请注明各层", "text"),
                ("交付时间", "项目计划完成节点", "text"),
                ("预算范围", "可不填", "text"),
            ]),
            ("企业解读", [
                ("成立时间与主营业务", "企业何时成立，做什么", "textarea"),
                ("核心产品/技术", "最具代表性的产品或技术", "textarea"),
                ("品牌slogan/使命愿景", "企业的口号、使命、愿景", "textarea"),
                ("最自豪的事", "企业最引以为豪的1-3件事", "textarea"),
                ("重大里程碑", "近年重大成就（获奖/上市/突破）", "textarea"),
            ]),
            ("受众分析", [
                ("主要参观人群", "政务领导/商务客户/行业伙伴/员工/公众", "textarea"),
                ("参观目的", "品牌认知/技术验证/商务谈判/招聘招商等", "textarea"),
                ("期望留下的印象", "参观后希望对方记住什么", "textarea"),
            ]),
            ("内容方向", [
                ("展示重点", "产品线/技术/历史/文化/未来战略", "textarea"),
                ("禁忌内容", "不能涉及的内容", "textarea"),
                ("参考案例", "欣赏的同类展厅（如有）", "textarea"),
                ("现有品牌视觉", "是否有VI/色彩规范等", "textarea"),
            ]),
        ],
    },
    "b": {
        "title": "博物馆 / 文化馆 · 项目信息收集表",
        "sections": [
            ("基本信息", [
                ("场馆名称", "场馆/项目全称", "text"),
                ("场馆类型", "历史博物馆/纪念馆/非遗馆/校史馆/档案馆/科技馆", "text"),
                ("展陈面积", "建筑面积与展陈面积，分层填写", "text"),
                ("交付时间", "项目计划完成节点", "text"),
            ]),
            ("内容主体", [
                ("核心展示对象", "地域历史/特定人物/某类文物/某项技艺/某段事件", "textarea"),
                ("馆藏实物", "是否有文物/实物，数量与类型", "textarea"),
                ("已有研究成果", "现成的学术研究、史料文献", "textarea"),
                ("内容时间跨度", "如：从史前到当代", "text"),
                ("必须展示的重点", "领导/政策要求的标志性内容", "textarea"),
            ]),
            ("受众与定位", [
                ("主要参观人群", "本地市民/学生研学/外地游客/专业研究者", "textarea"),
                ("教育目标", "知识普及/价值传承/爱国教育/专业研究", "textarea"),
                ("运营需求", "是否需兼顾文创/研学/临展空间", "textarea"),
            ]),
            ("约束条件", [
                ("政策导向", "上级指导意见、政策要求", "textarea"),
                ("审查要求", "重大历史/人物的官方表述要求", "textarea"),
                ("同类场馆现状", "本地区同类场馆情况（差异化定位用）", "textarea"),
            ]),
        ],
    },
    "c": {
        "title": "文旅 / 主题展馆 · 项目信息收集表",
        "sections": [
            ("基本信息", [
                ("项目名称", "场馆/项目全称", "text"),
                ("项目类型", "城市展示馆/规划馆/景区展厅/沉浸式主题馆/IP主题展", "text"),
                ("场地条件", "面积、层高、空间结构特点", "textarea"),
                ("区位信息", "地段、周边交通、客流来源", "textarea"),
                ("交付时间", "项目计划完成节点", "text"),
            ]),
            ("内容与资源", [
                ("核心主题", "城市文化/自然景观/特定IP/某种体验概念", "textarea"),
                ("独特资源", "当地独一无二的文化/自然资源", "textarea"),
                ("IP/合作内容", "是否有IP授权或合作内容", "textarea"),
                ("政策背景", "文旅规划、产业政策", "textarea"),
            ]),
            ("受众与运营", [
                ("目标客群", "本地市民/亲子家庭/年轻打卡群体/外地游客", "textarea"),
                ("运营诉求", "门票收益/二次消费/网红传播/城市形象/研学", "textarea"),
                ("预期客流", "预期日均客流量", "text"),
            ]),
            ("体验偏好", [
                ("体验类型", "沉浸式数字/实景互动/静态展陈/混合", "textarea"),
                ("技术倾向", "重多媒体/轻量化", "text"),
                ("参考案例", "欣赏的同类网红场馆", "textarea"),
            ]),
        ],
    },
}


def build_html(cfg):
    rows = []
    field_ids = []
    for sec_name, fields in cfg["sections"]:
        rows.append(f'<h2>{sec_name}</h2>')
        for label, hint, ftype in fields:
            fid = f"f_{len(field_ids)}"
            field_ids.append((fid, label))
            if ftype == "textarea":
                inp = f'<textarea id="{fid}" rows="3" placeholder="{hint}"></textarea>'
            else:
                inp = f'<input type="text" id="{fid}" placeholder="{hint}">'
            rows.append(
                f'<div class="field"><label for="{fid}">{label}'
                f'<span class="hint">{hint}</span></label>{inp}</div>'
            )
    fields_html = "\n".join(rows)

    # 生成 JS 中的字段映射
    js_map = ",".join([f'["{fid}","{label}"]' for fid, label in field_ids])

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cfg['title']}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
    max-width: 760px; margin: 0 auto; padding: 32px 20px;
    background: #f7f7f8; color: #1a1a1a; line-height: 1.6;
  }}
  h1 {{ font-size: 24px; border-bottom: 3px solid #2563eb; padding-bottom: 12px; }}
  h2 {{ font-size: 17px; color: #2563eb; margin-top: 28px; }}
  .intro {{ background:#fff; border-left:4px solid #2563eb; padding:12px 16px; border-radius:6px; font-size:14px; color:#555; }}
  .field {{ margin: 14px 0; }}
  label {{ display: block; font-weight: 600; margin-bottom: 4px; font-size: 14px; }}
  .hint {{ display:block; font-weight: 400; color: #999; font-size: 12px; }}
  input, textarea {{
    width: 100%; padding: 9px 12px; border: 1px solid #d1d5db;
    border-radius: 6px; font-size: 14px; font-family: inherit; resize: vertical;
  }}
  input:focus, textarea:focus {{ outline: none; border-color: #2563eb; }}
  .btn {{
    background: #2563eb; color: #fff; border: none; padding: 12px 24px;
    border-radius: 6px; font-size: 15px; cursor: pointer; margin-top: 24px;
  }}
  .btn:hover {{ background: #1d4ed8; }}
  #output {{
    width: 100%; height: 240px; margin-top: 16px; padding: 12px;
    border: 2px solid #2563eb; border-radius: 6px; font-family: monospace;
    font-size: 13px; display: none;
  }}
  .copy-tip {{ color: #16a34a; font-size: 13px; margin-top: 8px; display: none; }}
</style>
</head>
<body>
<h1>{cfg['title']}</h1>
<p class="intro">请填写以下信息（不必每项都填，已知信息尽量填写）。完成后点击底部按钮，把生成的文本复制回策划助手对话。</p>
{fields_html}
<button class="btn" onclick="genResult()">生成填写结果</button>
<p class="copy-tip" id="tip">✓ 已生成，请复制下方文本框内容回传给策划助手</p>
<textarea id="output" readonly></textarea>

<script>
const FIELDS = [{js_map}];
function genResult() {{
  let out = "【项目信息收集表 - 填写结果】\\n\\n";
  for (const [fid, label] of FIELDS) {{
    const el = document.getElementById(fid);
    const val = el ? el.value.trim() : "";
    if (val) out += label + "：" + val + "\\n";
  }}
  const ta = document.getElementById("output");
  ta.value = out;
  ta.style.display = "block";
  document.getElementById("tip").style.display = "block";
  ta.select();
}}
</script>
</body>
</html>"""


def main():
    if len(sys.argv) < 2 or sys.argv[1].lower() not in FIELDS:
        print("用法: python3 generate_brief_form.py <a|b|c> [output_dir]")
        print("  a = 企业展厅, b = 博物馆/文化馆, c = 文旅/主题展馆")
        sys.exit(1)

    ptype = sys.argv[1].lower()
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "brief-form.html")

    html = build_html(FIELDS[ptype])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ 已生成信息收集表: {out_path}")
    print(f"   项目类型: {FIELDS[ptype]['title']}")
    print(f"   请在浏览器中打开，填写后将结果回传给策划助手。")


if __name__ == "__main__":
    main()
