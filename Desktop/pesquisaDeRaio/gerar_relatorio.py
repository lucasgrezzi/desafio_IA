import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
import io, os, tempfile

# ── Leitura ──────────────────────────────────────────────────────────────────
df = pd.read_excel("estudo_raio_6km (2).xlsx")
df["CNPJ_STR"] = df["CNPJ_ALVO"].astype(str)

PRODUTOS = df["Produto"].unique().tolist()
CNPJS    = df["CNPJ_STR"].unique().tolist()

CORES_PRODUTO = {"TAE": "#1f77b4", "TRE": "#ff7f0e", "TF": "#2ca02c"}
CORES_CNPJ = [
    "#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd",
    "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def cnpj_label(c):
    """Formata CNPJ com pontuação para exibição."""
    c = str(c).zfill(14)
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"

df["CNPJ_LABEL"] = df["CNPJ_STR"].apply(cnpj_label)

LABEL_MAP = dict(zip(df["CNPJ_STR"], df["CNPJ_LABEL"]))

# ═══════════════════════════════════════════════════════════════════════════════
# 1. RELATÓRIO HTML INTERATIVO (Plotly)
# ═══════════════════════════════════════════════════════════════════════════════

charts_html = []

# ─── 1.1 Volume total por CNPJ (agrupado por produto) ────────────────────────
df_vol = df.groupby(["CNPJ_LABEL", "Produto"], as_index=False)["volume_total_rs"].sum()
fig1 = px.bar(
    df_vol, x="CNPJ_LABEL", y="volume_total_rs", color="Produto",
    color_discrete_map=CORES_PRODUTO,
    title="Volume Total (R$) por CNPJ e Produto",
    labels={"volume_total_rs": "Volume (R$)", "CNPJ_LABEL": "CNPJ"},
    barmode="group", text_auto=".2s",
)
fig1.update_layout(xaxis_tickangle=-35, height=450)
charts_html.append(("Volume por CNPJ e Produto", fig1.to_html(full_html=False, include_plotlyjs=False)))

# ─── 1.2 Ranking: CNPJ que mais faturou (volume total consolidado) ────────────
df_rank = df.groupby("CNPJ_LABEL", as_index=False)["volume_total_rs"].sum().sort_values("volume_total_rs", ascending=True)
df_rank["color"] = [CORES_CNPJ[i % len(CORES_CNPJ)] for i in range(len(df_rank))]
fig2 = go.Figure(go.Bar(
    x=df_rank["volume_total_rs"], y=df_rank["CNPJ_LABEL"],
    orientation="h",
    marker_color=df_rank["color"],
    text=[fmt_brl(v) for v in df_rank["volume_total_rs"]],
    textposition="outside",
))
fig2.update_layout(
    title="Ranking de CNPJs por Volume Total (R$)",
    xaxis_title="Volume Total (R$)", yaxis_title="CNPJ",
    height=420, margin=dict(l=220)
)
charts_html.append(("Ranking Geral de CNPJs", fig2.to_html(full_html=False, include_plotlyjs=False)))

# ─── 1.3 Comparativo de produtos — métricas múltiplas (radar) ────────────────
metricas_radar = ["volume_total_rs", "ticket_medio_rs", "recorrencia_usuario_media",
                  "qtd_estabelecimentos_credenciados"]
df_prod = df.groupby("Produto")[metricas_radar].mean().reset_index()
df_prod_norm = df_prod.copy()
for col in metricas_radar:
    mx = df_prod[col].max()
    df_prod_norm[col] = df_prod[col] / mx if mx else 0

labels_radar = ["Volume Total", "Ticket Médio", "Recorrência Usuário", "Qtd Estabelecimentos"]
fig3 = go.Figure()
for _, row in df_prod_norm.iterrows():
    values = [row[m] for m in metricas_radar]
    values.append(values[0])  # fechar polígono
    fig3.add_trace(go.Scatterpolar(
        r=values, theta=labels_radar + [labels_radar[0]],
        fill="toself", name=row["Produto"],
        line_color=CORES_PRODUTO.get(row["Produto"])
    ))
fig3.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    title="Comparativo de Produtos — Radar (valores normalizados)",
    showlegend=True, height=480
)
charts_html.append(("Radar de Produtos", fig3.to_html(full_html=False, include_plotlyjs=False)))

# ─── 1.4 Ticket médio por produto e CNPJ ─────────────────────────────────────
fig4 = px.bar(
    df, x="CNPJ_LABEL", y="ticket_medio_rs", color="Produto",
    color_discrete_map=CORES_PRODUTO,
    title="Ticket Médio (R$) por CNPJ e Produto",
    labels={"ticket_medio_rs": "Ticket Médio (R$)", "CNPJ_LABEL": "CNPJ"},
    barmode="group", text_auto=".2s",
)
fig4.update_layout(xaxis_tickangle=-35, height=450)
charts_html.append(("Ticket Médio por CNPJ", fig4.to_html(full_html=False, include_plotlyjs=False)))

# ─── 1.5 Recorrência por produto ──────────────────────────────────────────────
fig5 = px.box(
    df, x="Produto", y="recorrencia_usuario_media", color="Produto",
    color_discrete_map=CORES_PRODUTO,
    points="all",
    title="Distribuição da Recorrência de Usuário por Produto",
    labels={"recorrencia_usuario_media": "Recorrência Média"},
)
fig5.update_layout(height=420)
charts_html.append(("Recorrência por Produto", fig5.to_html(full_html=False, include_plotlyjs=False)))

# ─── 1.6 Saldos médios por produto (TAE / TRE / TFE) ─────────────────────────
df_saldos = df.groupby("Produto")[["saldo_medio_tae", "saldo_medio_tre", "saldo_medio_tfe"]].mean().reset_index()
df_saldos_m = df_saldos.melt(id_vars="Produto", var_name="Saldo", value_name="Valor")
df_saldos_m["Saldo"] = df_saldos_m["Saldo"].str.replace("saldo_medio_", "").str.upper()
fig6 = px.bar(
    df_saldos_m, x="Produto", y="Valor", color="Saldo",
    barmode="group", text_auto=".2s",
    title="Saldos Médios (TAE / TRE / TFE) por Produto",
    labels={"Valor": "Saldo Médio (R$)"},
)
fig6.update_layout(height=420)
charts_html.append(("Saldos Médios por Produto", fig6.to_html(full_html=False, include_plotlyjs=False)))

# ─── 1.7 Scatter: Ticket Médio vs Recorrência por produto ────────────────────
fig7 = px.scatter(
    df, x="ticket_medio_rs", y="recorrencia_usuario_media",
    color="Produto", symbol="Produto",
    color_discrete_map=CORES_PRODUTO,
    hover_data=["CNPJ_LABEL", "volume_total_rs"],
    size="volume_total_rs",
    title="Ticket Médio vs Recorrência (tamanho = Volume Total)",
    labels={"ticket_medio_rs": "Ticket Médio (R$)", "recorrencia_usuario_media": "Recorrência Média"},
)
fig7.update_layout(height=460)
charts_html.append(("Ticket Médio vs Recorrência", fig7.to_html(full_html=False, include_plotlyjs=False)))

# ─── 1.8 Qtd estabelecimentos por produto e CNPJ ─────────────────────────────
fig8 = px.bar(
    df, x="CNPJ_LABEL", y="qtd_estabelecimentos_credenciados", color="Produto",
    color_discrete_map=CORES_PRODUTO,
    title="Qtd. Estabelecimentos Credenciados por CNPJ e Produto",
    labels={"qtd_estabelecimentos_credenciados": "Qtd. Estabelecimentos", "CNPJ_LABEL": "CNPJ"},
    barmode="group", text_auto=True,
)
fig8.update_layout(xaxis_tickangle=-35, height=450)
charts_html.append(("Estabelecimentos Credenciados", fig8.to_html(full_html=False, include_plotlyjs=False)))

# ─── KPIs para o HTML ─────────────────────────────────────────────────────────
top_cnpj_vol = df.groupby("CNPJ_LABEL")["volume_total_rs"].sum().idxmax()
top_vol      = df.groupby("CNPJ_LABEL")["volume_total_rs"].sum().max()
top_produto  = df.groupby("Produto")["volume_total_rs"].sum().idxmax()
top_prod_vol = df.groupby("Produto")["volume_total_rs"].sum().max()
avg_ticket   = df["ticket_medio_rs"].mean()
avg_recorr   = df["recorrencia_usuario_media"].mean()
total_estab  = df["qtd_estabelecimentos_credenciados"].sum()
total_vol    = df["volume_total_rs"].sum()

kpi_html = f"""
<div style="display:flex;flex-wrap:wrap;gap:16px;margin:20px 0">
  {''.join(f"""
  <div style="background:{bg};border-radius:10px;padding:18px 24px;min-width:200px;flex:1;color:white">
    <div style="font-size:13px;opacity:.85">{label}</div>
    <div style="font-size:22px;font-weight:700;margin-top:6px">{value}</div>
    <div style="font-size:12px;opacity:.75;margin-top:4px">{sub}</div>
  </div>"""
  for bg, label, value, sub in [
    ("#1f77b4", "CNPJ Maior Volume", top_cnpj_vol.split("/")[0]+"...", fmt_brl(top_vol)),
    ("#ff7f0e", "Produto Líder", top_produto, fmt_brl(top_prod_vol)),
    ("#2ca02c", "Volume Total Geral", fmt_brl(total_vol), f"{len(CNPJS)} CNPJs · {len(PRODUTOS)} produtos"),
    ("#9467bd", "Ticket Médio Geral", fmt_brl(avg_ticket), "média todos os CNPJs/produtos"),
    ("#8c564b", "Recorrência Média", f"{avg_recorr:.2f}x", "recorrência usuário"),
    ("#e377c2", "Estab. Credenciados", f"{total_estab:,}", "total no raio"),
  ])}
</div>
"""

# ─── Montar HTML final ────────────────────────────────────────────────────────
sections = ""
for title, html in charts_html:
    sections += f"""
    <section style="margin-bottom:40px">
      <h2 style="color:#2c3e50;border-left:4px solid #1f77b4;padding-left:10px">{title}</h2>
      {html}
    </section>
    """

html_final = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Estudo de Raio — Relatório Interativo</title>
  <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
  <style>
    * {{ box-sizing:border-box; margin:0; padding:0 }}
    body {{ font-family:'Segoe UI',sans-serif; background:#f4f6f9; color:#333 }}
    header {{ background:linear-gradient(135deg,#1f3c88,#1f77b4); color:white; padding:30px 40px }}
    header h1 {{ font-size:28px }} header p {{ opacity:.85; margin-top:6px }}
    main {{ max-width:1200px; margin:auto; padding:30px 20px }}
    section {{ background:white; border-radius:12px; padding:24px; box-shadow:0 2px 8px rgba(0,0,0,.07) }}
    h2 {{ font-size:17px; margin-bottom:16px }}
    footer {{ text-align:center; padding:20px; color:#888; font-size:12px }}
  </style>
</head>
<body>
  <header>
    <h1>Estudo de Raio — Relatório Analítico</h1>
    <p>Raio: 6 km &nbsp;·&nbsp; {len(CNPJS)} CNPJs &nbsp;·&nbsp; Produtos: {', '.join(PRODUTOS)}</p>
  </header>
  <main>
    <h2 style="margin:24px 0 8px;color:#2c3e50">Indicadores-Chave (KPIs)</h2>
    {kpi_html}
    {sections}
  </main>
  <footer>Gerado automaticamente · Estudo de Raio 6 km</footer>
</body>
</html>"""

with open("relatorio_estudo_raio.html", "w", encoding="utf-8") as f:
    f.write(html_final)
print("HTML salvo: relatorio_estudo_raio.html")

# ═══════════════════════════════════════════════════════════════════════════════
# 2. PDF ESTÁTICO (matplotlib + reportlab)
# ═══════════════════════════════════════════════════════════════════════════════

# Gera imagens PNG dos gráficos com matplotlib
plt.rcParams.update({"figure.dpi": 130, "font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})
CMAP = {"TAE": "#1f77b4", "TRE": "#ff7f0e", "TF": "#2ca02c"}
img_paths = []

def save_fig(fig, name):
    p = os.path.join(tempfile.gettempdir(), f"{name}.png")
    fig.savefig(p, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    img_paths.append((name, p))
    return p

# P1 — Volume por CNPJ (stacked)
fig, ax = plt.subplots(figsize=(10, 4.5))
df_pv = df.pivot_table(index="CNPJ_LABEL", columns="Produto", values="volume_total_rs", aggfunc="sum").fillna(0)
df_pv.plot(kind="bar", ax=ax, color=[CMAP.get(c, "#999") for c in df_pv.columns], edgecolor="white", width=0.7)
ax.set_title("Volume Total (R$) por CNPJ e Produto", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("CNPJ"); ax.set_ylabel("Volume (R$)")
ax.tick_params(axis="x", rotation=35, labelsize=7)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"R${x/1e3:.0f}k" if x >= 1000 else f"R${x:.0f}"))
ax.legend(title="Produto")
save_fig(fig, "p1_volume_cnpj")

# P2 — Ranking horizontal
fig, ax = plt.subplots(figsize=(9, 4))
df_rank_plt = df.groupby("CNPJ_LABEL")["volume_total_rs"].sum().sort_values()
colors_bar = [CORES_CNPJ[i % len(CORES_CNPJ)] for i in range(len(df_rank_plt))]
bars = ax.barh(df_rank_plt.index, df_rank_plt.values, color=colors_bar)
for bar, val in zip(bars, df_rank_plt.values):
    ax.text(bar.get_width() * 1.01, bar.get_y() + bar.get_height()/2,
            fmt_brl(val), va="center", fontsize=7)
ax.set_title("Ranking de CNPJs por Volume Total", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Volume (R$)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"R${x/1e3:.0f}k" if x >= 1000 else f"R${x:.0f}"))
plt.tight_layout()
save_fig(fig, "p2_ranking")

# P3 — Ticket médio por produto (boxplot)
fig, ax = plt.subplots(figsize=(7, 4))
data_box = [df[df["Produto"] == p]["ticket_medio_rs"].values for p in PRODUTOS]
bp = ax.boxplot(data_box, labels=PRODUTOS, patch_artist=True, notch=False)
for patch, prod in zip(bp["boxes"], PRODUTOS):
    patch.set_facecolor(CMAP.get(prod, "#ccc"))
    patch.set_alpha(0.8)
ax.set_title("Distribuição do Ticket Médio por Produto", fontsize=13, fontweight="bold", pad=12)
ax.set_ylabel("Ticket Médio (R$)")
save_fig(fig, "p3_ticket_box")

# P4 — Recorrência por produto (bar + scatter)
fig, ax = plt.subplots(figsize=(8, 4))
df_rec = df.groupby("Produto")["recorrencia_usuario_media"].agg(["mean", "min", "max"]).reset_index()
x = np.arange(len(df_rec))
bars = ax.bar(x, df_rec["mean"], color=[CMAP.get(p, "#999") for p in df_rec["Produto"]], alpha=0.8, edgecolor="white")
ax.errorbar(x, df_rec["mean"],
            yerr=[df_rec["mean"] - df_rec["min"], df_rec["max"] - df_rec["mean"]],
            fmt="none", capsize=5, color="gray", linewidth=1.5)
for bar, val in zip(bars, df_rec["mean"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f"{val:.2f}x",
            ha="center", fontsize=10, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(df_rec["Produto"])
ax.set_title("Recorrência Média por Produto (barras de erro: min/max)", fontsize=12, fontweight="bold")
ax.set_ylabel("Recorrência Média")
save_fig(fig, "p4_recorrencia")

# P5 — Saldos médios por produto
fig, ax = plt.subplots(figsize=(9, 4))
df_s = df.groupby("Produto")[["saldo_medio_tae", "saldo_medio_tre", "saldo_medio_tfe"]].mean()
df_s.columns = ["TAE", "TRE", "TFE"]
df_s.plot(kind="bar", ax=ax, edgecolor="white", width=0.7)
ax.set_title("Saldos Médios (TAE / TRE / TFE) por Produto", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Produto"); ax.set_ylabel("Saldo Médio (R$)")
ax.tick_params(axis="x", rotation=0)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"R${x:.0f}"))
save_fig(fig, "p5_saldos")

# P6 — Qtd estabelecimentos por produto
fig, ax = plt.subplots(figsize=(10, 4.5))
df_estab = df.pivot_table(index="CNPJ_LABEL", columns="Produto", values="qtd_estabelecimentos_credenciados", aggfunc="sum").fillna(0)
df_estab.plot(kind="bar", ax=ax, color=[CMAP.get(c, "#999") for c in df_estab.columns], edgecolor="white", width=0.7)
ax.set_title("Qtd. Estabelecimentos Credenciados por CNPJ e Produto", fontsize=12, fontweight="bold", pad=12)
ax.set_xlabel("CNPJ"); ax.set_ylabel("Qtd. Estabelecimentos")
ax.tick_params(axis="x", rotation=35, labelsize=7)
ax.legend(title="Produto")
save_fig(fig, "p6_estabelecimentos")

print(f"Imagens geradas: {len(img_paths)}")

# ─── Montar PDF com ReportLab ─────────────────────────────────────────────────
PDF_PATH = "relatorio_estudo_raio.pdf"
doc = SimpleDocTemplate(PDF_PATH, pagesize=A4,
                        rightMargin=1.8*cm, leftMargin=1.8*cm,
                        topMargin=2*cm, bottomMargin=2*cm)
styles = getSampleStyleSheet()

H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=18, textColor=colors.HexColor("#1f3c88"),
                    spaceAfter=6, alignment=TA_CENTER)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, textColor=colors.HexColor("#1f77b4"),
                    spaceBefore=18, spaceAfter=8, borderPad=(0,0,0,6))
NORMAL = ParagraphStyle("NORMAL", parent=styles["Normal"], fontSize=9, leading=14)
SMALL  = ParagraphStyle("SMALL",  parent=styles["Normal"], fontSize=8, textColor=colors.grey)
BOLD   = ParagraphStyle("BOLD",   parent=styles["Normal"], fontSize=9, fontName="Helvetica-Bold")
CENTER = ParagraphStyle("CENTER", parent=styles["Normal"], fontSize=9, alignment=TA_CENTER)

W_PAGE = A4[0] - 3.6*cm  # largura útil

story = []

# Capa
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("Estudo de Raio — Relatório Analítico", H1))
story.append(Paragraph("Raio: 6 km", ParagraphStyle("sub", parent=styles["Normal"], fontSize=12,
                        alignment=TA_CENTER, textColor=colors.grey, spaceAfter=4)))
story.append(Paragraph(f"Data de geração: 06/05/2026  ·  {len(CNPJS)} CNPJs  ·  Produtos: {', '.join(PRODUTOS)}",
                        ParagraphStyle("sub2", parent=styles["Normal"], fontSize=10, alignment=TA_CENTER,
                                       textColor=colors.grey)))
story.append(Spacer(1, 0.6*cm))
story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1f77b4")))
story.append(Spacer(1, 0.8*cm))

# KPIs em tabela
story.append(Paragraph("Indicadores-Chave (KPIs)", H2))
kpi_data = [
    ["Indicador", "Valor", "Detalhe"],
    ["CNPJ com maior volume", top_cnpj_vol, fmt_brl(top_vol)],
    ["Produto líder em volume", top_produto, fmt_brl(top_prod_vol)],
    ["Volume total geral", fmt_brl(total_vol), f"{len(CNPJS)} CNPJs"],
    ["Ticket médio geral", fmt_brl(avg_ticket), "média todos os registros"],
    ["Recorrência média", f"{avg_recorr:.2f}x", "todos os CNPJs/produtos"],
    ["Total estab. credenciados", f"{total_estab:,}", "soma no raio de 6 km"],
]
kpi_table = Table(kpi_data, colWidths=[6*cm, 7*cm, 5.5*cm])
kpi_table.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#1f3c88")),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",    (0,0), (-1,0), 9),
    ("FONTSIZE",    (0,1), (-1,-1), 8),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#eaf1fb"), colors.white]),
    ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#b0c4de")),
    ("ALIGN",       (1,1), (-1,-1), "RIGHT"),
    ("ALIGN",       (0,0), (-1,0), "CENTER"),
    ("TOPPADDING",  (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
]))
story.append(kpi_table)
story.append(Spacer(1, 0.5*cm))

# Tabela resumo por produto
story.append(Paragraph("Resumo Consolidado por Produto", H2))
df_summ = df.groupby("Produto").agg(
    Volume_Total=("volume_total_rs", "sum"),
    Ticket_Medio=("ticket_medio_rs", "mean"),
    Recorrencia=("recorrencia_usuario_media", "mean"),
    Qtd_Estab=("qtd_estabelecimentos_credenciados", "sum"),
    Saldo_TAE=("saldo_medio_tae", "mean"),
    Saldo_TRE=("saldo_medio_tre", "mean"),
    Saldo_TFE=("saldo_medio_tfe", "mean"),
).reset_index()

summ_rows = [["Produto", "Volume Total", "Ticket Médio", "Recorrência", "Qtd Estab.", "Saldo TAE", "Saldo TRE", "Saldo TFE"]]
for _, r in df_summ.iterrows():
    summ_rows.append([
        r["Produto"], fmt_brl(r["Volume_Total"]), fmt_brl(r["Ticket_Medio"]),
        f"{r['Recorrencia']:.2f}x", str(int(r["Qtd_Estab"])),
        fmt_brl(r["Saldo_TAE"]), fmt_brl(r["Saldo_TRE"]), fmt_brl(r["Saldo_TFE"]),
    ])
summ_table = Table(summ_rows, colWidths=[1.7*cm, 2.8*cm, 2.4*cm, 2.0*cm, 1.8*cm, 2.2*cm, 2.2*cm, 2.2*cm])
summ_table.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#1f3c88")),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",    (0,0), (-1,-1), 7.5),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#eaf1fb"), colors.white]),
    ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#b0c4de")),
    ("ALIGN",       (1,0), (-1,-1), "RIGHT"),
    ("TOPPADDING",  (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 5),
]))
story.append(summ_table)
story.append(Spacer(1, 0.5*cm))

# Tabela detalhada por CNPJ
story.append(Paragraph("Ranking de CNPJs por Volume Total", H2))
df_cnpj_rank = df.groupby("CNPJ_LABEL").agg(
    Volume=("volume_total_rs", "sum"),
    Ticket=("ticket_medio_rs", "mean"),
    Recorrencia=("recorrencia_usuario_media", "mean"),
    Estab=("qtd_estabelecimentos_credenciados", "sum"),
).sort_values("Volume", ascending=False).reset_index()
df_cnpj_rank.insert(0, "#", range(1, len(df_cnpj_rank)+1))

rank_rows = [["#", "CNPJ", "Volume Total", "Ticket Médio", "Recorrência", "Qtd Estab."]]
for _, r in df_cnpj_rank.iterrows():
    rank_rows.append([
        str(int(r["#"])), r["CNPJ_LABEL"], fmt_brl(r["Volume"]),
        fmt_brl(r["Ticket"]), f"{r['Recorrencia']:.2f}x", str(int(r["Estab"])),
    ])
rank_table = Table(rank_rows, colWidths=[1*cm, 5.5*cm, 3.5*cm, 3*cm, 2.5*cm, 2.5*cm])
rank_table.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), colors.HexColor("#1f3c88")),
    ("TEXTCOLOR",   (0,0), (-1,0), colors.white),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE",    (0,0), (-1,-1), 8),
    ("BACKGROUND",  (0,1), (-1,1), colors.HexColor("#fff3cd")),  # destaque top 1
    ("ROWBACKGROUNDS", (0,2), (-1,-1), [colors.HexColor("#eaf1fb"), colors.white]),
    ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#b0c4de")),
    ("ALIGN",       (2,0), (-1,-1), "RIGHT"),
    ("TOPPADDING",  (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(rank_table)

# Gráficos no PDF
story.append(PageBreak())
story.append(Paragraph("Análise Visual — Gráficos", H2))

grafico_titles = [
    ("p1_volume_cnpj", "Volume Total (R$) por CNPJ e Produto"),
    ("p2_ranking",     "Ranking de CNPJs por Volume Total"),
    ("p3_ticket_box",  "Distribuição do Ticket Médio por Produto"),
    ("p4_recorrencia", "Recorrência Média por Produto"),
    ("p5_saldos",      "Saldos Médios por Produto"),
    ("p6_estabelecimentos", "Qtd. Estabelecimentos Credenciados por CNPJ e Produto"),
]

for name, title in grafico_titles:
    path = os.path.join(tempfile.gettempdir(), f"{name}.png")
    if os.path.exists(path):
        story.append(Paragraph(title, H2))
        img = Image(path, width=W_PAGE, height=W_PAGE * 0.45)
        story.append(img)
        story.append(Spacer(1, 0.4*cm))

# Rodapé
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#b0c4de")))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("Relatório gerado automaticamente · Estudo de Raio 6 km · 06/05/2026", SMALL))

doc.build(story)
print(f"PDF salvo: {PDF_PATH}")
print("\nArquivos gerados:")
print(f"  - relatorio_estudo_raio.html  (interativo, abra no navegador)")
print(f"  - relatorio_estudo_raio.pdf   (relatório estático)")
