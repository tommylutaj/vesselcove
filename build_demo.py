#!/usr/bin/env python3
"""
Builds VesselCove v2 — Production-Grade 3D WebGL PBR Configurator & B2B Marketplace Prototype
Uses Three.js r128 (inlined from ./vendor/three.min.js for 100% offline/online reliability)
with procedural PMREM Studio HDR lighting, PBR glass/liquid/metal/sleeve materials,
2048x1024 dynamic UV shrink-sleeve texture, and direct 3D raycast barcode dragging on the vessel.
"""
import base64
from pathlib import Path

BASE_DIR = Path("/Users/thomas/.gemini/antigravity/scratch/vesselcove_demo")
LOGO_PATH = Path("/Users/thomas/.gemini/antigravity/scratch/vesselcove_audit_2026/logos/vesselcove_official.png")
FAVICON_PATH = BASE_DIR / "favicon.png"
THREE_PATH = BASE_DIR / "vendor" / "three.min.js"


def main():
    logo_b64 = "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    favicon_b64 = "data:image/png;base64," + base64.b64encode(FAVICON_PATH.read_bytes()).decode("ascii")
    three_js = THREE_PATH.read_text(encoding="utf-8")

    html = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VesselCove</title>
<link rel="icon" type="image/png" href="__VC_FAVICON__">
<link rel="shortcut icon" type="image/png" href="__VC_FAVICON__">
<link rel="apple-touch-icon" href="__VC_FAVICON__">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg-ivory: #F5F6F8;
    --bg-stone: #F1F3F6;
    --bg-panel: #FFFFFF;
    --bg-subtle: #F4F4F6;
    --ink: #18181B;
    --espresso: #27272A;
    --charcoal: #3F3F46;
    --slate: #64748B;
    --muted: #94A3B8;
    --border: #E5E7EB;
    --border-light: #EEF0F3;
    --crimson: #C2180E;
    --crimson-dark: #9E130B;
    --crimson-soft: #FEF2F2;
    --green: #147A3B;
    --green-soft: #ECFDF3;
    --amber: #B87D00;
    --amber-dot: #E5A000;
    --amber-soft: #FFFBEB;
    --display: 'Plus Jakarta Sans', 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
    --sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    --mono: 'JetBrains Mono', 'SF Mono', Menlo, Monaco, Consolas, monospace;
    --shadow-sm: 0 2px 8px rgba(15, 23, 42, 0.04);
    --shadow-md: 0 8px 24px rgba(15, 23, 42, 0.06);
    --shadow-lg: 0 18px 44px rgba(15, 23, 42, 0.12);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; font-variant-numeric: tabular-nums; scrollbar-width: thin; scrollbar-color: #B8B0A4 transparent; }
  *::-webkit-scrollbar { width: 5px; height: 5px; }
  *::-webkit-scrollbar-track { background: transparent; }
  *::-webkit-scrollbar-thumb { background: #B8B0A4; border-radius: 1px; }
  *::-webkit-scrollbar-thumb:hover { background: var(--ink); }
  html, body {
    height: 100%;
    background-color: var(--bg-ivory);
    background-image:
      linear-gradient(to right, rgba(18, 17, 16, 0.024) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(18, 17, 16, 0.024) 1px, transparent 1px);
    background-size: 28px 28px;
    color: var(--ink);
    font-family: var(--sans);
    -webkit-font-smoothing: antialiased;
    overflow: hidden;
  }

  /* ==================== TOP ARCHITECTURAL COMMAND HEADER ==================== */
  .app-header {
    height: 66px;
    background: #FFFFFF;
    border-bottom: 1px solid var(--border);
    padding: 0 28px;
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 14px;
    z-index: 50;
    position: relative;
  }
  .brand-area {
    display: flex;
    align-items: center;
    gap: 12px;
    justify-self: start;
    transition: opacity 0.16s ease;
  }
  .brand-area:hover { opacity: 0.82; }
  .brand-area img { height: 26px; width: auto; display: block; }

  .nav-tabs {
    display: flex;
    align-items: center;
    background: #F4F4F6;
    padding: 4px;
    border-radius: 999px;
    border: 1px solid #EAECEF;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
    justify-self: center;
    gap: 4px;
    overflow: hidden;
  }
  .nav-back-btn {
    border: none;
    border-right: 1.5px solid var(--ink);
    background: var(--bg-panel);
    width: 34px;
    height: 34px;
    border-radius: 0;
    font-family: var(--mono);
    font-size: 15px;
    font-weight: 800;
    color: var(--ink);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.16s ease, color 0.16s ease;
  }
  .nav-back-btn:hover:not(:disabled) {
    background: var(--crimson);
    color: #FFFFFF;
  }
  .nav-back-btn:disabled {
    opacity: 0.25;
    cursor: default;
  }
  .nav-tab {
    border: none;
    border-right: 1px solid var(--border);
    background: transparent;
    padding: 0 18px;
    height: 34px;
    border-radius: 0;
    font-family: var(--display);
    font-size: 11.5px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--slate);
    cursor: default;
    display: inline-flex;
    align-items: center;
    gap: 7px;
    white-space: nowrap;
    transition: background-color 0.22s ease, color 0.2s ease, box-shadow 0.22s ease;
  }
  .nav-tab:last-child { border-right: none; }
  .nav-tab.active {
    background: var(--espresso);
    color: #FFFFFF;
    box-shadow: inset 0 -3px 0 var(--crimson);
  }
  .nav-tab .step-tag {
    font-family: var(--mono);
    font-size: 10px;
    opacity: 0.72;
  }
  .nav-tab.active .step-tag {
    color: #FFFFFF;
    opacity: 0.92;
  }

  .hdr-right {
    display: flex;
    align-items: center;
    gap: 8px;
    justify-self: end;
  }
  .lang-toggle {
    display: flex;
    border: 1.5px solid var(--ink);
    border-radius: 2px;
    overflow: hidden;
    background: var(--bg-panel);
  }
  .lang-b {
    border: none;
    background: transparent;
    padding: 6px 12px;
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 800;
    color: var(--slate);
    cursor: pointer;
    transition: background-color 0.18s ease, color 0.18s ease;
  }
  .lang-b.active { background: var(--crimson); color: #FFFFFF; }

  @keyframes viewFadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes stageSlide {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes popoverDrop {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes modalPop {
    from { opacity: 0; transform: translateY(8px) scale(0.985); }
    to { opacity: 1; transform: translateY(0) scale(1); }
  }

  /* ==================== MAIN STUDIO 3-COL LAYOUT ==================== */
  .view-container {
    height: calc(100vh - 60px);
    display: none;
  }
  .view-container.active {
    display: block;
    animation: viewFadeIn 0.24s cubic-bezier(0.22, 1, 0.36, 1) both;
  }

  .studio-grid {
    height: 100%;
    display: grid;
    grid-template-columns: 356px minmax(500px, 1fr) 388px;
    background: var(--ink);
    gap: 1.5px;
  }

  /* LEFT INSPECTOR DOCK */
  .dock-left, .dock-right {
    background: var(--bg-panel);
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
  }

  .inspector-tabs {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    background: var(--bg-stone);
    border-bottom: 1.5px solid var(--ink);
    flex-shrink: 0;
  }
  .inspector-tabs.two-tabs {
    grid-template-columns: repeat(2, 1fr);
  }
  .insp-tab {
    border: none;
    border-right: 1px solid var(--border);
    background: transparent;
    padding: 11px 10px;
    cursor: pointer;
    text-align: left;
    font-family: var(--sans);
    position: relative;
    transition: background-color 0.18s ease, color 0.18s ease;
  }
  .insp-tab:hover:not(.active) { background: rgba(18, 17, 16, 0.04); }
  .insp-tab:last-child { border-right: none; }
  .insp-tab.active { background: var(--bg-panel); }
  .insp-tab::after {
    content: "";
    position: absolute;
    left: 0; right: 0; bottom: 0;
    height: 3px;
    background: var(--crimson);
    transform: scaleX(0);
    transition: transform 0.22s cubic-bezier(0.22, 1, 0.36, 1);
  }
  .insp-tab.active::after { transform: scaleX(1); }
  .insp-tab .t-num {
    font-family: var(--mono);
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: var(--slate);
    display: block;
  }
  .insp-tab.active .t-num { color: var(--crimson); }
  .insp-tab .t-lbl {
    font-family: var(--display);
    font-size: 12px;
    font-weight: 700;
    color: var(--charcoal);
    margin-top: 2px;
    display: block;
    line-height: 1.15;
  }
  .insp-tab.active .t-lbl { color: var(--ink); }

  .dock-scroll {
    flex: 1 1 auto;
    overflow-y: auto;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .sec-block {
    display: flex;
    flex-direction: column;
    gap: 7px;
  }
  @keyframes secReveal {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .sec-block.reveal-anim {
    animation: secReveal 0.22s cubic-bezier(0.22, 1, 0.36, 1) both;
  }
  .sec-hdr {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 6px;
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--slate);
    padding-bottom: 4px;
    border-bottom: 1px solid var(--border-light);
  }
  .sec-hdr .val-pill {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 700;
    color: var(--ink);
    background: var(--bg-stone);
    border: 1px solid var(--border);
    padding: 1.5px 6px;
    border-radius: 2px;
    white-space: nowrap;
    flex-shrink: 0;
  }

  /* PRODUCT & CLOSURE SELECTOR CARDS */
  .prod-list { display: flex; flex-direction: column; gap: 6px; }
  .prod-item {
    border: 1px solid var(--border);
    border-radius: 2px;
    background: var(--bg-panel);
    padding: 9px 11px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    text-align: left;
    font-family: var(--sans);
    transition: border-color 0.16s ease, background-color 0.16s ease, transform 0.14s ease, box-shadow 0.16s ease;
  }
  .prod-item:hover:not(.active):not(.clash-active) { border-color: var(--ink); background: var(--bg-subtle); transform: translate(-1px, -1px); box-shadow: var(--shadow-sm); }
  .prod-item.active {
    border-color: var(--crimson);
    background: var(--crimson-soft);
    color: var(--ink);
    box-shadow: inset 3.5px 0 0 var(--crimson);
  }
  .prod-item.active .prod-title { color: var(--ink); }
  .prod-item.active .prod-meta { color: var(--charcoal); }
  .prod-item.clash-active {
    border-color: var(--crimson);
    background: var(--crimson-soft);
    box-shadow: inset 3.5px 0 0 var(--crimson);
  }
  .prod-title { font-size: 12.5px; font-weight: 700; color: var(--ink); transition: color 0.18s ease; }
  .prod-meta { font-size: 11px; color: var(--slate); margin-top: 1px; transition: color 0.18s ease; }
  .spec-tag {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 700;
    padding: 3px 7px;
    border-radius: 2px;
    background: var(--bg-stone);
    color: var(--espresso);
    white-space: nowrap;
  }
  .spec-tag.ok { background: var(--green-soft); color: var(--green); border: 1px solid rgba(20,122,59,0.28); }
  .spec-tag.clash { background: var(--crimson); color: #FFFFFF; }
  .spec-tag.red-soft { background: var(--crimson-soft); color: var(--crimson-dark); border: 1px solid rgba(194,24,14,0.38); }

  /* UNIFIED 3-ROW SPEC BOX (COLLO / MATERIALE / CAPACITA') */
  .spec-stack {
    display: flex;
    flex-direction: column;
    border: 1px solid var(--border);
    border-radius: 2px;
    background: var(--bg-subtle);
    overflow: hidden;
  }
  .spec-stack-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    padding: 4.5px 10px;
    font-size: 11px;
    line-height: 1.25;
  }
  .spec-stack-row + .spec-stack-row {
    border-top: 1px solid var(--border-light);
  }
  .spec-stack-k {
    font-family: var(--mono);
    font-size: 9px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--slate);
  }
  .spec-stack-v {
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 700;
    color: var(--ink);
  }
  .fixed-mat-card {
    border: 1px solid var(--border);
    border-left: 3.5px solid var(--ink);
    border-radius: 2px;
    background: var(--bg-subtle);
    padding: 9px 11px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }

  /* SWATCH & PILL GRIDS */
  .swatch-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(46px, 1fr));
    gap: 5px;
  }
  .swatch-btn {
    border: 1px solid var(--border);
    border-radius: 2px;
    background: var(--bg-panel);
    padding: 6px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    font-family: var(--sans);
    font-size: 10.5px;
    font-weight: 600;
    color: var(--charcoal);
  }
  .swatch-btn.active { border-color: var(--ink); box-shadow: 0 0 0 1.5px var(--ink); font-weight: 700; }
  .swatch-circle {
    width: 22px; height: 22px; border-radius: 2px;
    border: 1px solid rgba(0,0,0,0.22);
  }

  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
  .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
  .opt-pill {
    border: 1px solid var(--border);
    border-radius: 2px;
    background: var(--bg-panel);
    padding: 8px 10px;
    font-family: var(--sans);
    font-size: 11.5px;
    font-weight: 600;
    color: var(--charcoal);
    cursor: pointer;
    text-align: left;
    transition: background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease, transform 0.14s ease, box-shadow 0.16s ease;
  }
  .opt-pill:hover:not(.active) { border-color: var(--ink); background: var(--bg-subtle); transform: translate(-1px, -1px); box-shadow: var(--shadow-sm); }
  .opt-pill small { display: block; font-size: 10px; color: var(--slate); font-weight: 500; margin-top: 1px; transition: color 0.16s ease; }
  .opt-pill.active {
    border-color: var(--crimson);
    background: var(--crimson-soft);
    color: var(--ink);
    font-weight: 700;
    box-shadow: inset 3.5px 0 0 var(--crimson);
  }
  .opt-pill.active small { color: var(--charcoal); }

  /* REAL-TIME BARCODE 3D CONTROLLER CARD */
  .bc-control-card {
    background: var(--bg-subtle);
    border: 1.5px solid var(--ink);
    border-radius: 2px;
    padding: 12px 13px;
    display: flex;
    flex-direction: column;
    gap: 9px;
    box-shadow: var(--shadow-sm);
  }
  .bc-slider-row { display: flex; flex-direction: column; gap: 3px; }
  .bc-slider-row label {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    font-weight: 700;
    color: var(--charcoal);
  }
  .bc-slider-row label span.mono { font-family: var(--mono); color: var(--crimson); }
  .bc-slider-row input[type=range] {
    width: 100%;
    accent-color: var(--crimson);
    cursor: pointer;
  }
  .bc-scale-hints {
    display: flex;
    justify-content: space-between;
    font-size: 9.5px;
    color: var(--slate);
  }

  /* ==================== CENTER 3D WEBGL VIEWPORT ==================== */
  .viewport-stage {
    position: relative;
    width: 100%;
    height: 100%;
    background:
      linear-gradient(to right, rgba(18, 17, 16, 0.03) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(18, 17, 16, 0.03) 1px, transparent 1px),
      radial-gradient(circle at 50% 42%, #FFFFFF 0%, #F2EDE4 58%, #E4DDD2 100%);
    background-size: 32px 32px, 32px 32px, 100% 100%;
    overflow: hidden;
    user-select: none;
  }
  .viewport-stage.dark-studio {
    background:
      linear-gradient(to right, rgba(255, 255, 255, 0.035) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255, 255, 255, 0.035) 1px, transparent 1px),
      radial-gradient(circle at 50% 42%, #2E2927 0%, #1B1816 62%, #110F0E 100%);
    background-size: 32px 32px, 32px 32px, 100% 100%;
  }
  #webglCanvas {
    width: 100%;
    height: 100%;
    display: block;
    touch-action: none !important;
    -webkit-user-select: none !important;
    user-select: none !important;
  }

  /* FLOATING TOP STUDIO TOOLBAR (SWISS CAD INSTRUMENT BEZELS) */
  .floating-hud-top {
    position: absolute;
    top: 14px;
    left: 14px;
    right: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
    pointer-events: none;
    z-index: 10;
  }
  .hud-group {
    pointer-events: auto;
    background: rgba(255, 255, 255, 0.96);
    border: 1.5px solid var(--ink);
    border-radius: 2px;
    padding: 3px 4px;
    display: flex;
    align-items: center;
    gap: 2px;
    box-shadow: 3px 3px 0 rgba(18, 17, 16, 0.14);
    transition: background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
  }
  .hud-divider {
    width: 1px;
    height: 18px;
    background: var(--border);
    margin: 0 2px;
    flex-shrink: 0;
  }
  .hud-chip {
    border: 1px solid transparent;
    background: transparent;
    padding: 5px 7.5px;
    border-radius: 2px;
    font-family: var(--sans);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.01em;
    color: var(--charcoal);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    white-space: nowrap;
    transition: background-color 0.16s ease, color 0.16s ease, border-color 0.16s ease, opacity 0.16s ease, transform 0.14s ease;
  }
  .hud-chip svg {
    width: 12px;
    height: 12px;
    flex-shrink: 0;
    transition: transform 0.16s ease;
  }
  .hud-chip:hover:not(:disabled) {
    background: var(--bg-stone);
    color: var(--ink);
    transform: translateY(-1px);
  }
  .hud-chip:active:not(:disabled) {
    transform: translateY(0);
  }
  .hud-chip.active {
    background: var(--espresso);
    color: #FFFFFF;
    box-shadow: inset 0 -2px 0 var(--crimson);
  }
  .hud-chip.active:hover:not(:disabled) {
    background: var(--espresso);
    color: #FFFFFF;
  }
  .hud-chip:disabled,
  .hud-chip.disabled {
    cursor: not-allowed;
    opacity: 0.34;
    color: var(--slate);
    background: transparent !important;
    box-shadow: none !important;
    transform: none !important;
  }
  .hud-chip.accent-tool.active {
    background: var(--crimson);
    color: #FFFFFF;
    box-shadow: inset 0 -2px 0 var(--ink);
  }
  .hud-chip.accent-tool.active:hover:not(:disabled) {
    background: var(--crimson-dark);
    color: #FFFFFF;
  }
  .hud-chip.icon-only {
    padding: 5px 7px;
  }
  .hud-chip.info-chip {
    width: 18px;
    height: 18px;
    padding: 0;
    justify-content: center;
    border-radius: 2px;
    border: 1.25px solid var(--ink);
    font-family: var(--mono);
    font-style: normal;
    font-size: 10px;
    font-weight: 800;
    line-height: 1;
    color: var(--ink);
    margin: 0 2px 0 2px;
    background: var(--bg-subtle);
  }
  .hud-chip.info-chip:hover:not(:disabled) {
    border-color: var(--crimson);
    background: var(--crimson-soft);
    color: var(--crimson);
  }
  .hud-chip.info-chip.active {
    background: var(--crimson);
    border-color: var(--crimson);
    color: #FFFFFF;
    box-shadow: none;
  }
  .viewport-stage.dark-studio .hud-group {
    background: rgba(18, 17, 16, 0.94);
    border-color: rgba(255, 255, 255, 0.35);
    box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.45);
  }
  .viewport-stage.dark-studio .hud-divider {
    background: rgba(255, 255, 255, 0.18);
  }
  .viewport-stage.dark-studio .hud-chip {
    color: rgba(255, 255, 255, 0.85);
  }
  .viewport-stage.dark-studio .hud-chip:hover:not(:disabled):not(.active) {
    background: rgba(255, 255, 255, 0.12);
    color: #FFFFFF;
  }
  .viewport-stage.dark-studio .hud-chip.active:not(.accent-tool):not(.info-chip) {
    background: #FFFFFF;
    color: var(--ink);
  }
  .viewport-stage.dark-studio .hud-chip.info-chip {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.55);
    color: #FFFFFF;
  }
  .vessel-info-popover {
    position: absolute;
    top: 54px;
    left: 14px;
    width: 304px;
    background: var(--bg-panel);
    border: 1.5px solid var(--ink);
    border-top: 3.5px solid var(--crimson);
    border-radius: 2px;
    padding: 14px 16px;
    box-shadow: var(--shadow-lg);
    z-index: 25;
    display: none;
    flex-direction: column;
    gap: 8px;
  }
  .vessel-info-popover.open {
    display: flex;
    animation: popoverDrop 0.2s cubic-bezier(0.22, 1, 0.36, 1) both;
  }

  /* 3D INTERACTIVE DRAG TELEMETRY STRIP */
  .drag-toast {
    position: absolute;
    bottom: 14px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--ink);
    border: 1px solid var(--charcoal);
    color: #FFFFFF;
    padding: 6px 12px;
    border-radius: 2px;
    font-family: var(--sans);
    font-size: 10px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 7px;
    pointer-events: none;
    z-index: 10;
    box-shadow: 3px 3px 0 rgba(18, 17, 16, 0.20);
    white-space: nowrap;
    transition: opacity 0.2s ease, transform 0.2s ease;
  }
  .drag-toast .pulse-dot {
    width: 7px; height: 7px; border-radius: 1px;
    background: #22C55E;
  }

  /* 3D PIN OVERLAYS (CAD CALLOUT FLAGS) */
  .pin-overlay {
    position: absolute;
    pointer-events: none;
    z-index: 9;
    transform: translate(-50%, -50%);
    transition: opacity 0.16s ease;
  }
  .pin-card {
    background: rgba(255, 255, 255, 0.96);
    border: 1.5px solid var(--ink);
    border-left-width: 4px;
    border-radius: 2px;
    padding: 5px 10px;
    font-family: var(--sans);
    font-size: 10.5px;
    font-weight: 700;
    box-shadow: 3px 3px 0 rgba(18, 17, 16, 0.12);
    white-space: nowrap;
    transition: background-color 0.22s ease, border-color 0.22s ease, color 0.22s ease, box-shadow 0.22s ease;
  }
  .pin-card.ok { border-color: var(--green); color: var(--green); }
  .pin-card.warn { border-color: var(--amber); color: var(--amber); background: var(--amber-soft); }
  .pin-card.err { border-color: var(--crimson); color: var(--crimson); background: var(--crimson-soft); }
  .pin-sub {
    display: block;
    font-family: var(--mono);
    font-size: 9.5px;
    color: var(--slate);
    font-weight: 600;
  }
  .pin-dim {
    display: block;
    font-family: var(--mono);
    font-size: 9.5px;
    font-weight: 800;
    color: var(--ink);
    margin-top: 3px;
    padding-top: 3px;
    border-top: 1px dashed rgba(18, 17, 16, 0.22);
  }

  /* FLOATING BOTTOM TELEMETRY BAR */
  .floating-hud-bottom {
    position: absolute;
    bottom: 14px;
    left: 16px;
    right: 16px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 10px;
    pointer-events: none;
    z-index: 10;
  }
  .telem-cards {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    pointer-events: auto;
  }
  .telem-card {
    background: rgba(255, 255, 255, 0.93);
    backdrop-filter: blur(8px);
    border: 1px solid var(--border);
    border-left: 3.5px solid var(--ink);
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 11px;
    box-shadow: var(--shadow-sm);
  }
  .telem-card.ok { border-left-color: var(--green); }
  .telem-card.warn { border-left-color: var(--amber-dot); }
  .telem-card.err { border-left-color: var(--crimson); background: rgba(253, 242, 241, 0.95); }
  .telem-card small {
    display: block;
    font-size: 9.5px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--slate);
  }
  .telem-card strong { font-family: var(--mono); font-size: 11.5px; color: var(--ink); }

  /* ==================== RIGHT PANEL: TRAFFIC LIGHT & DIAGNOSTICS (ZERO LAYOUT JUMP) ==================== */
  .traffic-banner {
    padding: 13px 16px;
    border-bottom: 1.5px solid var(--ink);
    flex-shrink: 0;
    transition: background-color 0.28s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.28s ease;
  }
  .traffic-banner.g { background: #DCFCE7; border-left: 6px solid #15803D; }
  .traffic-banner.y { background: #FEF08A; border-left: 6px solid #D97706; }
  .traffic-banner.r { background: #FECACA; border-left: 6px solid #C2180E; }

  .tl-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 24px;
    margin-bottom: 4px;
  }
  .tl-lights {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #1A1817;
    padding: 4px 8px;
    border-radius: 14px;
    flex-shrink: 0;
  }
  .tl-bulb {
    width: 10px; height: 10px; border-radius: 50%;
    opacity: 0.22;
    transition: opacity 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
  }
  .tl-bulb.active { opacity: 1; box-shadow: 0 0 8px currentColor; transform: scale(1.08); }
  .tl-bulb.r { background: #EF4444; color: #EF4444; }
  .tl-bulb.y { background: #F59E0B; color: #F59E0B; }
  .tl-bulb.g { background: #22C55E; color: #22C55E; }

  .tl-status-title {
    font-family: var(--display);
    font-size: 13.5px;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--ink);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .tl-desc {
    font-size: 11px;
    line-height: 15.5px;
    height: 31px;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    color: var(--ink);
    margin-bottom: 2px;
  }

  /* RIGHT UNIFIED TECHNICAL VALIDATION BOARD (SEAMLESS FULL-HEIGHT PANEL) */
  .diag-scroll {
    flex: 1 1 auto;
    overflow-y: auto;
    padding: 0;
    display: flex;
    flex-direction: column;
  }
  .diag-board {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    border: none;
    border-radius: 0;
    overflow: hidden;
    background: var(--bg-panel);
    box-shadow: none;
  }
  .diag-row {
    flex: 1 1 auto;
    display: flex;
    align-items: stretch;
    border-bottom: 1px solid var(--border);
    transition: background-color 0.24s ease, box-shadow 0.24s ease, border-color 0.24s ease, color 0.2s ease;
  }
  .diag-row:last-child { border-bottom: none; }
  .diag-pillar {
    width: 46px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    font-family: var(--mono);
    color: #FFFFFF;
    font-weight: 800;
    transition: background-color 0.24s ease;
  }
  .diag-pillar-num { font-size: 9.5px; opacity: 0.88; }
  .diag-pillar-ico { font-size: 15px; line-height: 1; }
  .diag-row.idle { background: #F7F6F4; }
  .diag-row.idle .diag-pillar { background: #9CA3AF; }
  .diag-row.ok { background: #F5FBF7; }
  .diag-row.ok .diag-pillar { background: #15803D; }
  .diag-row.warn {
    background: #FEF08A;
    box-shadow: inset 0 0 0 2px #D97706;
  }
  .diag-row.warn .diag-pillar { background: #D97706; }
  .diag-row.err {
    background: #FECACA;
    box-shadow: inset 0 0 0 2px #C2180E;
  }
  .diag-row.err .diag-pillar { background: #C2180E; }

  .diag-body {
    flex: 1;
    padding: 8px 11px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 2px;
    min-width: 0;
  }
  .diag-row-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 6px;
  }
  .diag-pill {
    font-family: var(--mono);
    font-size: 9.5px;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 2px;
    color: #FFFFFF;
    white-space: nowrap;
    transition: background-color 0.24s ease, color 0.2s ease;
  }
  .diag-pill.idle { background: #9CA3AF; color: #FFFFFF; }
  .diag-pill.ok { background: #15803D; }
  .diag-pill.warn { background: #B45309; }
  .diag-pill.err { background: #C2180E; }

  /* Keep .diag-card for left Tab 3 weight card */
  .diag-card {
    border: 1px solid var(--border);
    border-left: 3.5px solid var(--border);
    border-radius: 2px;
    padding: 10px 12px;
    background: var(--bg-subtle);
  }
  .diag-card.weight-red {
    border: 1.5px solid var(--crimson-dark);
    border-left: 4px solid var(--crimson-dark);
    background: var(--crimson);
    color: #FFFFFF;
    box-shadow: 2px 2px 0 rgba(18, 17, 16, 0.14);
  }
  .diag-card.weight-red .diag-card-k { color: rgba(255, 255, 255, 0.86); }
  .diag-card.weight-red .diag-card-v { color: #FFFFFF !important; }
  .diag-card.weight-red .diag-card-s { color: rgba(255, 255, 255, 0.94); }
  .diag-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 3px;
  }
  .diag-card-k {
    font-family: var(--mono);
    font-size: 9.5px;
    font-weight: 800;
    color: var(--slate);
    text-transform: uppercase;
  }
  .diag-card-v {
    font-family: var(--mono);
    font-size: 11px;
    font-weight: 800;
  }
  .diag-card-t { font-size: 12px; font-weight: 700; color: var(--ink); }
  .diag-card-s { font-size: 11px; color: var(--charcoal); margin-top: 2px; line-height: 1.35; }

  .supply-card {
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 9px 12px;
    background: var(--bg-subtle);
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 8px;
  }
  .sup-p-tag {
    font-family: var(--mono);
    font-size: 9.5px;
    font-weight: 700;
    color: var(--crimson);
    text-transform: uppercase;
  }
  .sup-p-name { font-size: 12px; font-weight: 700; color: var(--ink); }
  .sup-p-sub { font-size: 10.5px; color: var(--slate); }
  .sup-p-price { font-family: var(--mono); font-size: 12px; font-weight: 800; color: var(--espresso); }

  .checkout-footer {
    padding: 13px 16px;
    background: var(--bg-stone);
    border-top: 1.5px solid var(--ink);
    flex-shrink: 0;
    height: 128px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .checkout-footer .sec-hdr {
    white-space: nowrap;
    height: 16px;
    line-height: 16px;
    font-size: 10px;
    letter-spacing: 0.04em;
    border-bottom: none;
    padding-bottom: 0;
  }
  .start-price-hero {
    font-family: var(--display);
    font-size: 26px;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -0.02em;
    line-height: 1.1;
    transition: color 0.2s ease;
  }
  .cta-btn {
    width: 100%;
    height: 41px;
    border: 1.5px solid var(--ink);
    border-radius: 2px;
    padding: 0 14px;
    font-family: var(--display);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.02em;
    cursor: pointer;
    background: var(--crimson);
    color: #FFFFFF;
    box-shadow: 2px 2px 0 var(--ink);
    display: flex;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transition: background-color 0.16s ease, color 0.16s ease, border-color 0.16s ease, transform 0.14s ease, box-shadow 0.14s ease;
  }
  .cta-btn:hover:not(:disabled) {
    background: var(--crimson-dark);
    transform: translate(-1px, -1px);
    box-shadow: 3px 3px 0 var(--ink);
  }
  .cta-btn:active:not(:disabled) {
    transform: translate(1px, 1px);
    box-shadow: 1px 1px 0 var(--ink);
  }
  .cta-btn:disabled {
    background: #D6CFC5;
    border-color: var(--border);
    color: #6E6861;
    box-shadow: none;
    cursor: not-allowed;
  }
  .cta-btn.dark {
    background: var(--espresso);
    border-color: var(--ink);
    box-shadow: 2px 2px 0 var(--ink);
  }
  .cta-btn.dark:hover:not(:disabled) {
    background: var(--crimson);
    box-shadow: 3px 3px 0 var(--ink);
  }
  .cta-btn.white {
    background: #FFFFFF;
    color: var(--ink);
    border: 1.5px solid var(--ink);
    box-shadow: 2px 2px 0 rgba(18, 17, 16, 0.14);
  }
  .cta-btn.white:hover:not(:disabled) {
    background: var(--bg-stone);
    box-shadow: 3px 3px 0 rgba(18, 17, 16, 0.20);
  }

  /* STEP 03 BOX CONFIGURATOR */
  .box-preview-card {
    background: #FFFFFF;
    border: 1.5px solid var(--ink);
    border-radius: 2px;
    padding: 10px;
    box-shadow: var(--shadow-sm);
  }
  .qty-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 5px;
  }
  .qty-btn {
    border: 1px solid var(--border);
    background: var(--bg-panel);
    border-radius: 2px;
    padding: 7px 4px;
    text-align: center;
    cursor: pointer;
    font-family: var(--sans);
    font-size: 12px;
    font-weight: 800;
    color: var(--charcoal);
    transition: background-color 0.16s ease, color 0.16s ease, border-color 0.16s ease, transform 0.14s ease;
  }
  .qty-btn:hover:not(:disabled):not(.active) { border-color: var(--ink); transform: translate(-1px, -1px); }
  .qty-btn small {
    display: block;
    font-family: var(--mono);
    font-size: 9px;
    font-weight: 600;
    color: var(--slate);
    margin-top: 1px;
  }
  .qty-btn.active {
    background: var(--crimson-soft);
    color: var(--crimson-dark);
    border-color: var(--crimson);
    box-shadow: inset 3.5px 0 0 var(--crimson);
  }
  .qty-btn.active small { color: var(--charcoal); }
  .qty-btn:disabled,
  .qty-btn.disabled {
    opacity: 0.38;
    cursor: not-allowed;
    background: var(--bg-subtle) !important;
    color: var(--slate) !important;
    border-style: dashed !important;
    border-color: var(--border) !important;
  }
  .qty-btn:disabled small,
  .qty-btn.disabled small { color: var(--slate) !important; opacity: 0.85; }

  /* ==================== VIEW 01: CONTAINER MARKETPLACE (SWISS ATELIER BENTO) ==================== */
  .catalog-view {
    height: 100%;
    overflow-y: auto;
    padding: 22px 28px 46px 28px;
    max-width: 1500px;
    margin: 0 auto;
  }
  .catalog-hero-card {
    display: grid;
    grid-template-columns: 1.45fr 1fr;
    background: var(--bg-panel);
    border: 1.5px solid var(--ink);
    border-left: 6px solid var(--crimson);
    border-radius: 2px;
    box-shadow: var(--shadow-md);
    overflow: hidden;
  }
  .cat-hero-main {
    padding: 20px 24px;
    border-right: 1.5px solid var(--ink);
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .cat-hero-eye {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--crimson);
  }
  .cat-hero-title {
    font-family: var(--display);
    font-size: 30px;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.06;
    color: var(--ink);
    margin-top: 6px;
  }
  .cat-hero-aside {
    padding: 18px 22px;
    background: var(--bg-subtle);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 10px;
  }
  .cat-hero-code {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.1em;
    color: var(--slate);
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
  }
  .cat-hero-stat {
    font-size: 13px;
    font-weight: 600;
    color: var(--charcoal);
    line-height: 1.35;
  }

  .cat-filter-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin: 16px 0 20px 0;
    padding: 8px 10px;
    background: var(--bg-stone);
    border: 1.5px solid var(--ink);
    border-radius: 2px;
    flex-wrap: wrap;
  }
  .pillar-pills { display: flex; gap: 6px; flex-wrap: wrap; }
  .p-pill {
    border: 1px solid var(--border);
    background: var(--bg-panel);
    padding: 7px 13px;
    border-radius: 2px;
    font-family: var(--sans);
    font-size: 11.5px;
    font-weight: 700;
    color: var(--charcoal);
    cursor: pointer;
    transition: background-color 0.16s ease, color 0.16s ease, border-color 0.16s ease, transform 0.14s ease, box-shadow 0.14s ease;
  }
  .p-pill:hover:not(.active) { border-color: var(--ink); background: #FFFFFF; transform: translate(-1px, -1px); box-shadow: var(--shadow-sm); }
  .p-pill.active {
    background: var(--espresso);
    color: #FFFFFF;
    border-color: var(--ink);
    box-shadow: inset 0 2.5px 0 var(--crimson);
  }

  .cat-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 16px;
  }
  .cat-card {
    grid-column: span 6;
    background: var(--bg-panel);
    border: 1.5px solid var(--ink);
    border-radius: 2px;
    padding: 0;
    display: grid;
    grid-template-columns: 158px 1fr;
    gap: 0;
    align-items: stretch;
    box-shadow: 4px 4px 0 rgba(18, 17, 16, 0.08);
    overflow: hidden;
    transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s cubic-bezier(0.22, 1, 0.36, 1);
    animation: secReveal 0.24s cubic-bezier(0.22, 1, 0.36, 1) both;
  }
  .cat-card:nth-child(4n+1),
  .cat-card:nth-child(4n+4) { grid-column: span 7; }
  .cat-card:nth-child(4n+2),
  .cat-card:nth-child(4n+3) { grid-column: span 5; }
  .cat-card:only-child {
    grid-column: span 12;
    grid-template-columns: 240px 1fr;
  }
  .cat-card:hover {
    border-color: var(--crimson);
    box-shadow: 6px 6px 0 rgba(194, 24, 14, 0.18);
    transform: translate(-2px, -2px);
  }
  .cat-thumb {
    width: 100%;
    height: 100%;
    min-height: 196px;
    position: relative;
    background-color: var(--bg-subtle);
    background-image:
      linear-gradient(to right, rgba(18, 17, 16, 0.04) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(18, 17, 16, 0.04) 1px, transparent 1px);
    background-size: 14px 14px;
    border-right: 1.5px solid var(--ink);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px 10px 10px 10px;
  }
  .cat-spec-stamp {
    position: absolute;
    top: 8px;
    left: 8px;
    font-family: var(--mono);
    font-size: 9.5px;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--espresso);
    background: var(--bg-panel);
    border: 1px solid var(--ink);
    padding: 2px 6px;
  }
  .cat-card-body {
    padding: 18px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 12px;
    min-width: 0;
  }
  .cat-card-body h3 {
    font-family: var(--display);
    font-size: 17px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--ink);
    line-height: 1.22;
  }

  /* ==================== VIEW 03: STEP-BY-STEP SUPPLY CHAIN WIZARD ==================== */
  .pillars-portal {
    width: 100%;
    max-width: 100%;
    height: 100%;
    overflow-y: auto;
    padding: 18px 32px 28px 32px;
    margin: 0;
  }
  .filiera-stepper {
    display: flex;
    align-items: center;
    gap: 6px;
    width: 100%;
    margin: 12px 0 10px 0;
    flex-wrap: nowrap;
  }
  .fstep-pill {
    flex: 1 1 0;
    min-width: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 8px 8px;
    border: 1.5px solid var(--border);
    border-radius: 2px;
    background: var(--bg-panel);
    font-family: var(--sans);
    font-size: 11px;
    font-weight: 700;
    color: var(--slate);
    white-space: nowrap;
    overflow: hidden;
    cursor: default;
    transition: all 0.14s ease;
  }
  .fstep-pill.clickable { cursor: pointer; }
  .fstep-pill.clickable:hover { border-color: var(--ink); color: var(--ink); }
  .fstep-pill.done {
    border-color: var(--green);
    background: var(--green-soft);
    color: var(--ink);
  }
  .fstep-pill.active {
    border-color: var(--ink);
    background: var(--espresso);
    color: #FFFFFF;
    box-shadow: inset 0 -3px 0 var(--crimson);
  }
  .fstep-pill.upcoming { opacity: 0.52; background: var(--bg-subtle); }
  .fstep-num {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 800;
    padding: 2px 6px;
    border-radius: 2px;
    background: rgba(0, 0, 0, 0.08);
  }
  .fstep-pill.active .fstep-num { background: var(--crimson); color: #FFFFFF; }
  .fstep-pill.done .fstep-num { background: var(--green); color: #FFFFFF; }

  .filiera-confirmed-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    padding: 9px 14px;
    margin-bottom: 10px;
    background: var(--bg-panel);
    border: 1px solid var(--ink);
    border-radius: 2px;
  }
  .filiera-confirmed-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
  }
  .f-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    background: var(--bg-subtle);
    border: 1px solid var(--border);
    border-left: 3.5px solid var(--green);
    border-radius: 2px;
    font-size: 11px;
    font-weight: 700;
    color: var(--ink);
    cursor: default;
  }

  .filiera-stage-card {
    background: var(--bg-panel);
    border: 1.5px solid var(--ink);
    border-top: 4px solid var(--crimson);
    border-radius: 2px;
    padding: 18px 22px;
    box-shadow: var(--shadow-md);
    margin-bottom: 14px;
    animation: stageSlide 0.24s cubic-bezier(0.22, 1, 0.36, 1) both;
  }
  .filiera-stage-card h2 { font-family: var(--display); letter-spacing: -0.02em; }
  .filiera-locked-red-text {
    margin-top: 12px;
    font-size: 11.8px;
    font-weight: 700;
    line-height: 1.4;
    color: var(--crimson-dark);
    white-space: nowrap;
  }

  .supplier-list-rich {
    display: flex;
    flex-direction: column;
    gap: 9px;
    margin-top: 12px;
  }
  .supplier-rich-opt {
    position: relative;
    border: 1.5px solid var(--border);
    border-radius: 2px;
    background: var(--bg-subtle);
    padding: 12px 15px;
    text-align: left;
    font-family: var(--sans);
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    transition: border-color 0.16s ease, background-color 0.16s ease, transform 0.14s ease, box-shadow 0.16s ease;
  }
  .supplier-rich-opt:hover:not(.selected) { border-color: var(--ink); background: #FFFFFF; transform: translate(-1px, -1px); box-shadow: var(--shadow-sm); }
  .supplier-rich-opt.sponsored {
    background: #FFFDF8;
    border-color: #D9B76C;
    border-left: 4px solid #C98A1C;
  }
  .supplier-rich-opt.selected,
  .supplier-rich-opt.sponsored.selected {
    border-color: var(--crimson);
    border-left: 1.5px solid var(--crimson);
    background: var(--crimson-soft);
    color: var(--ink);
    box-shadow: inset 4px 0 0 var(--crimson);
  }
  .supplier-rich-opt.selected .sup-name,
  .supplier-rich-opt.selected .sup-price { color: var(--ink); }
  .supplier-rich-opt.selected .sup-desc { color: var(--charcoal); }
  .supplier-rich-opt.selected .meta-tag { background: #FFFFFF; color: var(--charcoal); border-color: rgba(194,24,14,0.22); }
  .supplier-rich-opt.selected .rating-pill { background: #FFFFFF; border-color: rgba(194,24,14,0.25); color: var(--ink); }
  .supplier-rich-opt.selected .rating-pill .rating-rev { color: var(--slate); }
  .supplier-rich-opt.selected .spec-tag.ok { background: var(--green-soft); color: var(--green); border-color: rgba(20,122,59,0.28); }
  .supplier-rich-opt.selected .sup-alloc { color: var(--green); }
  .sponsored-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: #B45309;
    color: #FFFFFF;
    font-family: var(--mono);
    font-size: 9.5px;
    font-weight: 800;
    letter-spacing: 0.08em;
    padding: 3px 7px;
    border-radius: 2px;
  }
  .lowest-price-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: var(--green);
    color: #FFFFFF;
    font-family: var(--mono);
    font-size: 9.5px;
    font-weight: 800;
    letter-spacing: 0.08em;
    padding: 3px 7px;
    border-radius: 2px;
  }
  .rating-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #FFFFFF;
    border: 1px solid var(--border);
    padding: 2px 7px;
    border-radius: 2px;
    font-size: 11px;
    font-weight: 800;
    color: var(--ink);
  }
  .rating-stars { color: #D97706; letter-spacing: 0.04em; }
  .meta-tags-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 7px;
  }
  .meta-tag {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 700;
    color: var(--charcoal);
    background: #FFFFFF;
    border: 1px solid var(--border);
    padding: 2px 7px;
    border-radius: 2px;
  }
  .supplier-rich-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 6px;
    flex-shrink: 0;
    min-width: 110px;
  }

  .filiera-nav-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-top: 18px;
    padding-top: 14px;
    border-top: 1px solid var(--border);
  }
  .filling-mode-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-top: 14px;
  }
  .filling-mode-card {
    border: 1.5px solid var(--border);
    border-radius: 2px;
    background: var(--bg-subtle);
    padding: 15px 17px;
    text-align: left;
    cursor: pointer;
    font-family: var(--sans);
    display: flex;
    flex-direction: column;
    gap: 6px;
    transition: background-color 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease, transform 0.14s ease;
  }
  .filling-mode-card:hover:not(.active):not(:disabled) { border-color: var(--ink); background: #FFFFFF; transform: translate(-1px, -1px); box-shadow: var(--shadow-sm); }
  .filling-mode-card.active {
    border-color: var(--crimson);
    background: var(--crimson-soft);
    color: var(--ink);
    box-shadow: inset 4px 0 0 var(--crimson);
  }
  .filling-mode-card.active strong { color: var(--ink); }
  .filling-mode-card.active .fill-sub { color: var(--charcoal); }
  .filling-mode-card.active .fill-price-green { color: var(--green); }
  .filling-mode-card.active .fill-price-red { color: var(--crimson); }
  .filling-mode-card.disabled,
  .filling-mode-card:disabled {
    opacity: 0.58;
    cursor: not-allowed;
    background: var(--bg-subtle);
    border-style: dashed;
    border-color: var(--border);
    box-shadow: none;
  }
  .filling-mode-card.disabled:hover,
  .filling-mode-card:disabled:hover {
    border-color: var(--border);
    background: var(--bg-subtle);
    transform: none;
  }
  .filling-box {
    margin-top: 12px;
    padding: 13px 15px;
    border: 1px dashed var(--ink);
    border-radius: 2px;
    background: var(--bg-ivory);
    display: flex;
    flex-direction: column;
    gap: 9px;
    animation: secReveal 0.22s ease both;
  }
  .filling-unavail-text {
    margin-top: 10px;
    font-size: 12px;
    font-weight: 700;
    color: var(--crimson);
    line-height: 1.45;
  }
  .filling-alert {
    background: var(--crimson-soft);
    border: 1.5px solid var(--crimson);
    border-radius: 2px;
    padding: 11px 14px;
    font-size: 12px;
    font-weight: 700;
    color: var(--crimson-dark);
    margin: 12px 0;
  }

  .summary-strip-3 {
    background: var(--bg-panel);
    border: 1.5px solid var(--ink);
    border-radius: 2px;
    padding: 14px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    flex-wrap: nowrap;
    box-shadow: var(--shadow-md);
  }

  /* MODAL */
  .modal-mask {
    position: fixed;
    inset: 0;
    background: rgba(18, 17, 16, 0.62);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 200;
    padding: 20px;
  }
  .modal-mask.open { display: flex; }
  .modal-mask.open .modal-card { animation: modalPop 0.22s cubic-bezier(0.22, 1, 0.36, 1) both; }
  .modal-card {
    background: var(--bg-panel);
    border: 2px solid var(--ink);
    border-top: 5px solid var(--crimson);
    border-radius: 2px;
    max-width: 680px;
    width: 100%;
    padding: 24px 26px;
    box-shadow: var(--shadow-lg);
  }
  .modal-card h2 { font-family: var(--display); }

  /* ==================== HEADER PROFILE BUTTON & MARKETPLACE RED CTA ==================== */
  .profile-hdr-btn {
    border: 1.5px solid var(--ink);
    background: var(--bg-panel);
    border-radius: 2px;
    padding: 3px 11px 3px 4px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-family: var(--sans);
    font-size: 11.5px;
    font-weight: 700;
    color: var(--ink);
    box-shadow: 2px 2px 0 rgba(18, 17, 16, 0.10);
    transition: border-color 0.16s ease, background-color 0.16s ease, box-shadow 0.16s ease, transform 0.14s ease;
    position: relative;
  }
  .profile-hdr-btn:hover { background: var(--bg-subtle); transform: translate(-1px, -1px); box-shadow: 3px 3px 0 rgba(18, 17, 16, 0.14); }
  .profile-hdr-btn.active {
    border-color: var(--crimson);
    background: var(--crimson-soft);
    color: var(--crimson-dark);
  }
  .profile-avatar {
    width: 26px;
    height: 26px;
    border-radius: 2px;
    background: var(--espresso);
    color: #FFFFFF;
    font-family: var(--mono);
    font-size: 10.5px;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    letter-spacing: 0.03em;
    flex-shrink: 0;
  }
  .profile-hdr-btn.active .profile-avatar { background: var(--crimson); }
  .profile-req-badge {
    display: none;
    align-items: center;
    justify-content: center;
    min-width: 18px;
    height: 18px;
    padding: 0 5px;
    border-radius: 2px;
    background: var(--crimson);
    color: #FFFFFF;
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 800;
  }
  .profile-req-badge.visible { display: inline-flex; }

  .p-pill.red-cta {
    background: #18181B;
    border: 1px solid #18181B;
    border-radius: 999px;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 12.5px;
    padding: 9px 18px;
    margin-left: auto;
    box-shadow: 0 2px 10px rgba(24, 24, 27, 0.10);
    transition: background-color 0.16s ease, border-color 0.16s ease, transform 0.16s ease, box-shadow 0.16s ease;
  }
  .p-pill.red-cta:hover {
    background: var(--crimson);
    border-color: var(--crimson);
    color: #FFFFFF;
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(194, 24, 14, 0.22);
  }

  /* ==================== CENTERED AR QR MODAL IN 3D STUDIO ==================== */

  .ar-qr-overlay {
    position: absolute;
    inset: 0;
    background: rgba(15, 23, 42, 0.42);
    backdrop-filter: blur(4px);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 30;
    padding: 18px;
  }
  .ar-qr-overlay.open { display: flex; }
  .ar-qr-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 22px;
    width: 100%;
    max-width: 390px;
    padding: 24px 26px;
    box-shadow: var(--shadow-lg);
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    animation: modalPop 0.22s cubic-bezier(0.22, 1, 0.36, 1) both;
  }
  .ar-qr-card h3 { font-family: var(--display); }
  .ar-qr-frame {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 14px;
    box-shadow: var(--shadow-sm);
  }
  .demo-red-text {
    font-family: var(--sans);
    font-size: 12.5px;
    font-weight: 700;
    color: var(--crimson);
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0;
    line-height: 1.4;
  }

  /* ==================== CUSTOM CONTAINER UPLOAD DEMO ==================== */
  .custom-vessel-stage {
    height: 100%;
    overflow-y: auto;
    padding: 26px 32px 42px 32px;
    background: transparent;
  }
  .custom-vessel-inner {
    max-width: 1160px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 18px;
    animation: stageSlide 0.24s cubic-bezier(0.22, 1, 0.36, 1) both;
  }
  .custom-vessel-inner h1 { font-family: var(--display); letter-spacing: -0.025em; }
  .custom-panel-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px 26px;
    box-shadow: var(--shadow-md);
    display: flex;
    flex-direction: column;
    gap: 18px;
  }
  .custom-blueprint-grid {
    display: grid;
    grid-template-columns: 0.9fr 1.35fr;
    gap: 24px;
    align-items: start;
  }
  .custom-bp-left {
    display: flex;
    flex-direction: column;
    gap: 12px;
    border-right: 1px solid var(--border-light);
    padding-right: 22px;
  }
  .custom-bp-right {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .custom-spec-checklist {
    border: 1px solid var(--border-light);
    border-radius: 14px;
    background: #F8F9FA;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    gap: 7px;
    font-family: var(--mono);
    font-size: 11px;
    color: var(--charcoal);
  }
  .upload-datasheet-box {
    border: 1.5px dashed #CBD5E1;
    border-radius: 14px;
    background: #F8FAFC;
    padding: 16px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    cursor: pointer;
    transition: border-color 0.16s ease, background-color 0.16s ease;
  }
  .upload-datasheet-box:hover { border-color: var(--crimson); background: var(--crimson-soft); }
  .upload-datasheet-box.loaded { border-style: solid; border-color: var(--green); background: var(--green-soft); }
  .upload-slot-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }
  .upload-slot {
    border: 1.5px dashed #D5DAE2;
    border-radius: 14px;
    background: #F8FAFC;
    padding: 14px 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 5px;
    cursor: pointer;
    min-height: 110px;
    transition: border-color 0.16s ease, background-color 0.16s ease, transform 0.16s ease, box-shadow 0.16s ease;
    position: relative;
    overflow: hidden;
  }
  .upload-slot:hover { border-color: var(--ink); background: #F1F5F9; transform: translateY(-2px); box-shadow: var(--shadow-sm); }
  .upload-slot.loaded { border-style: solid; border-color: var(--green); background: var(--green-soft); }
  .upload-slot-num {
    font-family: var(--mono);
    font-size: 9.5px;
    font-weight: 800;
    color: var(--crimson);
    letter-spacing: 0.08em;
  }
  .upload-slot.loaded .upload-slot-num { color: var(--green); }
  .upload-slot-title { font-size: 12px; font-weight: 700; color: var(--ink); }
  .upload-slot-sub { font-size: 10.5px; color: var(--slate); }

  /* ==================== USER PROFILE & FAVORITES VIEW ==================== */
  .profile-view {
    height: 100%;
    overflow-y: auto;
    padding: 26px 32px 48px 32px;
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  .profile-view h1, .profile-view h2 { font-family: var(--display); letter-spacing: -0.025em; }
  .profile-grid {
    display: grid;
    grid-template-columns: 330px 1fr;
    gap: 20px;
    align-items: start;
  }
  .profile-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 22px 24px;
    box-shadow: var(--shadow-md);
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  .profile-avatar-lg {
    width: 54px;
    height: 54px;
    border-radius: 999px;
    background: #18181B;
    color: #FFFFFF;
    font-family: var(--mono);
    font-size: 17px;
    font-weight: 800;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    border: 1px solid #18181B;
  }
  .profile-info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    padding: 9px 0;
    border-bottom: 1px solid var(--border-light);
    font-size: 12.5px;
  }
  .profile-info-row:last-child { border-bottom: none; }
  .req-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .req-sent-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-family: var(--mono);
    font-size: 10.5px;
    font-weight: 700;
    color: var(--charcoal);
    background: #F4F4F6;
    border: 1px solid var(--border);
    padding: 4px 10px;
    border-radius: 999px;
    white-space: nowrap;
  }
  .req-spec-line {
    font-size: 12px;
    font-weight: 600;
    color: var(--charcoal);
    background: #F8F9FA;
    border: 1px solid var(--border-light);
    border-radius: 10px;
    padding: 8px 12px;
    margin-top: 8px;
    line-height: 1.4;
  }
  .req-cancel-btn {
    border: 1px solid rgba(194, 24, 14, 0.32);
    background: var(--crimson-soft);
    color: var(--crimson);
    font-family: var(--sans);
    font-size: 12px;
    font-weight: 700;
    padding: 8px 16px;
    border-radius: 10px;
    cursor: pointer;
    white-space: nowrap;
    transition: background-color 0.16s ease, color 0.16s ease, border-color 0.16s ease;
  }
  .req-cancel-btn:hover {
    background: var(--crimson);
    color: #FFFFFF;
    border-color: var(--crimson);
  }
  .req-card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    border-top: 1px solid var(--border-light);
    padding-top: 12px;
    margin-top: 2px;
  }
  .req-overall-status-box {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: 10px;
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    color: #1E293B;
    font-family: var(--sans);
    font-size: 12px;
    font-weight: 700;
  }
  .req-overall-status-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: #D97706;
    flex-shrink: 0;
  }
  .req-sup-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
    background: #F8F9FA;
    border: 1px solid var(--border-light);
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 12px;
  }
  .req-status-pill {
    font-family: var(--mono);
    font-size: 9.5px;
    font-weight: 800;
    padding: 4px 9px;
    border-radius: 999px;
    background: var(--amber-soft);
    color: #92400E;
    border: 1px solid rgba(245, 158, 11, 0.35);
    white-space: nowrap;
  }
  .req-deadline-pill {
    font-family: var(--mono);
    font-size: 9.5px;
    font-weight: 700;
    padding: 4px 9px;
    border-radius: 999px;
    background: var(--crimson-soft);
    color: var(--crimson-dark);
    border: 1px solid rgba(194,24,14,0.22);
    white-space: nowrap;
  }

  /* ==================== V26 SELLORA + ESTORE + BRAND BROWN DESIGN SYSTEM ==================== */
  html, body {
    background: #34251B !important;
    background-image: none !important;
  }
  .view-container {
    background: #34251B !important;
  }
  .nav-back-btn {
    width: 30px;
    height: 30px;
    border-radius: 999px !important;
    border: none !important;
    background: #FFFFFF;
    color: var(--ink);
    font-weight: 800;
    font-size: 13px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.08);
    margin: 0 2px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
  .nav-back-btn:hover { background: #E4E4E7; color: var(--ink); }
  .nav-tab {
    border: none !important;
    border-radius: 999px !important;
    background: transparent !important;
    color: #64748B !important;
    height: 36px !important;
    padding: 0 16px !important;
    font-size: 12.5px !important;
    font-weight: 600 !important;
    gap: 7px !important;
    box-shadow: none !important;
  }
  .nav-tab:hover { color: #18181B !important; background: rgba(255,255,255,0.65) !important; }
  .nav-tab.active {
    background: #18181B !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 8px rgba(24,24,27,0.16) !important;
  }
  .nav-tab .step-tag {
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 700;
    opacity: 0.55;
    padding: 0 !important;
    border: none !important;
    background: transparent !important;
  }
  .nav-tab.active .step-tag { opacity: 0.72; color: #FFFFFF; }

  .hdr-right { display: flex; align-items: center; justify-content: flex-end; gap: 10px; justify-self: end; }
  .profile-hdr-btn {
    height: 38px;
    padding: 0 13px 0 5px;
    border-radius: 999px !important;
    border: 1px solid var(--border) !important;
    background: #FFFFFF !important;
    color: var(--ink) !important;
    box-shadow: none !important;
    gap: 8px;
    transition: border-color 0.16s ease, background-color 0.16s ease, color 0.16s ease, transform 0.14s ease, box-shadow 0.16s ease !important;
  }
  .profile-hdr-btn:hover {
    border-color: var(--crimson) !important;
    background: var(--crimson-soft) !important;
    color: var(--crimson) !important;
    transform: none !important;
    box-shadow: none !important;
  }
  .profile-hdr-btn:hover .profile-hdr-name {
    color: var(--crimson) !important;
  }
  .profile-avatar {
    border-radius: 999px !important;
    background: #18181B !important;
    color: #FFFFFF !important;
    width: 28px !important;
    height: 28px !important;
    font-size: 11px !important;
  }
  .profile-req-badge { border-radius: 999px !important; }

  /* Minimal Sellora + ESTORE Marketplace */
  .custom-vessel-stage {
    padding: 0 !important;
  }
  .catalog-view,
  .pillars-portal,
  .profile-view,
  .custom-vessel-inner {
    max-width: none !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 16px 24px 32px 24px !important;
  }
  .cat-header-minimal {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 18px;
    flex-wrap: wrap;
    border-bottom: 1px solid rgba(255, 255, 255, 0.18);
    padding-bottom: 14px;
    margin-bottom: 12px;
  }
  .cat-title-minimal {
    font-family: var(--display);
    font-size: 25px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.025em;
    line-height: 1.15;
    margin: 0;
  }
  .cat-sub-minimal {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.78);
    margin-top: 3px;
    margin-bottom: 0;
    font-weight: 500;
  }
  .cat-toolbar-minimal {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin: 0 0 12px 0;
    padding: 0;
    background: transparent !important;
    border: none !important;
  }
  .pillar-pills { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  .p-pill {
    border-radius: 999px !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    background: rgba(255, 255, 255, 0.96) !important;
    color: #18181B !important;
    padding: 8px 16px !important;
    font-size: 12.5px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    transition: background-color 0.16s ease, color 0.16s ease, border-color 0.16s ease !important;
  }
  .p-pill:hover {
    border-color: #FFFFFF !important;
    background: #FFFFFF !important;
    color: #18181B !important;
  }
  .p-pill.active {
    background: var(--crimson) !important;
    border-color: var(--crimson) !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.22) !important;
  }
  .p-pill.red-cta {
    background: #FFFFFF !important;
    border: 1px solid #FFFFFF !important;
    color: #34251B !important;
  }
  .p-pill.red-cta:hover {
    background: var(--crimson) !important;
    border-color: var(--crimson) !important;
    color: #FFFFFF !important;
    transform: none !important;
    box-shadow: none !important;
  }

  .cat-grid {
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    gap: 14px !important;
  }
  .cat-card {
    grid-column: auto !important;
    display: grid !important;
    grid-template-columns: 188px 1fr !important;
    align-items: stretch !important;
    background: #FFFFFF !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    padding: 12px !important;
    gap: 16px !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.14) !important;
    cursor: pointer;
    transition: none !important;
  }
  .cat-card:hover,
  .cat-card.selected {
    transform: none !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.14) !important;
    border-color: var(--border) !important;
  }
  .cat-stage {
    position: relative;
    background: linear-gradient(180deg, #F0F2F5 0%, #E5E8EE 100%);
    border-radius: 14px;
    width: 188px !important;
    height: 188px !important;
    min-height: 188px !important;
    aspect-ratio: 1 / 1;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 10px;
  }
  .cat-real-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
    transition: none !important;
    transform: none !important;
    filter: drop-shadow(0 12px 18px rgba(15, 23, 42, 0.12));
  }
  .cat-card:hover .cat-real-img {
    transform: none !important;
  }
  .cat-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }
  .fav-heart-btn {
    position: relative;
    top: auto;
    right: auto;
    width: 34px;
    height: 34px;
    flex-shrink: 0;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: #FFFFFF;
    color: #94A3B8;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: none;
    transition: color 0.16s ease, background-color 0.16s ease, border-color 0.16s ease;
    z-index: 4;
  }
  .fav-heart-btn:hover {
    transform: none;
    color: var(--crimson);
    border-color: rgba(194, 24, 14, 0.25);
  }
  .fav-heart-btn.active {
    color: var(--crimson);
    background: #FFF5F5;
    border-color: rgba(194, 24, 14, 0.28);
  }
  .fav-heart-btn.active svg {
    fill: var(--crimson);
    stroke: var(--crimson);
  }
  .cat-meta-body {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 0 4px 2px 4px;
    flex: 1;
  }
  .cat-meta-title {
    font-size: 14.5px;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.25;
    letter-spacing: -0.01em;
  }
  .vessel-specs-2col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 14px;
    padding-top: 8px;
    border-top: 1px solid var(--border-light);
  }
  .vspec-col {
    display: flex;
    flex-direction: column;
    gap: 5px;
    min-width: 0;
  }
  .vspec-row {
    display: flex;
    flex-direction: column;
    gap: 1px;
    min-width: 0;
  }
  .vspec-k {
    font-family: var(--mono);
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
  }
  .vspec-v {
    font-size: 11.5px;
    font-weight: 600;
    color: var(--ink);
    line-height: 1.25;
    word-break: break-word;
  }
  .cat-meta-footer {
    margin-top: auto;
    padding-top: 6px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
  }
  .cat-select-btn {
    border: 1px solid #D5DAE2;
    background: #FFFFFF;
    color: var(--ink);
    font-family: var(--sans);
    font-size: 12px;
    font-weight: 700;
    padding: 7px 18px;
    border-radius: 999px;
    cursor: pointer;
    transition: background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease;
  }
  .cat-select-btn:hover {
    background: var(--crimson) !important;
    border-color: var(--crimson) !important;
    color: #FFFFFF !important;
  }

  /* Minimal Profile Favorites Section */
  .fav-prof-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
  }
  .fav-prof-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 12px;
    display: grid;
    grid-template-columns: 168px 1fr;
    align-items: stretch;
    gap: 14px;
    box-shadow: var(--shadow-sm);
  }
  .fav-prof-stage {
    position: relative;
    background: linear-gradient(180deg, #F0F2F5 0%, #E5E8EE 100%);
    border-radius: 12px;
    width: 168px;
    height: 168px;
    min-height: 168px;
    aspect-ratio: 1 / 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
    overflow: hidden;
  }
  .verified-seal {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  /* Studio 3D Modern Rounded Surfaces */
  .studio-grid {
    background: #34251B !important;
    grid-template-columns: 300px minmax(460px, 1fr) 304px !important;
    gap: 12px !important;
    padding: 12px !important;
  }
  .dock-left, .dock-right {
    background: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18) !important;
    overflow: hidden !important;
  }
  .dock-left .dock-header, .dock-right .dock-header {
    background: #FFFFFF !important;
    border-bottom: 1px solid var(--border-light) !important;
  }
  .viewport-stage {
    background: radial-gradient(circle at 50% 44%, #FFFFFF 0%, #F4F4F6 68%, #ECEEF2 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18) !important;
  }
  .viewport-stage.dark-studio {
    background: radial-gradient(circle at 50% 42%, #23252C 0%, #141519 72%, #0B0C0F 100%) !important;
  }
  .inspector-tabs {
    background: #F4F4F6 !important;
    border-bottom: 1px solid var(--border-light) !important;
    padding: 6px !important;
    gap: 6px !important;
  }
  .itab {
    border: none !important;
    border-radius: 999px !important;
    background: transparent !important;
    color: var(--slate) !important;
    font-weight: 600 !important;
    font-size: 12px !important;
    padding: 7px 10px !important;
  }
  .itab.active {
    background: #18181B !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 6px rgba(24,24,27,0.12) !important;
  }
  .spec-tag {
    border-radius: 999px !important;
    padding: 3px 10px !important;
    font-weight: 700 !important;
  }
  /* Uniform Rounded Shape & Faded-Red ("Rosso Sbiadito") Interaction Across Left Sidebar */
  .dock-left .prod-item,
  .dock-left .opt-pill,
  .dock-left .qty-btn {
    border: 1.5px solid var(--border) !important;
    border-radius: 14px !important;
    background: #FFFFFF !important;
    color: var(--ink) !important;
    box-shadow: none !important;
    transform: none !important;
    transition: background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease !important;
  }
  .dock-left .prod-item:hover:not(:disabled):not(.disabled),
  .dock-left .opt-pill:hover:not(:disabled):not(.disabled),
  .dock-left .qty-btn:hover:not(:disabled):not(.disabled) {
    background: var(--crimson-soft) !important;
    border-color: rgba(194, 24, 14, 0.45) !important;
    color: var(--ink) !important;
    transform: none !important;
    box-shadow: none !important;
  }
  .dock-left .prod-item.active,
  .dock-left .prod-item.selected,
  .dock-left .prod-item.clash-active,
  .dock-left .opt-pill.active,
  .dock-left .opt-pill.selected,
  .dock-left .qty-btn.active {
    background: var(--crimson-soft) !important;
    border: 1.5px solid var(--crimson) !important;
    color: var(--ink) !important;
    box-shadow: none !important;
  }
  .dock-left .opt-pill.active small,
  .dock-left .opt-pill.selected small,
  .dock-left .prod-item.active .prod-meta,
  .dock-left .qty-btn.active small {
    color: var(--charcoal) !important;
  }
  .dock-left .prod-item.active .prod-title,
  .dock-left .opt-pill.active,
  .dock-left .qty-btn.active {
    color: var(--crimson-dark) !important;
  }
  .dock-left #btnAddCustomGraphic {
    border-radius: 14px !important;
    border: 1.5px solid var(--border) !important;
    background: #FFFFFF !important;
    color: var(--ink) !important;
    box-shadow: none !important;
    transform: none !important;
    transition: background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease !important;
  }
  .dock-left #btnAddCustomGraphic:hover:not(:disabled) {
    background: var(--crimson-soft) !important;
    border-color: rgba(194, 24, 14, 0.45) !important;
    color: var(--crimson-dark) !important;
    transform: none !important;
  }
  .box-preview-card {
    border-radius: 14px !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
  }
  .diag-card.weight-red {
    border-radius: 14px !important;
    border: 1px solid var(--crimson-dark) !important;
    box-shadow: none !important;
  }
  .swatch-btn {
    border-radius: 14px !important;
    border: 1.5px solid var(--border) !important;
  }
  .swatch-btn.selected, .swatch-btn.active {
    border: 1.5px solid var(--crimson) !important;
    background: var(--crimson-soft) !important;
    box-shadow: none !important;
  }
  .floating-hud-top {
    left: 14px !important;
    right: 14px !important;
    padding: 0 !important;
    gap: 8px !important;
    justify-content: space-between !important;
    flex-wrap: nowrap !important;
  }
  .floating-hud-top .hud-group {
    background: rgba(255, 255, 255, 0.94) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(229, 231, 235, 0.95) !important;
    border-radius: 999px !important;
    padding: 4px !important;
    gap: 3px !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08) !important;
  }
  .hud-chip {
    border-radius: 999px !important;
    border: none !important;
    background: transparent !important;
    color: var(--ink) !important;
    padding: 5.5px 9px !important;
    font-size: 10.2px !important;
    gap: 4px !important;
  }
  .hud-chip.info-chip {
    width: 24px !important;
    height: 24px !important;
    padding: 0 !important;
    border-radius: 999px !important;
    border: 1px solid var(--border) !important;
  }
  .hud-chip:hover:not(:disabled) { background: #F4F4F6 !important; transform: none !important; }
  .hud-chip.active {
    background: #18181B !important;
    color: #FFFFFF !important;
    box-shadow: none !important;
  }
  .hud-chip.active:hover:not(:disabled) {
    background: #18181B !important;
    color: #FFFFFF !important;
  }
  .hud-chip.active-green { background: var(--green) !important; color: #FFFFFF !important; }
  .hud-chip.active-amber { background: var(--amber) !important; color: #FFFFFF !important; }
  .hud-chip.active-red { background: var(--crimson) !important; color: #FFFFFF !important; }
  .pin-card {
    background: rgba(255, 255, 255, 0.94) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06) !important;
  }
  .vessel-info-popover {
    width: 356px !important;
    border: 1px solid var(--border) !important;
    border-radius: 18px !important;
    box-shadow: var(--shadow-lg) !important;
  }
  .drag-toast {
    border-radius: 999px !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.16) !important;
  }
  .traffic-banner {
    margin: 10px 12px 0 12px !important;
    padding: 10px 14px !important;
    height: 80px !important;
    min-height: 80px !important;
    max-height: 80px !important;
    flex-shrink: 0 !important;
    border-radius: 14px !important;
    border: 1px solid rgba(20, 122, 59, 0.22) !important;
    box-shadow: none !important;
    overflow: hidden !important;
  }
  .traffic-banner.y { border-color: rgba(229, 160, 0, 0.35) !important; }
  .traffic-banner.r { border-color: rgba(194, 24, 14, 0.30) !important; }
  .tl-status-title {
    overflow: visible !important;
    text-overflow: unset !important;
    font-size: 13px !important;
  }
  .tl-desc {
    height: 28px !important;
    min-height: 28px !important;
    max-height: 28px !important;
    font-size: 10.5px !important;
    line-height: 14px !important;
    overflow: hidden !important;
    margin-bottom: 0 !important;
  }
  .diag-scroll {
    flex: 1 1 0 !important;
    min-height: 0 !important;
    padding: 10px 12px !important;
    display: flex !important;
    flex-direction: column !important;
    overflow-y: auto !important;
  }
  .diag-board {
    flex: 1 1 auto !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 9px !important;
    border: none !important;
    background: transparent !important;
    padding: 0 !important;
  }
  .diag-row {
    flex: 1 1 0 !important;
    min-height: 92px !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    background: #FFFFFF !important;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03) !important;
    overflow: hidden !important;
  }
  .diag-body {
    padding: 10px 12px !important;
    gap: 3px !important;
  }
  .diag-card-s {
    font-size: 11px !important;
    line-height: 1.32 !important;
  }
  .checkout-footer {
    border-top: 1px solid var(--border-light) !important;
    background: #FFFFFF !important;
    height: auto !important;
    min-height: 142px !important;
    padding: 14px 16px 16px 16px !important;
    gap: 8px !important;
  }
  .checkout-footer .sec-hdr {
    display: flex !important;
    flex-wrap: wrap !important;
    justify-content: space-between !important;
    align-items: baseline !important;
    height: auto !important;
    line-height: 1.35 !important;
    margin-bottom: 4px !important;
    gap: 4px 10px !important;
    font-size: 9.5px !important;
  }
  .cta-btn {
    border-radius: 999px !important;
    border: 1px solid var(--crimson) !important;
    box-shadow: 0 4px 14px rgba(194, 24, 14, 0.16) !important;
    font-weight: 700 !important;
  }
  .cta-btn.white {
    background: #FFFFFF !important;
    border: 1px solid var(--border) !important;
    color: var(--ink) !important;
    box-shadow: none !important;
  }
  .cta-btn.white:hover { background: #F4F4F6 !important; border-color: #CBD5E1 !important; }

  /* Filiera & Modals Rounded Minimal */
  .filiera-stepper {
    background: #FFFFFF !important;
    border: 1px solid var(--border) !important;
    border-radius: 999px !important;
    padding: 5px !important;
    box-shadow: var(--shadow-sm) !important;
  }
  .fstep-pill {
    border-radius: 999px !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
  }
  .fstep-pill.active {
    background: #18181B !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(24,24,27,0.16) !important;
  }
  .fstep-pill.active .fstep-num {
    background: rgba(255,255,255,0.22) !important;
    color: #FFFFFF !important;
  }
  .fstep-pill.done {
    background: var(--green-soft) !important;
    color: var(--green) !important;
  }
  .meta-tag, .rating-pill {
    border-radius: 999px !important;
    padding: 3px 10px !important;
  }
  .filiera-confirmed-bar, .filiera-stage-card {
    background: #FFFFFF !important;
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16) !important;
  }
  .supplier-rich-opt, .filling-mode-card {
    border: 1.5px solid var(--border) !important;
    border-radius: 14px !important;
    box-shadow: none !important;
    transition: background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease !important;
  }
  .supplier-rich-opt:hover:not(:disabled),
  .filling-mode-card:hover:not(:disabled) {
    background: var(--crimson-soft) !important;
    border-color: rgba(194, 24, 14, 0.45) !important;
  }
  .supplier-rich-opt.selected,
  .filling-mode-card.selected,
  .filling-mode-card.active {
    background: var(--crimson-soft) !important;
    border: 1.5px solid var(--crimson) !important;
  }
  .fill-types-grid .qty-btn {
    border-radius: 14px !important;
    border: 1.5px solid var(--border) !important;
    background: #FFFFFF !important;
    color: var(--ink) !important;
    box-shadow: none !important;
    transform: none !important;
  }
  .fill-types-grid .qty-btn:hover:not(:disabled):not(.disabled) {
    background: var(--crimson-soft) !important;
    border-color: rgba(194, 24, 14, 0.45) !important;
  }
  .fill-types-grid .qty-btn.active {
    background: var(--crimson-soft) !important;
    border-color: var(--crimson) !important;
    color: var(--crimson-dark) !important;
  }
  .filling-box {
    border-radius: 14px !important;
    border: 1px dashed var(--border) !important;
    background: #F8FAFC !important;
  }
  .summary-strip-3 > div, .cost-pill-card {
    border-radius: 14px !important;
    border: 1px solid var(--border-light) !important;
  }
  .modal-card {
    border: 1px solid var(--border) !important;
    border-radius: 22px !important;
    box-shadow: var(--shadow-lg) !important;
  }
  .profile-card {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16) !important;
  }
  .brown-hdr-bar {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 1px solid rgba(255, 255, 255, 0.18);
    padding-bottom: 14px;
    gap: 12px;
    flex-wrap: wrap;
  }
  .brown-hdr-kicker {
    font-size: 11px;
    font-weight: 800;
    color: #FCA5A5;
    letter-spacing: 0.12em;
  }
  .brown-hdr-title {
    font-family: var(--display);
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.025em;
    line-height: 1.15;
    margin: 0;
    color: #FFFFFF;
  }
  .brown-hdr-muted {
    font-size: 10px;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.72);
    letter-spacing: 0.08em;
  }
  .brown-hdr-total {
    font-family: var(--mono);
    font-size: 20px;
    font-weight: 800;
    color: #FFFFFF;
  }

  /* ==================== RESPONSIVE: NON-FULLSCREEN CHROME, TABLET & MOBILE ==================== */
  @media (max-width: 1460px) {
    .hud-chip { padding: 4.5px 6.5px; font-size: 9.5px; gap: 3px; }
    .hud-chip svg { width: 11px; height: 11px; }
  }
  @media (max-width: 1280px) {
    .studio-grid {
      grid-template-columns: 300px minmax(340px, 1fr) 310px;
    }
    .app-header { padding: 0 18px; }
    .nav-tab { padding: 0 12px !important; font-size: 11.5px !important; }
    .dock-scroll { padding: 12px; }
    .floating-hud-top {
      justify-content: space-between !important;
      gap: 4px !important;
    }
    .hud-chip { padding: 4px 5.5px !important; font-size: 9px !important; gap: 3px !important; }
    .hud-chip svg { width: 11px; height: 11px; }
    .drag-toast { left: 50%; font-size: 9.5px; padding: 5px 10px; }
    .filiera-locked-red-text { white-space: normal; }
    .fstep-pill { font-size: 10px; padding: 7px 5px; }
    .pillars-portal, .catalog-view, .profile-view, .custom-vessel-inner { padding: 16px 24px 32px 24px !important; }
    .cat-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
  }

  @media (max-width: 1024px) {
    html, body {
      height: auto !important;
      min-height: 100% !important;
      overflow-y: auto !important;
      overflow-x: clip !important;
    }
    .app-header {
      position: fixed !important;
      top: 0 !important;
      left: 0 !important;
      right: 0 !important;
      width: 100% !important;
      height: 58px !important;
      min-height: 58px !important;
      padding: 8px 14px !important;
      grid-template-columns: auto 1fr auto;
      gap: 8px;
      z-index: 1200 !important;
    }
    body {
      padding-top: 58px !important;
    }
    .view-container {
      height: auto !important;
      min-height: calc(100vh - 58px) !important;
      width: 100% !important;
    }
    .studio-grid {
      height: auto !important;
      width: 100% !important;
      grid-template-columns: 1fr 1fr !important;
      grid-template-rows: 460px auto !important;
    }
    .viewport-stage {
      grid-column: 1 / -1;
      grid-row: 1;
      height: 460px;
      width: 100% !important;
    }
    .dock-left {
      grid-column: 1;
      grid-row: 2;
      height: auto !important;
      overflow: visible !important;
    }
    .dock-right {
      grid-column: 2;
      grid-row: 2;
      height: auto !important;
      overflow: visible !important;
    }
    .dock-scroll, .diag-scroll { overflow-y: visible !important; }
    .diag-row { flex: none !important; min-height: 86px !important; height: auto !important; }
    .checkout-footer { height: auto !important; gap: 10px; }
    .cat-grid { grid-template-columns: 1fr !important; }
    .fav-prof-grid { grid-template-columns: 1fr !important; }
    .profile-grid { grid-template-columns: 1fr; }
    .custom-blueprint-grid { grid-template-columns: 1fr; }
    .custom-bp-left { border-right: none; border-bottom: 1px solid var(--border-light); padding-right: 0; padding-bottom: 16px; }
    .filiera-stepper { flex-wrap: wrap; border-radius: 16px !important; }
    .fstep-pill { flex: 1 1 calc(33% - 8px); }
    .summary-strip-3 { flex-wrap: wrap; }
    .upload-slot-grid { grid-template-columns: repeat(2, 1fr); }
    .catalog-view, .pillars-portal, .profile-view, .custom-vessel-stage { height: auto !important; overflow-y: visible !important; }
  }

  @media (max-width: 768px) {
    body {
      padding-top: 56px !important;
    }
    .app-header {
      position: fixed !important;
      top: 0 !important;
      left: 0 !important;
      right: 0 !important;
      width: 100% !important;
      height: 56px !important;
      min-height: 56px !important;
      padding: 0 14px !important;
      display: flex !important;
      justify-content: space-between !important;
      align-items: center !important;
      gap: 10px !important;
      z-index: 1200 !important;
    }
    .brand-area { margin: 0 !important; }
    .brand-area img { height: 22px !important; }
    .nav-tabs { display: none !important; }
    .hdr-right { margin-left: auto !important; }
    .profile-hdr-name,
    .profile-req-badge { display: none !important; }
    .profile-hdr-btn {
      padding: 0 !important;
      width: 34px !important;
      height: 34px !important;
      min-width: 34px !important;
      border-radius: 999px !important;
      border: none !important;
      background: transparent !important;
      box-shadow: none !important;
      display: inline-flex !important;
      align-items: center !important;
      justify-content: center !important;
    }
    .profile-hdr-btn:hover {
      background: transparent !important;
      border-color: transparent !important;
    }
    .profile-avatar {
      width: 34px !important;
      height: 34px !important;
      font-size: 12px !important;
    }

    /* Marketplace mobile: clear separation of Custom Container CTA + vertical portrait stage */
    .catalog-view,
    .pillars-portal,
    .profile-view,
    .custom-vessel-inner {
      padding: 14px 12px 28px 12px !important;
    }
    .cat-toolbar-minimal {
      flex-direction: column !important;
      align-items: stretch !important;
      gap: 10px !important;
      margin-bottom: 14px !important;
    }
    .p-pill.red-cta {
      width: 100% !important;
      margin-left: 0 !important;
      background: var(--crimson) !important;
      color: #FFFFFF !important;
      border: 1.5px solid rgba(255, 255, 255, 0.34) !important;
      border-radius: 12px !important;
      padding: 11px 16px !important;
      font-size: 13px !important;
      font-weight: 700 !important;
      text-align: center !important;
      justify-content: center !important;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.22) !important;
    }
    .cat-card, .cat-card:only-child, .fav-prof-card {
      grid-template-columns: 122px 1fr !important;
      align-items: stretch !important;
      gap: 12px !important;
    }
    .cat-stage, .fav-prof-stage {
      width: 122px !important;
      height: auto !important;
      min-height: 198px !important;
      aspect-ratio: auto !important;
      align-self: stretch !important;
      padding: 8px 6px !important;
    }
    .cat-thumb { width: 100%; height: 148px; min-height: 148px; border-right: none; border-bottom: 1.5px solid var(--ink); }
    .cat-card-header-flex { flex-direction: column !important; }
    .cat-filter-bar { flex-direction: column; align-items: stretch; }

    /* Studio 3D mobile: full width, zero right brown strip, taller 440px stage, centered compact top HUD */
    .studio-grid {
      display: flex !important;
      flex-direction: column !important;
      width: 100% !important;
      max-width: 100% !important;
      height: auto !important;
      padding: 10px 12px 24px 12px !important;
      gap: 12px !important;
    }
    .viewport-stage {
      order: 1 !important;
      width: 100% !important;
      height: 440px !important;
      min-height: 440px !important;
      flex-shrink: 0 !important;
    }
    .dock-left {
      order: 2 !important;
      width: 100% !important;
      height: auto !important;
      overflow: visible !important;
    }
    .dock-right {
      order: 3 !important;
      width: 100% !important;
      height: auto !important;
      overflow: visible !important;
    }
    .floating-hud-top {
      top: 10px !important;
      left: 10px !important;
      right: 10px !important;
      flex-direction: row !important;
      justify-content: center !important;
      align-items: center !important;
      gap: 0 !important;
    }
    .floating-hud-top .hud-group:nth-child(2),
    #btnShowAR {
      display: none !important;
    }
    .floating-hud-top .hud-group:first-child {
      margin: 0 auto !important;
      justify-content: center !important;
      flex-wrap: nowrap !important;
      width: auto !important;
    }
    .vessel-info-popover {
      width: calc(100% - 20px) !important;
      left: 10px !important;
      right: 10px !important;
      top: 56px !important;
    }
    .traffic-banner {
      height: auto !important;
      min-height: 76px !important;
      max-height: none !important;
    }
    .tl-desc {
      height: auto !important;
      min-height: 24px !important;
      max-height: none !important;
    }
    .pin-card { font-size: 9.5px; padding: 3px 6px; }
    .pin-sub { font-size: 8.5px; }
    .drag-toast { display: none; }
    .cat-hero-title { font-size: 24px; }

    /* Filiera mobile: left-aligned top total, left-aligned step pills, left-aligned final total above centered CTA buttons */
    .brown-hdr-total-wrap {
      width: 100% !important;
      text-align: left !important;
    }
    .fstep-pill {
      flex: 1 1 calc(50% - 6px) !important;
      justify-content: flex-start !important;
      text-align: left !important;
      padding: 8px 10px !important;
    }
    .supplier-rich-opt { flex-direction: column; align-items: flex-start; }
    .supplier-rich-right { flex-direction: row; align-items: center; justify-content: space-between; width: 100%; }
    .filling-mode-grid { grid-template-columns: 1fr; }
    .fill-types-grid { grid-template-columns: repeat(2, 1fr) !important; }
    .summary-grid-2 { grid-template-columns: 1fr !important; }
    .filiera-nav-row { flex-direction: column-reverse; align-items: stretch; }
    .filiera-nav-row .cta-btn { width: 100% !important; min-width: 0 !important; }
    .filiera-final-nav-row {
      flex-direction: column !important;
      align-items: flex-start !important;
      gap: 14px !important;
    }
    .filiera-final-total-box {
      width: 100% !important;
      text-align: left !important;
      align-items: flex-start !important;
    }
    .filiera-final-actions {
      width: 100% !important;
      margin-left: 0 !important;
      display: flex !important;
      justify-content: center !important;
      align-items: center !important;
      gap: 10px !important;
      flex-wrap: nowrap !important;
    }
    .filiera-final-actions .cta-btn {
      width: auto !important;
      min-width: 136px !important;
      flex: 0 1 auto !important;
      padding: 0 18px !important;
    }
    .summary-strip-3 > div:last-child { width: 100%; flex-direction: column-reverse; }
    .summary-strip-3 .cta-btn { width: 100% !important; min-width: 0 !important; }
    .upload-slot-grid { grid-template-columns: 1fr; }
    .modal-card { padding: 16px; }
  }
</style>
</head>
<body>

<!-- ==================== TOP HEADER ==================== -->
<header class="app-header">
  <div class="brand-area" style="cursor:pointer;" onclick="returnToMarketplaceAfterSubmit(true)">
    <img src="__VC_LOGO__" alt="VesselCove">
  </div>

  <nav class="nav-tabs">
    <button class="nav-back-btn" id="navBackBtn" onclick="goStepBack()" title="Indietro">&lt;</button>
    <button class="nav-tab active" id="navCatalog" type="button">
      <span class="step-tag">01</span><span id="ui_nav_catalog">Marketplace</span>
    </button>
    <button class="nav-tab" id="navStudio" type="button">
      <span class="step-tag">02</span><span id="ui_nav_studio">Studio 3D</span>
    </button>
    <button class="nav-tab" id="navPillars" type="button">
      <span class="step-tag">03</span><span id="ui_nav_pillars">Filiera</span>
    </button>
  </nav>

  <div class="hdr-right">
    <button class="profile-hdr-btn" id="btnProfile" onclick="openProfileView()" title="Profilo">
      <span class="profile-avatar">TL</span>
      <span class="profile-hdr-name" id="ui_profile_name">Thomas Lutaj</span>
      <span class="profile-req-badge" id="profileReqBadge">0</span>
    </button>
  </div>
</header>

<!-- ==================== VIEW 01: CONTAINER MARKETPLACE ==================== -->
<div class="view-container active" id="viewCatalog">
  <div class="catalog-view">
    <div class="cat-header-minimal">
      <div>
        <h1 class="cat-title-minimal" id="ui_cat_title">Marketplace Contenitori</h1>
        <p class="cat-sub-minimal" id="ui_cat_stat">Scegli il contenitore per avviare lo Studio 3D</p>
      </div>
    </div>

    <div class="cat-toolbar-minimal">
      <div class="pillar-pills" id="catPillarPills"></div>
      <button class="p-pill red-cta" id="btnCustomVessel" onclick="openCustomVesselStudio()">Continua con il mio contenitore</button>
    </div>

    <div class="cat-grid" id="catGrid"></div>
  </div>
</div>

<!-- ==================== VIEW 02: 3D PARAMETRIC STUDIO ==================== -->
<div class="view-container" id="viewStudio">
  <div class="custom-vessel-stage" id="customVesselStage" style="display:none;"></div>
  <div class="studio-grid" id="studioGridMain">

    <!-- LEFT INSPECTOR -->
    <aside class="dock-left">
      <div class="inspector-tabs" id="inspectorTabs">
        <button class="insp-tab active" id="itab1" onclick="setInspTab(1)">
          <span class="t-num" id="ui_tnum1">PASSO 01</span>
          <span class="t-lbl" id="ui_itab1">Chiusura</span>
        </button>
        <button class="insp-tab" id="itab2" onclick="setInspTab(2)">
          <span class="t-num" id="ui_tnum2">PASSO 02</span>
          <span class="t-lbl" id="ui_itab2">Rivestimento</span>
        </button>
        <button class="insp-tab" id="itab3" onclick="setInspTab(3)">
          <span class="t-num" id="ui_tnum3">PASSO 03</span>
          <span class="t-lbl" id="ui_itab3">Imballaggio</span>
        </button>
      </div>

      <div class="dock-scroll" id="inspectorBody"></div>
    </aside>

    <!-- CENTER 3D WEBGL VIEWPORT -->
    <main class="viewport-stage" id="viewportStage">
      <div class="floating-hud-top">
        <div class="hud-group">
          <button class="hud-chip info-chip" id="btnVesselInfo" onclick="toggleVesselInfoPopover()" title="Scheda tecnica">i</button>
          <span class="hud-divider"></span>
          <button class="hud-chip accent-tool active" id="toolOrbit" onclick="setPointerTool('orbit')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3.6 9h16.8"/><path d="M3.6 15h16.8"/><path d="M12 3a14 14 0 0 0 0 18"/><path d="M12 3a14 14 0 0 1 0 18"/></svg>
            <span id="ui_tool_orbit">Ruota 3D</span>
          </button>
          <button class="hud-chip accent-tool" id="toolSleeve" onclick="setPointerTool('sleeve')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><path d="M8 7l4-4 4 4"/><path d="M8 17l4 4 4-4"/><rect x="5" y="9" width="14" height="6" rx="1.5"/></svg>
            <span id="ui_tool_sleeve">Sposta Sleeve</span>
          </button>
          <button class="hud-chip" id="btnShowAR" onclick="toggleARModal(true)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 8V5a1 1 0 0 1 1-1h3"/><path d="M16 4h3a1 1 0 0 1 1 1v3"/>
              <path d="M4 16v3a1 1 0 0 0 1 1h3"/><path d="M16 20h3a1 1 0 0 0 1-1v-3"/>
              <rect x="8.5" y="8.5" width="7" height="7" rx="1"/>
              <line x1="12" y1="8.5" x2="12" y2="15.5"/><line x1="8.5" y1="12" x2="15.5" y2="12"/>
            </svg>
            <span id="ui_btn_ar">Vedi in AR</span>
          </button>
        </div>

        <div class="hud-group">
          <button class="hud-chip" id="btnExplode" onclick="toggle3DFlag('exploded')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 20 6.5 12 11 4 6.5 12 2"/><polyline points="4 12 12 16.5 20 12"/><polyline points="4 17.5 12 22 20 17.5"/></svg>
            <span id="ui_btn_explode">Vista Esplosa</span>
          </button>
          <button class="hud-chip" id="btnHeatmap" onclick="toggle3DFlag('heatmap')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 1 1 4 0Z"/><line x1="12" y1="14" x2="12" y2="9"/></svg>
            <span id="ui_btn_heat">Mappa TD%</span>
          </button>
          <button class="hud-chip" id="btnWire" onclick="toggle3DFlag('wireframe')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
            <span id="ui_btn_wire">Mesh CAD</span>
          </button>
          <span class="hud-divider"></span>
          <button class="hud-chip icon-only" id="btnDarkBg" onclick="toggle3DFlag('darkStudio')" title="Tema Studio">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
          </button>
        </div>
      </div>

      <div class="vessel-info-popover" id="vesselInfoPopover"></div>

      <div class="ar-qr-overlay" id="arQrOverlay" onclick="if(event.target===this) toggleARModal(false)">
        <div class="ar-qr-card" id="arQrCard"></div>
      </div>

      <div class="drag-toast" id="dragToast">
        <span class="pulse-dot"></span>
        <span id="ui_drag_toast">Trascina per ruotare il modello 3D a 360° · Rotella mouse per zoom</span>
      </div>

      <canvas id="webglCanvas"></canvas>

      <!-- DYNAMIC 3D PIN OVERLAYS -->
      <div class="pin-overlay" id="pinNeck">
        <div class="pin-card ok" id="pinNeckCard">
          <span id="pinNeckTitle">24/410 LOCK OK</span>
          <span class="pin-sub" id="pinNeckSub">Filetto e tenuta validati</span>
          <span class="pin-dim" id="pinNeckDim">Dimensioni: Ø 28 × H 46 mm</span>
        </div>
      </div>

      <div class="pin-overlay" id="pinSleeve">
        <div class="pin-card ok" id="pinSleeveCard">
          <span id="pinSlTitle">SLEEVE 3D · GRADE A</span>
          <span class="pin-sub" id="pinSlSub">Scritte su corpo piano · 0°</span>
          <span class="pin-dim" id="pinSlDim">Dimensioni: 170 × 82 mm</span>
        </div>
      </div>

      <div class="pin-overlay" id="pinBarcode">
        <div class="pin-card ok" id="pinBarcodeCard">
          <span id="pinBcTitle">EAN-13 · GRADE A</span>
          <span class="pin-sub" id="pinBcSub">Zona cilindrica piana · 180°</span>
          <span class="pin-dim" id="pinBcDim">Dimensioni: 37 × 26 mm</span>
        </div>
      </div>
    </main>

    <!-- RIGHT DIAGNOSTIC & SEMAFORO COLUMN (ZERO SUPPLY LIST, ZERO JUMP) -->
    <aside class="dock-right">
      <div class="traffic-banner g" id="tlBanner">
        <div class="tl-top">
          <div class="tl-status-title" id="tlTitle">COMPATIBILE · VALIDATO IN 3D</div>
          <div class="tl-lights">
            <span class="tl-bulb r" id="bulbR"></span>
            <span class="tl-bulb y" id="bulbY"></span>
            <span class="tl-bulb g active" id="bulbG"></span>
          </div>
        </div>
        <div class="tl-desc" id="tlDesc"></div>
      </div>

      <div class="diag-scroll" id="diagDetails"></div>

      <div class="checkout-footer">
        <div class="sec-hdr">
          <span id="ui_chk_hdr">PREZZO DI PARTENZA PROVA PRE-SERIE</span>
          <span style="font-size:10px; color:var(--espresso);" id="ui_ship_note">Spedizioni escluse</span>
        </div>
        <div class="start-price-hero" id="val_sp_lot">Da €1,080</div>
        <button class="cta-btn" id="btnCheckout" onclick="proceedToPillars()"></button>
      </div>
    </aside>

  </div>
</div>

<!-- ==================== VIEW 03: 6-PILLAR COMPOSITION & SUPPLY CHAIN ==================== -->
<div class="view-container" id="viewPillars">
  <div class="pillars-portal" id="pillarsPortalBody"></div>
</div>

<!-- ==================== VIEW 04: USER PROFILE & SUBMITTED REQUESTS ==================== -->
<div class="view-container" id="viewProfile">
  <div class="profile-view" id="profilePortalBody"></div>
</div>

<!-- ==================== CHECKOUT MODAL ==================== -->
<div class="modal-mask" id="checkoutModal">
  <div class="modal-card" id="checkoutModalBody"></div>
</div>

<script>
__THREE_JS__
</script>
<script>
// ==================== BILINGUAL DICTIONARY ====================
const TXT = {
  it: {
    navCatalog: "Marketplace",
    navStudio: "Studio 3D",
    navPillars: "Filiera",
    itab1: "Chiusura",
    itab2: "Rivestimento",
    itab3: "Imballaggio",
    toolOrbit: "Ruota 3D",
    toolSleeve: "Sposta Sleeve",
    toolLabel: "Sposta Etichetta",
    toolBc: "Sposta Barcode",
    btnExplode: "Vista Esplosa",
    btnExplodeLocked: "Vista Esplosa 🔒",
    backTitle: "Torna allo step precedente",
    btnHeat: "Mappa TD%",
    btnWire: "Mesh CAD",
    dragToastOrbit: "Trascina per ruotare il modello 3D a 360° · Rotella mouse per zoom",
    chkHdr: "PREZZO DI PARTENZA PROVA PRE-SERIE",
    shipNote: "Spedizioni escluse",
    ctaOk: "Conferma",
    ctaWarn: "Conferma con avviso",
    ctaBlock: "Risolvi errori",
    tlGreenT: "COMPATIBILE · VALIDATO 3D",
    tlGreenD: "Tutti gli elementi configurati rispettano i limiti fisici.",
    tlAmberT: "AVVISO TECNICO",
    tlAmberD: "Elemento su spalla curva, margine saldatura o grinza etichetta: richiesta verifica.",
    tlRedT: "BLOCCO FISICO",
    tlRedD: "Incompatibilità meccanica o distorsione oltre limite fisico: correggi prima di procedere.",
    chk1: "Accoppiamento Chiusura",
    chk2: "Tenuta Rivestimento e Grafica",
    chk3: "Scannabilità Barcode"
  },
  en: {
    navCatalog: "Marketplace",
    navStudio: "3D Studio",
    navPillars: "Supply Chain",
    itab1: "Closure",
    itab2: "Wrap",
    itab3: "Packaging",
    toolOrbit: "Orbit 3D",
    toolSleeve: "Drag Sleeve",
    toolLabel: "Drag Label",
    toolBc: "Drag Barcode",
    btnExplode: "Exploded View",
    btnExplodeLocked: "Exploded View 🔒",
    backTitle: "Back to previous step",
    btnHeat: "TD% Map",
    btnWire: "CAD Mesh",
    dragToastOrbit: "Drag to orbit the 3D vessel 360° · Scroll to zoom",
    chkHdr: "STARTING PRE-SERIES TRIAL PRICE",
    shipNote: "Shipping excluded",
    ctaOk: "Confirm",
    ctaWarn: "Confirm with warning",
    ctaBlock: "Resolve errors",
    tlGreenT: "COMPATIBLE · 3D VALIDATED",
    tlGreenD: "All configured elements meet physical tolerances.",
    tlAmberT: "TECHNICAL WARNING",
    tlAmberD: "Artwork or barcode enters curve, heat-seal margin or wrinkle threshold: check required.",
    tlRedT: "PHYSICAL BLOCK",
    tlRedD: "Mechanical closure mismatch or warp past physical threshold: fix before continuing.",
    chk1: "Closure and Seal Fit",
    chk2: "Wrap and Graphic Integrity",
    chk3: "Barcode Readability"
  }
};

// ==================== CATALOG OF REAL 3D VESSELS (RIGID ENGINE A + FLEXIBLE ENGINE B) ====================
const VESSELS = [
  {
    id: "serum_250",
    engine: "A",
    catGroup: "cylindrical",
    neck: "24/410",
    shape: "cyl_tall",
    vol: "250 ml",
    matIt: "PET Lucido",
    matEn: "Glossy PET",
    hMm: 158, wMm: 54, dMm: 54,
    weightG: 265,
    maxShoulderTD: 58,
    defaultFinish: "pet_gloss",
    defaultWrap: "sleeve",
    liquidColor: "#DCEEF8",
    vendor: "PoliPlast Lombardia Srl (BG)",
    it: "Flacone Cilindrico 250 ml in PET Lucido",
    en: "250 ml Cylindrical Bottle in Glossy PET",
    subIt: "Ø 54 × H 158 mm",
    subEn: "Ø 54 × H 158 mm",
    badgeIt: "FLACONE CILINDRICO",
    badgeEn: "CYLINDRICAL BOTTLE"
  },
  {
    id: "square_500",
    engine: "A",
    catGroup: "square",
    neck: "28/410",
    shape: "square_soft",
    vol: "500 ml",
    matIt: "HDPE Opaco",
    matEn: "Matte HDPE",
    hMm: 184, wMm: 72, dMm: 58,
    weightG: 530,
    maxShoulderTD: 56,
    defaultFinish: "hdpe_white",
    defaultWrap: "sleeve",
    liquidColor: "#D8EFE6",
    vendor: "Emilia BlowMold SpA (BO)",
    it: "Flacone Quadro 500 ml in HDPE Opaco",
    en: "500 ml Square Bottle in Matte HDPE",
    subIt: "72 × 58 × 184 mm",
    subEn: "72 × 58 × 184 mm",
    badgeIt: "FLACONE QUADRO",
    badgeEn: "SQUARE BOTTLE"
  },
  {
    id: "wine_750",
    engine: "A",
    catGroup: "wine",
    neck: "Bague 29mm",
    shape: "wine_bordeaux",
    vol: "750 ml",
    matIt: "Vetro Verde",
    matEn: "Green Glass",
    hMm: 300, wMm: 76, dMm: 76,
    weightG: 1180,
    maxShoulderTD: 74,
    defaultFinish: "wine_green",
    defaultWrap: "label",
    liquidColor: "#4A0E17",
    vendor: "Vetreria Padana SpA (BS)",
    it: "Bottiglia 750 ml in Vetro Verde",
    en: "750 ml Bottle in Green Glass",
    subIt: "Ø 76 × H 300 mm",
    subEn: "Ø 76 × H 300 mm",
    badgeIt: "BOTTIGLIA",
    badgeEn: "BOTTLE"
  },
  {
    id: "jar_100",
    engine: "A",
    catGroup: "jars",
    neck: "58/400",
    shape: "jar_lux",
    vol: "100 ml",
    matIt: "Vetro Satinato",
    matEn: "Frosted Glass",
    hMm: 68, wMm: 74, dMm: 74,
    weightG: 215,
    maxShoulderTD: 26,
    defaultFinish: "frosted",
    defaultWrap: "sleeve",
    liquidColor: "#FAF3E8",
    vendor: "Vetreria Brianza Srl (MB)",
    it: "Vaso 100 ml in Vetro Satinato",
    en: "100 ml Jar in Frosted Glass",
    subIt: "Ø 74 × H 68 mm",
    subEn: "Ø 74 × H 68 mm",
    badgeIt: "VASO",
    badgeEn: "JAR"
  },
  {
    id: "can_330",
    engine: "A",
    catGroup: "cans",
    neck: "SOT 202",
    shape: "alu_can",
    vol: "330 ml",
    matIt: "Alluminio",
    matEn: "Aluminum",
    hMm: 146, wMm: 58, dMm: 58,
    weightG: 355,
    maxShoulderTD: 24,
    defaultFinish: "alu_brushed",
    defaultWrap: "sleeve",
    liquidColor: "#F59E0B",
    vendor: "AluCan Packaging Italia SpA (MI)",
    it: "Lattina 330 ml in Alluminio",
    en: "330 ml Can in Aluminum",
    subIt: "Ø 58 × H 146 mm",
    subEn: "Ø 58 × H 146 mm",
    badgeIt: "LATTINA",
    badgeEn: "CAN"
  },
  {
    id: "doypack_1000",
    engine: "B",
    catGroup: "flexibles",
    neck: "Zip 220mm",
    shape: "doypack",
    vol: "1000 g",
    matIt: "Polimero Bianco Soft-Touch",
    matEn: "White Soft-Touch Polymer",
    hMm: 310, wMm: 220, dMm: 95,
    weightG: 1050,
    maxShoulderTD: 12,
    defaultFinish: "matte_pouch",
    defaultWrap: "pouch",
    liquidColor: "#E8D5B7",
    vendor: "FlexPack Lombardia Srl (MI)",
    it: "Doypack 1000 g in Polimero Bianco",
    en: "1000 g Doypack in White Polymer",
    subIt: "220 × 310 × P 95 mm",
    subEn: "220 × 310 × D 95 mm",
    badgeIt: "DOYPACK",
    badgeEn: "DOYPACK"
  }
];

const RIGID_FINISHES = [
  { id: "pet_gloss", it: "PET Lucido", en: "Glossy PET", swatch: "linear-gradient(135deg,#FFFFFF,#D5E3EE)" },
  { id: "frosted", it: "Vetro Satinato", en: "Frosted Glass", swatch: "linear-gradient(135deg,#FFFFFF,#DBD6CD)" },
  { id: "clear_pet", it: "PET Cristallo", en: "Crystal Clear PET", swatch: "linear-gradient(135deg,#EBF3F8,#BCCAD4)" },
  { id: "amber", it: "Vetro Ambrato", en: "Amber Glass", swatch: "linear-gradient(135deg,#B85D14,#4F2005)" },
  { id: "hdpe_white", it: "HDPE Opaco", en: "Matte HDPE", swatch: "linear-gradient(135deg,#FAF8F5,#E2DDD4)" },
  { id: "wine_green", it: "Vetro Verde", en: "Green Glass", swatch: "linear-gradient(135deg,#224D34,#0B1D13)" },
  { id: "alu_brushed", it: "Alluminio", en: "Aluminum", swatch: "linear-gradient(135deg,#F2F4F7,#9AA1A8)" }
];

const POUCH_FINISHES = [
  { id: "matte_pouch", it: "Bianco Soft-Touch", en: "White Soft-Touch", swatch: "linear-gradient(135deg,#FFFFFF,#EAE5DC)" },
  { id: "gloss_pouch", it: "Lucido Gloss", en: "High Gloss", swatch: "linear-gradient(135deg,#FFFFFF,#DCE3EA)" },
  { id: "kraft_pouch", it: "Carta Kraft", en: "Kraft Paper", swatch: "linear-gradient(135deg,#CFA87C,#9C7248)" },
  { id: "foil_pouch", it: "Foil ALU", en: "Brushed ALU", swatch: "linear-gradient(135deg,#EAEAEA,#A6ABB0)" }
];

const CLOSURES = [
  { id: "none", neck: "NONE", type: "none", hasCapSupplier: false, it: "Nessuna chiusura", en: "No closure", vendor: "—", addH: 0 },
  { id: "pump_24", neck: "24/410", type: "pump", it: "Pompa Dispenser", en: "Dispenser Pump", vendor: "Closures Italia Srl (MB)", addH: 30 },
  { id: "pump_slim_24", neck: "24/410", type: "pump_slim", it: "Pompa Lozione Sottile", en: "Slim Lotion Pump", vendor: "DispenserTech Lombardia Srl (BG)", addH: 24 },
  { id: "dropper_24", neck: "24/410", type: "dropper", it: "Contagocce Pipetta", en: "Pipette Dropper", vendor: "Droppers Italia Srl (BG)", addH: 26 },
  { id: "spray_24", neck: "24/410", type: "spray", it: "Spray Nebulizzatore", en: "Atomizer Spray", vendor: "EuroAtomizers Srl (MI)", addH: 24 },
  { id: "fliptop_24", neck: "24/410", type: "fliptop24", it: "Tappo Flip-Top 24/410", en: "24/410 Flip-Top Cap", vendor: "PlastChiusure Nord Srl (VA)", addH: 18 },
  { id: "cap_28", neck: "28/410", type: "cap28", it: "Tappo a Vite Zigrinato 28/410", en: "28/410 Ribbed Screw Cap", vendor: "CapMold Emilia Srl (MO)", addH: 14 },
  { id: "disctop_28", neck: "28/410", type: "disctop28", it: "Tappo Disc-Top 28/410", en: "28/410 Disc-Top Cap", vendor: "PlastChiusure Nord Srl (VA)", addH: 18 },
  { id: "fliptop_28", neck: "28/410", type: "fliptop28", it: "Tappo Flip-Top Largo 28/410", en: "28/410 Wide Flip-Top Cap", vendor: "CapMold Emilia Srl (MO)", addH: 20 },
  { id: "pushpull_28", neck: "28/410", type: "pushpull28", it: "Tappo Dosatore Pull-Push 28/410", en: "28/410 Pull-Push Spout Cap", vendor: "Closures Italia Srl (MB)", addH: 26 },
  { id: "lid_58", neck: "58/400", type: "lid58", it: "Coperchio Vaso Piatto 58/400", en: "58/400 Flat Jar Lid", vendor: "CapMold Emilia Srl (MO)", addH: 12 },
  { id: "lid_bevel_58", neck: "58/400", type: "lid_bevel58", it: "Coperchio Vaso Smussato 58/400", en: "58/400 Beveled Jar Lid", vendor: "LidMold Lombardia Srl (MI)", addH: 15 },
  { id: "lid_double_58", neck: "58/400", type: "lid_double58", it: "Coperchio Doppia Parete 58/400", en: "58/400 Double-Wall Lid", vendor: "Closures Italia Srl (MB)", addH: 19 },
  { id: "lid_dome_70", neck: "70/400", type: "lid_dome70", it: "Coperchio Bombato Largo 70/400", en: "70/400 Wide Domed Lid", vendor: "LidMold Lombardia Srl (MI)", addH: 18 },
  { id: "lid_tall_70", neck: "70/400", type: "lid_tall70", it: "Coperchio Alto 70/400", en: "70/400 Tall Wide Lid", vendor: "CapMold Emilia Srl (MO)", addH: 22 },
  { id: "cork_29", neck: "Bague 29mm", type: "cork29", it: "Tappo Sughero e Capsula 29mm", en: "Cork and Capsule 29mm", vendor: "Sugherificio Piemonte Srl (CN)", addH: 6 },
  { id: "stelvin_29", neck: "Bague 29mm", type: "stelvin29", it: "Capsula a Vite Lunga 29mm", en: "Long-Skirt Screw Cap 29mm", vendor: "CapsulPack Veneto Srl (TV)", addH: 4 },
  { id: "pourer_29", neck: "Bague 29mm", type: "pourer29", it: "Tappo a Vite Dosatore", en: "Screw Pourer Cap", vendor: "GualaClosures Piemonte SpA (AL)", addH: 14 },
  { id: "bartop_29", neck: "Bague 29mm", type: "bartop29", it: "Tappo Bar-Top Legno 29mm", en: "29mm Wood Bar-Top Stopper", vendor: "Sugherificio Piemonte Srl (CN)", addH: 18 }
];

const FILMS = [
  { id: "PETG", name: "PETG TDO 50μm", maxTD: 75, warnTD: 28, errTD: 44, pinchScale: 0.55, ripple: 0.0, clearcoat: 0.96, roughness: 0.12, descIt: "Alta conformabilità su spalle strette (max 75% TD)", descEn: "High conformability on steep curves (max 75% TD)" },
  { id: "OPS", name: "OPS 45μm Soft", maxTD: 68, warnTD: 25, errTD: 39, pinchScale: 0.80, ripple: 0.18, clearcoat: 0.46, roughness: 0.28, descIt: "Bassa forza di retrazione, ideale su plastica (max 68% TD)", descEn: "Low shrink force for plastic vessels (max 68% TD)" },
  { id: "PVC", name: "PVC 50μm Rigido", maxTD: 52, warnTD: 20, errTD: 31, pinchScale: 1.15, ripple: 0.54, clearcoat: 0.68, roughness: 0.20, descIt: "Film economico rigido, tollera curve moderate (max 52% TD)", descEn: "Rigid economic film for moderate tapers (max 52% TD)" },
  { id: "RPET", name: "rPET 35% Riciclato", maxTD: 44, warnTD: 17, errTD: 26, pinchScale: 1.45, ripple: 0.88, clearcoat: 0.26, roughness: 0.38, descIt: "Film riciclato, bassa elasticità su curve (max 44% TD)", descEn: "Recycled film, limited curve elasticity (max 44% TD)" }
];

const LABEL_PAPERS = [
  { id: "COTTON", name: "Carta Cotone Vergata 90g", maxTD: 14, warnTD: 5, errTD: 12, stiffness: 1.00, roughness: 0.84, clearcoat: 0.02, transparentBg: false, laidTexture: true, descIt: "Carta rigida naturale · solo fascia cilindrica (max 14%)", descEn: "Rigid natural paper · cylinder only (max 14%)" },
  { id: "PP_WHITE", name: "PP Bianco Adesivo 60μm", maxTD: 22, warnTD: 9, errTD: 19, stiffness: 0.68, roughness: 0.20, clearcoat: 0.74, transparentBg: false, laidTexture: false, descIt: "Resistente acqua/olio · corpo dritto (max 22%)", descEn: "Water/oil proof · straight body (max 22%)" },
  { id: "PE_SQUEEZE", name: "PE Conformabile 80μm", maxTD: 32, warnTD: 15, errTD: 27, stiffness: 0.34, roughness: 0.34, clearcoat: 0.38, transparentBg: false, laidTexture: false, descIt: "Film elastico · segue raccordi e spigoli (max 32%)", descEn: "Elastic film · conforms to tapers and corners (max 32%)" },
  { id: "PET_CLEAR", name: "No-Label Look PET 50μm", maxTD: 16, warnTD: 6, errTD: 14, stiffness: 0.92, roughness: 0.08, clearcoat: 0.96, transparentBg: true, laidTexture: false, descIt: "Trasparente rigido · solo zona piana (max 16%)", descEn: "Crystal clear rigid film · flat zone only (max 16%)" }
];

const SERIGRAFIA_INKS = [
  { id: "UV_HIGH", name: "Serigrafia UV Alto Spessore", maxTD: 22, descIt: "Stampa diretta 360° su alluminio", descEn: "Direct 360° UV screen print" },
  { id: "MET_INK", name: "Inchiostro Metallizzato Direct", maxTD: 24, descIt: "Riflesso metallico su corpo alluminio", descEn: "Metallic ink sheen on bare metal" },
  { id: "TACTILE", name: "Vernice Rilievo Tattile 3D", maxTD: 20, descIt: "Texture micro-rilievo antiscivolo", descEn: "Raised tactile grip varnish" },
  { id: "MATTE_UV", name: "Serigrafia Soft-Matte UV", maxTD: 22, descIt: "Finitura opaca vellutata diretta", descEn: "Direct velvet matte screen print" }
];

const POUCH_LAMINATES = [
  { id: "ALU_TRI", name: "Triplice PET12/ALU/PE90", descIt: "Barriera O₂/UV massima · Triplo strato", descEn: "Max O₂/UV barrier · Triple laminate" },
  { id: "MONO_PE", name: "Mono-PE Riciclabile 110μm", descIt: "Riciclabile CE · Saldatura 145°C", descEn: "100% Recyclable PE laminate" },
  { id: "KRAFT_PLA", name: "Kraft + PLA Bio-Barriera", descIt: "Finitura naturale compostabile", descEn: "Natural compostable barrier" },
  { id: "BOPP_STD", name: "BOPP / CPP Standard 85μm", descIt: "Alta macchinabilità su linea verticale", descEn: "High-speed vertical pouch line" }
];

const NEUTRAL_SLEEVE_SKIN = {
  id: "neutral",
  styleType: "neutral_clear",
  brand: "NEUTRA",
  brandSub: "TRASPARENTE",
  product: "FILM NEUTRO TRASPARENTE",
  pouchSub: "FORMATO STANDARD",
  wineSub: "FILM NEUTRO",
  sub: "FILM NEUTRO TRASPARENTE",
  previewColors: ["rgba(245,250,255,0.92)", "#CBD5E1", "#94A3B8"],
  descIt: "Film trasparente neutro",
  descEn: "Clear neutral unprinted film",
  ean: "8 054192 000018",
  sleeveHeightMul: 1.0,
  labelHeightMul: 1.0,
  labelWidthMul: 1.0,
  labelShape: "arch"
};

const NEUTRAL_LABEL_SKIN = {
  id: "neutral",
  styleType: "neutral_white",
  brand: "BIANCA",
  brandSub: "SENZA SCRITTE",
  product: "ETICHETTA BIANCA NEUTRA",
  pouchSub: "FORMATO STANDARD",
  wineSub: "ETICHETTA BIANCA",
  sub: "ETICHETTA BIANCA NEUTRA",
  previewColors: ["#FFFFFF", "#F3F0EA", "#D6D0C5"],
  descIt: "Etichetta bianca senza scritte",
  descEn: "Blank white unprinted label",
  ean: "8 054192 000018",
  sleeveHeightMul: 1.0,
  labelHeightMul: 1.0,
  labelWidthMul: 1.0,
  labelShape: "arch"
};

const BRAND_SKINS = [
  {
    id: "lumina",
    styleType: "white_swiss",
    brand: "LUMINA",
    brandSub: "MILANO",
    product: "EDIZIONE 01 · FORMULA ORIGINALE",
    pouchSub: "FORMATO STANDARD · EDIZIONE 01",
    wineSub: "RISERVA SPECIALE · LOTTO 01",
    sub: "LINEA ESSENZIALE · CONFEZIONE PRIMARIA",
    previewColors: ["#FCFBF7", "#C2180E", "#161311"],
    descIt: "Bianco Svizzero · Formato standard",
    descEn: "Swiss White · Standard shape & length",
    ean: "8 054192 730148",
    sleeveHeightMul: 1.0,
    labelHeightMul: 1.0,
    labelWidthMul: 1.0,
    labelShape: "arch"
  },
  {
    id: "nocturne",
    styleType: "black_gold",
    brand: "NOCTURNE",
    brandSub: "NOBILE",
    product: "SERIE RISERVATA · SELEZIONE ORO",
    pouchSub: "EDIZIONE NERA · FORMATO 1000G",
    wineSub: "EDIZIONE NERA · RISERVA SELEZIONE",
    sub: "EDIZIONE SPECIALE · ALTA BARRIERA",
    previewColors: ["#121114", "#D9B263", "#1E3A8A"],
    descIt: "Taglio alto e stretto · Smussatura ottagonale",
    descEn: "Tall slim cut · Octagonal chamfered plaque",
    ean: "8 054192 910441",
    sleeveHeightMul: 1.24,
    labelHeightMul: 1.24,
    labelWidthMul: 0.78,
    labelShape: "octagon"
  },
  {
    id: "botanica",
    styleType: "emerald_cobalt",
    brand: "VERDE",
    brandSub: "BOTANICA",
    product: "LINEA NATURALE · ESTRATTI PURI",
    pouchSub: "SERIE BOTANICA · FORMATO 1000G",
    wineSub: "SELEZIONE NATURALE · RISERVA",
    sub: "ORIGINE CERTIFICATA · PICCOLI LOTTI",
    previewColors: ["#0F5C46", "#1D4ED8", "#EA580C"],
    descIt: "Fascia bassa larga · Scudo ovale panoramico",
    descEn: "Compact wide band · Panoramic oval shield",
    ean: "8 054192 881024",
    sleeveHeightMul: 0.72,
    labelHeightMul: 0.74,
    labelWidthMul: 1.24,
    labelShape: "pill_shield"
  }
];

const PRINTER_POOL = [
  { name: "SleevePrint Milano Srl (MI)", spec: "HP Indigo + Rotocalco 9 colori · Controllo TD", lead: "6 gg" },
  { name: "Grafiche TermoPack Bergamo (BG)", spec: "Specialista PETG/rPET e Laminati Flessibili", lead: "5 gg" }
];

const FILL_TYPES = [
  { id: "Liquidi", it: "Liquidi", en: "Liquids", cost: 220 },
  { id: "Polveri", it: "Polveri", en: "Powders", cost: 220 },
  { id: "Capsule", it: "Capsule", en: "Capsules", cost: 240 },
  { id: "Pillole", it: "Pillole", en: "Pills", cost: 240 }
];

// ==================== GLOBAL APP STATE ====================
const state = {
  lang: "it",
  mainView: "catalog", // 01 Marketplace -> 02 Studio 3D -> 03 Filiera
  inspTab: 1,
  vesselId: "serum_250",
  finishId: "pet_gloss",
  closureId: "none",
  wrapType: "none", // 'none' | 'sleeve' | 'label' | 'serigrafia' | 'pouch'
  pouchPrintType: "none", // 'none' | 'flexo' | 'digital'
  filmId: "PETG",
  labelMatId: "COTTON",
  serigrafiaInkId: "UV_HIGH",
  pouchMatId: "ALU_TRI",
  skinId: "none",
  // SLEEVE / ADHESIVE LABEL 3D POSITION (starts cleanly centered on flat body, well below curved shoulder):
  sleeveAngleDeg: 0,      // -180..+180 around bottle
  sleeveHeightPct: 18,    // 10 (low safe body) .. 88 (high curved shoulder!)
  // BARCODE 3D POSITION (starts on back face so front graphic stays unobstructed):
  bcAngleDeg: 180,        // -180..+180 around bottle (180 = rear)
  bcHeightPct: 24,        // 12..88 along bottle / pouch height
  bcLadder: false,
  // DOYPACK BARCODE SPECIFIC STATE:
  bcDoypackSide: "back",  // 'front' | 'back' (starts on back face!)
  bcDoypackX: 0,          // -42..+42 (% across active face)
  infoPopoverOpen: false,
  // CUSTOM CONTAINER UPLOAD DEMO, CUSTOM GRAPHIC DEMO, AR QR MODAL & USER PROFILE
  customVesselMode: false,
  customGraphicMode: false,
  customGraphicFile: "",
  customDatasheetFile: "",
  customPhotoFiles: ["", "", "", "", "", ""],
  arModalOpen: false,
  prevViewBeforeProfile: "catalog",
  submittedRequests: [],
  favoriteVessels: [],
  // STEP 03 MULTI-PACK BOX CONFIGURATOR
  boxMode: "grid",        // 'grid' | 'bulk' (bulk for plastic bottles only)
  boxQty: 1,              // 1, 2, 3, 6, 12
  bulkQty: 100,           // 50, 100, 150, 200
  boxDivider: false,      // internal protective partition
  boxBoard: "teso",       // 'teso' | 'eflute'
  // 3D VIEWPORT FLAGS
  pointerTool: "orbit",   // default 'orbit' ('Ruota 3D')
  exploded: false,
  explodeProgress: 0,
  xray: false,            // Interno / Liquido OFF by default!
  heatmap: false,
  wireframe: false,
  darkStudio: false,
  printerIdx: 0,
  activeCatGroup: "all",
  // STEP 03 FILIERA INTERACTIVE SELECTION & COPACKER FILLING
  filieraStep: 1,
  selectedSuppliers: { container: 0 },
  copackerFilling: false,
  copackerFillType: "Liquidi"
};

function getVessel() { return VESSELS.find(v => v.id === state.vesselId); }
function getClosure() { return CLOSURES.find(c => c.id === state.closureId) || CLOSURES[0]; }
function getFilm() { return FILMS.find(f => f.id === state.filmId); }
function getLabelPaper() { return LABEL_PAPERS.find(p => p.id === state.labelMatId); }
function getSerigrafiaInk() { return SERIGRAFIA_INKS.find(i => i.id === state.serigrafiaInkId); }
function getPouchLaminate() { return POUCH_LAMINATES.find(m => m.id === state.pouchMatId); }
function getAvailableSkinsForWrap(wt) {
  const mode = wt || state.wrapType;
  if (mode === "sleeve") return [NEUTRAL_SLEEVE_SKIN, ...BRAND_SKINS];
  if (mode === "label") return [NEUTRAL_LABEL_SKIN, ...BRAND_SKINS];
  return BRAND_SKINS;
}
function getSkin() {
  if (state.skinId === "neutral") {
    if (state.wrapType === "label") return NEUTRAL_LABEL_SKIN;
    if (state.wrapType === "sleeve") return NEUTRAL_SLEEVE_SKIN;
    return BRAND_SKINS[0];
  }
  return BRAND_SKINS.find(s => s.id === state.skinId) || null;
}
function getPrinter() { return PRINTER_POOL[state.printerIdx % PRINTER_POOL.length]; }
function isDoypack() { return getVessel().shape === "doypack"; }
function isPlasticBottle(v) { const vv = v || getVessel(); return vv.id === "serum_250" || vv.id === "square_500"; }
function hasWrap() { return state.wrapType !== "none"; }
function isSerigrafiaMode() { return getVessel().shape === "alu_can" && state.wrapType === "serigrafia"; }
function isLabelMode() { return !isDoypack() && state.wrapType === "label"; }

function getVesselTotalHeight(vessel) {
  if (vessel.shape === "jar_lux") return 1.48;
  if (vessel.shape === "wine_bordeaux") return 2.86;
  if (vessel.shape === "alu_can") return 2.65;
  if (vessel.shape === "doypack") return 2.60;
  return 2.55;
}

// Continuous radial distance at angle theta for any rigid vessel shape
function getRadialEnvelopeFactor(vessel, profileV, theta, baseRWorld) {
  if (vessel.shape === "square_soft" && profileV < 0.85) {
    const sqMix = Math.max(0, Math.min(1, (0.85 - profileV) / 0.20));
    const n = 2.0 + 2.8 * sqMix;
    const rx = baseRWorld * 1.07;
    const rz = baseRWorld * 0.90;
    const sx = Math.abs(Math.sin(theta)) / rx;
    const cz = Math.abs(Math.cos(theta)) / rz;
    const denom = Math.pow(Math.pow(sx, n) + Math.pow(cz, n), 1.0 / n);
    return denom > 1e-6 ? 1.0 / denom : baseRWorld;
  }
  return baseRWorld;
}

// Normalized radial profile r(v) for bottles & wine bottles
function getNormalizedRadiusAtV(vessel, v) {
  if (vessel.shape === "doypack") return 1.0;
  if (vessel.shape === "jar_lux") {
    if (v < 0.08) return 0.92 + (v / 0.08) * 0.08;
    if (v <= 0.74) return 1.0;
    const t = Math.min(1, (v - 0.74) / 0.10);
    return 1.0 - 0.26 * (t * t * (3 - 2 * t));
  }
  if (vessel.shape === "wine_bordeaux") {
    if (v < 0.04) return 0.90 + (v / 0.04) * 0.10;
    if (v <= 0.50) return 1.0;
    if (v <= 0.70) {
      const t = (v - 0.50) / 0.20;
      const s = t * t * (3 - 2 * t);
      return 1.0 - 0.72 * s;
    }
    if (v <= 0.95) return 0.28;
    return 0.315;
  }
  if (vessel.shape === "alu_can") {
    if (v < 0.05) return 0.84 + (v / 0.05) * 0.16;
    if (v <= 0.84) return 1.0;
    if (v <= 0.96) {
      const t = (v - 0.84) / 0.11;
      const s = t * t * (3 - 2 * t);
      return 1.0 - 0.26 * s;
    }
    return 0.855;
  }
  if (v < 0.05) return 0.90 + (v / 0.05) * 0.10;
  if (v <= 0.58) return 1.0;
  const t = Math.min(1, (v - 0.58) / 0.32);
  const s = t * t * (3 - 2 * t);
  return 1.0 - 0.62 * s;
}

// Compute vertical band [vMin, vMax] for sleeve or adhesive label
function getSleeveVerticalBand() {
  const vessel = getVessel();
  const skin = getSkin();
  if (isLabelMode()) {
    const mul = skin ? (skin.labelHeightMul || 1.0) : 1.0;
    if (vessel.shape === "alu_can") {
      const baseH = 0.72;
      const bandH = Math.min(0.84, Math.max(0.46, baseH * mul));
      const maxStart = Math.max(0.06, 0.93 - bandH - 0.06);
      const norm = Math.max(0, Math.min(1, (state.sleeveHeightPct - 10) / 76));
      const vMin = 0.06 + norm * maxStart;
      return { vMin, vMax: vMin + bandH };
    }
    const baseH = vessel.shape === "jar_lux" ? 0.44 : (vessel.shape === "wine_bordeaux" ? 0.38 : 0.42);
    const maxAllowedH = vessel.shape === "wine_bordeaux" ? 0.435 : (vessel.shape === "jar_lux" ? 0.54 : 0.56);
    const bandH = Math.min(maxAllowedH, Math.max(0.24, baseH * mul));
    const maxTop = vessel.shape === "jar_lux" ? 0.74 : (vessel.shape === "wine_bordeaux" ? 0.72 : 0.82);
    const baseStart = mul > 1.02 ? 0.045 : 0.06;
    const maxStart = Math.max(0.05, maxTop - bandH);
    const norm = Math.max(0, Math.min(1, (state.sleeveHeightPct - 10) / 76));
    const vMin = baseStart + norm * (maxStart - baseStart);
    return { vMin, vMax: Math.min(maxTop, vMin + bandH) };
  }
  const mul = skin ? (skin.sleeveHeightMul || 1.0) : 1.0;
  const baseH = vessel.shape === "alu_can" ? 0.74 : (vessel.shape === "wine_bordeaux" ? 0.42 : (vessel.shape === "jar_lux" ? 0.48 : 0.52));
  const maxAllowedH = vessel.shape === "alu_can" ? 0.86 : (vessel.shape === "wine_bordeaux" ? 0.48 : (vessel.shape === "jar_lux" ? 0.58 : 0.615));
  const bandH = Math.min(maxAllowedH, Math.max(0.28, baseH * mul));
  const norm = Math.max(0, Math.min(1, (state.sleeveHeightPct - 10) / 80));
  const maxCarrier = vessel.shape === "alu_can" ? 0.95 : (vessel.shape === "wine_bordeaux" ? 0.76 : 0.84);
  const travel = Math.max(0.10, maxCarrier - bandH - 0.04);
  const vMin = 0.04 + norm * travel;
  const vMax = Math.min(maxCarrier, vMin + bandH);
  return { vMin, vMax };
}

function getLabelWidthMultiplier(vessel) {
  const skin = getSkin();
  if (!skin) return 1.0;
  if (vessel && vessel.shape === "alu_can") {
    return skin.id === "nocturne" ? 0.78 : (skin.id === "botanica" ? 1.06 : 1.0);
  }
  return skin.labelWidthMul || 1.0;
}

function getWrapRealDimensionsMm(vessel) {
  const v = vessel || getVessel();
  const { vMin, vMax } = getSleeveVerticalBand();
  const isCan = v.shape === "alu_can";
  const isPouch = v.shape === "doypack";
  const isLabel = isLabelMode();
  const circMm = v.shape === "square_soft"
    ? Math.round(2 * (v.wMm + v.dMm) - 12)
    : Math.round(Math.PI * v.wMm);
  const spanH = isPouch ? 0.74 : (vMax - vMin);
  const wrapHmm = isPouch ? 230 : (isSerigrafiaMode() ? Math.round(v.hMm * 0.86) : Math.max(24, Math.round(spanH * v.hMm)));
  const wMul = getLabelWidthMultiplier(v);
  let wrapWmm = circMm;
  if (isPouch) {
    wrapWmm = 180;
  } else if (isLabel) {
    const baseFrac = isCan ? 0.85 : (v.shape === "jar_lux" ? 0.40 : (v.shape === "square_soft" ? 0.22 : (v.shape === "wine_bordeaux" ? 0.225 : 0.235)));
    wrapWmm = Math.round(circMm * baseFrac * wMul);
  }
  const bcWmm = v.shape === "jar_lux" ? 32 : 37;
  const bcHmm = v.shape === "jar_lux" ? 22 : 26;
  return {
    wrapWmm,
    wrapHmm,
    wrapDimStr: `${wrapWmm} × ${wrapHmm} mm`,
    bcWmm,
    bcHmm,
    bcDimStr: `${bcWmm} × ${bcHmm} mm`
  };
}

// Maximum physically applicable surface of the container (including yellow/red curvature zones)
function getMaxApplicableSurfaceDimensionsMm(vessel) {
  const v = vessel || getVessel();
  const isCan = v.shape === "alu_can";
  const isPouch = v.shape === "doypack";
  const isLabel = isLabelMode();
  const circMm = v.shape === "square_soft"
    ? Math.round(2 * (v.wMm + v.dMm) - 12)
    : Math.round(Math.PI * v.wMm);
  const bcWmm = v.shape === "jar_lux" ? 32 : 37;
  const bcHmm = v.shape === "jar_lux" ? 22 : 26;

  if (isPouch) {
    return {
      maxWmm: v.wMm,
      maxHmm: v.hMm,
      wrapDimStr: `${v.wMm} × ${v.hMm} mm`,
      bcDimStr: `${bcWmm} × ${bcHmm} mm`
    };
  }

  const maxCarrierV = isCan ? 0.95 : (v.shape === "wine_bordeaux" ? 0.76 : (v.shape === "jar_lux" ? 0.80 : 0.84));
  const minCarrierV = 0.04;
  const maxHmm = Math.round((maxCarrierV - minCarrierV) * v.hMm);
  let maxWmm = circMm;
  if (isLabel) {
    // Full applicable wrap-around width including corners/margins before self-overlap
    const maxLabelFrac = isCan ? 0.94 : (v.shape === "jar_lux" ? 0.65 : (v.shape === "square_soft" ? 0.45 : 0.50));
    maxWmm = Math.round(circMm * maxLabelFrac);
  }
  return {
    maxWmm,
    maxHmm,
    wrapDimStr: `${maxWmm} × ${maxHmm} mm`,
    bcDimStr: `${bcWmm} × ${bcHmm} mm`
  };
}

function getClosureRealDimensionsMm(cl) {
  if (!cl || cl.id === "none") return "";
  if (cl.neck === "24/410") return `Ø 28 × H ${cl.addH + 16} mm`;
  if (cl.neck === "28/410") return `Ø 32 × H ${cl.addH + 16} mm`;
  if (cl.neck === "58/400") return `Ø 62 × H ${cl.addH + 8} mm`;
  if (cl.neck === "70/400") return `Ø 74 × H ${cl.addH + 8} mm`;
  if (cl.id === "cork_29") return "Ø 31 × H 54 mm";
  if (cl.id === "stelvin_29") return "Ø 30 × H 60 mm";
  if (cl.id === "pourer_29") return "Ø 31 × H 42 mm";
  if (cl.id === "bartop_29") return "Ø 32 × H 38 mm";
  return `H ${cl.addH + 14} mm`;
}

// Barcode sits cleanly in lower region of Sleeve and scales dynamically with sleeve span
function getSleeveBarcodeHeightBounds() {
  const vessel = getVessel();
  if (vessel.shape === "doypack") return { minPct: 10, maxPct: 86 };
  if (isSerigrafiaMode()) return { minPct: 12, maxPct: 88 };
  const sSpan = vessel.shape === "wine_bordeaux" ? 0.74 : (vessel.shape === "alu_can" ? 0.90 : 0.80);
  const { vMin, vMax } = getSleeveVerticalBand();
  const fixedBcV = vMin + Math.min(0.11, (vMax - vMin) * 0.22);
  const pct = Math.max(8, Math.min(92, Math.round(((fixedBcV - 0.04) / sSpan) * 100)));
  return { minPct: pct, maxPct: pct };
}

function clampBarcodeToSleeve() {
  if (!isDoypack() && state.wrapType === "sleeve") {
    const b = getSleeveBarcodeHeightBounds();
    state.bcHeightPct = b.minPct;
  }
}

function getBoxLayout(qty) {
  const map = {
    1: { cols: 1, rows: 1, nameIt: "Scatola Singola 1×1", nameEn: "Single Box 1×1" },
    2: { cols: 2, rows: 1, nameIt: "Scatola 2×1", nameEn: "Box 2×1" },
    3: { cols: 3, rows: 1, nameIt: "Scatola 3×1", nameEn: "Box 3×1" },
    6: { cols: 3, rows: 2, nameIt: "Scatola 3×2", nameEn: "Box 3×2" },
    12: { cols: 4, rows: 3, nameIt: "Scatola 4×3", nameEn: "Box 4×3" }
  };
  return map[qty] || map[1];
}

function computeCartonMetrics(v, cl) {
  const isBulk = isPlasticBottle(v) && state.boxMode === "bulk";
  if (isBulk) {
    const bulkDims = {
      50: { h: 400, w: 600, d: 400 },
      100: { h: 500, w: 600, d: 500 },
      150: { h: 580, w: 600, d: 550 },
      200: { h: 600, w: 800, d: 600 }
    };
    const q = bulkDims[state.bulkQty] ? state.bulkQty : 100;
    const dim = bulkDims[q];
    const grossWeightG = q * 38 + 900;
    return {
      isBulk: true,
      packQty: q,
      layout: { cols: 1, rows: 1, nameIt: `Sparsi ${q} pz`, nameEn: `Loose ${q} pcs` },
      cartonH: dim.h,
      cartonW: dim.w,
      cartonD: dim.d,
      cartonStr: `${dim.h} × ${dim.w} × ${dim.d} mm`,
      grossWeightG
    };
  }
  const layout = getBoxLayout(state.boxQty);
  const boardAdd = state.boxBoard === "eflute" ? 6 : 2;
  const divCell = state.boxDivider ? 4 : 0;
  const padSide = v.shape === "doypack" ? 8 : 6;
  const padH = v.shape === "doypack" ? 12 : (cl.addH + 6);
  const cartonH = v.hMm + padH + boardAdd;
  const cartonW = layout.cols * v.wMm + (layout.cols - 1) * divCell + padSide + boardAdd;
  const cartonD = layout.rows * v.dMm + (layout.rows - 1) * divCell + padSide + boardAdd;
  const grossWeightG = state.boxQty * v.weightG + Math.round((cartonH * cartonW + cartonW * cartonD) * 0.004);
  return {
    isBulk: false,
    packQty: state.boxQty,
    layout,
    cartonH,
    cartonW,
    cartonD,
    cartonStr: `${cartonH} × ${cartonW} × ${cartonD} mm`,
    grossWeightG
  };
}

function evaluateLivePhysics() {
  clampBarcodeToSleeve();
  const v = getVessel();
  const cl = getClosure();
  const fm = getFilm();
  const lp = getLabelPaper();
  const isNoCap = (cl.id === "none");
  const neckMatch = isNoCap || (v.neck === cl.neck);
  const noWrap = !hasWrap();
  const carton = computeCartonMetrics(v, cl);

  if (noWrap) {
    return {
      isDoypack: v.shape === "doypack",
      isLabel: false,
      noWrap: true,
      isNoCap,
      neckMatch,
      localTD: 0,
      effectiveBarcodeTD: 0,
      ansiGrade: "A",
      sleeveTD: 0,
      sleeveStatus: "ok",
      status: neckMatch ? "g" : "r",
      ...carton
    };
  }

  // DOYPACK ENGINE B PHYSICS
  if (v.shape === "doypack") {
    const absX = Math.abs(state.bcDoypackX);
    const inSideSeal = absX > 33;
    const severeSideSeal = absX > 39;
    const inZipTop = state.bcHeightPct > 74;
    const severeZipTop = state.bcHeightPct > 81;
    const inGussetBot = state.bcHeightPct < 20;
    const severeGussetBot = state.bcHeightPct < 14;

    let ansiGrade = "A";
    let localTD = 4;
    let bcReasonIt = "Area piana ottimale e lontana dai margini di saldatura.";
    let bcReasonEn = "Clean flat panel well clear of pouch heat-seals.";

    if (severeSideSeal || severeZipTop || severeGussetBot) {
      ansiGrade = "F";
      localTD = 62;
      bcReasonIt = severeSideSeal
        ? "BLOCCO: Barcode sotto pinza termosaldatura laterale!"
        : (severeZipTop ? "BLOCCO: Barcode dentro zip / saldatura superiore!" : "BLOCCO: Barcode schiacciato nella piega soffietto inferiore!");
      bcReasonEn = "BLOCKED: Barcode enters pouch heat-seal / gusset pinch!";
    } else if (inSideSeal || inZipTop || inGussetBot) {
      ansiGrade = "C";
      localTD = 46;
      bcReasonIt = "Attenzione: Barcode vicino a margine saldatura o zip.";
      bcReasonEn = "Warning: Barcode close to heat-seal / zip margin.";
    }

    let status = "g";
    if (!neckMatch || ansiGrade === "F") status = "r";
    else if (ansiGrade === "C") status = "y";

    return {
      isDoypack: true,
      isLabel: false,
      noWrap: false,
      isNoCap,
      neckMatch,
      localTD,
      effectiveBarcodeTD: localTD,
      ansiGrade,
      sleeveTD: 4,
      sleeveStatus: "ok",
      bcReasonIt, bcReasonEn,
      status,
      ...carton
    };
  }

  // RIGID VESSELS (ENGINE A: SLEEVE, ADHESIVE LABEL, OR CAN SERIGRAFIA 360°)
  if (isSerigrafiaMode()) {
    const ink = getSerigrafiaInk();
    const bcV = 0.04 + (state.bcHeightPct / 100) * 0.90;
    const rAtBarcode = getNormalizedRadiusAtV(v, bcV);
    const localTD = Math.min(62, Math.round((1 - rAtBarcode) * 260));
    const effectiveBarcodeTD = state.bcLadder ? Math.round(localTD * 0.45) : localTD;

    let ansiGrade = "A";
    if (effectiveBarcodeTD > ink.maxTD + 10) ansiGrade = "F";
    else if (effectiveBarcodeTD >= ink.maxTD - 4) ansiGrade = "C";

    let status = "g";
    if (!neckMatch || ansiGrade === "F") status = "r";
    else if (ansiGrade === "C") status = "y";

    return {
      isDoypack: false,
      isLabel: false,
      isSerigrafia: true,
      noWrap: false,
      isNoCap,
      neckMatch,
      localTD,
      effectiveBarcodeTD,
      ansiGrade,
      sleeveTD: 0,
      sleeveStatus: "ok",
      status,
      ...carton
    };
  }

  const { vMin, vMax } = getSleeveVerticalBand();
  const isLabel = isLabelMode();

  if (isLabel) {
    const rTop = getNormalizedRadiusAtV(v, vMax);
    const rBot = getNormalizedRadiusAtV(v, vMin);
    const wMul = getLabelWidthMultiplier(v);
    let cornerStress = 0;
    if (v.shape === "square_soft") {
      const thS = (state.sleeveAngleDeg * Math.PI) / 180;
      const excessAngle = Math.max(0, 0.58 * wMul - 0.62);
      const cCenter = Math.abs(Math.sin(2 * thS));
      const cEdge = excessAngle > 0 ? Math.max(Math.abs(Math.sin(2 * (thS - excessAngle))), Math.abs(Math.sin(2 * (thS + excessAngle)))) * 0.35 : 0;
      cornerStress = Math.round(Math.max(cCenter, cEdge) * 26);
    }
    const rawScale = v.shape === "alu_can" ? 235 : 100;
    const topStress = Math.round((1 - rTop) * rawScale);
    const botStress = Math.round((1 - rBot) * rawScale * 0.85);
    const labelCurvePct = Math.min(68, Math.max(topStress, botStress) + cornerStress);
    let labelStatus = "ok";
    if (labelCurvePct >= lp.errTD || labelCurvePct > lp.maxTD) labelStatus = "err";
    else if (labelCurvePct >= lp.warnTD) labelStatus = "warn";

    // Independent local evaluation strictly at the EAN-13 barcode zone (lower band of the label)
    const isJar = v.shape === "jar_lux";
    const bcCenterV = isJar ? (vMin + vMax) * 0.5 : (vMin + Math.min(0.11, (vMax - vMin) * 0.22));
    const bcVTop = Math.min(vMax, bcCenterV + 0.045);
    const bcVBot = Math.max(0.04, bcCenterV - 0.045);
    const bcTopStress = Math.round((1 - getNormalizedRadiusAtV(v, bcVTop)) * rawScale);
    const bcBotStress = Math.round((1 - getNormalizedRadiusAtV(v, bcVBot)) * rawScale * 0.85);
    const bcCornerStress = v.shape === "square_soft"
      ? Math.round(Math.abs(Math.sin(2 * ((state.sleeveAngleDeg * Math.PI) / 180))) * 22)
      : 0;
    const bcCurvePct = Math.min(68, Math.max(bcTopStress, bcBotStress) + bcCornerStress);
    let ansiGrade = "A";
    if (bcCurvePct >= lp.errTD || bcCurvePct > lp.maxTD) ansiGrade = "F";
    else if (bcCurvePct >= lp.warnTD) ansiGrade = "C";

    let status = "g";
    if (!neckMatch || labelStatus === "err" || ansiGrade === "F") status = "r";
    else if (labelStatus === "warn" || ansiGrade === "C") status = "y";

    return {
      isDoypack: false,
      isLabel: true,
      noWrap: false,
      isNoCap,
      neckMatch,
      localTD: bcCurvePct,
      effectiveBarcodeTD: bcCurvePct,
      ansiGrade,
      sleeveTD: labelCurvePct,
      labelTopStress: topStress,
      labelBotStress: botStress,
      labelCornerStress: cornerStress,
      sleeveStatus: labelStatus,
      status,
      ...carton
    };
  }

  // SHRINK SLEEVE MODE ON RIGID VESSEL (barcode moves with lower sleeve zone, independent of upper sleeve shoulder)
  const bcSpan = v.shape === "jar_lux" ? 0.71 : (v.shape === "wine_bordeaux" ? 0.74 : (v.shape === "alu_can" ? 0.90 : 0.80));
  const bcV = 0.04 + (state.bcHeightPct / 100) * bcSpan;
  const bcTopV = Math.min(0.95, bcV + 0.075);
  const rAtBarcode = Math.min(getNormalizedRadiusAtV(v, bcV), getNormalizedRadiusAtV(v, bcTopV));
  let bcCornerPenalty = 0;
  const effBcDeg = state.sleeveAngleDeg >= 0 ? state.sleeveAngleDeg - 180 : state.sleeveAngleDeg + 180;
  if (v.shape === "square_soft") {
    const th = (effBcDeg * Math.PI) / 180;
    bcCornerPenalty = Math.round(Math.abs(Math.sin(2 * th)) * 10);
  }
  const localTD = Math.min(72, Math.round((1 - (rAtBarcode / 1.14)) * 100) + bcCornerPenalty);
  const effectiveBarcodeTD = localTD;

  const filmOkBc = localTD <= fm.maxTD && localTD < fm.errTD + 6;
  const bcWarnThr = Math.max(18, fm.warnTD - 2);
  const bcErrThr = Math.max(28, fm.errTD - 3);
  let ansiGrade = "A";
  if (effectiveBarcodeTD >= bcErrThr || !filmOkBc) ansiGrade = "F";
  else if (effectiveBarcodeTD >= bcWarnThr) ansiGrade = "C";
  else if (effectiveBarcodeTD >= Math.max(15, bcWarnThr - 5)) ansiGrade = "B";

  const sleeveCheckV = vMax;
  const rAtSleeveTop = getNormalizedRadiusAtV(v, sleeveCheckV);
  let slCornerPenalty = 0;
  if (v.shape === "square_soft") {
    const thS = (state.sleeveAngleDeg * Math.PI) / 180;
    slCornerPenalty = Math.round(Math.abs(Math.sin(2 * thS)) * 11);
  }
  const sleeveTD = Math.min(72, Math.round((1 - (rAtSleeveTop / 1.14)) * 100) + slCornerPenalty);
  const filmOkSleeve = sleeveTD <= fm.maxTD;
  let sleeveStatus = "ok";
  if (sleeveTD >= fm.errTD || !filmOkSleeve) sleeveStatus = "err";
  else if (sleeveTD >= fm.warnTD) sleeveStatus = "warn";

  let status = "g";
  if (!neckMatch || ansiGrade === "F" || sleeveStatus === "err") status = "r";
  else if (ansiGrade === "C" || sleeveStatus === "warn") status = "y";

  return {
    isDoypack: false,
    isLabel: false,
    noWrap: false,
    isNoCap,
    neckMatch,
    localTD,
    effectiveBarcodeTD,
    filmOkBc,
    ansiGrade,
    sleeveTD,
    sleeveStatus,
    filmOkSleeve,
    status,
    ...carton
  };
}

// ==================== HIGH-DPI 2048x1024 DYNAMIC UV TEXTURE ENGINE ====================
const texCanvas = document.createElement("canvas");
texCanvas.width = 2048;
texCanvas.height = 1024;
const texCtx = texCanvas.getContext("2d");
let sleeveTexture = null;

function drawEAN13Graphic(ctx, x, y, wBox, hBox, eanStr, statusCol, labelText, verticalLadder, distortWave) {
  ctx.save();
  ctx.translate(x, y);
  if (verticalLadder) ctx.rotate(-Math.PI / 2);

  ctx.fillStyle = "#FFFFFF";
  ctx.shadowColor = "rgba(0,0,0,0.22)";
  ctx.shadowBlur = 8;
  ctx.fillRect(-wBox / 2, -hBox / 2, wBox, hBox);
  ctx.shadowBlur = 0;

  ctx.strokeStyle = statusCol;
  ctx.lineWidth = 5;
  ctx.strokeRect(-wBox / 2, -hBox / 2, wBox, hBox);

  ctx.fillStyle = statusCol;
  ctx.font = "800 12.5px 'JetBrains Mono', monospace";
  ctx.textAlign = "center";
  ctx.fillText(labelText, 0, -hBox / 2 + 18);

  const pattern = "10100110110100101110100110101010110010100110110101011001011010010101";
  const startX = -wBox / 2 + 16;
  const modW = (wBox - 32) / pattern.length;
  ctx.fillStyle = "#111111";
  for (let i = 0; i < pattern.length; i++) {
    if (pattern[i] === "1") {
      const isGuard = (i < 3 || (i > 31 && i < 36) || i > pattern.length - 4);
      const barH = isGuard ? hBox - 42 : hBox - 52;
      const waveY = distortWave ? Math.sin(i * 0.65) * 4 : 0;
      ctx.fillRect(startX + i * modW, -hBox / 2 + 23 + waveY, modW * 1.05, barH);
    }
  }

  ctx.fillStyle = "#111111";
  ctx.font = "800 16px 'JetBrains Mono', monospace";
  ctx.textAlign = "center";
  ctx.fillText(eanStr, 0, hBox / 2 - 8);

  ctx.strokeStyle = statusCol;
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  ctx.moveTo(-wBox / 2 - 8, 3);
  ctx.lineTo(wBox / 2 + 8, 3);
  ctx.stroke();
  ctx.restore();
}

function renderDoypackUVTexture(skin, phys) {
  const w = texCanvas.width, h = texCanvas.height;
  texCtx.clearRect(0, 0, w, h);

  // Bare White Soft-Touch Doypack when no brand print is selected yet
  if (!skin || state.wrapType === "none") {
    const isKraft = state.finishId === "kraft_pouch";
    const isFoil = state.finishId === "foil_pouch";
    const bareGrad = texCtx.createLinearGradient(0, 0, 0, h);
    if (isKraft) {
      bareGrad.addColorStop(0, "#CFA87C");
      bareGrad.addColorStop(0.55, "#BE9568");
      bareGrad.addColorStop(1, "#A87E52");
    } else if (isFoil) {
      bareGrad.addColorStop(0, "#EBEEF2");
      bareGrad.addColorStop(0.55, "#D0D5DC");
      bareGrad.addColorStop(1, "#B4BBC4");
    } else {
      bareGrad.addColorStop(0, "#FFFFFF");
      bareGrad.addColorStop(0.55, "#F6F3EC");
      bareGrad.addColorStop(1, "#EAE5DC");
    }
    texCtx.fillStyle = bareGrad;
    texCtx.fillRect(0, 0, w, h);
    if (!isKraft && !isFoil) {
      // Delicate soft-touch seam & heat-seal contour shading so white Doypack pops crisply against studio background
      texCtx.fillStyle = "rgba(18,17,16,0.06)";
      texCtx.fillRect(0, 0, w, 128);
      texCtx.fillStyle = "rgba(18,17,16,0.16)";
      texCtx.fillRect(0, 126, w, 6);
      texCtx.fillRect(0, 146, w, 3);
      [0.25, 0.75].forEach(uSeam => {
        const sx = uSeam * w;
        const sg = texCtx.createLinearGradient(sx - 44, 0, sx + 44, 0);
        sg.addColorStop(0, "rgba(18,17,16,0)");
        sg.addColorStop(0.5, "rgba(18,17,16,0.10)");
        sg.addColorStop(1, "rgba(18,17,16,0)");
        texCtx.fillStyle = sg;
        texCtx.fillRect(sx - 44, 0, 88, h);
      });
    } else {
      texCtx.fillStyle = "rgba(18,17,16,0.10)";
      texCtx.fillRect(0, 128, w, 4);
      texCtx.fillStyle = "rgba(18,17,16,0.05)";
      texCtx.fillRect(0, 0, w, 128);
    }
    if (state.heatmap) {
      texCtx.fillStyle = "rgba(194,24,14,0.45)";
      texCtx.fillRect(0, 0, w, 175);
      texCtx.fillRect(0, h - 140, w, 140);
      [0.25, 0.75].forEach(seamU => texCtx.fillRect(seamU * w - 75, 0, 150, h));
    }
    if (sleeveTexture) sleeveTexture.needsUpdate = true;
    return;
  }

  let baseTop = "#FFFFFF", baseBot = "#EAE5DC", accent = "#C2180E", pill = "#C2180E", txtCol = "#141210";
  if (state.finishId === "kraft_pouch") {
    baseTop = "#CFA87C"; baseBot = "#AD8255"; txtCol = "#1C140C"; accent = "#0F5C46"; pill = "#C2180E";
  } else if (state.finishId === "foil_pouch") {
    baseTop = "#E5E7EB"; baseBot = "#B8BFC7"; txtCol = "#141619"; accent = "#1D4ED8"; pill = "#C2180E";
  } else if (skin.styleType === "black_gold") {
    baseTop = "#1C1A18"; baseBot = "#11100E"; accent = "#D9B263"; pill = "#C2180E"; txtCol = "#FAF7F2";
  } else if (skin.styleType === "white_swiss") {
    baseTop = "#FFFFFF"; baseBot = "#ECE7DD"; txtCol = "#141210"; accent = "#C2180E"; pill = "#C2180E";
  } else if (skin.styleType === "emerald_cobalt") {
    baseTop = "#0F5C46"; baseBot = "#083A2C"; txtCol = "#FAF7F0"; accent = "#EA580C"; pill = "#1D4ED8";
  }

  const grad = texCtx.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0, baseTop);
  grad.addColorStop(1, baseBot);
  texCtx.fillStyle = grad;
  texCtx.fillRect(0, 0, w, h);

  texCtx.fillStyle = "rgba(0,0,0,0.08)";
  texCtx.fillRect(0, 0, w, 128);
  texCtx.fillStyle = accent;
  texCtx.fillRect(0, 128, w, 10);

  if (state.heatmap) {
    texCtx.fillStyle = "rgba(194,24,14,0.45)";
    texCtx.fillRect(0, 0, w, 175);
    texCtx.fillRect(0, h - 140, w, 140);
    [0.25, 0.75].forEach(seamU => {
      texCtx.fillRect(seamU * w - 75, 0, 150, h);
    });
  }

  const fx = w * 0.5;
  texCtx.save();
  texCtx.textAlign = "center";
  texCtx.fillStyle = pill;
  texCtx.fillRect(fx - 170, 195, 340, 38);
  texCtx.fillStyle = "#FFFFFF";
  texCtx.font = "800 20px 'Inter', sans-serif";
  texCtx.fillText("STAND-UP POUCH · MOTORE B", fx, 221);

  texCtx.fillStyle = txtCol;
  texCtx.font = "900 72px 'Inter', sans-serif";
  texCtx.fillText(skin.brand, fx, 330);
  texCtx.fillStyle = accent;
  texCtx.font = "800 34px 'Inter', sans-serif";
  texCtx.fillText(skin.brandSub, fx, 378);

  texCtx.fillStyle = accent;
  texCtx.fillRect(fx - 260, 435, 520, 6);
  texCtx.fillStyle = txtCol;
  texCtx.font = "800 28px 'Inter', sans-serif";
  texCtx.fillText(skin.pouchSub, fx, 485);

  texCtx.strokeStyle = accent;
  texCtx.lineWidth = 4;
  texCtx.strokeRect(fx - 190, 535, 380, 125);
  texCtx.font = "900 38px 'JetBrains Mono', monospace";
  texCtx.fillText("CONTENUTO 1000 g", fx, 600);
  texCtx.font = "700 20px 'Inter', sans-serif";
  texCtx.fillText("ALTA BARRIERA · FORMATO 220MM", fx, 638);
  texCtx.restore();

  [0, w].forEach(bx => {
    texCtx.save();
    texCtx.translate(bx, 0);
    texCtx.fillStyle = txtCol;
    texCtx.textAlign = "center";
    texCtx.font = "900 32px 'Inter', sans-serif";
    texCtx.fillText("SPECIFICHE RETRO · BACK PANEL", 0, 215);
    texCtx.strokeStyle = txtCol;
    texCtx.lineWidth = 3;
    texCtx.strokeRect(-230, 240, 460, 320);

    texCtx.textAlign = "left";
    texCtx.font = "700 20px 'JetBrains Mono', monospace";
    const rows = [
      "Formato Busta .... 220 × 310 mm",
      "Soffietto Fondo ......... 95 mm",
      "Tenuta Saldatura ........ 145°C",
      "Barriera O₂/UV ....... Massima",
      "Peso Netto ............. 1000 g",
      `Stampa: ${state.pouchPrintType === "flexo" ? "Flessografica HD" : "Digitale Pre-Serie"}`
    ];
    rows.forEach((r, idx) => {
      texCtx.fillText(r, -205, 285 + idx * 44);
    });
    texCtx.restore();
  });

  const xOffNorm = (state.bcDoypackX / 100) * 0.46;
  const uPos = state.bcDoypackSide === "front" ? (0.5 + xOffNorm) : xOffNorm;
  const bcX = (((uPos % 1) + 1) % 1) * w;
  const bcY = Math.max(90, Math.min(h - 90, (1 - state.bcHeightPct / 100) * h));
  const statusCol = phys.ansiGrade === "F" ? "#C2180E" : (phys.ansiGrade === "C" ? "#E5A000" : "#147A3B");

  [bcX - w, bcX, bcX + w].forEach(drawX => {
    if (drawX < -280 || drawX > w + 280) return;
    drawEAN13Graphic(
      texCtx, drawX, bcY, 240, 130, skin.ean, statusCol,
      `EAN-13 · ${state.bcDoypackSide.toUpperCase()} · GRADE ${phys.ansiGrade}`,
      state.bcLadder, phys.ansiGrade === "F"
    );
  });

  if (sleeveTexture) sleeveTexture.needsUpdate = true;
}

// Shared 100% synchronized TD% / Curvature Heatmap matching evaluateLivePhysics() thresholds per active Film or Label substrate
function drawSynchronizedTDHeatmap(ctx, w, h, vessel, sSpan, isLabel, isOverlay) {
  const isSquare = vessel.shape === "square_soft";
  const fm = getFilm();
  const lp = getLabelPaper();
  const rawScale = vessel.shape === "alu_can" ? 235 : 100;
  const warnThr = isLabel ? lp.warnTD : fm.warnTD;
  const errThr = isLabel ? Math.min(lp.errTD, lp.maxTD) : Math.min(fm.errTD, fm.maxTD);

  const aOk = isOverlay ? 0.16 : 0.30;
  const aWarn = isOverlay ? 0.34 : 0.56;
  const aErr = isOverlay ? 0.44 : 0.68;

  const stepY = 8;
  const stepX = isSquare ? 32 : w;
  let prevBandState = null;

  for (let y = 0; y < h; y += stepY) {
    const vNorm = 0.04 + (1.0 - (y + stepY * 0.5) / h) * sSpan;
    const rNorm = getNormalizedRadiusAtV(vessel, vNorm);
    const baseMetric = isLabel
      ? Math.round((1 - rNorm) * (vNorm < 0.20 ? rawScale * 0.85 : rawScale))
      : Math.round((1 - rNorm / 1.14) * 100);

    if (!isSquare) {
      const mVal = Math.min(isLabel ? 68 : 72, baseMetric);
      const bState = mVal >= errThr ? "err" : (mVal >= warnThr ? "warn" : "ok");
      ctx.fillStyle = bState === "err"
        ? `rgba(194, 24, 14, ${aErr})`
        : (bState === "warn" ? `rgba(229, 160, 0, ${aWarn})` : `rgba(20, 122, 59, ${aOk})`);
      ctx.fillRect(0, y, w, stepY);

      // Crisp dashed threshold contour line right where yellow / red physics thresholds start
      if (isOverlay && prevBandState && prevBandState !== bState) {
        ctx.save();
        ctx.strokeStyle = (bState === "err" || prevBandState === "err") ? "#C2180E" : "#B45309";
        ctx.lineWidth = 4;
        ctx.setLineDash([18, 10]);
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
        ctx.restore();
      }
      prevBandState = bState;
    } else {
      for (let x = 0; x < w; x += stepX) {
        const theta = ((x + stepX * 0.5) / w - 0.5) * Math.PI * 2;
        const cornerPen = Math.round(Math.abs(Math.sin(2 * theta)) * (isLabel ? 26 : 11));
        const mVal = Math.min(isLabel ? 68 : 72, baseMetric + cornerPen);
        const bState = mVal >= errThr ? "err" : (mVal >= warnThr ? "warn" : "ok");
        ctx.fillStyle = bState === "err"
          ? `rgba(194, 24, 14, ${aErr})`
          : (bState === "warn" ? `rgba(229, 160, 0, ${aWarn})` : `rgba(20, 122, 59, ${aOk})`);
        ctx.fillRect(x, y, stepX, stepY);
      }
    }
  }
}

function renderAdhesiveLabelUVTexture(skin, vessel, phys) {
  const w = texCanvas.width, h = texCanvas.height;
  texCtx.clearRect(0, 0, w, h);

  const lp = getLabelPaper();
  const sSpan = vessel.shape === "jar_lux" ? 0.71 : (vessel.shape === "wine_bordeaux" ? 0.74 : (vessel.shape === "alu_can" ? 0.90 : 0.80));
  function vesselVtoY(vPos) {
    const t = Math.max(0, Math.min(1, (vPos - 0.04) / sSpan));
    return (1 - t) * h;
  }

  const { vMin, vMax } = getSleeveVerticalBand();
  const syTop = vesselVtoY(vMax);
  const syBot = vesselVtoY(vMin);
  const syH = Math.max(200, syBot - syTop);
  const cy = (syTop + syBot) / 2;
  const slOffsetPx = (state.sleeveAngleDeg / 360) * w;
  const statusCol = phys.sleeveStatus === "err" ? "#C2180E" : (phys.sleeveStatus === "warn" ? "#E5A000" : "#147A3B");
  const stressNorm = Math.max(0, Math.min(1.4, (phys.sleeveTD - (lp.warnTD - 2)) / Math.max(8, lp.errTD - lp.warnTD + 6)));
  const topStress = phys.labelTopStress || 0;
  const botStress = phys.labelBotStress || 0;
  const cornerStress = phys.labelCornerStress || 0;
  const isClear = !!lp.transparentBg;

  if (state.heatmap) {
    drawSynchronizedTDHeatmap(texCtx, w, h, vessel, sSpan, true, false);
  }

  [-w, 0, w].forEach(seamOff => {
    const cx = w * 0.5 + slOffsetPx + seamOff;
    const isCan = vessel.shape === "alu_can";
    const lwBase = isCan ? Math.round(w * 0.85) : (vessel.shape === "jar_lux" ? 820 : (vessel.shape === "square_soft" ? 450 : (vessel.shape === "wine_bordeaux" ? 460 : 480)));
    const lw = Math.min(Math.round(w * 0.90), Math.round(lwBase * getLabelWidthMultiplier(vessel)));
    const labelCenter = isCan ? (cx - 540) : cx;
    const labelLeft = labelCenter - lw / 2;
    const labelRight = labelCenter + lw / 2;
    if (labelRight < -100 || labelLeft > w + 100) return;
    const lh = syH;
    const lShape = skin.labelShape || "arch";
    const isNeutralWhite = skin.styleType === "neutral_white";

    function buildLabelPath() {
      texCtx.beginPath();
      if (isCan) {
        if (lShape === "octagon") {
          const ch = 26;
          texCtx.moveTo(labelLeft + ch, syTop + 6);
          texCtx.lineTo(labelRight - ch, syTop + 6);
          texCtx.lineTo(labelRight, syTop + 6 + ch);
          texCtx.lineTo(labelRight, syBot - 6 - ch);
          texCtx.lineTo(labelRight - ch, syBot - 6);
          texCtx.lineTo(labelLeft + ch, syBot - 6);
          texCtx.lineTo(labelLeft, syBot - 6 - ch);
          texCtx.lineTo(labelLeft, syTop + 6 + ch);
          texCtx.closePath();
        } else if (lShape === "pill_shield") {
          texCtx.roundRect(labelLeft, syTop + 10, lw, lh - 20, Math.min(68, (lh - 20) * 0.42));
        } else {
          texCtx.roundRect(labelLeft, syTop + 6, lw, lh - 12, 12);
        }
      } else if (lShape === "octagon") {
        // Tall octagonal emerald-cut plaque for Nocturne Nobile
        const ch = Math.min(44, Math.round(lw * 0.14));
        const crown = 16;
        texCtx.moveTo(cx - lw / 2 + ch, syTop + 10);
        texCtx.lineTo(cx, syTop - crown);
        texCtx.lineTo(cx + lw / 2 - ch, syTop + 10);
        texCtx.lineTo(cx + lw / 2, syTop + 10 + ch);
        texCtx.lineTo(cx + lw / 2, syBot - 10 - ch);
        texCtx.lineTo(cx + lw / 2 - ch, syBot - 10);
        texCtx.lineTo(cx - lw / 2 + ch, syBot - 10);
        texCtx.lineTo(cx - lw / 2, syBot - 10 - ch);
        texCtx.lineTo(cx - lw / 2, syTop + 10 + ch);
        texCtx.closePath();
      } else if (lShape === "pill_shield") {
        // Panoramic oval-pill shield for Verde Botanica
        const rad = Math.min(92, Math.round(lh * 0.42));
        texCtx.moveTo(cx - lw / 2 + rad, syTop + 12);
        texCtx.quadraticCurveTo(cx, syTop - 22, cx + lw / 2 - rad, syTop + 12);
        texCtx.quadraticCurveTo(cx + lw / 2, syTop + 12, cx + lw / 2, cy);
        texCtx.quadraticCurveTo(cx + lw / 2, syBot - 12, cx + lw / 2 - rad, syBot - 12);
        texCtx.quadraticCurveTo(cx, syBot + 8, cx - lw / 2 + rad, syBot - 12);
        texCtx.quadraticCurveTo(cx - lw / 2, syBot - 12, cx - lw / 2, cy);
        texCtx.quadraticCurveTo(cx - lw / 2, syTop + 12, cx - lw / 2 + rad, syTop + 12);
        texCtx.closePath();
      } else if (vessel.shape === "wine_bordeaux") {
        texCtx.moveTo(cx - lw / 2, syTop + 44);
        texCtx.quadraticCurveTo(cx, syTop - 16, cx + lw / 2, syTop + 44);
        texCtx.lineTo(cx + lw / 2, syBot - 16);
        texCtx.lineTo(cx - lw / 2, syBot - 16);
        texCtx.closePath();
      } else if (vessel.shape === "jar_lux") {
        texCtx.roundRect(cx - lw / 2, syTop + 12, lw, lh - 24, 28);
      } else if (vessel.shape === "square_soft") {
        texCtx.roundRect(cx - lw / 2, syTop + 8, lw, lh - 16, 42);
      } else {
        texCtx.moveTo(cx - lw / 2, syTop + 70);
        texCtx.quadraticCurveTo(cx, syTop - 20, cx + lw / 2, syTop + 70);
        texCtx.lineTo(cx + lw / 2, syBot - 24);
        texCtx.quadraticCurveTo(cx + lw / 2, syBot, cx + lw / 2 - 24, syBot);
        texCtx.lineTo(cx - lw / 2 + 24, syBot);
        texCtx.quadraticCurveTo(cx - lw / 2, syBot, cx - lw / 2, syBot - 24);
        texCtx.closePath();
      }
    }

    const darkVessel = vessel.shape === "wine_bordeaux";
    const lFill = isClear
      ? (skin.styleType === "black_gold" ? "rgba(18, 16, 20, 0.22)" : (skin.styleType === "emerald_cobalt" ? "rgba(15, 92, 70, 0.20)" : "rgba(255, 255, 255, 0.22)"))
      : (skin.styleType === "black_gold" ? "#151418" : (skin.styleType === "emerald_cobalt" ? "#0F5C46" : (lp.laidTexture ? "#F8F3E8" : "#FFFFFF")));
    const lText = isClear
      ? (darkVessel ? "#FAF7F0" : (skin.styleType === "black_gold" ? "#161311" : (skin.styleType === "emerald_cobalt" ? "#0B4333" : "#161311")))
      : ((skin.styleType === "white_swiss" || isNeutralWhite) ? "#161311" : "#FAF7F0");
    const lAccent = isNeutralWhite ? "#B8B0A4" : (skin.styleType === "black_gold" ? "#C99F45" : (skin.styleType === "emerald_cobalt" ? "#EA580C" : "#C2180E"));
    const bcStatCol = phys.ansiGrade === "F" ? "#C2180E" : (phys.ansiGrade === "C" ? "#E5A000" : "#147A3B");

    texCtx.save();
    // Physical die-cut drop shadow underneath the adhesive sticker (grows stronger as corners lift!)
    buildLabelPath();
    texCtx.shadowColor = `rgba(18, 13, 10, ${(0.24 + 0.26 * Math.min(1, stressNorm) * lp.stiffness).toFixed(2)})`;
    texCtx.shadowBlur = 12 + Math.round(14 * Math.min(1, stressNorm) * lp.stiffness);
    texCtx.shadowOffsetX = 0;
    texCtx.shadowOffsetY = 4 + Math.round(6 * Math.min(1, stressNorm) * lp.stiffness);
    texCtx.fillStyle = lFill;
    texCtx.fill();
    texCtx.shadowColor = "transparent";
    texCtx.shadowBlur = 0;
    texCtx.shadowOffsetY = 0;

    // Die-cut rim stroke
    texCtx.lineWidth = isClear ? 3.5 : (isCan ? 6 : 5);
    texCtx.strokeStyle = isClear
      ? (phys.sleeveStatus === "ok" ? "rgba(255,255,255,0.58)" : statusCol)
      : (phys.sleeveStatus === "ok" ? lAccent : statusCol);
    texCtx.stroke();
    texCtx.clip();

    // 1) Substrate-specific surface grain / sheen
    if (lp.laidTexture) {
      // Fine horizontal vergata laid-cotton paper lines
      texCtx.fillStyle = (skin.styleType === "white_swiss" || isNeutralWhite) ? "rgba(110, 92, 68, 0.055)" : "rgba(255, 250, 240, 0.045)";
      for (let ly = syTop; ly < syBot; ly += 7) {
        texCtx.fillRect(labelLeft, ly, lw, 1.8);
      }
    } else if (isClear) {
      // Crystal clear PET diagonal specular film reflection
      const sheenG = texCtx.createLinearGradient(labelLeft, syTop, labelRight, syBot);
      sheenG.addColorStop(0.0, "rgba(255,255,255,0.16)");
      sheenG.addColorStop(0.35, "rgba(255,255,255,0.03)");
      sheenG.addColorStop(0.52, "rgba(255,255,255,0.22)");
      sheenG.addColorStop(0.68, "rgba(255,255,255,0.02)");
      sheenG.addColorStop(1.0, "rgba(255,255,255,0.14)");
      texCtx.fillStyle = sheenG;
      texCtx.fillRect(labelLeft, syTop, lw, lh);
    } else {
      // Subtle edge-vignette wrap shading on PP / PE film labels
      const wrapG = texCtx.createLinearGradient(labelLeft, 0, labelRight, 0);
      wrapG.addColorStop(0, "rgba(0,0,0,0.07)");
      wrapG.addColorStop(0.18, "rgba(255,255,255,0.04)");
      wrapG.addColorStop(0.82, "rgba(255,255,255,0.04)");
      wrapG.addColorStop(1, "rgba(0,0,0,0.07)");
      texCtx.fillStyle = wrapG;
      texCtx.fillRect(labelLeft, syTop, lw, lh);
    }

    // Inner die-cut gold/white accent frame for octagon & pill shapes (adds distinctive craft detail)
    if (!isNeutralWhite && lShape === "octagon") {
      texCtx.strokeStyle = "rgba(217, 178, 99, 0.55)";
      texCtx.lineWidth = 2.5;
      texCtx.strokeRect(labelLeft + 20, syTop + 26, lw - 40, lh - 52);
    }

    // Subtle upper graphic warp when label creases on curved shoulder
    const topPinch = stressNorm > 0.35 ? Math.max(0.76, 1 - (stressNorm - 0.35) * 0.24 * lp.stiffness) : 1.0;

    texCtx.textAlign = "center";
    if (isNeutralWhite) {
      // Blank white unprinted die-cut label: ONLY integrated EAN-13 barcode, zero brand copy!
      const bcXPos = isCan ? (cx - 90) : (vessel.shape === "jar_lux" ? cx : cx);
      const bcYPos = vessel.shape === "jar_lux" ? cy : (syBot - Math.min(92, Math.round(lh * 0.26)));
      drawEAN13Graphic(texCtx, bcXPos, bcYPos, Math.min(230, lw - 38), Math.min(108, lh - 38), skin.ean, bcStatCol, `EAN-13 · GRADE ${phys.ansiGrade}`, false, phys.ansiGrade === "F");
    } else if (isCan) {
      texCtx.fillStyle = lAccent;
      texCtx.fillRect(labelLeft, syTop + 18, lw, 12);
      texCtx.fillRect(labelLeft, syBot - 26, lw, 12);

      const fx = cx - 90;
      texCtx.save();
      texCtx.translate(fx, syTop + lh * 0.30);
      texCtx.scale(topPinch, 1.0);
      texCtx.fillStyle = lAccent;
      texCtx.font = "800 18px 'Inter', sans-serif";
      texCtx.fillText(`ETICHETTA FULL-WRAP LATTINA · ${lp.id}`, 0, -lh * 0.30 + 62);

      texCtx.fillStyle = lText;
      texCtx.font = "900 66px 'Inter', sans-serif";
      texCtx.fillText(skin.brand, 0, -lh * 0.03);
      texCtx.fillStyle = lAccent;
      texCtx.font = "800 30px 'Inter', sans-serif";
      texCtx.fillText(skin.brandSub, 0, lh * 0.07);
      texCtx.fillStyle = lText;
      texCtx.font = "700 22px 'Inter', sans-serif";
      texCtx.fillText("EDIZIONE SPECIALE · 330 ML", 0, lh * 0.18);
      texCtx.font = "600 16px 'JetBrains Mono', monospace";
      texCtx.fillText(lp.name, 0, lh * 0.26);
      texCtx.restore();

      const lx = labelLeft + 340;
      if (lw > 1200) {
        texCtx.strokeStyle = lAccent;
        texCtx.lineWidth = 3;
        texCtx.strokeRect(lx - 150, syTop + 120, 300, lh - 220);
        texCtx.fillStyle = lText;
        texCtx.font = "800 22px 'Inter', sans-serif";
        texCtx.fillText("SPECIFICHE LATTINA", lx, syTop + 170);
        texCtx.font = "600 19px 'JetBrains Mono', monospace";
        ["Formato: 330 ml Sleek", "Corpo: Alluminio ALU 41", "Riciclo: 100% Riciclabile", "Fondo: SOT 202 Ermetico"].forEach((row, i) => {
          texCtx.fillText(row, lx, syTop + 228 + i * 48);
        });
      }

      drawEAN13Graphic(texCtx, fx, syBot - 110, 236, 110, skin.ean, bcStatCol, `EAN-13 · GRADE ${phys.ansiGrade}`, false, phys.ansiGrade === "F");
    } else if (vessel.shape === "jar_lux") {
      texCtx.save();
      texCtx.translate(cx - Math.min(130, lw * 0.17), cy);
      texCtx.scale(topPinch, 1.0);
      texCtx.fillStyle = lText;
      texCtx.font = lShape === "octagon" ? "900 38px Georgia, serif" : "900 44px 'Inter', sans-serif";
      texCtx.fillText(skin.brand + " " + skin.brandSub, 0, -24);
      texCtx.fillStyle = lAccent;
      texCtx.font = "700 20px 'Inter', sans-serif";
      texCtx.fillText(lp.name, 0, 18);
      texCtx.restore();
      drawEAN13Graphic(texCtx, cx + Math.min(220, lw * 0.25), cy, Math.min(220, lw * 0.34), Math.min(112, lh * 0.42), skin.ean, bcStatCol, `EAN-13 · GRADE ${phys.ansiGrade}`, false, phys.ansiGrade === "F");
    } else {
      const subTitle = vessel.shape === "wine_bordeaux" ? skin.wineSub : skin.product;
      const wScale = Math.min(1.0, lw / 470);
      const hScale = Math.min(1.0, lh / 320);
      const tScale = Math.min(wScale, hScale);
      const topYFrac = lShape === "pill_shield" ? 0.36 : 0.34;
      texCtx.save();
      texCtx.translate(cx, syTop + lh * topYFrac);
      texCtx.scale(topPinch * tScale, tScale);
      texCtx.fillStyle = lAccent;
      texCtx.font = "800 18px 'Inter', sans-serif";
      texCtx.fillText(`ETICHETTA ${lp.id}`, 0, lShape === "pill_shield" ? -68 : -82);

      texCtx.fillStyle = lText;
      texCtx.font = (vessel.shape === "wine_bordeaux" || lShape === "octagon") ? "800 50px Georgia, serif" : "900 54px 'Inter', sans-serif";
      texCtx.fillText(skin.brand, 0, -4);
      texCtx.fillStyle = lAccent;
      texCtx.font = "700 26px 'Inter', sans-serif";
      texCtx.fillText(skin.brandSub, 0, 34);
      texCtx.fillStyle = lText;
      texCtx.font = "700 19px 'Inter', sans-serif";
      texCtx.fillText(subTitle, 0, 70);
      texCtx.restore();

      const bcW = Math.min(240, lw - 44);
      const bcH = Math.min(114, Math.round(lh * (lShape === "pill_shield" ? 0.31 : 0.34)));
      drawEAN13Graphic(texCtx, cx, syBot - Math.round(bcH * 0.56) - 18, bcW, bcH, skin.ean, bcStatCol, `EAN-13 · GRADE ${phys.ansiGrade}`, false, phys.ansiGrade === "F");
    }

    // 2) PHOTOREALISTIC MOVEMENT-DRIVEN ADHESIVE LABEL PHYSICS (creases, dog-ear lift, air blisters, silvering)
    if (stressNorm > 0.05) {
      const eff = Math.min(1.15, stressNorm * (0.45 + 0.65 * lp.stiffness));
      const foldCount = lp.laidTexture ? 7 : (isClear ? 6 : 5);
      const fromBottom = botStress > topStress;
      const edgeY = fromBottom ? syBot : syTop;
      const dirY = fromBottom ? -1 : 1;
      const foldSpan = lh * (0.24 + 0.28 * Math.min(1, eff));

      // A. Radial paper/film dart-wrinkle folds (realistic light & shadow valleys, not cartoon lines!)
      if (topStress > 2 || botStress > 2) {
        for (let f = 0; f < foldCount; f++) {
          const frac = (f + 0.5) / foldCount;
          const xTop = labelLeft + lw * (0.06 + frac * 0.88);
          const fanSpread = (frac - 0.5) * lw * 0.14;
          const xEnd = xTop - fanSpread;
          const foldW = (14 + 18 * eff) * (lp.laidTexture ? 1.15 : 0.88);
          const shAlpha = Math.min(0.46, 0.14 + 0.26 * eff);
          const hiAlpha = Math.min(0.55, 0.18 + 0.30 * eff);

          const gCrease = texCtx.createLinearGradient(xTop - foldW, edgeY, xTop + foldW, edgeY);
          gCrease.addColorStop(0.0, "rgba(0,0,0,0)");
          gCrease.addColorStop(0.32, `rgba(22, 16, 12, ${shAlpha.toFixed(3)})`);
          gCrease.addColorStop(0.50, `rgba(255, 255, 255, ${hiAlpha.toFixed(3)})`);
          gCrease.addColorStop(0.72, `rgba(28, 20, 14, ${(shAlpha * 0.72).toFixed(3)})`);
          gCrease.addColorStop(1.0, "rgba(0,0,0,0)");

          texCtx.save();
          texCtx.fillStyle = gCrease;
          texCtx.beginPath();
          texCtx.moveTo(xTop - foldW, edgeY);
          texCtx.lineTo(xTop + foldW, edgeY);
          texCtx.lineTo(xEnd + foldW * 0.28, edgeY + dirY * foldSpan);
          texCtx.lineTo(xEnd - foldW * 0.28, edgeY + dirY * foldSpan);
          texCtx.closePath();
          texCtx.fill();
          texCtx.restore();
        }

        // B. Dog-ear corner lift shadows & adhesive-gap curl on outer corners
        const cornerW = lw * (0.14 + 0.10 * Math.min(1, eff));
        const cornerH = lh * (0.16 + 0.12 * Math.min(1, eff));
        [labelLeft, labelRight].forEach((edgeX, sideIdx) => {
          const sgn = sideIdx === 0 ? 1 : -1;
          const gDog = texCtx.createLinearGradient(edgeX, edgeY, edgeX + sgn * cornerW, edgeY + dirY * cornerH);
          if (isClear) {
            // Silvering white air-halo under lifted clear PET corner
            gDog.addColorStop(0.0, `rgba(245, 248, 255, ${Math.min(0.68, 0.26 + 0.38 * eff).toFixed(2)})`);
            gDog.addColorStop(0.55, `rgba(225, 232, 242, ${Math.min(0.32, 0.12 + 0.18 * eff).toFixed(2)})`);
            gDog.addColorStop(1.0, "rgba(255,255,255,0)");
          } else {
            gDog.addColorStop(0.0, `rgba(18, 12, 8, ${Math.min(0.42, 0.14 + 0.24 * eff).toFixed(2)})`);
            gDog.addColorStop(0.45, `rgba(255, 250, 242, ${Math.min(0.38, 0.12 + 0.22 * eff).toFixed(2)})`);
            gDog.addColorStop(1.0, "rgba(0,0,0,0)");
          }
          texCtx.fillStyle = gDog;
          texCtx.beginPath();
          texCtx.moveTo(edgeX, edgeY);
          texCtx.lineTo(edgeX + sgn * cornerW, edgeY);
          texCtx.lineTo(edgeX, edgeY + dirY * cornerH);
          texCtx.closePath();
          texCtx.fill();
        });
      }

      // C. Vertical corner-wrap crease & air-channel on Square Bottle when dragged across 45° corners
      if (cornerStress > 4 && vessel.shape === "square_soft") {
        const cEff = Math.min(1.1, (cornerStress / 24) * (0.45 + 0.65 * lp.stiffness));
        const seamShift = Math.sin((state.sleeveAngleDeg * Math.PI) / 90) * lw * 0.24;
        const creaseX = labelCenter + seamShift;
        const gVert = texCtx.createLinearGradient(creaseX - 28, 0, creaseX + 28, 0);
        gVert.addColorStop(0.0, "rgba(0,0,0,0)");
        gVert.addColorStop(0.35, `rgba(18, 13, 10, ${(0.28 * cEff).toFixed(3)})`);
        gVert.addColorStop(0.52, `rgba(255, 255, 255, ${(0.48 * cEff).toFixed(3)})`);
        gVert.addColorStop(0.70, `rgba(24, 18, 14, ${(0.22 * cEff).toFixed(3)})`);
        gVert.addColorStop(1.0, "rgba(0,0,0,0)");
        texCtx.fillStyle = gVert;
        texCtx.fillRect(creaseX - 28, syTop, 56, lh);
      }

      // D. Trapped air bubbles / silvering blisters (prominent on PP_WHITE & PET_CLEAR, subtle on PE_SQUEEZE)
      if (!lp.laidTexture && eff > 0.25) {
        const bubCount = isClear ? 7 : 5;
        for (let b = 0; b < bubCount; b++) {
          const bf = (b + 0.4) / bubCount;
          const bx = labelLeft + lw * (0.10 + bf * 0.80);
          const by = edgeY + dirY * (26 + ((b * 37) % 92) + 18 * Math.sin(b * 2.1));
          const brx = (14 + ((b * 13) % 18)) * Math.min(1.15, eff);
          const bry = (7 + ((b * 9) % 10)) * Math.min(1.15, eff);
          texCtx.save();
          texCtx.translate(bx, by);
          texCtx.rotate((bf - 0.5) * 0.75);
          // Outer trapped-air shadow ring
          texCtx.fillStyle = isClear
            ? `rgba(235, 242, 252, ${Math.min(0.62, 0.28 * eff).toFixed(2)})`
            : `rgba(25, 18, 14, ${Math.min(0.24, 0.14 * eff).toFixed(2)})`;
          texCtx.beginPath();
          texCtx.ellipse(0, 2, brx, bry, 0, 0, Math.PI * 2);
          texCtx.fill();
          // Raised glossy blister highlight crescent
          texCtx.fillStyle = `rgba(255, 255, 255, ${Math.min(0.65, 0.36 * eff).toFixed(2)})`;
          texCtx.beginPath();
          texCtx.ellipse(-brx * 0.15, -bry * 0.18, brx * 0.72, bry * 0.52, 0, 0, Math.PI * 2);
          texCtx.fill();
          texCtx.restore();
        }
      }
    }

    texCtx.restore();
  });

  if (state.heatmap) {
    drawSynchronizedTDHeatmap(texCtx, w, h, vessel, sSpan, true, true);
  }

  if (sleeveTexture) sleeveTexture.needsUpdate = true;
}

function renderSerigrafiaCanUVTexture(skin, vessel, phys) {
  const w = texCanvas.width, h = texCanvas.height;
  texCtx.clearRect(0, 0, w, h);

  const ink = getSerigrafiaInk();
  // Full 360° silk-screen ink printed directly on brushed aluminum body
  if (skin.styleType === "black_gold") {
    texCtx.fillStyle = "rgba(18, 17, 20, 0.84)";
    texCtx.fillRect(0, 26, w, h - 52);
    texCtx.fillStyle = "#D9B263";
    texCtx.fillRect(0, 38, w, 10);
    texCtx.fillRect(0, h - 48, w, 12);
  } else if (skin.styleType === "emerald_cobalt") {
    texCtx.fillStyle = "rgba(15, 92, 70, 0.86)";
    texCtx.fillRect(0, 26, w, h - 52);
    texCtx.fillStyle = "#EA580C";
    texCtx.fillRect(0, 38, w, 14);
    texCtx.fillRect(0, h - 50, w, 16);
  } else {
    texCtx.fillStyle = "rgba(250, 247, 240, 0.88)";
    texCtx.fillRect(0, 26, w, h - 52);
    texCtx.fillStyle = "#C2180E";
    texCtx.fillRect(0, 38, w, 18);
    texCtx.fillStyle = "#B89352";
    texCtx.fillRect(0, 62, w, 5);
    texCtx.fillRect(0, h - 42, w, 10);
  }

  if (state.heatmap) {
    for (let y = 0; y < h; y += 8) {
      const vNorm = 0.04 + (1 - y / h) * 0.90;
      const curvePct = Math.round((1 - getNormalizedRadiusAtV(vessel, vNorm)) * 260);
      texCtx.fillStyle = curvePct > ink.maxTD + 10 ? "rgba(194,24,14,0.48)" : (curvePct >= ink.maxTD - 4 ? "rgba(229,160,0,0.38)" : "rgba(20,122,59,0.16)");
      texCtx.fillRect(0, y, w, 8);
    }
  }

  const centerX = w * 0.5;
  const inkTxt = skin.styleType === "white_swiss" ? "#161311" : "#FAF7F0";
  const inkAcc = skin.styleType === "black_gold" ? "#D9B263" : (skin.styleType === "emerald_cobalt" ? "#EA580C" : "#C2180E");

  texCtx.save();
  texCtx.textAlign = "center";
  texCtx.fillStyle = inkAcc;
  texCtx.fillRect(centerX - 210, 145, 420, 34);
  texCtx.fillStyle = "#FFFFFF";
  texCtx.font = "800 17px 'Inter', sans-serif";
  texCtx.fillText(`SERIGRAFIA DIRETTA 360° · ${ink.id}`, centerX, 168);

  texCtx.fillStyle = inkTxt;
  texCtx.font = "900 76px 'Inter', sans-serif";
  texCtx.fillText(skin.brand, centerX, h * 0.34);
  texCtx.fillStyle = inkAcc;
  texCtx.font = "800 34px 'Inter', sans-serif";
  texCtx.fillText(skin.brandSub, centerX, h * 0.42);
  texCtx.fillStyle = inkTxt;
  texCtx.font = "700 24px 'Inter', sans-serif";
  texCtx.fillText("STAMPA SERIGRAFICA DIRETTA SU ALLUMINIO 330 ML", centerX, h * 0.52);
  texCtx.font = "600 17px 'JetBrains Mono', monospace";
  texCtx.fillText(ink.name.toUpperCase(), centerX, h * 0.58);
  texCtx.restore();

  // Back side 360° metallic typography
  [0, w].forEach(bx => {
    texCtx.save();
    texCtx.translate(bx, 0);
    texCtx.textAlign = "center";
    texCtx.fillStyle = inkTxt;
    texCtx.font = "800 26px 'Inter', sans-serif";
    texCtx.fillText("SERIGRAFIA INDUSTRIALE 360°", 0, h * 0.28);
    texCtx.font = "600 18px 'JetBrains Mono', monospace";
    texCtx.fillText("Zero pellicola adesiva · zero giunta verticale", 0, h * 0.34);
    texCtx.fillText("Riciclabilità 100% ALU 41", 0, h * 0.40);
    texCtx.restore();
  });

  // Movable barcode anywhere over full can surface
  const uNorm = (((0.5 + (state.bcAngleDeg / 360)) % 1) + 1) % 1;
  const vBcPos = 0.04 + (state.bcHeightPct / 100) * 0.90;
  const bcX = uNorm * w;
  const bcY = Math.max(82, Math.min(h - 82, (1 - (vBcPos - 0.04) / 0.90) * h));
  const bcStatCol = phys.ansiGrade === "F" ? "#C2180E" : (phys.ansiGrade === "C" ? "#E5A000" : "#147A3B");

  [bcX - w, bcX, bcX + w].forEach(drawX => {
    if (drawX < -300 || drawX > w + 300) return;
    drawEAN13Graphic(texCtx, drawX, bcY, 240, 132, skin.ean, bcStatCol, `EAN-13 SERIGRAFIA · GRADE ${phys.ansiGrade}`, state.bcLadder, phys.ansiGrade === "F" && !state.bcLadder);
  });

  if (sleeveTexture) sleeveTexture.needsUpdate = true;
}

function renderSleeveUVTexture() {
  const skin = getSkin();
  const vessel = getVessel();
  clampBarcodeToSleeve();
  const phys = evaluateLivePhysics();

  if (vessel.shape === "doypack") {
    return renderDoypackUVTexture(skin, phys);
  }
  if (!hasWrap() || !skin) {
    texCtx.clearRect(0, 0, texCanvas.width, texCanvas.height);
    if (sleeveTexture) sleeveTexture.needsUpdate = true;
    return;
  }
  if (isSerigrafiaMode()) {
    return renderSerigrafiaCanUVTexture(skin, vessel, phys);
  }
  if (isLabelMode()) {
    return renderAdhesiveLabelUVTexture(skin, vessel, phys);
  }

  const w = texCanvas.width, h = texCanvas.height;
  texCtx.clearRect(0, 0, w, h);

  const sSpan = vessel.shape === "jar_lux" ? 0.71 : (vessel.shape === "wine_bordeaux" ? 0.74 : (vessel.shape === "alu_can" ? 0.90 : 0.80));
  function vesselVtoY(vPos) {
    const t = Math.max(0, Math.min(1, (vPos - 0.04) / sSpan));
    return (1 - t) * h;
  }

  texCtx.fillStyle = "rgba(255, 255, 255, 0.05)";
  texCtx.fillRect(0, 0, w, h);

  if (state.heatmap) {
    drawSynchronizedTDHeatmap(texCtx, w, h, vessel, sSpan, false, false);
  }

  const { vMin, vMax } = getSleeveVerticalBand();
  const syTop = vesselVtoY(vMax);
  const syBot = vesselVtoY(vMin);
  const syH = Math.max(190, syBot - syTop);
  const slOffsetPx = (state.sleeveAngleDeg / 360) * w;

  [-w, 0, w].forEach(seamOff => {
    const centerX = w * 0.5 + slOffsetPx + seamOff;
    if (centerX < -w * 0.8 || centerX > w * 1.8) return;

    texCtx.save();
    texCtx.beginPath();
    texCtx.rect(0, syTop, w, syH);
    texCtx.clip();

    if (skin.styleType === "neutral_clear") {
      // Clear unprinted transparent shrink sleeve film (lets underlying bottle & liquid show cleanly through!)
      const gClear = texCtx.createLinearGradient(0, syTop, 0, syBot);
      gClear.addColorStop(0.0, "rgba(244, 249, 255, 0.30)");
      gClear.addColorStop(0.5, "rgba(232, 242, 252, 0.16)");
      gClear.addColorStop(1.0, "rgba(222, 234, 246, 0.28)");
      texCtx.fillStyle = gClear;
      texCtx.fillRect(centerX - w / 2, syTop, w, syH);

      // Vertical cylindrical film specular streaks so transparent shrink film is visibly mounted & moving
      [0.22, 0.38, 0.64, 0.81].forEach(uFrac => {
        const sx = centerX - w / 2 + uFrac * w;
        const gSheen = texCtx.createLinearGradient(sx - 28, 0, sx + 28, 0);
        gSheen.addColorStop(0, "rgba(255,255,255,0)");
        gSheen.addColorStop(0.5, "rgba(255,255,255,0.34)");
        gSheen.addColorStop(1, "rgba(255,255,255,0)");
        texCtx.fillStyle = gSheen;
        texCtx.fillRect(sx - 28, syTop, 56, syH);
      });

      // Top & bottom transparent film cut-rim borders (shows live shrink contour height)
      const rimCol = phys.sleeveStatus === "err" ? "rgba(194, 24, 14, 0.82)" : (phys.sleeveStatus === "warn" ? "rgba(217, 119, 6, 0.82)" : "rgba(71, 85, 105, 0.45)");
      texCtx.fillStyle = rimCol;
      texCtx.fillRect(centerX - w / 2, syTop, w, 5);
      texCtx.fillRect(centerX - w / 2, syBot - 5, w, 5);
      texCtx.fillStyle = "rgba(255, 255, 255, 0.72)";
      texCtx.fillRect(centerX - w / 2, syTop + 5, w, 3);
      texCtx.fillRect(centerX - w / 2, syBot - 8, w, 3);

    } else if (skin.styleType === "white_swiss") {
      const g = texCtx.createLinearGradient(0, syTop, 0, syBot);
      g.addColorStop(0, "#FDFCF9");
      g.addColorStop(1, "#EFEBE2");
      texCtx.fillStyle = g;
      texCtx.globalAlpha = state.xray ? 0.86 : 0.96;
      texCtx.fillRect(centerX - w / 2, syTop, w, syH);
      texCtx.globalAlpha = 1.0;

      texCtx.fillStyle = "#C2180E";
      texCtx.fillRect(centerX - w / 2, syTop + 14, w, 18);
      texCtx.fillStyle = "#B89352";
      texCtx.fillRect(centerX - w / 2, syTop + 36, w, 4);
      texCtx.fillRect(centerX - w / 2, syBot - 22, w, 10);

      const fmCur = getFilm();
      const tdOver = Math.max(0, phys.sleeveTD - (fmCur.warnTD - 4));
      const topPinch = tdOver > 0 ? Math.max(0.54, 1 - (tdOver * fmCur.pinchScale) / 72) : 1.0;
      texCtx.save();
      texCtx.translate(centerX, syTop + syH * 0.28);
      texCtx.scale(topPinch, 1.0);
      texCtx.textAlign = "center";

      texCtx.fillStyle = "#C2180E";
      texCtx.fillRect(-130, -95, 260, 32);
      texCtx.fillStyle = "#FFFFFF";
      texCtx.font = "800 16px 'Inter', sans-serif";
      texCtx.fillText("MILANO · SWISS SCIENCE", 0, -73);

      texCtx.fillStyle = "#161311";
      texCtx.font = "900 68px 'Inter', sans-serif";
      texCtx.fillText(skin.brand, 0, -8);
      texCtx.font = "400 28px 'Inter', sans-serif";
      texCtx.fillText(skin.brandSub, 0, 32);
      texCtx.restore();

      texCtx.save();
      texCtx.translate(centerX, syTop + syH * 0.65);
      texCtx.strokeStyle = "#B89352";
      texCtx.lineWidth = 2.5;
      texCtx.strokeRect(-185, -45, 370, 128);
      texCtx.fillStyle = "#161311";
      texCtx.textAlign = "center";
      texCtx.font = "800 21px 'Inter', sans-serif";
      texCtx.fillText(vessel.shape === "wine_bordeaux" ? skin.wineSub : skin.product, 0, -10);
      texCtx.fillStyle = "#C2180E";
      texCtx.font = "700 15px 'JetBrains Mono', monospace";
      texCtx.fillText(skin.sub, 0, 22);
      texCtx.fillStyle = "#4A443F";
      texCtx.font = "600 16px 'JetBrains Mono', monospace";
      texCtx.fillText(`${vessel.vol} e · SLEEVE ${state.filmId}`, 0, 58);
      texCtx.restore();

    } else if (skin.styleType === "black_gold") {
      const g = texCtx.createLinearGradient(0, syTop, 0, syBot);
      g.addColorStop(0, "#19171B");
      g.addColorStop(0.55, "#0D0C0E");
      g.addColorStop(1, "#1D1A16");
      texCtx.fillStyle = g;
      texCtx.globalAlpha = state.xray ? 0.90 : 0.98;
      texCtx.fillRect(centerX - w / 2, syTop, w, syH);
      texCtx.globalAlpha = 1.0;

      texCtx.fillStyle = "#D9B263";
      [-480, -464, 464, 480].forEach(dx => texCtx.fillRect(centerX + dx, syTop + 26, 4, syH - 52));
      texCtx.fillStyle = "#1E3A8A";
      texCtx.fillRect(centerX - w / 2, syBot - 52, w, 26);
      texCtx.fillStyle = "#D9B263";
      texCtx.fillRect(centerX - w / 2, syTop + 14, w, 8);
      texCtx.fillRect(centerX - w / 2, syBot - 26, w, 12);

      const fmCur = getFilm();
      const tdOver = Math.max(0, phys.sleeveTD - (fmCur.warnTD - 4));
      const topPinch = tdOver > 0 ? Math.max(0.54, 1 - (tdOver * fmCur.pinchScale) / 72) : 1.0;
      texCtx.save();
      texCtx.translate(centerX, syTop + syH * 0.34);
      texCtx.scale(topPinch, 1.0);
      texCtx.strokeStyle = "#E2C07D";
      texCtx.lineWidth = 4;
      texCtx.save();
      texCtx.translate(0, -64);
      texCtx.rotate(Math.PI / 4);
      texCtx.strokeRect(-42, -42, 84, 84);
      texCtx.restore();
      texCtx.fillStyle = "#E2C07D";
      texCtx.textAlign = "center";
      texCtx.font = "700 28px Georgia, serif";
      texCtx.fillText("NN", 0, -54);

      texCtx.fillStyle = "#FAF5E8";
      texCtx.font = "700 50px Georgia, serif";
      texCtx.fillText(skin.brand, 0, 32);
      texCtx.fillStyle = "#D9B263";
      texCtx.font = "600 26px Georgia, serif";
      texCtx.fillText("— " + skin.brandSub + " —", 0, 74);
      texCtx.restore();

      texCtx.save();
      texCtx.translate(centerX, syTop + syH * 0.74);
      texCtx.textAlign = "center";
      texCtx.fillStyle = "#E2C07D";
      texCtx.font = "700 22px 'Inter', sans-serif";
      texCtx.fillText(vessel.shape === "wine_bordeaux" ? skin.wineSub : skin.product, 0, -10);
      texCtx.fillStyle = "#B8B0A0";
      texCtx.font = "500 15px 'Inter', sans-serif";
      texCtx.fillText(`${skin.sub} · ${vessel.vol}`, 0, 22);
      texCtx.restore();

    } else {
      const g = texCtx.createLinearGradient(0, syTop, 0, syBot);
      g.addColorStop(0, "#0F5C46");
      g.addColorStop(1, "#093D2E");
      texCtx.fillStyle = g;
      texCtx.globalAlpha = state.xray ? 0.90 : 0.98;
      texCtx.fillRect(centerX - w / 2, syTop, w, syH);
      texCtx.globalAlpha = 1.0;

      texCtx.fillStyle = "#1D4ED8";
      texCtx.beginPath();
      texCtx.moveTo(centerX - w / 2, syTop);
      texCtx.lineTo(centerX + w / 2, syTop);
      texCtx.lineTo(centerX + w / 2, syTop + syH * 0.28);
      texCtx.quadraticCurveTo(centerX, syTop + syH * 0.42, centerX - w / 2, syTop + syH * 0.24);
      texCtx.closePath();
      texCtx.fill();

      texCtx.save();
      texCtx.translate(centerX - 180, syTop + syH * 0.56);
      texCtx.fillStyle = "rgba(167, 243, 208, 0.20)";
      texCtx.beginPath();
      texCtx.ellipse(0, 0, 90, 28, -0.5, 0, Math.PI * 2);
      texCtx.fill();
      texCtx.beginPath();
      texCtx.ellipse(55, 36, 75, 22, 0.4, 0, Math.PI * 2);
      texCtx.fill();
      texCtx.restore();

      texCtx.save();
      texCtx.translate(centerX + 160, syTop + syH * 0.30);
      texCtx.fillStyle = "#EA580C";
      texCtx.beginPath();
      texCtx.arc(0, 0, 56, 0, Math.PI * 2);
      texCtx.fill();
      texCtx.fillStyle = "#FFFFFF";
      texCtx.textAlign = "center";
      texCtx.font = "900 22px 'Inter', sans-serif";
      texCtx.fillText("99.4%", 0, 2);
      texCtx.font = "700 13px 'Inter', sans-serif";
      texCtx.fillText("ORGANIC", 0, 22);
      texCtx.restore();

      const fmCur = getFilm();
      const tdOver = Math.max(0, phys.sleeveTD - (fmCur.warnTD - 4));
      const topPinch = tdOver > 0 ? Math.max(0.54, 1 - (tdOver * fmCur.pinchScale) / 72) : 1.0;
      texCtx.save();
      texCtx.translate(centerX - 18, syTop + syH * 0.34);
      texCtx.scale(topPinch, 1.0);
      texCtx.textAlign = "center";
      texCtx.fillStyle = "#FAF7F0";
      texCtx.font = "900 58px 'Inter', sans-serif";
      texCtx.fillText(skin.brand, 0, -24);
      texCtx.fillStyle = "#A7F3D0";
      texCtx.font = "800 34px 'Inter', sans-serif";
      texCtx.fillText(skin.brandSub, 0, 20);
      texCtx.restore();

      texCtx.fillStyle = "#EA580C";
      texCtx.fillRect(centerX - w / 2, syBot - 36, w, 24);
      texCtx.fillStyle = "#FAF7F0";
      texCtx.textAlign = "center";
      texCtx.font = "800 24px 'Inter', sans-serif";
      texCtx.fillText(vessel.shape === "wine_bordeaux" ? skin.wineSub : skin.product, centerX, syTop + syH * 0.68);
      texCtx.fillStyle = "#A7F3D0";
      texCtx.font = "600 17px 'JetBrains Mono', monospace";
      texCtx.fillText(`${skin.sub} · ${vessel.vol}`, centerX, syTop + syH * 0.76);
    }

    texCtx.restore();
  });

  // Film-specific micro-ripple shading on upper curved zone for stiffer films (PVC / rPET)
  const fmRip = getFilm();
  if (fmRip.ripple > 0 && phys.sleeveTD >= fmRip.warnTD) {
    const ripStrength = Math.min(1, ((phys.sleeveTD - fmRip.warnTD + 4) / 22) * fmRip.ripple);
    const ripH = Math.round(syH * 0.34);
    texCtx.save();
    for (let rx = 0; rx < w; rx += 22) {
      const alpha = (0.06 + 0.14 * ripStrength) * (0.5 + 0.5 * Math.sin(rx * 0.08));
      texCtx.fillStyle = `rgba(30, 22, 18, ${alpha.toFixed(3)})`;
      texCtx.fillRect(rx, syTop + 6, 8, ripH);
      texCtx.fillStyle = `rgba(255, 255, 255, ${(alpha * 0.7).toFixed(3)})`;
      texCtx.fillRect(rx + 8, syTop + 6, 5, ripH);
    }
    texCtx.restore();
  }

  if (state.heatmap) {
    drawSynchronizedTDHeatmap(texCtx, w, h, vessel, sSpan, false, true);
  }

  const effBcDeg = state.sleeveAngleDeg >= 0 ? state.sleeveAngleDeg - 180 : state.sleeveAngleDeg + 180;
  const uNorm = (((0.5 + (effBcDeg / 360)) % 1) + 1) % 1;
  const vBcPos = 0.04 + (state.bcHeightPct / 100) * sSpan;
  const bcX = uNorm * w;
  const bcY = Math.max(82, Math.min(h - 82, vesselVtoY(vBcPos)));
  const bcStatCol = phys.ansiGrade === "F" ? "#C2180E" : (phys.ansiGrade === "C" ? "#E5A000" : "#147A3B");

  [bcX - w, bcX, bcX + w].forEach(drawX => {
    if (drawX < -300 || drawX > w + 300) return;
    const warpX = (phys.localTD >= 24) ? Math.max(0.60, 1 - (phys.localTD - 22) / 92) : 1.0;
    texCtx.save();
    texCtx.translate(drawX, bcY);
    texCtx.scale(warpX, 1.0);
    drawEAN13Graphic(texCtx, 0, 0, 248, 136, skin.ean, bcStatCol, `EAN-13 · TD ${phys.localTD}% · GRADE ${phys.ansiGrade}`, false, phys.ansiGrade === "F");
    texCtx.restore();
  });

  if (sleeveTexture) {
    sleeveTexture.needsUpdate = true;
  }
}

// ==================== THREE.JS WEBGL PBR STUDIO ENGINE ====================
let renderer, scene, camera, productGroup, vesselMesh, liquidMesh, sleeveMesh, closureGroup, dipTubeMesh, clashRingMesh;
let raycaster, pointerNDC;
let activeDragMode = null; // null | 'barcode' | 'sleeve' | 'orbit'
let prevPtr = { x: 0, y: 0 };
let camSpherical = { theta: 0.25, phi: 1.38, radius: 6.15 };
let camTargetRadius = 6.15;
let camTargetTheta = null;

function getZoomBounds(vessel) {
  const v = vessel || getVessel();
  if (v.shape === "jar_lux") return { min: 3.2, max: 7.6 };
  if (v.shape === "wine_bordeaux") return { min: 4.3, max: 9.6 };
  return { min: 3.5, max: 9.0 };
}

function clampAndSetZoom(radius, immediate) {
  const zb = getZoomBounds(getVessel());
  const clamped = Math.max(zb.min, Math.min(zb.max, radius));
  camTargetRadius = clamped;
  if (immediate) camSpherical.radius = clamped;
}

function createStudioEnvironment(renderer) {
  const pmrem = new THREE.PMREMGenerator(renderer);
  pmrem.compileEquirectangularShader();
  const envScene = new THREE.Scene();
  envScene.background = new THREE.Color(0xEAE4DA);

  const boxGeo = new THREE.BoxGeometry(1, 1, 1);
  const topLight = new THREE.Mesh(boxGeo, new THREE.MeshBasicMaterial({ color: 0xFFFFFF }));
  topLight.scale.set(10, 0.2, 10);
  topLight.position.set(0, 7, 0);
  envScene.add(topLight);

  const keyLight = new THREE.Mesh(boxGeo, new THREE.MeshBasicMaterial({ color: 0xFFFDF9 }));
  keyLight.scale.set(0.2, 8, 8);
  keyLight.position.set(-6, 2, 4);
  envScene.add(keyLight);

  const rimLight = new THREE.Mesh(boxGeo, new THREE.MeshBasicMaterial({ color: 0xF5EFE6 }));
  rimLight.scale.set(0.2, 9, 4);
  rimLight.position.set(6, 2, -3);
  envScene.add(rimLight);

  const floorBounce = new THREE.Mesh(boxGeo, new THREE.MeshBasicMaterial({ color: 0xD8D0C2 }));
  floorBounce.scale.set(14, 0.2, 14);
  floorBounce.position.set(0, -5, 0);
  envScene.add(floorBounce);

  const envTex = pmrem.fromScene(envScene, 0.04).texture;
  pmrem.dispose();
  return envTex;
}

// Exact single-source Doypack stand-up pouch surface point + bottom gusset fold
function getDoypackPoint(vessel, u, v) {
  const totalH = getVesselTotalHeight(vessel);
  const halfW = 0.92;
  const maxHalfD = 0.41;
  const theta = (u - 0.5) * Math.PI * 2;
  const sinT = Math.sin(theta);
  const cosT = Math.cos(theta);

  // Width narrows slightly at bottom gusset corners for realistic stand-up pouch silhouette
  const wScale = v < 0.08 ? (0.93 + 0.07 * (v / 0.08)) : 1.0;
  const x = halfW * wScale * sinT;
  const y = -1.25 + v * totalH;

  // Belly inflation inside side fin-seals (|sinT| < 0.88) and below top zip seal (v < 0.81)
  const vEnv = v < 0.16
    ? (0.68 + 0.32 * Math.sin((v / 0.16) * Math.PI * 0.5))
    : (v < 0.81 ? Math.pow(Math.max(0, 1 - (v - 0.16) / 0.65), 0.72) : 0.0);
  const sideMask = Math.max(0, 1 - Math.pow(Math.abs(sinT) / 0.88, 2.2));
  const edgeTaper = Math.min(1, Math.abs(cosT) / 0.06);

  // Raised 3D interlock zip rail across pouch top (v in 0.845..0.875)
  const zipRidge = (v >= 0.845 && v <= 0.875 && Math.abs(sinT) < 0.86)
    ? 0.022 * Math.sin(((v - 0.845) / 0.03) * Math.PI)
    : 0.0;

  const halfDepth = (0.014 + maxHalfD * vEnv * sideMask + zipRidge) * edgeTaper;
  const z = Math.sign(cosT || 1) * halfDepth * Math.pow(Math.abs(cosT), 0.55);
  return { x, y, z, cosT, sinT };
}

function createDoypackGeometry(vessel, radialSegs, heightSegs) {
  const geo = new THREE.BufferGeometry();
  const positions = [];
  const uvs = [];
  const indices = [];

  // Ring 0 is inward-tucked bottom gusset fold so underside never looks hollow
  for (let ix = 0; ix <= radialSegs; ix++) {
    const u = ix / radialSegs;
    const pt0 = getDoypackPoint(vessel, u, 0.0);
    positions.push(pt0.x * 0.96, -1.16, pt0.z * 0.18);
    uvs.push(u, 0.0);
  }

  for (let iy = 0; iy <= heightSegs; iy++) {
    const v = iy / heightSegs;
    for (let ix = 0; ix <= radialSegs; ix++) {
      const u = ix / radialSegs;
      const pt = getDoypackPoint(vessel, u, v);
      positions.push(pt.x, pt.y, pt.z);
      uvs.push(u, v);
    }
  }

  const totalRings = heightSegs + 2;
  for (let iy = 0; iy < totalRings - 1; iy++) {
    for (let ix = 0; ix < radialSegs; ix++) {
      const a = iy * (radialSegs + 1) + ix;
      const b = a + 1;
      const c = (iy + 1) * (radialSegs + 1) + ix;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }

  geo.setIndex(indices);
  geo.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
  geo.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2));
  geo.computeVertexNormals();
  return geo;
}

// Builds high-resolution parametric 3D geometry (smooth continuous polar superellipse, wine neck & doypack)
function createParametricVesselGeometry(vessel, radialSegs, heightSegs, yMin, yMax, radiusScale, isSleeve) {
  if (vessel.shape === "doypack") {
    return createDoypackGeometry(vessel, radialSegs, heightSegs);
  }

  const geo = new THREE.BufferGeometry();
  const positions = [];
  const uvs = [];
  const indices = [];
  const wrapMeta = isSleeve ? [] : null;

  const totalH = getVesselTotalHeight(vessel);
  const baseScale = vessel.shape === "jar_lux" ? 0.92 : (vessel.shape === "wine_bordeaux" ? 0.58 : (vessel.shape === "alu_can" ? 0.60 : 0.68));

  for (let iy = 0; iy <= heightSegs; iy++) {
    const v = iy / heightSegs;
    const profileV = yMin + v * (yMax - yMin);
    const yWorld = -1.25 + profileV * totalH;

    let rBase = getNormalizedRadiusAtV(vessel, profileV);
    if (!isSleeve && vessel.shape === "jar_lux" && profileV > 0.80) {
      // Recessed neck wall on jar (smaller than jar outer body 1.0 -> lid screws OVER it!)
      rBase = 0.76;
    } else if (!isSleeve && vessel.shape !== "jar_lux" && vessel.shape !== "wine_bordeaux" && vessel.shape !== "alu_can" && profileV > 0.88) {
      rBase = 0.34;
      if (profileV > 0.885 && profileV < 0.91) rBase += 0.035;
    }

    const rWorld = rBase * baseScale * radiusScale;

    for (let ix = 0; ix <= radialSegs; ix++) {
      const u = ix / radialSegs;
      const theta = (u - 0.5) * Math.PI * 2;
      const sinT = Math.sin(theta), cosT = Math.cos(theta);

      let rFinal = getRadialEnvelopeFactor(vessel, profileV, theta, rWorld);

      if (wrapMeta) {
        wrapMeta.push({ profileV, yWorld, rBase, theta, sinT, cosT, baseR: rFinal });
      }

      // 3D Helical screw thread ridges on neck (cosmetic/dermo jars & bottles only)
      if (!isSleeve && vessel.shape !== "jar_lux" && vessel.shape !== "wine_bordeaux" && vessel.shape !== "alu_can" && profileV >= 0.92 && profileV <= 0.985) {
        const threadPhase = (profileV - 0.92) * 32 * Math.PI * 2 + theta * 2;
        if (Math.sin(threadPhase) > 0.2) rFinal += 0.018;
      }
      if (!isSleeve && vessel.shape === "jar_lux" && profileV >= 0.84 && profileV <= 0.96) {
        const threadPhase = (profileV - 0.84) * 28 * Math.PI * 2 + theta * 2;
        if (Math.sin(threadPhase) > 0.25) rFinal += 0.016;
      }

      const x = rFinal * sinT;
      const z = rFinal * cosT;

      positions.push(x, yWorld, z);
      uvs.push(u, v);
    }
  }

  for (let iy = 0; iy < heightSegs; iy++) {
    for (let ix = 0; ix < radialSegs; ix++) {
      const a = iy * (radialSegs + 1) + ix;
      const b = a + 1;
      const c = (iy + 1) * (radialSegs + 1) + ix;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }

  geo.setIndex(indices);
  geo.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
  geo.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2));
  if (wrapMeta) {
    geo.userData.wrapMeta = wrapMeta;
    geo.userData.baseScale = baseScale;
    applyDynamicWrapMeshDeformation(geo, vessel);
  } else {
    geo.computeVertexNormals();
  }
  return geo;
}

// Real-time 3D mesh deformation for both Shrink Sleeves (shoulder flare/creases) and Adhesive Labels (dog-ear lift, buckling flutes, square-corner bridging)
function applyDynamicWrapMeshDeformation(geo, vessel) {
  const meta = geo && geo.userData && geo.userData.wrapMeta;
  if (!meta) return;
  const pos = geo.attributes.position;
  const baseScale = geo.userData.baseScale || 0.68;
  const isLabel = isLabelMode();
  const isSleeveOnly = state.wrapType === "sleeve";
  const { vMin, vMax } = getSleeveVerticalBand();
  const bandSpan = Math.max(0.05, vMax - vMin);

  if (isLabel) {
    const lp = getLabelPaper();
    const slTheta = (state.sleeveAngleDeg / 360) * Math.PI * 2;
    const isCan = vessel.shape === "alu_can";
    const centerTheta = isCan ? (slTheta - (540 / 2048) * Math.PI * 2) : slTheta;
    const labelHalfRadBase = isCan ? 2.67 : (vessel.shape === "jar_lux" ? 1.26 : (vessel.shape === "square_soft" ? 0.69 : (vessel.shape === "wine_bordeaux" ? 0.71 : 0.74)));
    const labelHalfRad = Math.min(Math.PI * 0.90, labelHalfRadBase * getLabelWidthMultiplier(vessel));

    for (let i = 0; i < meta.length; i++) {
      const m = meta[i];
      let r = m.baseR;
      if (m.profileV >= vMin - 0.025 && m.profileV <= vMax + 0.025) {
        let dTheta = m.theta - centerTheta;
        while (dTheta > Math.PI) dTheta -= Math.PI * 2;
        while (dTheta < -Math.PI) dTheta += Math.PI * 2;
        const absD = Math.abs(dTheta);
        if (absD <= labelHalfRad * 1.06) {
          const hFrac = Math.min(1.0, absD / labelHalfRad);
          const vFrac = Math.max(0, Math.min(1, (m.profileV - vMin) / bandSpan));
          const curv = Math.max(0, 1.0 - m.rBase);
          if (curv > 0.008) {
            // Flat die-cut label cannot shrink on curved shoulder/heel -> realistic physical dog-ear corner lift (4-8mm) + 3D crease flutes
            const curvClamp = Math.min(0.28, curv);
            const cornerTent = curvClamp * lp.stiffness * (0.09 + 0.42 * hFrac * hFrac) * baseScale;
            const foldWave = curvClamp * lp.stiffness * 0.075 * Math.sin(dTheta * 20.0 + vFrac * 4.5) * (0.25 + 0.75 * hFrac) * baseScale;
            r += cornerTent + foldWave;
          }
          if (vessel.shape === "square_soft") {
            // Stiff adhesive labels lift/buckle when dragged horizontally over 45° corners of the square bottle
            const cornerAmt = Math.abs(Math.sin(2 * m.theta));
            if (cornerAmt > 0.35) {
              const sqBridge = (cornerAmt - 0.35) * lp.stiffness * (0.048 + 0.028 * Math.sin(vFrac * Math.PI * 5.0)) * baseScale;
              r += sqBridge;
            }
          }
        }
      }
      pos.setXYZ(i, r * m.sinT, m.yWorld, r * m.cosT);
    }
  } else if (isSleeveOnly) {
    const fmS = getFilm();
    for (let i = 0; i < meta.length; i++) {
      const m = meta[i];
      let r = m.baseR;
      if (m.rBase < 0.985 && m.profileV >= vMin - 0.02 && m.profileV <= vMax + 0.02) {
        const shrinkDeficit = Math.max(0, (1.0 - m.rBase) - (fmS.maxTD - 32) / 100);
        if (shrinkDeficit > 0 && fmS.ripple > 0) {
          const flare = shrinkDeficit * (0.14 + 0.34 * fmS.ripple) * baseScale;
          const creaseAmp = shrinkDeficit * (0.045 * fmS.ripple) * baseScale;
          const creaseWave = Math.sin(m.theta * (12 + Math.round(fmS.ripple * 8)) + m.profileV * 9.0);
          r += flare + creaseAmp * creaseWave;
        }
      }
      pos.setXYZ(i, r * m.sinT, m.yWorld, r * m.cosT);
    }
  } else {
    for (let i = 0; i < meta.length; i++) {
      const m = meta[i];
      pos.setXYZ(i, m.baseR * m.sinT, m.yWorld, m.baseR * m.cosT);
    }
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();
}

function buildClosure3DGroup(cl, vessel) {
  const grp = new THREE.Group();
  if (!cl || cl.type === "none") return grp;
  const darkMat = new THREE.MeshStandardMaterial({ color: 0x1A1817, roughness: 0.28, metalness: 0.15 });
  const metalMat = new THREE.MeshStandardMaterial({ color: 0xD6D3CD, roughness: 0.22, metalness: 0.88 });
  const rubberMat = new THREE.MeshStandardMaterial({ color: 0x24201E, roughness: 0.65, metalness: 0.05 });

  // Knurled ribbed collar helper
  function makeRibbedCylinder(rTop, rBot, h, segs, mat) {
    const g = new THREE.CylinderGeometry(rTop, rBot, h, segs, 1, false);
    const pos = g.attributes.position;
    for (let i = 0; i < pos.count; i++) {
      const vx = pos.getX(i), vz = pos.getZ(i);
      const rad = Math.hypot(vx, vz);
      if (rad > rTop * 0.85) {
        const ang = Math.atan2(vz, vx);
        const rib = 1 + 0.022 * Math.sin(ang * 48);
        pos.setX(i, vx * rib);
        pos.setZ(i, vz * rib);
      }
    }
    g.computeVertexNormals();
    return new THREE.Mesh(g, mat);
  }

  if (cl.type === "pump") {
    const collar = makeRibbedCylinder(0.28, 0.28, 0.34, 96, darkMat);
    collar.position.y = 0.17;
    grp.add(collar);

    const trimRing = new THREE.Mesh(new THREE.CylinderGeometry(0.285, 0.285, 0.05, 64), metalMat);
    trimRing.position.y = 0.025;
    grp.add(trimRing);

    const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.13, 0.26, 48), metalMat);
    stem.position.y = 0.44;
    grp.add(stem);

    const head = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.25, 0.24, 64), darkMat);
    head.position.y = 0.64;
    grp.add(head);

    // Ergonomic Pump Nozzle Spout pointing forward (+Z / +X)
    const spoutCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0, 0.66, 0.10),
      new THREE.Vector3(0, 0.67, 0.38),
      new THREE.Vector3(0, 0.61, 0.58)
    ]);
    const spoutGeo = new THREE.TubeGeometry(spoutCurve, 24, 0.058, 24, false);
    const spout = new THREE.Mesh(spoutGeo, darkMat);
    grp.add(spout);
  } else if (cl.type === "pump_slim") {
    const slimMat = new THREE.MeshStandardMaterial({ color: 0xF5F2EB, roughness: 0.22, metalness: 0.06 });
    const collar = new THREE.Mesh(new THREE.CylinderGeometry(0.265, 0.275, 0.28, 64), metalMat);
    collar.position.y = 0.14;
    grp.add(collar);
    const neckStem = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.095, 0.22, 40), slimMat);
    neckStem.position.y = 0.38;
    grp.add(neckStem);
    const head = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.18, 0.18, 48), slimMat);
    head.position.y = 0.56;
    grp.add(head);
    const beak = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.07, 0.34), slimMat);
    beak.position.set(0, 0.58, 0.22);
    grp.add(beak);
  } else if (cl.type === "fliptop24") {
    const capMat = new THREE.MeshStandardMaterial({ color: 0x1E1C1B, roughness: 0.24, metalness: 0.08 });
    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.275, 0.28, 0.36, 64), capMat);
    body.position.y = 0.18;
    grp.add(body);
    const hinge = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.12, 0.06), capMat);
    hinge.position.set(0, 0.30, -0.27);
    grp.add(hinge);
    const seam = new THREE.Mesh(new THREE.CylinderGeometry(0.278, 0.278, 0.02, 64), metalMat);
    seam.position.y = 0.29;
    grp.add(seam);
    const lip = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.04, 0.06), metalMat);
    lip.position.set(0, 0.32, 0.27);
    grp.add(lip);
  } else if (cl.type === "dropper") {
    const collar = makeRibbedCylinder(0.28, 0.28, 0.30, 96, metalMat);
    collar.position.y = 0.15;
    grp.add(collar);

    const bulb = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.19, 0.38, 48), rubberMat);
    bulb.position.y = 0.48;
    grp.add(bulb);

    const bulbTop = new THREE.Mesh(new THREE.SphereGeometry(0.15, 48, 24), rubberMat);
    bulbTop.position.y = 0.67;
    grp.add(bulbTop);
  } else if (cl.type === "spray") {
    const collar = makeRibbedCylinder(0.27, 0.27, 0.28, 96, metalMat);
    collar.position.y = 0.14;
    grp.add(collar);

    const nozzle = new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.20, 0.26, 48), new THREE.MeshStandardMaterial({ color: 0xF7F4EE, roughness: 0.25 }));
    nozzle.position.y = 0.41;
    grp.add(nozzle);

    const dot = new THREE.Mesh(new THREE.SphereGeometry(0.03, 16, 16), darkMat);
    dot.position.set(0, 0.43, 0.19);
    grp.add(dot);

    // Clear protective overcap
    const overcapMat = new THREE.MeshPhysicalMaterial({ color: 0xFFFFFF, transparent: true, opacity: 0.32, roughness: 0.08, transmission: 0.6 });
    const overcap = new THREE.Mesh(new THREE.CylinderGeometry(0.275, 0.275, 0.60, 48), overcapMat);
    overcap.position.y = 0.32;
    grp.add(overcap);
  } else if (cl.type === "disctop28") {
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0x201E1D, roughness: 0.22, metalness: 0.12 });
    const shell = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.355, 0.40, 64), bodyMat);
    shell.position.y = 0.20;
    grp.add(shell);
    const disc = new THREE.Mesh(new THREE.CylinderGeometry(0.31, 0.31, 0.055, 48), metalMat);
    disc.position.set(0, 0.41, 0.02);
    disc.rotation.x = 0.14;
    grp.add(disc);
  } else if (cl.type === "fliptop28") {
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0x2E2A28, roughness: 0.30, metalness: 0.08 });
    const base = makeRibbedCylinder(0.35, 0.36, 0.32, 72, bodyMat);
    base.position.y = 0.16;
    grp.add(base);
    const lidTop = new THREE.Mesh(new THREE.CylinderGeometry(0.335, 0.345, 0.13, 64), bodyMat);
    lidTop.position.y = 0.385;
    grp.add(lidTop);
    const thumbNotch = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.04, 0.08), metalMat);
    thumbNotch.position.set(0, 0.36, 0.34);
    grp.add(thumbNotch);
  } else if (cl.type === "pushpull28") {
    const capMat = new THREE.MeshStandardMaterial({ color: 0x1E1C1A, roughness: 0.26, metalness: 0.10 });
    const spoutMat = new THREE.MeshStandardMaterial({ color: 0xC2180E, roughness: 0.22, metalness: 0.08 });
    const skirt = makeRibbedCylinder(0.35, 0.36, 0.28, 72, capMat);
    skirt.position.y = 0.14;
    grp.add(skirt);
    const dome = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.34, 0.14, 56), capMat);
    dome.position.y = 0.35;
    grp.add(dome);
    const valve = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.15, 0.22, 40), spoutMat);
    valve.position.y = 0.50;
    grp.add(valve);
    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.115, 0.024, 12, 32), spoutMat);
    rim.rotation.x = Math.PI / 2;
    rim.position.y = 0.61;
    grp.add(rim);
  } else if (cl.type === "lid58") {
    const lid = makeRibbedCylinder(0.89, 0.89, 0.38, 96, darkMat);
    lid.position.y = 0.19;
    grp.add(lid);
    const goldTop = new THREE.Mesh(new THREE.CylinderGeometry(0.84, 0.84, 0.024, 64), metalMat);
    goldTop.position.y = 0.392;
    grp.add(goldTop);
  } else if (cl.type === "lid_bevel58") {
    const satinMat = new THREE.MeshStandardMaterial({ color: 0xF5F1E9, roughness: 0.20, metalness: 0.10 });
    const base = new THREE.Mesh(new THREE.CylinderGeometry(0.86, 0.89, 0.26, 72), satinMat);
    base.position.y = 0.13;
    grp.add(base);
    const bevel = new THREE.Mesh(new THREE.CylinderGeometry(0.74, 0.86, 0.14, 72), satinMat);
    bevel.position.y = 0.33;
    grp.add(bevel);
    const ring = new THREE.Mesh(new THREE.CylinderGeometry(0.895, 0.895, 0.028, 72), metalMat);
    ring.position.y = 0.02;
    grp.add(ring);
  } else if (cl.type === "lid_double58") {
    const outerMat = new THREE.MeshStandardMaterial({ color: 0x1F1D1C, roughness: 0.18, metalness: 0.24 });
    const goldTrimMat = new THREE.MeshStandardMaterial({ color: 0xD4AF37, roughness: 0.20, metalness: 0.88 });
    const wall = new THREE.Mesh(new THREE.CylinderGeometry(0.90, 0.90, 0.44, 72), outerMat);
    wall.position.y = 0.22;
    grp.add(wall);
    const band = new THREE.Mesh(new THREE.CylinderGeometry(0.908, 0.908, 0.045, 72), goldTrimMat);
    band.position.y = 0.045;
    grp.add(band);
    const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.86, 0.90, 0.06, 72), outerMat);
    crown.position.y = 0.47;
    grp.add(crown);
  } else if (cl.type === "lid_dome70") {
    const domeMat = new THREE.MeshStandardMaterial({ color: 0x262120, roughness: 0.24, metalness: 0.22 });
    const goldTrimMat = new THREE.MeshStandardMaterial({ color: 0xD4AF37, roughness: 0.22, metalness: 0.88 });
    const wall = makeRibbedCylinder(0.95, 0.97, 0.26, 96, domeMat);
    wall.position.y = 0.14;
    grp.add(wall);
    const crown = new THREE.Mesh(new THREE.SphereGeometry(0.95, 48, 24, 0, Math.PI * 2, 0, Math.PI * 0.5), domeMat);
    crown.scale.set(1.0, 0.26, 1.0);
    crown.position.y = 0.27;
    grp.add(crown);
    const band = new THREE.Mesh(new THREE.CylinderGeometry(0.975, 0.975, 0.032, 64), goldTrimMat);
    band.position.y = 0.02;
    grp.add(band);
  } else if (cl.type === "lid_tall70") {
    const tallMat = new THREE.MeshStandardMaterial({ color: 0x3A3532, roughness: 0.30, metalness: 0.15 });
    const wall = makeRibbedCylinder(0.96, 0.98, 0.48, 96, tallMat);
    wall.position.y = 0.24;
    grp.add(wall);
    const topRing = new THREE.Mesh(new THREE.CylinderGeometry(0.92, 0.96, 0.05, 64), metalMat);
    topRing.position.y = 0.50;
    grp.add(topRing);
  } else if (cl.type === "bartop29") {
    const woodMat = new THREE.MeshStandardMaterial({ color: 0x6B4423, roughness: 0.58, metalness: 0.04 });
    const corkMat = new THREE.MeshStandardMaterial({ color: 0xC69C68, roughness: 0.78, metalness: 0.02 });
    const plug = new THREE.Mesh(new THREE.CylinderGeometry(0.146, 0.140, 0.34, 48), corkMat);
    plug.position.y = -0.02;
    grp.add(plug);
    const head = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.25, 0.24, 64), woodMat);
    head.position.y = 0.24;
    grp.add(head);
    const chamfer = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.26, 0.05, 64), woodMat);
    chamfer.position.y = 0.38;
    grp.add(chamfer);
  } else if (cl.type === "cork29") {
    const corkMat = new THREE.MeshStandardMaterial({ color: 0xC69C68, roughness: 0.78, metalness: 0.02 });
    const foilMat = new THREE.MeshStandardMaterial({ color: 0x4A080C, roughness: 0.34, metalness: 0.15 });
    const goldMat = new THREE.MeshStandardMaterial({ color: 0xD4AF37, roughness: 0.22, metalness: 0.88 });
    // Natural cork plug seated inside bottle bore & protruding inside capsule
    const cork = new THREE.Mesh(new THREE.CylinderGeometry(0.148, 0.142, 0.38, 48), corkMat);
    cork.position.y = -0.02;
    grp.add(cork);
    // Heat-shrink wine capsule raised so top completely encloses bottle lip (+0.129)
    const capsule = new THREE.Mesh(new THREE.CylinderGeometry(0.194, 0.198, 0.56, 64), foilMat);
    capsule.position.y = -0.08;
    grp.add(capsule);
    const capTopDisc = new THREE.Mesh(new THREE.CylinderGeometry(0.194, 0.194, 0.016, 64), foilMat);
    capTopDisc.position.y = 0.20;
    grp.add(capTopDisc);
    const goldBand = new THREE.Mesh(new THREE.CylinderGeometry(0.197, 0.197, 0.028, 64), goldMat);
    goldBand.position.y = 0.06;
    grp.add(goldBand);
  } else if (cl.type === "stelvin29") {
    const aluMat = new THREE.MeshStandardMaterial({ color: 0x262423, roughness: 0.24, metalness: 0.78 });
    const trimMat = new THREE.MeshStandardMaterial({ color: 0xD8D4CC, roughness: 0.20, metalness: 0.90 });
    const stelvin = new THREE.Mesh(new THREE.CylinderGeometry(0.196, 0.200, 0.70, 64), aluMat);
    stelvin.position.y = -0.14;
    grp.add(stelvin);
    const crimpRing = new THREE.Mesh(new THREE.CylinderGeometry(0.203, 0.203, 0.04, 64), trimMat);
    crimpRing.position.y = 0.02;
    grp.add(crimpRing);
  } else if (cl.type === "pourer29") {
    const oliveCapMat = new THREE.MeshStandardMaterial({ color: 0x1E261E, roughness: 0.32, metalness: 0.12 });
    const goldRingMat = new THREE.MeshStandardMaterial({ color: 0xD4AF37, roughness: 0.22, metalness: 0.88 });
    // Vinegar/oil style ribbed screw skirt + stepped precision pourer neck & flip lid
    const skirt = makeRibbedCylinder(0.204, 0.208, 0.36, 48, oliveCapMat);
    skirt.position.y = 0.06;
    grp.add(skirt);
    const goldCollar = new THREE.Mesh(new THREE.CylinderGeometry(0.210, 0.210, 0.028, 48), goldRingMat);
    goldCollar.position.y = 0.23;
    grp.add(goldCollar);
    const shoulderStep = new THREE.Mesh(new THREE.CylinderGeometry(0.155, 0.202, 0.09, 48), oliveCapMat);
    shoulderStep.position.y = 0.285;
    grp.add(shoulderStep);
    const spoutNeck = new THREE.Mesh(new THREE.CylinderGeometry(0.112, 0.145, 0.12, 36), oliveCapMat);
    spoutNeck.position.y = 0.38;
    grp.add(spoutNeck);
    const flipTop = new THREE.Mesh(new THREE.CylinderGeometry(0.128, 0.128, 0.048, 36), darkMat);
    flipTop.position.y = 0.455;
    grp.add(flipTop);
  } else if (cl.type === "sot202_cap") {
    const capMat = new THREE.MeshPhysicalMaterial({ color: 0x1A1817, transparent: true, opacity: 0.86, roughness: 0.25, clearcoat: 0.7 });
    const overcap = new THREE.Mesh(new THREE.CylinderGeometry(0.534, 0.534, 0.24, 64), capMat);
    overcap.position.y = 0.08;
    grp.add(overcap);
  } else if (cl.type === "zip_ok") {
    const zipMat = new THREE.MeshStandardMaterial({ color: 0x242220, roughness: 0.30, metalness: 0.20 });
    const sliderMat = new THREE.MeshStandardMaterial({ color: 0xC2180E, roughness: 0.25, metalness: 0.25 });
    const track = new THREE.Mesh(new THREE.BoxGeometry(1.66, 0.042, 0.056), zipMat);
    grp.add(track);
    const pullTab = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.085, 0.072), sliderMat);
    pullTab.position.set(0.62, 0.01, 0.018);
    grp.add(pullTab);
  } else {
    // 28/410 Oversized Ribbed Screw Cap
    const cap = makeRibbedCylinder(0.36, 0.36, 0.36, 96, darkMat);
    cap.position.y = 0.18;
    grp.add(cap);
  }

  return grp;
}

function getVesselPhysicalMaterial(finishId) {
  if (finishId === "matte_pouch") {
    return new THREE.MeshPhysicalMaterial({
      map: sleeveTexture,
      roughness: 0.68,
      metalness: 0.02,
      clearcoat: 0.08,
      side: THREE.DoubleSide
    });
  }
  if (finishId === "gloss_pouch") {
    return new THREE.MeshPhysicalMaterial({
      map: sleeveTexture,
      roughness: 0.14,
      metalness: 0.06,
      clearcoat: 0.92,
      clearcoatRoughness: 0.10,
      side: THREE.DoubleSide
    });
  }
  if (finishId === "kraft_pouch") {
    return new THREE.MeshPhysicalMaterial({
      map: sleeveTexture,
      roughness: 0.84,
      metalness: 0.0,
      clearcoat: 0.02,
      side: THREE.DoubleSide
    });
  }
  if (finishId === "foil_pouch") {
    return new THREE.MeshPhysicalMaterial({
      map: sleeveTexture,
      roughness: 0.24,
      metalness: 0.58,
      clearcoat: 0.45,
      clearcoatRoughness: 0.18,
      side: THREE.DoubleSide
    });
  }
  if (finishId === "alu_brushed") {
    return new THREE.MeshStandardMaterial({
      color: 0xD8DCE0,
      roughness: 0.22,
      metalness: 0.88,
      side: THREE.DoubleSide
    });
  }
  if (finishId === "wine_green") {
    return new THREE.MeshStandardMaterial({
      color: 0x0E2B19,
      transparent: true,
      opacity: 0.94,
      roughness: 0.16,
      metalness: 0.10,
      side: THREE.DoubleSide
    });
  }
  if (finishId === "clear_pet") {
    return new THREE.MeshPhysicalMaterial({
      color: 0xF7FAFC,
      transparent: true,
      opacity: 0.38,
      roughness: 0.07,
      metalness: 0.0,
      reflectivity: 0.9,
      clearcoat: 1.0,
      clearcoatRoughness: 0.06,
      side: THREE.DoubleSide
    });
  }
  if (finishId === "amber") {
    return new THREE.MeshPhysicalMaterial({
      color: 0x8F3B08,
      transparent: true,
      opacity: 0.78,
      roughness: 0.10,
      metalness: 0.02,
      clearcoat: 1.0,
      clearcoatRoughness: 0.08,
      side: THREE.DoubleSide
    });
  }
  if (finishId === "hdpe_white") {
    return new THREE.MeshPhysicalMaterial({
      color: 0xF5F2EB,
      roughness: 0.34,
      metalness: 0.02,
      clearcoat: 0.35,
      clearcoatRoughness: 0.25
    });
  }
  if (finishId === "pet_gloss") {
    return new THREE.MeshPhysicalMaterial({
      color: 0xF3F7FB,
      transparent: true,
      opacity: 0.86,
      roughness: 0.04,
      metalness: 0.03,
      reflectivity: 0.96,
      clearcoat: 1.0,
      clearcoatRoughness: 0.03,
      side: THREE.DoubleSide
    });
  }
  // Frosted Satin Glass
  return new THREE.MeshPhysicalMaterial({
    color: 0xEFECE6,
    transparent: true,
    opacity: 0.82,
    roughness: 0.26,
    metalness: 0.02,
    clearcoat: 0.65,
    clearcoatRoughness: 0.18,
    side: THREE.DoubleSide
  });
}

function rebuild3DProduct() {
  if (!scene) return;
  if (productGroup) scene.remove(productGroup);

  productGroup = new THREE.Group();
  const vessel = getVessel();
  const cl = getClosure();
  const phys = evaluateLivePhysics();
  const totalH = getVesselTotalHeight(vessel);
  const pouchMode = isDoypack();
  const baseScale = vessel.shape === "jar_lux" ? 0.92 : (vessel.shape === "wine_bordeaux" ? 0.58 : (vessel.shape === "alu_can" ? 0.60 : 0.68));

  // Render dynamic UV texture BEFORE building material (Doypack uses sleeveTexture directly)
  renderSleeveUVTexture();

  // 1) Outer Vessel / Pouch Body (0.0 to 1.0)
  const vGeo = createParametricVesselGeometry(vessel, pouchMode ? 112 : 96, pouchMode ? 84 : 110, 0.0, 1.0, 1.0, false);
  const vMat = getVesselPhysicalMaterial(state.finishId);
  vMat.wireframe = state.wireframe;
  vesselMesh = new THREE.Mesh(vGeo, vMat);
  productGroup.add(vesselMesh);

  // Molded neck lip torus on open rigid bottles & jars so uncapped container looks complete
  if (!pouchMode && vessel.shape !== "alu_can") {
    const lipGeo = vessel.shape === "jar_lux"
      ? new THREE.TorusGeometry(0.676, 0.024, 14, 64)
      : (vessel.shape === "wine_bordeaux"
          ? new THREE.TorusGeometry(0.160, 0.023, 14, 48)
          : new THREE.TorusGeometry(0.214, 0.019, 14, 48));
    lipGeo.rotateX(Math.PI / 2);
    const lipMesh = new THREE.Mesh(lipGeo, vMat);
    lipMesh.position.y = -1.25 + totalH;
    productGroup.add(lipMesh);
  }

  // 2) Internal Liquid Volume + Dip Tube (visible ONLY when Interno / Liquido toggle is manually enabled)
  const showInternals = !pouchMode && vessel.shape !== "alu_can" && state.xray;
  const hasDipTube = ["pump", "spray", "dropper"].includes(cl.type);
  if (showInternals) {
    const liqTop = (vessel.shape === "jar_lux" || vessel.shape === "wine_bordeaux") ? 0.64 : 0.56;
    const liqGeo = createParametricVesselGeometry(vessel, 64, 48, 0.03, liqTop, 0.92, true);
    const liqMat = new THREE.MeshPhysicalMaterial({
      color: new THREE.Color(vessel.liquidColor),
      transparent: true,
      opacity: state.xray ? 0.62 : 0.45,
      roughness: 0.15,
      clearcoat: 0.8
    });
    liquidMesh = new THREE.Mesh(liqGeo, liqMat);
    productGroup.add(liquidMesh);

    if (hasDipTube && vessel.shape !== "jar_lux" && vessel.shape !== "wine_bordeaux") {
      const tubeCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(0, 1.05, 0),
        new THREE.Vector3(0.02, 0.10, 0.02),
        new THREE.Vector3(0.18, -1.12, 0.12)
      ]);
      const dtGeo = new THREE.TubeGeometry(tubeCurve, 32, 0.032, 16, false);
      const dtMat = new THREE.MeshPhysicalMaterial({
        color: phys.neckMatch ? 0xFFFFFF : 0xFF3333,
        transparent: true,
        opacity: 0.78,
        roughness: 0.15
      });
      dipTubeMesh = new THREE.Mesh(dtGeo, dtMat);
      productGroup.add(dipTubeMesh);
    } else {
      dipTubeMesh = null;
    }
  } else {
    liquidMesh = null;
    dipTubeMesh = null;
  }

  // Integral aluminum base disk & SOT 202 top seam/tab deck on can body
  if (vessel.shape === "alu_can") {
    const botDisk = new THREE.Mesh(
      new THREE.CylinderGeometry(0.50, 0.50, 0.02, 48),
      new THREE.MeshStandardMaterial({ color: 0xC8CDD2, roughness: 0.26, metalness: 0.88 })
    );
    botDisk.position.y = -1.24;
    productGroup.add(botDisk);

    const canTopY = -1.25 + 0.965 * totalH;
    const rimMat = new THREE.MeshStandardMaterial({ color: 0xE2E5E9, roughness: 0.18, metalness: 0.92 });
    const deckMat = new THREE.MeshStandardMaterial({ color: 0xC6CCD2, roughness: 0.28, metalness: 0.88 });
    const chime = new THREE.Mesh(new THREE.TorusGeometry(0.516, 0.022, 16, 64), rimMat);
    chime.rotation.x = Math.PI / 2;
    chime.position.y = canTopY;
    productGroup.add(chime);
    const deck = new THREE.Mesh(new THREE.CylinderGeometry(0.495, 0.495, 0.018, 64), deckMat);
    deck.position.y = canTopY - 0.022;
    productGroup.add(deck);
    const rivet = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.03, 24), rimMat);
    rivet.position.y = canTopY;
    productGroup.add(rivet);
    const pullRing = new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.014, 12, 32), rimMat);
    pullRing.rotation.x = Math.PI / 2;
    pullRing.position.set(0, canTopY + 0.008, -0.14);
    productGroup.add(pullRing);
    const tabBlade = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.016, 0.18), rimMat);
    tabBlade.position.set(0, canTopY + 0.008, 0.04);
    productGroup.add(tabBlade);
  }

  // 3) UV-Wrapped Form-Fitting 3D Sleeve OR Adhesive Label Mesh (only when a wrap is selected!)
  if (!pouchMode && hasWrap()) {
    const sMaxV = vessel.shape === "wine_bordeaux" ? 0.76 : (vessel.shape === "alu_can" ? 0.95 : 0.84);
    const sGeo = createParametricVesselGeometry(vessel, 96, 96, 0.04, sMaxV, 1.024, true);
    const lpCur = getLabelPaper();
    const fmCur = getFilm();
    const isLabelCur = isLabelMode();
    const isSleeveOnly = state.wrapType === "sleeve";
    const isNeutralClearSleeve = isSleeveOnly && state.skinId === "neutral";
    const sMat = new THREE.MeshPhysicalMaterial({
      map: sleeveTexture,
      transparent: true,
      alphaTest: 0.01,
      depthWrite: !(isNeutralClearSleeve || (isLabelCur && lpCur.transparentBg)),
      opacity: isLabelCur ? 1.0 : (isNeutralClearSleeve ? 0.94 : 0.98),
      roughness: isLabelCur ? lpCur.roughness : (isSleeveOnly ? fmCur.roughness : 0.18),
      metalness: 0.04,
      clearcoat: isLabelCur ? lpCur.clearcoat : (isSleeveOnly ? fmCur.clearcoat : 0.85),
      clearcoatRoughness: isLabelCur ? (lpCur.roughness * 0.65) : (isSleeveOnly ? fmCur.roughness * 0.75 : 0.12),
      polygonOffset: true,
      polygonOffsetFactor: -2,
      polygonOffsetUnits: -2,
      wireframe: state.wireframe
    });
    sleeveMesh = new THREE.Mesh(sGeo, sMat);
    productGroup.add(sleeveMesh);
  } else {
    sleeveMesh = null;
  }

  // 4) 3D Closure Group seated ON TOP of neck/jar/wine bague, SOT 202 can chime or pouch zip track
  if (!phys.neckMatch) state.exploded = true;
  closureGroup = buildClosure3DGroup(cl, vessel);
  const neckV = pouchMode ? 0.865 : (vessel.shape === "jar_lux" ? 0.80 : (vessel.shape === "wine_bordeaux" ? 0.955 : (vessel.shape === "alu_can" ? 0.965 : 0.88)));
  const neckBaseY = -1.25 + neckV * totalH;
  closureGroup.userData.baseY = neckBaseY;
  const clashExtra = phys.neckMatch ? 0 : (vessel.shape === "wine_bordeaux" ? 0.04 : 0.08);
  const explodeLift = vessel.shape === "wine_bordeaux" ? 0.15 : (pouchMode ? 0.28 : 0.34);
  closureGroup.position.y = neckBaseY + clashExtra + (state.exploded ? explodeLift : 0);
  productGroup.add(closureGroup);

  // 5) Red/Green Neck or Zip Validation Indicator
  const ringMat = new THREE.MeshBasicMaterial({ color: phys.neckMatch ? 0x147A3B : 0xC2180E });
  if (pouchMode) {
    const barGeo = new THREE.BoxGeometry(2.04, 0.025, 0.08);
    clashRingMesh = new THREE.Mesh(barGeo, ringMat);
    clashRingMesh.position.y = neckBaseY + 0.08;
  } else {
    const ringR = vessel.shape === "jar_lux" ? 0.78 : (vessel.shape === "wine_bordeaux" ? 0.22 : (vessel.shape === "alu_can" ? 0.54 : 0.34));
    const ringGeo = new THREE.TorusGeometry(ringR, 0.018, 16, 64);
    ringGeo.rotateX(Math.PI / 2);
    clashRingMesh = new THREE.Mesh(ringGeo, ringMat);
    clashRingMesh.position.y = neckBaseY + 0.10;
  }
  clashRingMesh.visible = !phys.isNoCap && (!phys.neckMatch || state.exploded);
  productGroup.add(clashRingMesh);

  scene.add(productGroup);
}

function initWebGL() {
  const canvas = document.getElementById("webglCanvas");
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.06;
  renderer.outputEncoding = THREE.sRGBEncoding;

  scene = new THREE.Scene();
  scene.environment = createStudioEnvironment(renderer);

  camera = new THREE.PerspectiveCamera(34, 1, 0.1, 50);

  const amb = new THREE.AmbientLight(0xFFFDF9, 0.55);
  scene.add(amb);
  const dirKey = new THREE.DirectionalLight(0xFFFDF8, 0.95);
  dirKey.position.set(4, 7, 5);
  scene.add(dirKey);
  const dirRim = new THREE.DirectionalLight(0xE8E0D5, 0.55);
  dirRim.position.set(-5, 3, -4);
  scene.add(dirRim);

  const floorGroup = new THREE.Group();
  floorGroup.position.y = -1.27;
  const gridHelper = new THREE.GridHelper(6.5, 16, 0xC2180E, 0xD2CBBF);
  gridHelper.material.opacity = 0.42;
  gridHelper.material.transparent = true;
  floorGroup.add(gridHelper);

  const shCanvas = document.createElement("canvas");
  shCanvas.width = 256; shCanvas.height = 256;
  const shCtx = shCanvas.getContext("2d");
  const shG = shCtx.createRadialGradient(128, 128, 12, 128, 128, 120);
  shG.addColorStop(0, "rgba(26, 18, 12, 0.34)");
  shG.addColorStop(0.55, "rgba(26, 18, 12, 0.12)");
  shG.addColorStop(1, "rgba(26, 18, 12, 0.0)");
  shCtx.fillStyle = shG;
  shCtx.fillRect(0, 0, 256, 256);
  const shTex = new THREE.CanvasTexture(shCanvas);
  const shPlane = new THREE.Mesh(
    new THREE.PlaneGeometry(2.6, 2.6),
    new THREE.MeshBasicMaterial({ map: shTex, transparent: true, depthWrite: false })
  );
  shPlane.rotation.x = -Math.PI / 2;
  shPlane.position.y = 0.005;
  floorGroup.add(shPlane);
  scene.add(floorGroup);

  sleeveTexture = new THREE.CanvasTexture(texCanvas);
  sleeveTexture.encoding = THREE.sRGBEncoding;
  sleeveTexture.wrapS = THREE.RepeatWrapping;
  sleeveTexture.wrapT = THREE.ClampToEdgeWrapping;
  sleeveTexture.anisotropy = renderer.capabilities.getMaxAnisotropy();

  raycaster = new THREE.Raycaster();
  pointerNDC = new THREE.Vector2();

  setupViewportInteractions(canvas);
  rebuild3DProduct();
  resizeWebGL();
  window.addEventListener("resize", resizeWebGL);
}

function setupViewportInteractions(canvas) {
  function getNDC(e) {
    const r = canvas.getBoundingClientRect();
    pointerNDC.x = ((e.clientX - r.left) / r.width) * 2 - 1;
    pointerNDC.y = -((e.clientY - r.top) / r.height) * 2 + 1;
  }

  function intersectBottleUV(e) {
    const targetMesh = isDoypack() ? vesselMesh : sleeveMesh;
    if (!targetMesh) return null;
    getNDC(e);
    raycaster.setFromCamera(pointerNDC, camera);
    const hits = raycaster.intersectObject(targetMesh, false);
    return (hits.length > 0 && hits[0].uv) ? hits[0].uv : null;
  }

  canvas.addEventListener("pointerdown", e => {
    prevPtr = { x: e.clientX, y: e.clientY };
    if (state.pointerTool === "sleeve" && !isDoypack() && !isSerigrafiaMode()) {
      if (intersectBottleUV(e)) {
        activeDragMode = "sleeve";
        canvas.style.cursor = "grabbing";
        return;
      }
    }
    activeDragMode = "orbit";
    canvas.style.cursor = "grabbing";
  });

  window.addEventListener("pointermove", e => {
    if (activeDragMode === "sleeve") {
      const dx = e.clientX - prevPtr.x;
      const dy = e.clientY - prevPtr.y;
      prevPtr = { x: e.clientX, y: e.clientY };
      state.sleeveAngleDeg = Math.max(-175, Math.min(175, Math.round(state.sleeveAngleDeg + dx * 0.45)));
      state.sleeveHeightPct = Math.max(10, Math.min(88, Math.round(state.sleeveHeightPct - dy * 0.35)));
      clampBarcodeToSleeve();
      if (sleeveMesh && sleeveMesh.geometry) applyDynamicWrapMeshDeformation(sleeveMesh.geometry, getVessel());
      renderSleeveUVTexture();
      updateFastTelemetryUI();
      return;
    }
    if (activeDragMode === "orbit") {
      camTargetTheta = null;
      const dx = e.clientX - prevPtr.x;
      const dy = e.clientY - prevPtr.y;
      prevPtr = { x: e.clientX, y: e.clientY };
      camSpherical.theta -= dx * 0.0085;
      camSpherical.phi = Math.max(0.55, Math.min(2.15, camSpherical.phi - dy * 0.0075));
      return;
    }
    const targetMesh = isDoypack() ? vesselMesh : sleeveMesh;
    if (state.mainView === "studio" && targetMesh) {
      if (state.pointerTool === "sleeve" && !isDoypack() && !isSerigrafiaMode()) {
        canvas.style.cursor = intersectBottleUV(e) ? "crosshair" : "grab";
      } else {
        canvas.style.cursor = "grab";
      }
    }
  });

  window.addEventListener("pointerup", () => {
    if (activeDragMode === "sleeve") {
      activeDragMode = null;
      renderInspector();
    }
    activeDragMode = null;
  });

  canvas.addEventListener("wheel", e => {
    e.preventDefault();
    const rawDelta = e.deltaMode === 1 ? e.deltaY * 18 : e.deltaY;
    const step = Math.max(-1.1, Math.min(1.1, rawDelta * 0.0085));
    const zb = getZoomBounds(getVessel());
    camTargetRadius = Math.max(zb.min, Math.min(zb.max, camTargetRadius + step));
  }, { passive: false });

  canvas.addEventListener("touchstart", e => {
    e.preventDefault();
  }, { passive: false });
  canvas.addEventListener("touchmove", e => {
    e.preventDefault();
  }, { passive: false });
}

function resizeWebGL() {
  if (!renderer || !camera) return;
  const stage = document.getElementById("viewportStage");
  const w = stage.clientWidth, h = stage.clientHeight;
  if (w === 0 || h === 0) return;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}

function projectWorldToScreen(vec3) {
  const stage = document.getElementById("viewportStage");
  const w = stage.clientWidth, h = stage.clientHeight;
  const v = vec3.clone().project(camera);
  return {
    x: (v.x * 0.5 + 0.5) * w,
    y: (-v.y * 0.5 + 0.5) * h,
    visible: v.z < 1.0
  };
}

function animateWebGL() {
  requestAnimationFrame(animateWebGL);
  if (state.mainView !== "studio" || !renderer) return;

  const vessel = getVessel();
  const pouchMode = isDoypack();
  const phys = evaluateLivePhysics();
  if (!phys.neckMatch) state.exploded = true;

  const targetExp = state.exploded ? 1.0 : 0.0;
  state.explodeProgress += (targetExp - state.explodeProgress) * 0.14;

  const zb = getZoomBounds(vessel);
  camTargetRadius = Math.max(zb.min, Math.min(zb.max, camTargetRadius));
  camSpherical.radius += (camTargetRadius - camSpherical.radius) * 0.24;
  camSpherical.radius = Math.max(zb.min, Math.min(zb.max, camSpherical.radius));
  if (camTargetTheta !== null) {
    let diff = camTargetTheta - camSpherical.theta;
    while (diff > Math.PI) diff -= Math.PI * 2;
    while (diff < -Math.PI) diff += Math.PI * 2;
    if (Math.abs(diff) < 0.008) {
      camSpherical.theta = camTargetTheta;
      camTargetTheta = null;
    } else {
      camSpherical.theta += diff * 0.14;
    }
  }

  if (closureGroup) {
    const clashExtra = phys.neckMatch ? 0 : (vessel.shape === "wine_bordeaux" ? 0.04 : 0.08);
    const explodeLift = vessel.shape === "wine_bordeaux" ? 0.15 : (pouchMode ? 0.28 : 0.34);
    closureGroup.position.y = closureGroup.userData.baseY + clashExtra + state.explodeProgress * explodeLift;
  }
  if (dipTubeMesh) {
    dipTubeMesh.position.y = state.explodeProgress * (vessel.shape === "wine_bordeaux" ? 0.16 : 0.24);
  }

  const lookY = vessel.shape === "jar_lux"
    ? (state.exploded ? -0.18 : -0.35)
    : (vessel.shape === "wine_bordeaux"
        ? (state.exploded ? 0.56 : 0.16)
        : (vessel.shape === "alu_can" ? 0.08 : (pouchMode ? 0.05 : 0.22)));
  camera.position.x = camSpherical.radius * Math.sin(camSpherical.phi) * Math.sin(camSpherical.theta);
  camera.position.y = camSpherical.radius * Math.cos(camSpherical.phi) + lookY + 0.05;
  camera.position.z = camSpherical.radius * Math.sin(camSpherical.phi) * Math.cos(camSpherical.theta);
  camera.lookAt(0, lookY, 0);

  renderer.render(scene, camera);
  update3DPinOverlays();
}

function update3DPinOverlays() {
  const vessel = getVessel();
  const pouchMode = isDoypack();
  const labelMode = isLabelMode();
  const stageEl = document.getElementById("viewportStage");
  const stageW = stageEl ? stageEl.clientWidth : 760;
  const stageH = stageEl ? stageEl.clientHeight : 680;
  const isCompactStage = stageW < 460;
  const totalH = getVesselTotalHeight(vessel);
  const baseScale = vessel.shape === "jar_lux" ? 0.92 : (vessel.shape === "wine_bordeaux" ? 0.58 : (vessel.shape === "alu_can" ? 0.60 : 0.68));

  // 1) Neck Pin (hidden for Can & Doypack which have no closure step, or when no closure selected)
  const pinNeck = document.getElementById("pinNeck");
  if (pouchMode || vessel.shape === "alu_can" || state.closureId === "none") {
    pinNeck.style.display = "none";
  } else {
    pinNeck.style.display = "block";
    const neckVec = new THREE.Vector3(
      vessel.shape === "wine_bordeaux" ? 0.24 : 0.45,
      -1.25 + (vessel.shape === "jar_lux" ? 0.85 : (vessel.shape === "wine_bordeaux" ? 0.94 : 0.92)) * totalH + state.explodeProgress * 0.35,
      0.22
    );
    const neckScr = projectWorldToScreen(neckVec);
    const nxOff = isCompactStage ? 58 : 88;
    const minX = isCompactStage ? 78 : 110;
    const maxX = Math.max(minX, stageW - (isCompactStage ? 84 : 115));
    pinNeck.style.left = `${Math.min(Math.max(neckScr.x + nxOff, minX), maxX)}px`;
    pinNeck.style.top = `${Math.min(Math.max(neckScr.y - 6, isCompactStage ? 92 : 88), stageH - 54)}px`;
  }

  // 2) Floating Sleeve / Label Wrap Pin (left of bottle for BOTH Sleeve AND Adhesive Label!)
  const pinSl = document.getElementById("pinSleeve");
  if (pinSl) {
    if (pouchMode || (state.wrapType !== "sleeve" && state.wrapType !== "label")) {
      pinSl.style.display = "none";
    } else {
      pinSl.style.display = "block";
      const thetaSl = (state.sleeveAngleDeg / 360) * Math.PI * 2;
      const { vMin, vMax } = getSleeveVerticalBand();
      const vSl = Math.max(0.18, vMax - 0.07);
      const rNormSl = getNormalizedRadiusAtV(vessel, vSl) * baseScale;
      const rEnvSl = getRadialEnvelopeFactor(vessel, vSl, thetaSl, rNormSl);
      const slWorld = new THREE.Vector3(rEnvSl * Math.sin(thetaSl), -1.25 + vSl * totalH, rEnvSl * Math.cos(thetaSl));
      const slScr = projectWorldToScreen(slWorld);
      const sxOff = isCompactStage ? 92 : 195;
      const sMinX = isCompactStage ? 90 : 122;
      const sMaxX = Math.max(sMinX, stageW - (isCompactStage ? 95 : 140));
      pinSl.style.left = `${Math.min(Math.max(slScr.x - sxOff, sMinX), sMaxX)}px`;
      pinSl.style.top = `${Math.min(Math.max(slScr.y - 12, isCompactStage ? 96 : 96), stageH - 64)}px`;
    }
  }

  // 3) Independent Barcode Pin (always separate from #pinSleeve — at bottom/right on Label or rear/center on Sleeve!)
  const pinBc = document.getElementById("pinBarcode");
  if (!hasWrap()) {
    pinBc.style.display = "none";
  } else {
    pinBc.style.display = "block";
    let bcWorld;
    let bcFacingCam = true;
    const camXZ = new THREE.Vector2(camera.position.x, camera.position.z).normalize();
    if (pouchMode) {
      const xOffNorm = (state.bcDoypackX / 100) * 0.46;
      const uBc = (((state.bcDoypackSide === "front" ? 0.5 + xOffNorm : xOffNorm) % 1) + 1) % 1;
      const pt = getDoypackPoint(vessel, uBc, state.bcHeightPct / 100);
      bcWorld = new THREE.Vector3(pt.x, pt.y, pt.z);
      bcFacingCam = state.bcDoypackSide === "front" ? (camXZ.y >= -0.05) : (camXZ.y <= 0.05);
    } else if (labelMode) {
      const theta = (state.sleeveAngleDeg / 360) * Math.PI * 2;
      const { vMin, vMax } = getSleeveVerticalBand();
      const vNorm = vessel.shape === "jar_lux" ? (vMin + vMax) * 0.5 : (vMin + Math.min(0.11, (vMax - vMin) * 0.22));
      const rNormBase = getNormalizedRadiusAtV(vessel, vNorm) * baseScale;
      const rEnv = getRadialEnvelopeFactor(vessel, vNorm, theta, rNormBase);
      bcWorld = new THREE.Vector3(rEnv * Math.sin(theta), -1.25 + vNorm * totalH, rEnv * Math.cos(theta));
      bcFacingCam = (Math.sin(theta) * camXZ.x + Math.cos(theta) * camXZ.y) >= -0.05;
    } else if (state.wrapType === "sleeve") {
      const effBcDeg = state.sleeveAngleDeg >= 0 ? state.sleeveAngleDeg - 180 : state.sleeveAngleDeg + 180;
      const theta = (effBcDeg / 360) * Math.PI * 2;
      const sMaxV = vessel.shape === "wine_bordeaux" ? 0.76 : (vessel.shape === "alu_can" ? 0.95 : 0.84);
      const vNorm = 0.04 + (state.bcHeightPct / 100) * (sMaxV - 0.04);
      const rNormBase = getNormalizedRadiusAtV(vessel, vNorm) * baseScale;
      const rEnv = getRadialEnvelopeFactor(vessel, vNorm, theta, rNormBase);
      bcWorld = new THREE.Vector3(rEnv * Math.sin(theta), -1.25 + vNorm * totalH, rEnv * Math.cos(theta));
      bcFacingCam = (Math.sin(theta) * camXZ.x + Math.cos(theta) * camXZ.y) >= -0.05;
    } else {
      const theta = (state.bcAngleDeg / 360) * Math.PI * 2;
      const sMaxV = vessel.shape === "wine_bordeaux" ? 0.76 : (vessel.shape === "alu_can" ? 0.95 : 0.84);
      const vNorm = 0.04 + (state.bcHeightPct / 100) * (sMaxV - 0.04);
      const rNormBase = getNormalizedRadiusAtV(vessel, vNorm) * baseScale;
      const rEnv = getRadialEnvelopeFactor(vessel, vNorm, theta, rNormBase);
      bcWorld = new THREE.Vector3(rEnv * Math.sin(theta), -1.25 + vNorm * totalH, rEnv * Math.cos(theta));
      bcFacingCam = (Math.sin(theta) * camXZ.x + Math.cos(theta) * camXZ.y) >= -0.05;
    }
    pinBc.style.opacity = bcFacingCam ? "1" : "0";
    const bcScr = projectWorldToScreen(bcWorld);
    const bcOffsetX = isCompactStage ? 72 : (labelMode ? 185 : 135);
    const bMinX = isCompactStage ? 88 : 120;
    const bMaxX = Math.max(bMinX, stageW - (isCompactStage ? 92 : 130));
    pinBc.style.left = `${Math.min(Math.max(bcScr.x + bcOffsetX, bMinX), bMaxX)}px`;
    pinBc.style.top = `${Math.min(Math.max(bcScr.y + (labelMode ? 22 : 0), 100), stageH - 58)}px`;
  }
}

// ==================== UI ACTIONS & MUTUALLY EXCLUSIVE TOOLS ====================
function vesselHasClosureStep(v) {
  const vv = v || getVessel();
  return vv.shape !== "doypack" && vv.shape !== "alu_can";
}

function resetVesselConfigState(vid) {
  const v = VESSELS.find(item => item.id === vid) || getVessel();
  state.vesselId = v.id;
  state.finishId = v.defaultFinish;
  state.inspTab = vesselHasClosureStep(v) ? 1 : 2; // Skip Chiusura step for Can & Doypack
  state.closureId = "none";
  state.wrapType = "none";
  state.pouchPrintType = "none";
  state.skinId = "none";
  state.filmId = "PETG";
  state.labelMatId = "COTTON";
  state.serigrafiaInkId = "UV_HIGH";
  state.pouchMatId = "ALU_TRI";
  state.sleeveAngleDeg = 0;
  state.sleeveHeightPct = 18;
  state.bcAngleDeg = 180; // Behind the front graphic initially
  state.bcHeightPct = 24;
  state.bcLadder = false;
  state.bcDoypackSide = "back"; // Behind the front pouch graphic initially
  state.bcDoypackX = 0;
  camTargetTheta = null;
  state.infoPopoverOpen = false;
  state.customVesselMode = false;
  state.customGraphicMode = false;
  state.customGraphicFile = "";
  state.arModalOpen = false;
  state.boxMode = "grid";
  state.boxQty = 1;
  state.bulkQty = 100;
  state.boxDivider = false;
  state.boxBoard = "teso";
  state.pointerTool = "orbit"; // Always start with Ruota 3D active
  state.exploded = false;
  state.explodeProgress = 0;
  state.xray = false;
  state.heatmap = false;
  state.wireframe = false;
  state.filieraStep = 1;
  state.selectedSuppliers = { container: 0 };
  state.copackerFilling = false;
  state.copackerFillType = (getAllowedFillTypes(v)[0]?.id) || "Liquidi";
  if (v.shape === "doypack") camSpherical = { theta: 0.22, phi: 1.38, radius: 5.85 };
  else if (v.shape === "jar_lux") camSpherical = { theta: 0.25, phi: 1.30, radius: 4.85 };
  else if (v.shape === "wine_bordeaux") camSpherical = { theta: 0.25, phi: 1.38, radius: 6.75 };
  else if (v.shape === "alu_can") camSpherical = { theta: 0.44, phi: 1.36, radius: 5.85 };
  else camSpherical = { theta: 0.25, phi: 1.38, radius: 6.15 };
  camTargetRadius = camSpherical.radius;
}

function selectVesselFromMarketplace(vid) {
  state.customVesselMode = false;
  state.customGraphicMode = false;
  resetVesselConfigState(vid);
  switchMainView("studio");
  rebuild3DProduct();
  renderAllUI();
}

function goStepBack() {
  if (state.mainView === "profile") {
    const backTarget = (state.prevViewBeforeProfile && state.prevViewBeforeProfile !== "profile") ? state.prevViewBeforeProfile : "catalog";
    switchMainView(backTarget);
    return;
  }
  if (state.mainView === "pillars") {
    state.filieraStep = 1;
    state.selectedSuppliers = { container: 0 };
    state.copackerFilling = false;
    switchMainView("studio");
    rebuild3DProduct();
    renderAllUI();
  } else if (state.mainView === "studio") {
    if (state.customGraphicMode) {
      closeCustomGraphicStudio();
      return;
    }
    state.customVesselMode = false;
    resetVesselConfigState(state.vesselId);
    switchMainView("catalog");
  }
}

function setDoypackPrintType(pt) {
  if (!isDoypack()) return;
  if (hasWrap() && state.pouchPrintType === pt) {
    state.wrapType = "none";
    state.pouchPrintType = "none";
    state.skinId = "none";
    state.pointerTool = "orbit";
  } else {
    state.wrapType = "pouch";
    state.pouchPrintType = pt;
    if (state.skinId === "none" || state.skinId === "neutral") state.skinId = "lumina";
  }
  state.selectedSuppliers = { container: 0 };
  state.filieraStep = 1;
  rebuild3DProduct();
  renderAllUI();
}

function setWrapType(wt) {
  if (isDoypack()) return;
  if (wt === "serigrafia" && getVessel().shape !== "alu_can") return;
  // Re-clicking active wrap toggles back to bare container ('none')
  if (state.wrapType === wt) {
    state.wrapType = "none";
    state.skinId = "none";
    state.pointerTool = "orbit";
  } else {
    if (wt === "sleeve" || wt === "label") {
      state.sleeveHeightPct = 18;
      state.sleeveAngleDeg = 0;
    }
    state.wrapType = wt;
    if (wt === "sleeve" || wt === "label") {
      // Sleeve defaults initially to Neutra Trasparente; Adhesive Label defaults initially to Bianca Senza Scritte
      state.skinId = "neutral";
    } else if (state.skinId === "none" || state.skinId === "neutral") {
      state.skinId = "lumina";
    }
    if (wt === "serigrafia" && state.pointerTool === "sleeve") {
      state.pointerTool = "orbit";
    }
  }
  state.selectedSuppliers = { container: 0 };
  state.filieraStep = 1;
  rebuild3DProduct();
  renderAllUI();
}

function selectSkin(sid) {
  if (isDoypack()) {
    state.skinId = sid;
    state.wrapType = "pouch";
    if (state.pouchPrintType === "none") state.pouchPrintType = "digital";
    state.selectedSuppliers = { container: 0 };
    state.filieraStep = 1;
    rebuild3DProduct();
    renderAllUI();
    return;
  }
  const prevSkin = state.skinId;
  state.skinId = sid;
  if ((prevSkin === "neutral") !== (sid === "neutral")) {
    rebuild3DProduct();
  } else {
    if (sleeveMesh && sleeveMesh.geometry) applyDynamicWrapMeshDeformation(sleeveMesh.geometry, getVessel());
    renderSleeveUVTexture();
  }
  renderInspector();
  updateFastTelemetryUI();
}

function flipDoypackSide(targetSide) {
  state.bcDoypackSide = targetSide || (state.bcDoypackSide === "front" ? "back" : "front");
  camTargetTheta = state.bcDoypackSide === "back" ? (Math.PI + 0.22) : 0.22;
  renderSleeveUVTexture();
  renderAllUI();
}

function updateDoypackBarcode(xPct, yPct) {
  if (xPct !== null) state.bcDoypackX = Number(xPct);
  if (yPct !== null) state.bcHeightPct = Number(yPct);
  camSpherical.theta = state.bcDoypackSide === "back" ? (Math.PI + 0.22) : 0.22;
  renderSleeveUVTexture();
  updateFastTelemetryUI();
}

function getActiveDragToast(tr) {
  return tr.dragToastOrbit;
}

function setLanguage(l) {
  state.lang = l;
  const bIt = document.getElementById("btnLangIT");
  const bEn = document.getElementById("btnLangEN");
  if (bIt) bIt.classList.toggle("active", l === "it");
  if (bEn) bEn.classList.toggle("active", l === "en");
  renderAllUI();
}

let isApplyingHistoryState = false;

function getRouteKey() {
  if (state.mainView === "studio" && state.customVesselMode) return "custom-vessel";
  if (state.mainView === "studio" && state.customGraphicMode) return `custom-graphic:${state.vesselId}`;
  if (state.mainView === "studio") return `studio:${state.vesselId}`;
  if (state.mainView === "pillars") return `pillars:${state.vesselId}:${state.filieraStep || 1}`;
  if (state.mainView === "profile") return "profile";
  return "catalog";
}

function buildHistoryStateSnapshot() {
  return {
    routeKey: getRouteKey(),
    mainView: state.mainView,
    customVesselMode: !!state.customVesselMode,
    customGraphicMode: !!state.customGraphicMode,
    vesselId: state.vesselId,
    filieraStep: state.filieraStep || 1
  };
}

function buildHistoryUrl(snap) {
  if (window.location.protocol === "file:") return null;
  try {
    const u = new URL(window.location.href);
    u.search = "";
    if (snap.customVesselMode && snap.mainView === "studio") {
      u.searchParams.set("view", "custom-vessel");
    } else if (snap.customGraphicMode && snap.mainView === "studio") {
      u.searchParams.set("view", "custom-graphic");
      u.searchParams.set("vessel", snap.vesselId);
    } else {
      u.searchParams.set("view", snap.mainView || "catalog");
      if (snap.mainView === "studio") {
        u.searchParams.set("vessel", snap.vesselId);
      } else if (snap.mainView === "pillars") {
        u.searchParams.set("vessel", snap.vesselId);
        u.searchParams.set("fstep", String(snap.filieraStep || 1));
      }
    }
    return u.pathname + u.search;
  } catch (e) {
    return null;
  }
}

function syncBrowserHistory(forceReplace) {
  if (isApplyingHistoryState || !window.history || !window.history.pushState) return;
  try {
    const snap = buildHistoryStateSnapshot();
    const urlArg = buildHistoryUrl(snap);
    if (forceReplace) {
      window.history.replaceState(snap, "", urlArg);
    } else if (!window.history.state || window.history.state.routeKey !== snap.routeKey) {
      window.history.pushState(snap, "", urlArg);
    }
  } catch (e) {}
}

window.addEventListener("popstate", e => {
  const modal = document.getElementById("checkoutModal");
  if (modal) modal.classList.remove("open");
  let snap = e.state;
  if (!snap || !snap.mainView) {
    const qs = new URLSearchParams(window.location.search);
    const vParam = qs.get("view") || "catalog";
    snap = {
      mainView: (vParam === "custom-vessel" || vParam === "custom-graphic") ? "studio" : vParam,
      customVesselMode: vParam === "custom-vessel",
      customGraphicMode: vParam === "custom-graphic",
      vesselId: qs.get("vessel") || state.vesselId || "serum_250",
      filieraStep: Number(qs.get("fstep")) || 1
    };
  }
  isApplyingHistoryState = true;
  try {
    if (snap.vesselId && VESSELS.some(v => v.id === snap.vesselId) && snap.vesselId !== state.vesselId) {
      resetVesselConfigState(snap.vesselId);
    }
    state.customVesselMode = !!snap.customVesselMode;
    state.customGraphicMode = !!snap.customGraphicMode;
    if (snap.mainView === "pillars") {
      const targetStep = Math.max(1, Number(snap.filieraStep) || 1);
      const previewSteps = buildSupplyChainSteps(evaluateLivePhysics());
      previewSteps.slice(0, Math.max(0, targetStep - 1)).forEach(s => {
        if (!s.lockedFixed && state.selectedSuppliers[s.key] === undefined) {
          state.selectedSuppliers[s.key] = 0;
        }
      });
      state.filieraStep = targetStep;
    }
    if (snap.mainView === "studio" && !state.customVesselMode && !state.customGraphicMode) {
      rebuild3DProduct();
    }
    switchMainView(snap.mainView || "catalog");
  } finally {
    isApplyingHistoryState = false;
  }
});

function switchMainView(v) {
  if (v !== "profile" && state.mainView !== "profile") {
    state.prevViewBeforeProfile = v;
  }
  state.mainView = v;
  state.infoPopoverOpen = false;
  state.arModalOpen = false;
  const arOv = document.getElementById("arQrOverlay");
  if (arOv) arOv.classList.remove("open");

  document.getElementById("navCatalog").classList.toggle("active", v === "catalog");
  document.getElementById("navStudio").classList.toggle("active", v === "studio");
  document.getElementById("navPillars").classList.toggle("active", v === "pillars");
  const btnProf = document.getElementById("btnProfile");
  if (btnProf) btnProf.classList.toggle("active", v === "profile");

  document.getElementById("viewCatalog").classList.toggle("active", v === "catalog");
  document.getElementById("viewStudio").classList.toggle("active", v === "studio");
  document.getElementById("viewPillars").classList.toggle("active", v === "pillars");
  const vProf = document.getElementById("viewProfile");
  if (vProf) vProf.classList.toggle("active", v === "profile");

  const gridMain = document.getElementById("studioGridMain");
  const customStage = document.getElementById("customVesselStage");
  if (gridMain && customStage) {
    const showCustom = (v === "studio" && (state.customVesselMode || state.customGraphicMode));
    gridMain.style.display = showCustom ? "none" : "";
    customStage.style.display = showCustom ? "block" : "none";
  }

  if (v === "studio" && !state.customVesselMode && !state.customGraphicMode) setTimeout(resizeWebGL, 25);
  syncBrowserHistory(false);
  renderAllUI();
  if (window.scrollY !== 0) window.scrollTo(0, 0);
}

// ==================== CUSTOM CONTAINER UPLOAD & CUSTOM GRAPHIC UPLOAD DEMO (UNDER 02 STUDIO 3D) ====================
function openCustomVesselStudio() {
  state.customGraphicMode = false;
  state.customVesselMode = true;
  switchMainView("studio");
}

function openCustomGraphicStudio() {
  state.customVesselMode = false;
  state.customGraphicMode = true;
  state.customGraphicFile = "";
  switchMainView("studio");
}

function closeCustomGraphicStudio() {
  state.customGraphicMode = false;
  switchMainView("studio");
  rebuild3DProduct();
  renderAllUI();
}

function handleCustomGraphicUpload(inputEl) {
  const file = inputEl && inputEl.files && inputEl.files[0];
  if (!file) return;
  state.customGraphicFile = file.name;
  renderCustomGraphicView();
}

function renderCustomGraphicView() {
  const host = document.getElementById("customVesselStage");
  if (!host || !state.customGraphicMode) return;
  const l = state.lang;
  const v = getVessel();
  const maxDims = getMaxApplicableSurfaceDimensionsMm(v);
  const pouchMode = isDoypack();
  const labelMode = isLabelMode();
  const serigMode = isSerigrafiaMode();

  const processIt = pouchMode
    ? (state.pouchPrintType === "flexo" ? "Stampa Flessografica su Doypack" : "Stampa Digitale su Doypack")
    : (serigMode
        ? "Serigrafia Diretta 360° su Alluminio"
        : (labelMode ? "Etichetta Adesiva Fustellata" : "Sleeve Termoretraibile 360°"));
  const processEn = pouchMode
    ? (state.pouchPrintType === "flexo" ? "Flexographic Pouch Printing" : "Digital Pouch Printing")
    : (serigMode
        ? "360° Direct-to-Can Silk Screen"
        : (labelMode ? "Die-Cut Adhesive Label" : "360° Heat-Shrink Sleeve"));

  const matName = pouchMode
    ? (l === "it" ? (POUCH_FINISHES.find(f => f.id === state.finishId)?.it || "Bianco Soft-Touch") : (POUCH_FINISHES.find(f => f.id === state.finishId)?.en || "White Soft-Touch"))
    : (serigMode
        ? getSerigrafiaInk().name
        : (labelMode ? getLabelPaper().name : getFilm().name));

  const formatNoteIt = pouchMode
    ? "Area massima applicabile sull'intera facciata della busta (incluse zone di saldatura e zip)"
    : (serigMode
        ? "Superficie massima cilindrica 360° applicabile sul corpo lattina (incluse zone di rastrematura)"
        : (labelMode
            ? "Area massima di applicazione su corpo e spalle del contenitore (incluse eventuali zone gialle/rosse)"
            : "Superficie massima applicabile dello sleeve 360° sull'intero corpo e spalla (incluse zone gialle/rosse)"));
  const formatNoteEn = pouchMode
    ? "Maximum applicable surface across full pouch panel (including heat-seals and zip)"
    : (serigMode
        ? "Maximum 360° cylindrical surface area across full can wall (including chime taper)"
        : (labelMode
            ? "Maximum applicable label envelope across full container surface (including yellow/red warning zones)"
            : "Maximum 360° shrink-sleeve envelope across full container body and shoulder (including warning/error zones)"));

  host.innerHTML = `
    <div class="custom-vessel-inner">
      <div class="brown-hdr-bar">
        <div>
          <div class="brown-hdr-kicker">${l === "it" ? "CARICAMENTO GRAFICA ESECUTIVA DI STAMPA" : "CUSTOM PRINT ARTWORK UPLOAD"}</div>
          <h1 class="brown-hdr-title">${l === "it" ? "Inserisci il file della tua grafica" : "Upload your custom graphic file"}</h1>
        </div>
      </div>

      <div class="custom-panel-card">
        <div class="custom-blueprint-grid">
          <div class="custom-bp-left">
            <div>
              <span style="font-family:var(--mono); font-size:10.5px; font-weight:800; color:var(--crimson);">${l === "it" ? "SPECIFICHE SUPERFICIE MASSIMA" : "MAXIMUM APPLICABLE SURFACE SPECS"}</span>
              <h2 style="font-family:var(--display); font-size:18px; font-weight:700; color:var(--ink); margin-top:3px;">${l === "it" ? processIt : processEn}</h2>
              <p style="font-size:12px; color:var(--slate); margin-top:4px; line-height:1.45;">
                ${l === "it"
                  ? "Le dimensioni indicate rappresentano la superficie massima totale di applicazione sul contenitore (comprese le fasce curve in avviso o blocco)."
                  : "Dimensions indicate the maximum total application area across the container (including curved warning and error zones)."}
              </p>
            </div>

            <div class="custom-spec-checklist">
              <div style="font-weight:800; color:var(--ink); letter-spacing:0.06em;">${l === "it" ? "PARAMETRI ATTIVI IN STUDIO 3D" : "ACTIVE 3D STUDIO PARAMETERS"}</div>
              <div>01 // ${l === "it" ? "Misure:" : "Dimensions:"} <strong>${l === "it" ? v.subIt : v.subEn}</strong></div>
              <div>02 // ${l === "it" ? "Lavorazione:" : "Process:"} <strong>${l === "it" ? processIt : processEn}</strong></div>
              <div>03 // ${l === "it" ? "Materiale:" : "Material:"} <strong>${matName}</strong></div>
            </div>
          </div>

          <div class="custom-bp-right">
            <div>
              <span style="font-family:var(--mono); font-size:10.5px; font-weight:800; color:var(--crimson);">${l === "it" ? "UPLOAD FILE GRAFICA" : "ARTWORK FILE UPLOAD"}</span>
              <h2 style="font-family:var(--display); font-size:18px; font-weight:700; color:var(--ink); margin-top:3px;">${l === "it" ? "Dimensioni max applicabili" : "Max applicable dimensions"}</h2>
              <p style="font-size:12px; color:var(--slate); margin-top:4px; line-height:1.45;">${l === "it" ? formatNoteIt : formatNoteEn}</p>
            </div>

            <label class="upload-datasheet-box ${state.customGraphicFile ? "loaded" : ""}" style="min-height:132px; justify-content:center; flex-direction:column; text-align:center;">
              <div style="font-family:var(--mono); font-size:20px; font-weight:800; color:var(--crimson);">${maxDims.wrapDimStr}</div>
              <div style="font-size:13.5px; font-weight:800; color:var(--ink);">
                ${state.customGraphicFile ? `✓ ${state.customGraphicFile}` : (l === "it" ? `Carica esecutivo grafica (max ${maxDims.wrapDimStr})` : `Upload graphic file (max ${maxDims.wrapDimStr})`)}
              </div>
              <div style="font-size:11px; color:var(--slate);">
                ${l === "it" ? "PDF vettoriale, Adobe Illustrator (.ai), TIFF o PNG · 300 DPI · Quadricromia CMYK + Pantone" : "Vector PDF, Adobe Illustrator (.ai), TIFF or PNG · 300 DPI · CMYK + Spot"}
              </div>
              <span class="spec-tag ${state.customGraphicFile ? "ok" : ""}">${state.customGraphicFile ? (l === "it" ? "CARICATO ✓" : "UPLOADED ✓") : (l === "it" ? "SELEZIONA FILE" : "SELECT FILE")}</span>
              <input type="file" accept=".pdf,.ai,.eps,.svg,.png,.jpg,.jpeg,.tif,.tiff" style="display:none;" onchange="handleCustomGraphicUpload(this)">
            </label>
          </div>
        </div>

        <p class="demo-red-text">
          ${l === "it"
            ? "Anteprima dimostrativa: funzione ancora in fase di sviluppo"
            : "Demonstrative preview: feature still in development"}
        </p>

        <div style="display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap; border-top:1.5px solid var(--border); padding-top:12px;">
          <button class="cta-btn white" style="width:auto; min-width:200px; padding:0 22px;" onclick="closeCustomGraphicStudio()">
            ${l === "it" ? "Torna allo Studio 3D" : "Back to 3D Studio"}
          </button>
          <button class="cta-btn" id="btnCustomGraphicProceedDemo" style="width:auto; min-width:240px; padding:0 22px;" disabled>
            ${l === "it" ? "Applica grafica nello Studio 3D" : "Apply graphic in 3D Studio"}
          </button>
        </div>
      </div>
    </div>
  `;
}

function handleCustomUpload(type, idx, inputEl) {
  const file = inputEl && inputEl.files && inputEl.files[0];
  if (!file) return;
  if (type === "datasheet") {
    state.customDatasheetFile = file.name;
  } else {
    state.customPhotoFiles[idx] = file.name;
  }
  renderCustomVesselView();
}

function renderCustomVesselView() {
  const host = document.getElementById("customVesselStage");
  if (!host || !state.customVesselMode) return;
  const l = state.lang;
  const slots = [
    { it: "1. Lato Frontale", en: "1. Front Side", subIt: "Vista frontale dritta al centro", subEn: "Straight centered front view" },
    { it: "2. Lato Posteriore", en: "2. Back Side", subIt: "Vista posteriore a 180°", subEn: "180° rear side view" },
    { it: "3. Lato Sinistro", en: "3. Left Side", subIt: "Profilo laterale sinistro (90°)", subEn: "Left side profile (90°)" },
    { it: "4. Lato Destro", en: "4. Right Side", subIt: "Profilo laterale destro (270°)", subEn: "Right side profile (270°)" },
    { it: "5. Vista Dall'Alto (Sopra)", en: "5. Top View", subIt: "Imboccatura, collo e filettatura", subEn: "Mouth, neck finish and thread" },
    { it: "6. Vista Dal Basso (Sotto)", en: "6. Bottom View", subIt: "Fondo e profilo di appoggio", subEn: "Base and bottom footprint" }
  ];
  const uploadedPhotos = state.customPhotoFiles.filter(Boolean).length;

  host.innerHTML = `
    <div class="custom-vessel-inner">
      <div class="brown-hdr-bar">
        <div>
          <div class="brown-hdr-kicker">${l === "it" ? "DIGITALIZZAZIONE CONTENITORE PERSONALIZZATO" : "CUSTOM CONTAINER 3D DIGITIZATION"}</div>
          <h1 class="brown-hdr-title">${l === "it" ? "Ricrea il tuo contenitore nello Studio 3D" : "Recreate your container in the 3D Studio"}</h1>
        </div>
      </div>

      <div class="custom-panel-card">
        <div class="custom-blueprint-grid">
          <div class="custom-bp-left">
            <div>
              <span style="font-family:var(--mono); font-size:10.5px; font-weight:800; color:var(--crimson);">${l === "it" ? "REQUISITO 01 · SCHEDA TECNICA" : "REQUIREMENT 01 · TECHNICAL DATASHEET"}</span>
              <h2 style="font-family:var(--display); font-size:17px; font-weight:700; color:var(--ink); margin-top:3px;">${l === "it" ? "Carica la foto o il file della scheda tecnica del contenitore" : "Upload photo or file of your container technical datasheet"}</h2>
              <p style="font-size:12px; color:var(--slate); margin-top:4px; line-height:1.45;">${l === "it" ? "Necessaria per acquisire le quote esatte (altezza, diametro, filettatura collo, capacità e materiale)." : "Required to capture exact dimensions (height, diameter, neck finish, capacity and material)."}</p>
            </div>

            <label class="upload-datasheet-box ${state.customDatasheetFile ? "loaded" : ""}">
              <div>
                <div style="font-size:13px; font-weight:800; color:var(--ink);">${state.customDatasheetFile ? `✓ ${state.customDatasheetFile}` : (l === "it" ? "Carica foto o PDF della scheda tecnica" : "Upload datasheet photo or PDF")}</div>
                <div style="font-size:11px; color:var(--slate); margin-top:2px;">${l === "it" ? "Formati supportati: JPG, PNG, PDF · Quote meccaniche e collo" : "Supported formats: JPG, PNG, PDF · Mechanical specs and neck"}</div>
              </div>
              <span class="spec-tag ${state.customDatasheetFile ? "ok" : ""}">${state.customDatasheetFile ? (l === "it" ? "CARICATA ✓" : "UPLOADED ✓") : (l === "it" ? "SELEZIONA FILE" : "SELECT FILE")}</span>
              <input type="file" accept="image/*,.pdf" style="display:none;" onchange="handleCustomUpload('datasheet', 0, this)">
            </label>

            <div class="custom-spec-checklist">
              <div style="font-weight:800; color:var(--ink); letter-spacing:0.06em;">${l === "it" ? "PIPELINE PARAMETRICA" : "PARAMETRIC PIPELINE"}</div>
              <div>01 // ${l === "it" ? "Estrazione quote H × Ø e collo" : "Extract H × Ø dimensions and neck finish"}</div>
              <div>02 // ${l === "it" ? "Calibrazione mesh WebGL e curve spalla" : "WebGL mesh calibration and shoulder curves"}</div>
              <div>03 // ${l === "it" ? "Validazione TD% e filetti 1:1" : "TD% shrink physics and 1:1 thread lock"}</div>
            </div>
          </div>

          <div class="custom-bp-right">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px; flex-wrap:wrap;">
              <div>
                <span style="font-family:var(--mono); font-size:10.5px; font-weight:800; color:var(--crimson);">${l === "it" ? "REQUISITO 02 · ACQUISIZIONE FOTOGRAFICA MULTI-ANGOLO" : "REQUIREMENT 02 · MULTI-ANGLE PHOTO CAPTURE"}</span>
                <h2 style="font-family:var(--display); font-size:17px; font-weight:700; color:var(--ink); margin-top:3px;">${l === "it" ? "Carica almeno 6 foto da tutti i lati del contenitore" : "Upload at least 6 photos from all sides of the container"}</h2>
                <p style="font-size:12px; color:var(--slate); margin-top:4px; line-height:1.45;">${l === "it" ? "Carica le 4 viste laterali, la vista da sopra e la vista da sotto per permettere la ricostruzione parametrica 3D." : "Upload all 4 lateral sides, top view and bottom view to enable parametric 3D reconstruction."}</p>
              </div>
              <span class="spec-tag ${uploadedPhotos === 6 ? "ok" : ""}">${uploadedPhotos} / 6 ${l === "it" ? "FOTO" : "PHOTOS"}</span>
            </div>

            <div class="upload-slot-grid">
              ${slots.map((sl, idx) => {
                const fName = state.customPhotoFiles[idx];
                return `
                  <label class="upload-slot ${fName ? "loaded" : ""}">
                    <span class="upload-slot-num">${fName ? "✓ CARICATA" : `FOTO 0${idx + 1}`}</span>
                    <span class="upload-slot-title">${l === "it" ? sl.it : sl.en}</span>
                    <span class="upload-slot-sub">${fName ? fName : (l === "it" ? sl.subIt : sl.subEn)}</span>
                    <input type="file" accept="image/*" style="display:none;" onchange="handleCustomUpload('photo', ${idx}, this)">
                  </label>
                `;
              }).join("")}
            </div>
          </div>
        </div>

        <p class="demo-red-text">
          ${l === "it"
            ? "Anteprima dimostrativa: funzione ancora in fase di sviluppo"
            : "Demonstrative preview: feature still in development"}
        </p>

        <div style="display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap; border-top:1.5px solid var(--border); padding-top:12px;">
          <button class="cta-btn white" style="width:auto; min-width:200px; padding:0 22px;" onclick="state.customVesselMode=false; switchMainView('catalog');">
            ${l === "it" ? "Torna al Marketplace" : "Back to Marketplace"}
          </button>
          <button class="cta-btn" id="btnCustomProceedDemo" style="width:auto; min-width:240px; padding:0 22px;" disabled>
            ${l === "it" ? "Ricrea nel Configuratore 3D" : "Recreate in 3D Configurator"}
          </button>
        </div>
      </div>
    </div>
  `;
}

// ==================== AUGMENTED REALITY (AR) FICTITIOUS QR CODE OVERLAY ====================
function buildFictitiousQRSVG(seedStr) {
  const N = 25;
  const grid = Array.from({ length: N }, () => Array(N).fill(false));
  const reserved = Array.from({ length: N }, () => Array(N).fill(false));

  function drawFinder(r0, c0) {
    for (let r = -1; r <= 7; r++) {
      for (let c = -1; c <= 7; c++) {
        const rr = r0 + r, cc = c0 + c;
        if (rr < 0 || rr >= N || cc < 0 || cc >= N) continue;
        reserved[rr][cc] = true;
        const inOuter = r >= 0 && r <= 6 && c >= 0 && c <= 6;
        const border = r === 0 || r === 6 || c === 0 || c === 6;
        const inner = r >= 2 && r <= 4 && c >= 2 && c <= 4;
        grid[rr][cc] = inOuter && (border || inner);
      }
    }
  }
  drawFinder(0, 0);
  drawFinder(0, N - 7);
  drawFinder(N - 7, 0);

  // Alignment pattern at (16..20, 16..20)
  for (let r = 16; r <= 20; r++) {
    for (let c = 16; c <= 20; c++) {
      reserved[r][c] = true;
      const b = r === 16 || r === 20 || c === 16 || c === 20 || (r === 18 && c === 18);
      grid[r][c] = b;
    }
  }
  // Timing tracks
  for (let i = 8; i < N - 8; i++) {
    reserved[6][i] = true; grid[6][i] = (i % 2 === 0);
    reserved[i][6] = true; grid[i][6] = (i % 2 === 0);
  }
  // Center quiet area for crimson cube emblem
  for (let r = 10; r <= 14; r++) {
    for (let c = 10; c <= 14; c++) {
      reserved[r][c] = true;
      grid[r][c] = false;
    }
  }
  // Deterministic pseudo-random modules from seedStr
  let hVal = 2166136261;
  for (let i = 0; i < seedStr.length; i++) {
    hVal ^= seedStr.charCodeAt(i);
    hVal = Math.imul(hVal, 16777619);
  }
  for (let r = 0; r < N; r++) {
    for (let c = 0; c < N; c++) {
      if (reserved[r][c]) continue;
      hVal ^= (r * 31 + c * 17);
      hVal = Math.imul(hVal, 16777619);
      grid[r][c] = ((hVal >>> 0) % 100) < 48;
    }
  }

  const cell = 8;
  const pad = 12;
  const size = N * cell + pad * 2;
  let rects = "";
  for (let r = 0; r < N; r++) {
    for (let c = 0; c < N; c++) {
      if (grid[r][c]) {
        rects += `<rect x="${pad + c * cell}" y="${pad + r * cell}" width="${cell}" height="${cell}" rx="1.2" fill="#121110"/>`;
      }
    }
  }
  const cx = size / 2, cy = size / 2;
  return `
    <svg width="212" height="212" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
      <rect width="${size}" height="${size}" fill="#FFFFFF"/>
      ${rects}
      <rect x="${cx - 19}" y="${cy - 19}" width="38" height="38" rx="6" fill="#FFFFFF" stroke="#C2180E" stroke-width="2.5"/>
      <polygon points="${cx},${cy - 11} ${cx + 11},${cy - 5} ${cx},${cy + 1} ${cx - 11},${cy - 5}" fill="#121110"/>
      <polygon points="${cx - 11},${cy - 3} ${cx - 1},${cy + 3} ${cx - 1},${cy + 12} ${cx - 11},${cy + 6}" fill="#C2180E"/>
      <polygon points="${cx + 11},${cy - 3} ${cx + 1},${cy + 3} ${cx + 1},${cy + 12} ${cx + 11},${cy + 6}" fill="#3A2D26"/>
    </svg>
  `;
}

function toggleARModal(openVal) {
  state.arModalOpen = (openVal !== undefined) ? !!openVal : !state.arModalOpen;
  const overlay = document.getElementById("arQrOverlay");
  const card = document.getElementById("arQrCard");
  if (!overlay || !card) return;
  overlay.classList.toggle("open", state.arModalOpen);
  if (!state.arModalOpen) return;
  const l = state.lang;
  const v = getVessel();
  const qrSvg = buildFictitiousQRSVG(`${v.id}-${state.closureId}-${state.wrapType}-${state.skinId}`);
  card.innerHTML = `
    <div style="width:100%; display:flex; justify-content:space-between; align-items:center;">
      <span style="font-family:var(--mono); font-size:10px; font-weight:800; color:var(--crimson); letter-spacing:0.1em;">${l === "it" ? "REALTÀ AUMENTATA · SCALA REALE 1:1" : "AUGMENTED REALITY · REAL 1:1 SCALE"}</span>
      <button type="button" style="border:none; background:transparent; cursor:pointer; font-size:16px; font-weight:800; color:var(--slate);" onclick="toggleARModal(false)">✕</button>
    </div>
    <h3 style="font-size:17px; font-weight:800; color:var(--ink); margin-top:2px;">${l === "it" ? "Visualizza il prodotto sul tuo tavolo" : "View the product on your desk"}</h3>
    <div style="font-family:var(--mono); font-size:12px; font-weight:700; color:var(--espresso); text-align:center; line-height:1.45;">
      <div>${l === "it" ? v.it : v.en}</div>
      <div style="color:var(--slate); font-weight:600; margin-top:2px;">${l === "it" ? v.subIt : v.subEn}</div>
    </div>
    <div class="ar-qr-frame">${qrSvg}</div>
    <p style="font-size:12px; color:var(--charcoal); line-height:1.45;">
      ${l === "it"
        ? "Inquadra questo QR code con la fotocamera dello smartphone per aprire la vista in realtà aumentata e posizionare il contenitore nelle sue dimensioni reali dove preferisci."
        : "Scan this QR code with your smartphone camera to open the augmented reality viewer and place the container at true 1:1 scale on any surface."}
    </p>
    <p class="demo-red-text" style="text-align:center; width:100%; margin:2px 0 0;">
      ${l === "it" ? "Anteprima dimostrativa: funzione ancora in fase di sviluppo" : "Demonstrative preview: feature still in development"}
    </p>
  `;
}

// ==================== USER PROFILE, FAVORITES & SUBMITTED REQUESTS PERSISTENCE ====================
const REQUEST_STORAGE_KEY = "vesselcove_submitted_requests_v19";
const FAVORITES_STORAGE_KEY = "vesselcove_favorite_vessels_v25";
const ACCEPTANCE_DEADLINE_DAYS = 3;

function loadFavoriteVessels() {
  try {
    const raw = localStorage.getItem(FAVORITES_STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) state.favoriteVessels = parsed;
    }
  } catch {}
}

function saveFavoriteVessels() {
  try {
    localStorage.setItem(FAVORITES_STORAGE_KEY, JSON.stringify(state.favoriteVessels));
  } catch {}
}

function isVesselFavorite(vid) {
  return Array.isArray(state.favoriteVessels) && state.favoriteVessels.includes(vid);
}

function updateFavoritesBadges() {
  const count = Array.isArray(state.favoriteVessels) ? state.favoriteVessels.length : 0;
  const badge = document.getElementById("headerFavBadge");
  const btn = document.getElementById("btnHeaderFavs");
  if (badge) {
    badge.textContent = String(count);
    badge.classList.toggle("visible", count > 0);
  }
  if (btn) btn.classList.toggle("has-items", count > 0);
}

function toggleFavoriteVessel(vid, evt) {
  if (evt && typeof evt.stopPropagation === "function") evt.stopPropagation();
  const idx = state.favoriteVessels.indexOf(vid);
  if (idx >= 0) state.favoriteVessels.splice(idx, 1);
  else state.favoriteVessels.push(vid);
  const isFav = isVesselFavorite(vid);
  saveFavoriteVessels();
  updateFavoritesBadges();
  if (state.mainView === "catalog") {
    const l = state.lang;
    document.querySelectorAll(`.fav-heart-btn[data-fav-vid="${vid}"]`).forEach(btn => {
      btn.classList.toggle("active", isFav);
      btn.title = l === "it"
        ? (isFav ? "Rimuovi dai preferiti" : "Salva nei preferiti")
        : (isFav ? "Remove from favorites" : "Save to favorites");
      const svg = btn.querySelector("svg");
      if (svg) svg.setAttribute("fill", isFav ? "currentColor" : "none");
    });
  }
  if (state.mainView === "profile") renderProfileView();
}

function loadSubmittedRequests() {
  try {
    const raw = localStorage.getItem(REQUEST_STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) state.submittedRequests = parsed;
    }
  } catch {}
}

function saveSubmittedRequests() {
  try {
    localStorage.setItem(REQUEST_STORAGE_KEY, JSON.stringify(state.submittedRequests));
  } catch {}
}

function updateProfileBadge() {
  const badge = document.getElementById("profileReqBadge");
  if (!badge) return;
  const count = state.submittedRequests.length;
  badge.textContent = String(count);
  badge.classList.toggle("visible", count > 0);
}

function openProfileView(focusSection) {
  if (state.mainView === "profile" && !focusSection) {
    goStepBack();
    return;
  }
  if (state.mainView !== "profile") state.prevViewBeforeProfile = state.mainView;
  switchMainView("profile");
  requestAnimationFrame(() => {
    const pv = document.querySelector("#viewProfile .profile-view");
    if (pv) pv.scrollTop = 0;
    if (focusSection === "favorites" && window.innerWidth <= 1024) {
      const el = document.getElementById("profileFavoritesCard");
      if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
}

function returnToMarketplaceAfterSubmit(skipReset) {
  const modal = document.getElementById("checkoutModal");
  if (modal) modal.classList.remove("open");
  state.customVesselMode = false;
  if (!skipReset) resetVesselConfigState("serum_250");
  switchMainView("catalog");
}

function cancelSubmittedRequest(reqId) {
  state.submittedRequests = state.submittedRequests.filter(r => r.id !== reqId);
  saveSubmittedRequests();
  updateProfileBadge();
  renderProfileView();
}

function renderProfileView() {
  const host = document.getElementById("profilePortalBody");
  if (!host) return;
  const l = state.lang;
  const reqs = state.submittedRequests;
  const favIds = Array.isArray(state.favoriteVessels) ? state.favoriteVessels : [];
  const favVessels = favIds.map(id => VESSELS.find(v => v.id === id)).filter(Boolean);

  const favsHtml = favVessels.length === 0
    ? `
      <div style="text-align:center; padding:26px 18px; border:1.5px dashed var(--border); border-radius:16px; background:#F8F9FA;">
        <div style="font-size:14px; font-weight:700; color:var(--ink);">${l === "it" ? "Nessun contenitore nei preferiti" : "No favorite containers yet"}</div>
        <p style="font-size:12px; color:var(--slate); margin-top:5px;">
          ${l === "it"
            ? "Clicca sull'icona del cuore sui contenitori del Marketplace per salvarli rapidamente in questa sezione."
            : "Click the heart icon on any Marketplace container to save it here for quick access."}
        </p>
      </div>
    `
    : `
      <div class="fav-prof-grid">
        ${favVessels.map(v => `
          <div class="fav-prof-card" onclick="selectVesselFromMarketplace('${v.id}')" style="cursor:pointer;">
            <div class="fav-prof-stage">
              <img class="cat-real-img" src="${getVesselRealisticThumb(v)}" alt="${l === "it" ? v.it : v.en}">
            </div>
            <div class="cat-meta-body">
              <div class="cat-title-row">
                <div class="cat-meta-title">${l === "it" ? v.it : v.en}</div>
                <button type="button" class="fav-heart-btn active" data-fav-vid="${v.id}" onclick="toggleFavoriteVessel('${v.id}', event)" title="${l === "it" ? "Rimuovi dai preferiti" : "Remove from favorites"}" aria-label="${l === "it" ? "Rimuovi dai preferiti" : "Remove from favorites"}">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
                </button>
              </div>
              ${renderVesselTwoColSpecs(v, l)}
              <div class="cat-meta-footer">
                <button type="button" class="cat-select-btn" onclick="event.stopPropagation(); selectVesselFromMarketplace('${v.id}')">
                  ${l === "it" ? "Seleziona" : "Select"}
                </button>
              </div>
            </div>
          </div>
        `).join("")}
      </div>
    `;

  const reqsHtml = reqs.length === 0
    ? `
      <div style="text-align:center; padding:32px 18px; border:1.5px dashed var(--border); border-radius:16px; background:#F8F9FA;">
        <div style="font-size:14px; font-weight:700; color:var(--ink);">${l === "it" ? "Nessuna richiesta inviata al momento" : "No requests submitted yet"}</div>
        <p style="font-size:12px; color:var(--slate); margin-top:5px;">
          ${l === "it"
            ? "Configura un contenitore nello Studio 3D, scegli i fornitori in Filiera e clicca su Invia richiesta per monitorare qui lo stato di accettazione."
            : "Configure a container in the 3D Studio, pick your suppliers in Supply Chain and click Send request to monitor acceptance status here."}
        </p>
      </div>
    `
    : reqs.map(req => `
      <div class="req-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; flex-wrap:wrap; border-bottom:1px solid var(--border-light); padding-bottom:11px;">
          <div style="flex:1; min-width:240px;">
            <div style="font-size:11.5px; font-weight:600; color:var(--slate); margin-bottom:4px;">${l === "it" ? "Inviata il" : "Sent on"} ${req.createdAt}</div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span style="font-family:var(--mono); font-size:11px; font-weight:800; color:var(--crimson);">${req.id}</span>
            </div>
            <div style="font-size:15.5px; font-weight:800; color:var(--ink); margin-top:7px;">${l === "it" ? req.vesselIt : req.vesselEn}</div>
            <div class="req-spec-line">${req.summaryLine}</div>
          </div>
          <div style="text-align:right; flex-shrink:0;">
            <div style="font-family:var(--mono); font-size:17px; font-weight:800; color:var(--ink);">${formatEuro(req.totalCost)}</div>
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:6px;">
          <div style="font-size:10px; font-weight:800; color:var(--slate); letter-spacing:0.08em;">${l === "it" ? `FORNITORI IN ATTESA DI RISPOSTA (${req.suppliers.length})` : `SUPPLIERS AWAITING RESPONSE (${req.suppliers.length})`}</div>
          ${req.suppliers.map(sup => `
            <div class="req-sup-row">
              <div>
                <div style="font-weight:800; color:var(--ink);">${sup.name}</div>
                <div style="font-size:11px; color:var(--slate);">${l === "it" ? sup.roleIt : sup.roleEn} · ${sup.spec}</div>
              </div>
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                <span class="mono" style="font-weight:800; color:var(--ink);">€${sup.cost}</span>
                <span class="req-deadline-pill">${l === "it" ? `Limite accettazione: ${req.acceptDays} giorni` : `Acceptance limit: ${req.acceptDays} days`}</span>
                <span class="req-status-pill">${l === "it" ? "IN ATTESA" : "PENDING"}</span>
              </div>
            </div>
          `).join("")}
        </div>

        <div class="req-card-footer">
          <div class="req-overall-status-box">
            <span class="req-overall-status-dot"></span>
            <span>${l === "it" ? "In attesa di accettazione" : "Awaiting acceptance"}</span>
          </div>
          <button type="button" class="req-cancel-btn" onclick="cancelSubmittedRequest('${req.id}')">
            ${l === "it" ? "Annulla richiesta" : "Cancel request"}
          </button>
        </div>
      </div>
    `).join("");

  const greenVerifiedSeal = `<svg class="verified-seal" width="18" height="18" viewBox="0 0 24 24" aria-label="${l === "it" ? "Account verificato" : "Verified account"}"><path fill="#147A3B" d="M12 1.5l2.27 1.78 2.84-.29 1.08 2.64 2.52 1.38-.52 2.8 1.58 2.38-1.88 2.16.18 2.85-2.74.93-1.52 2.42-2.81-.68L12 22.5l-2.27-1.78-2.84.29-1.08-2.64-2.52-1.38.52-2.8-1.58-2.38 1.88-2.16-.18-2.85 2.74-.93 1.52-2.42 2.81.68L12 1.5z"/><path fill="#FFFFFF" d="M10.4 15.6l-3.3-3.3 1.4-1.4 1.9 1.9 4.9-4.9 1.4 1.4-6.3 6.3z"/></svg>`;

  host.innerHTML = `
    <div class="brown-hdr-bar">
      <div>
        <h1 class="brown-hdr-title">${l === "it" ? "Area Personale" : "Personal Area"}</h1>
      </div>
      <button class="cta-btn white" style="width:auto; padding:0 18px; height:38px;" onclick="returnToMarketplaceAfterSubmit(true)">
        ${l === "it" ? "Torna al Marketplace" : "Back to Marketplace"}
      </button>
    </div>

    <div class="profile-grid">
      <div class="profile-card">
        <div style="display:flex; align-items:center; gap:12px;">
          <div class="profile-avatar-lg">TL</div>
          <div>
            <div style="display:flex; align-items:center; gap:6px; font-size:17px; font-weight:800; color:var(--ink);">
              <span>Thomas Lutaj</span>
              ${greenVerifiedSeal}
            </div>
            <div style="font-size:12px; color:var(--slate); margin-top:2px;">${l === "it" ? "Brand · Account Demo" : "Brand · Demo Account"}</div>
          </div>
        </div>

        <div style="margin-top:4px;">
          <div class="profile-info-row">
            <span style="color:var(--slate); font-weight:600;">${l === "it" ? "Email" : "Email"}</span>
            <strong style="font-family:var(--mono); font-size:11px;">tommylutaj@gmail.com</strong>
          </div>
          <div class="profile-info-row">
            <span style="color:var(--slate); font-weight:600;">${l === "it" ? "Organizzazione" : "Organization"}</span>
            <strong>VesselCove Brand Lab</strong>
          </div>
          <div class="profile-info-row">
            <span style="color:var(--slate); font-weight:600;">${l === "it" ? "Sede" : "Location"}</span>
            <strong>Milano</strong>
          </div>
          <div class="profile-info-row">
            <span style="color:var(--slate); font-weight:600;">${l === "it" ? "Piano Brand" : "Brand Plan"}</span>
            <strong style="color:var(--green);">${l === "it" ? "Gratuito" : "Free"}</strong>
          </div>
        </div>

        <div style="border-top:1px solid var(--border-light); padding-top:12px; display:flex; justify-content:space-between; align-items:center; gap:10px;">
          <div>
            <div style="font-size:11px; font-weight:800; color:var(--ink);">${l === "it" ? "LINGUA INTERFACCIA" : "INTERFACE LANGUAGE"}</div>
            <div style="font-size:10.5px; color:var(--slate);">${l === "it" ? "Cambia lingua del portale" : "Switch portal language"}</div>
          </div>
          <div class="lang-toggle">
            <button class="lang-b ${l === "it" ? "active" : ""}" id="btnLangIT" onclick="setLanguage('it')">IT</button>
            <button class="lang-b ${l === "en" ? "active" : ""}" id="btnLangEN" onclick="setLanguage('en')">EN</button>
          </div>
        </div>
      </div>

      <div style="display:flex; flex-direction:column; gap:18px;">
        <div class="profile-card" id="profileFavoritesCard">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;">
            <div>
              <span style="font-family:var(--mono); font-size:10.5px; font-weight:800; color:var(--crimson);">${l === "it" ? "I TUOI PREFERITI" : "SAVED FAVORITES"}</span>
              <h2 style="font-size:18px; font-weight:800; color:var(--ink); margin-top:2px;">${l === "it" ? "Contenitori Preferiti" : "Favorite Containers"}</h2>
            </div>
            <span class="spec-tag">${favVessels.length} ${favVessels.length === 1 ? (l === "it" ? "SALVATO" : "SAVED") : (l === "it" ? "SALVATI" : "SAVED")}</span>
          </div>

          <p style="font-size:12px; color:var(--slate); line-height:1.4; margin:0;">
            ${l === "it"
              ? "Raccolta dei contenitori selezionati con l'icona cuore nel Marketplace."
              : "Collection of containers bookmarked with the heart icon in the Marketplace."}
          </p>

          ${favsHtml}
        </div>

        <div class="profile-card">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;">
            <div>
              <span style="font-family:var(--mono); font-size:10.5px; font-weight:800; color:var(--crimson);">${l === "it" ? "MONITORAGGIO FILIERA" : "SUPPLY CHAIN TRACKING"}</span>
              <h2 style="font-size:18px; font-weight:800; color:var(--ink); margin-top:2px;">${l === "it" ? "Richieste Inviate ai Fornitori" : "Requests Sent to Suppliers"}</h2>
            </div>
            <span class="spec-tag">${reqs.length} ${reqs.length === 1 ? (l === "it" ? "RICHIESTA" : "REQUEST") : (l === "it" ? "RICHIESTE" : "REQUESTS")}</span>
          </div>

          <p style="font-size:12px; color:var(--slate); line-height:1.4; margin:0;">
            ${l === "it"
              ? `Ogni fornitore dispone di ${ACCEPTANCE_DEADLINE_DAYS} giorni per accettare o rifiutare la lavorazione. Il pagamento verrà richiesto solo dopo la conferma di tutta la filiera.`
              : `Every supplier has ${ACCEPTANCE_DEADLINE_DAYS} days to accept or decline the order. Payment will be requested only after all suppliers confirm.`}
          </p>

          <div style="display:flex; flex-direction:column; gap:12px;">
            ${reqsHtml}
          </div>
        </div>
      </div>
    </div>
  `;
}

function setInspTab(n) {
  state.inspTab = n;
  for (let i = 1; i <= 3; i++) {
    document.getElementById("itab" + i).classList.toggle("active", i === n);
  }
  renderInspector();
}

function getHudCapabilityFlags() {
  const phys = evaluateLivePhysics();
  const pouchMode = isDoypack();
  const labelMode = isLabelMode();
  const serigMode = isSerigrafiaMode();
  const wrapActive = hasWrap();
  const canDragSleeve = wrapActive && !pouchMode && !serigMode;
  const canExplode = !phys.isNoCap && phys.neckMatch;
  const canHeatmap = wrapActive && !pouchMode && (state.wrapType === "sleeve" || state.wrapType === "label");
  return { phys, pouchMode, labelMode, serigMode, wrapActive, canDragSleeve, canExplode, canHeatmap };
}

// Mutually exclusive pointer tool ('orbit' | 'sleeve')
function setPointerTool(t) {
  const { canDragSleeve } = getHudCapabilityFlags();
  if (t === "sleeve" && !canDragSleeve) return;
  if (t !== "orbit" && t !== "sleeve") t = "orbit";
  state.pointerTool = t;
  document.getElementById("toolOrbit").classList.toggle("active", t === "orbit");
  document.getElementById("toolSleeve").classList.toggle("active", t === "sleeve");

  const tr = TXT[state.lang];
  const toastEl = document.getElementById("ui_drag_toast");
  if (toastEl) toastEl.textContent = getActiveDragToast(tr);
  if (state.inspTab === 2) renderInspector();
}

function toggle3DFlag(key) {
  const { phys, canHeatmap } = getHudCapabilityFlags();
  if (key === "exploded") {
    if (phys.isNoCap) {
      state.exploded = false;
      renderAllUI();
      return;
    }
    if (!phys.neckMatch) {
      state.exploded = true;
      renderAllUI();
      return;
    }
  }
  if (key === "heatmap" && !canHeatmap) {
    state.heatmap = false;
    renderAllUI();
    return;
  }
  state[key] = !state[key];
  if (key === "darkStudio") {
    document.getElementById("viewportStage").classList.toggle("dark-studio", state.darkStudio);
  }
  rebuild3DProduct();
  renderAllUI();
}

function updateBarcodePositionFromSlider(angleDeg, heightPct) {
  if (angleDeg !== null) {
    state.bcAngleDeg = Number(angleDeg);
    camSpherical.theta = (state.bcAngleDeg / 180) * Math.PI * 0.85;
  }
  if (heightPct !== null) {
    const bBounds = getSleeveBarcodeHeightBounds();
    state.bcHeightPct = Math.max(bBounds.minPct, Math.min(bBounds.maxPct, Number(heightPct)));
  }
  renderSleeveUVTexture();
  updateFastTelemetryUI();
}

function updateSleevePositionFromSlider(angleDeg, heightPct) {
  if (angleDeg !== null) {
    state.sleeveAngleDeg = Number(angleDeg);
    camSpherical.theta = 0.24 - (state.sleeveAngleDeg / 180) * Math.PI * 0.85;
  }
  if (heightPct !== null) {
    state.sleeveHeightPct = Number(heightPct);
    clampBarcodeToSleeve();
  }
  if (sleeveMesh && sleeveMesh.geometry) applyDynamicWrapMeshDeformation(sleeveMesh.geometry, getVessel());
  renderSleeveUVTexture();
  updateFastTelemetryUI();
}

function swapSupplier() {
  state.printerIdx = (state.printerIdx + 1) % PRINTER_POOL.length;
  renderAllUI();
}

function proceedToPillars() {
  const phys = evaluateLivePhysics();
  if (phys.status === "r") return;
  state.filieraStep = 1;
  state.selectedSuppliers = { container: 0 };
  switchMainView("pillars");
}

// ==================== HELPER RENDERERS (SHARED) ====================
function getVesselTypeLabel(v, l) {
  const map = {
    cyl_tall: l === "it" ? "Flacone Cilindrico" : "Cylindrical Bottle",
    square_soft: l === "it" ? "Flacone Quadro" : "Square Bottle",
    wine_bordeaux: l === "it" ? "Bottiglia" : "Bottle",
    jar_lux: l === "it" ? "Vaso" : "Jar",
    alu_can: l === "it" ? "Lattina" : "Can",
    doypack: "Doypack"
  };
  return map[v.shape] || (l === "it" ? v.badgeIt : v.badgeEn);
}

function renderVesselTwoColSpecs(v, l) {
  const k1 = l === "it" ? "Azienda" : "Company";
  const k2 = l === "it" ? "Misure" : "Dimensions";
  const k3 = l === "it" ? "Collo" : "Neck";
  const k4 = l === "it" ? "Tipologia" : "Type";
  const k5 = l === "it" ? "Quantità" : "Quantity";
  const k6 = l === "it" ? "Materiale" : "Material";
  return `
    <div class="vessel-specs-2col">
      <div class="vspec-col">
        <div class="vspec-row">
          <span class="vspec-k">${k1}</span>
          <span class="vspec-v">${v.vendor}</span>
        </div>
        <div class="vspec-row">
          <span class="vspec-k">${k2}</span>
          <span class="vspec-v">${l === "it" ? v.subIt : v.subEn}</span>
        </div>
        <div class="vspec-row">
          <span class="vspec-k">${k3}</span>
          <span class="vspec-v">${v.neck}</span>
        </div>
      </div>
      <div class="vspec-col">
        <div class="vspec-row">
          <span class="vspec-k">${k4}</span>
          <span class="vspec-v">${getVesselTypeLabel(v, l)}</span>
        </div>
        <div class="vspec-row">
          <span class="vspec-k">${k5}</span>
          <span class="vspec-v">${v.vol}</span>
        </div>
        <div class="vspec-row">
          <span class="vspec-k">${k6}</span>
          <span class="vspec-v">${l === "it" ? v.matIt : v.matEn}</span>
        </div>
      </div>
    </div>
  `;
}

function renderVesselSpecStack(v, l) {
  return renderVesselTwoColSpecs(v, l);
}

function renderVesselInfoPopover() {
  const pop = document.getElementById("vesselInfoPopover");
  const btn = document.getElementById("btnVesselInfo");
  if (!pop) return;
  const v = getVessel();
  const l = state.lang;
  pop.classList.toggle("open", !!state.infoPopoverOpen);
  if (btn) btn.classList.toggle("active", !!state.infoPopoverOpen);
  if (!state.infoPopoverOpen) return;
  pop.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px;">
      <div>
        <div style="font-size:10px; font-weight:800; letter-spacing:0.08em; color:var(--crimson); text-transform:uppercase;">${l === "it" ? "SCHEDA TECNICA CONTENITORE" : "CONTAINER TECHNICAL SPEC"}</div>
        <div style="font-size:14.5px; font-weight:800; color:var(--ink); margin-top:2px;">${l === "it" ? v.it : v.en}</div>
      </div>
      <button type="button" style="border:none; background:transparent; cursor:pointer; font-size:14px; color:var(--slate); font-weight:800;" onclick="toggleVesselInfoPopover(false)">✕</button>
    </div>
    ${renderVesselTwoColSpecs(v, l)}
  `;
}

function toggleVesselInfoPopover(forceVal) {
  state.infoPopoverOpen = (forceVal !== undefined) ? !!forceVal : !state.infoPopoverOpen;
  renderVesselInfoPopover();
}

function getVesselClosures(v) {
  if (!vesselHasClosureStep(v)) return [];
  let ids;
  if (v.shape === "jar_lux") ids = ["lid_58", "lid_bevel_58", "lid_double_58", "lid_dome_70", "lid_tall_70"];
  else if (v.shape === "wine_bordeaux") ids = ["cork_29", "stelvin_29", "pourer_29", "bartop_29", "pump_24", "cap_28"];
  else if (v.shape === "square_soft") ids = ["cap_28", "disctop_28", "fliptop_28", "pushpull_28", "pump_24", "spray_24"];
  else ids = ["pump_24", "pump_slim_24", "dropper_24", "spray_24", "fliptop_24", "cap_28", "disctop_28"];
  const items = ids.map(id => CLOSURES.find(c => c.id === id)).filter(Boolean);
  // Compatible closures first, incompatible closures last
  return items.sort((a, b) => (a.neck === v.neck ? 0 : 1) - (b.neck === v.neck ? 0 : 1));
}

function selectClosure(cid) {
  const v = getVessel();
  const nextId = (state.closureId === cid) ? "none" : cid;
  const c = CLOSURES.find(item => item.id === nextId) || CLOSURES[0];
  state.closureId = c.id;
  const isOk = (c.id === "none" || c.neck === v.neck);
  state.exploded = !isOk;
  if (v.shape === "wine_bordeaux") {
    clampAndSetZoom(isOk ? 6.75 : Math.max(camTargetRadius, 8.35), false);
  } else if (v.shape === "jar_lux") {
    clampAndSetZoom(isOk ? 4.85 : Math.max(camTargetRadius, 5.45), false);
  }
  state.selectedSuppliers = { container: 0 };
  state.filieraStep = 1;
  rebuild3DProduct();
  renderAllUI();
}

// ==================== RENDER ALL UI PANELS ====================
function renderAllUI() {
  const t = TXT[state.lang];
  const { phys, labelMode, canDragSleeve, canExplode, canHeatmap } = getHudCapabilityFlags();
  if (phys.isNoCap) state.exploded = false;
  else if (!phys.neckMatch) state.exploded = true;
  if (!canHeatmap) state.heatmap = false;
  if (state.pointerTool === "sleeve" && !canDragSleeve) state.pointerTool = "orbit";
  if (state.pointerTool !== "orbit" && state.pointerTool !== "sleeve") state.pointerTool = "orbit";

  document.getElementById("ui_nav_catalog").textContent = t.navCatalog;
  document.getElementById("ui_nav_studio").textContent = t.navStudio;
  document.getElementById("ui_nav_pillars").textContent = t.navPillars;

  const backBtn = document.getElementById("navBackBtn");
  if (backBtn) {
    backBtn.disabled = (state.mainView === "catalog");
    backBtn.title = t.backTitle;
  }

  const hasClosureTab = vesselHasClosureStep(getVessel());
  if (!hasClosureTab && state.inspTab === 1) state.inspTab = 2;
  const tabsBar = document.getElementById("inspectorTabs");
  if (tabsBar) tabsBar.classList.toggle("two-tabs", !hasClosureTab);
  const itab1 = document.getElementById("itab1");
  if (itab1) itab1.style.display = hasClosureTab ? "" : "none";
  const stepWord = state.lang === "it" ? "PASSO" : "STEP";
  const tn1 = document.getElementById("ui_tnum1");
  const tn2 = document.getElementById("ui_tnum2");
  const tn3 = document.getElementById("ui_tnum3");
  if (tn1) tn1.textContent = `${stepWord} 01`;
  if (tn2) tn2.textContent = hasClosureTab ? `${stepWord} 02` : `${stepWord} 01`;
  if (tn3) tn3.textContent = hasClosureTab ? `${stepWord} 03` : `${stepWord} 02`;

  document.getElementById("ui_itab1").textContent = t.itab1;
  document.getElementById("ui_itab2").textContent = t.itab2;
  document.getElementById("ui_itab3").textContent = t.itab3;
  for (let i = 1; i <= 3; i++) {
    document.getElementById("itab" + i).classList.toggle("active", state.inspTab === i);
  }

  const btnSl = document.getElementById("toolSleeve");
  if (btnSl) {
    btnSl.style.display = isDoypack() ? "none" : "";
    btnSl.disabled = !canDragSleeve;
    btnSl.classList.toggle("disabled", !canDragSleeve);
  }

  document.getElementById("ui_tool_orbit").textContent = t.toolOrbit;
  document.getElementById("ui_tool_sleeve").textContent = labelMode ? t.toolLabel : t.toolSleeve;
  document.getElementById("ui_btn_explode").textContent = (phys.isNoCap || phys.neckMatch) ? t.btnExplode : t.btnExplodeLocked;
  document.getElementById("ui_btn_heat").textContent = t.btnHeat;
  document.getElementById("ui_btn_wire").textContent = t.btnWire;
  document.getElementById("ui_drag_toast").textContent = getActiveDragToast(t);

  document.getElementById("toolOrbit").classList.toggle("active", state.pointerTool === "orbit");
  document.getElementById("toolSleeve").classList.toggle("active", state.pointerTool === "sleeve");

  const btnExpl = document.getElementById("btnExplode");
  btnExpl.classList.toggle("active", state.exploded);
  btnExpl.disabled = !canExplode;
  btnExpl.classList.toggle("disabled", !canExplode);

  const btnHeat = document.getElementById("btnHeatmap");
  btnHeat.classList.toggle("active", state.heatmap);
  btnHeat.disabled = !canHeatmap;
  btnHeat.classList.toggle("disabled", !canHeatmap);

  document.getElementById("btnWire").classList.toggle("active", state.wireframe);
  const btnDark = document.getElementById("btnDarkBg");
  if (btnDark) {
    btnDark.classList.toggle("active", state.darkStudio);
    btnDark.title = state.lang === "it" ? "Cambia sfondo studio" : "Toggle studio background";
  }
  const arLbl = document.getElementById("ui_btn_ar");
  if (arLbl) arLbl.textContent = state.lang === "it" ? "Vedi in AR" : "View in AR";
  const customBtn = document.getElementById("btnCustomVessel");
  if (customBtn) customBtn.textContent = state.lang === "it" ? "Continua con il mio contenitore" : "Continue with my container";
  updateProfileBadge();

  renderVesselInfoPopover();
  if (state.mainView === "studio" && state.customVesselMode) {
    renderCustomVesselView();
  } else if (state.mainView === "studio" && state.customGraphicMode) {
    renderCustomGraphicView();
  } else {
    renderInspector();
    updateFastTelemetryUI();
  }
  if (state.arModalOpen) toggleARModal(true);
  if (state.mainView === "catalog") renderCatalogView();
  if (state.mainView === "pillars") renderPillarsView();
  if (state.mainView === "profile") renderProfileView();
}

function renderInspector() {
  const l = state.lang;
  const v = getVessel();
  const cl = getClosure();
  const phys = evaluateLivePhysics();
  const box = document.getElementById("inspectorBody");
  const curInspKey = `${v.id}|${state.inspTab}|${state.wrapType}|${state.boxMode}|${l}`;
  const animCls = (state._lastInspKey === curInspKey) ? "" : " reveal-anim";
  state._lastInspKey = curInspKey;

  if (state.inspTab === 1 && vesselHasClosureStep(v)) {
    // STEP 01: CLOSURE ONLY (no Marketplace container card, no Material card, no CLASH text)
    const listClos = getVesselClosures(v);
    const closCards = listClos.map(item => {
      const isOk = (item.neck === v.neck);
      const isSel = (item.id === state.closureId);
      const cls = isSel ? (isOk ? "prod-item active" : "prod-item clash-active") : "prod-item";
      const tagText = isOk ? (item.neck + " ✓") : (item.neck + " ✕");
      return `
        <button class="${cls}" onclick="selectClosure('${item.id}')">
          <div>
            <div class="prod-title">${l === "it" ? item.it : item.en}</div>
            <div class="prod-meta">${item.vendor}</div>
          </div>
          <span class="spec-tag ${isOk ? "ok" : "clash"}">${tagText}</span>
        </button>
      `;
    }).join("");

    box.innerHTML = `
      <div class="sec-block${animCls}">
        <div class="sec-hdr">
          <span>${l === "it" ? "CHIUSURA" : "CLOSURE"}</span>
        </div>
        <div class="prod-list">${closCards}</div>
      </div>
    `;
  } else if (state.inspTab === 2) {
    const availSkins = getAvailableSkinsForWrap(state.wrapType);
    const skinPills = availSkins.map(s => {
      const swatchHtml = s.id === "neutral" && s.styleType === "neutral_clear"
        ? `<div style="width:22px; height:28px; border-radius:3px; border:1px dashed var(--slate); background:repeating-linear-gradient(45deg, #F8FAFC, #F8FAFC 4px, #E2E8F0 4px, #E2E8F0 8px); flex-shrink:0;"></div>`
        : `<div style="display:flex; flex-direction:column; width:22px; height:28px; border-radius:3px; overflow:hidden; border:1px solid var(--border); flex-shrink:0;">
            <span style="flex:2; background:${s.previewColors[0]};"></span>
            <span style="flex:1; background:${s.previewColors[1]};"></span>
            <span style="flex:1; background:${s.previewColors[2]};"></span>
          </div>`;
      const sTitle = s.id === "neutral"
        ? (s.styleType === "neutral_clear" ? (l === "it" ? "Neutra Trasparente" : "Clear Neutral") : (l === "it" ? "Bianca Senza Scritte" : "Blank White"))
        : `${s.brand} ${s.brandSub}`;
      return `
        <button class="prod-item ${s.id === state.skinId && hasWrap() ? "active" : ""}" onclick="selectSkin('${s.id}')">
          <div style="display:flex; align-items:center; gap:9px;">
            ${swatchHtml}
            <div>
              <div class="prod-title">${sTitle}</div>
              <div class="prod-meta">${l === "it" ? s.descIt : s.descEn}</div>
            </div>
          </div>
        </button>
      `;
    }).join("");

    const addCustomGraphicBtn = `
      <button class="cta-btn white" id="btnAddCustomGraphic" style="margin-top:8px; height:36px; font-size:11.5px; gap:6px;" onclick="openCustomGraphicStudio()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 5v14M5 12h14"/></svg>
        <span>${l === "it" ? "Aggiungi grafica" : "Add graphic"}</span>
      </button>
    `;

    if (isDoypack()) {
      const pouchPrintSwitchHtml = `
        <div class="sec-block" style="margin-bottom:2px;">
          <div class="sec-hdr">
            <span>${l === "it" ? "TIPO STAMPA DOYPACK" : "DOYPACK PRINT TECHNOLOGY"}</span>
          </div>
          <div class="grid-2">
            <button class="opt-pill ${hasWrap() && state.pouchPrintType === "flexo" ? "active" : ""}" onclick="setDoypackPrintType('flexo')">
              ${l === "it" ? "Stampa Flessografica" : "Flexographic Print"}
              <small>${l === "it" ? "Cilindri alta definizione" : "High-def flexo cylinders"}</small>
            </button>
            <button class="opt-pill ${hasWrap() && state.pouchPrintType === "digital" ? "active" : ""}" onclick="setDoypackPrintType('digital')">
              ${l === "it" ? "Stampa Digitale" : "Digital Print"}
              <small>${l === "it" ? "Zero avviamenti / pre-serie" : "Zero plate setup / pre-series"}</small>
            </button>
          </div>
        </div>
      `;

      if (!hasWrap()) {
        box.innerHTML = `
          ${pouchPrintSwitchHtml}
          <div class="sec-block${animCls}" style="font-size:11.5px; color:var(--slate); background:var(--bg-subtle); border:1px solid var(--border); border-radius:6px; padding:11px;">
            ${l === "it"
              ? "Busta neutra senza stampa. Scegli Stampa Flessografica o Stampa Digitale qui sopra per aprire le opzioni grafiche (riclicca lo stesso tasto per rimuovere)."
              : "Bare neutral pouch. Select Flexographic Print or Digital Print above to open graphic options (re-click to remove)."}
          </div>
        `;
        return;
      }

      box.innerHTML = `
        ${pouchPrintSwitchHtml}

        <div class="sec-block${animCls}">
          <div class="sec-hdr"><span>${l === "it" ? "GRAFICHE BRAND" : "BRAND GRAPHICS"}</span></div>
          <div class="prod-list">${skinPills}</div>
          ${addCustomGraphicBtn}
        </div>
      `;
      return;
    }

    // RIGID CONTAINERS: SLEEVE 360° vs ADHESIVE LABEL (+ SERIGRAFIA 360° ONLY FOR CANS!)
    const isCanVessel = v.shape === "alu_can";
    const serigActive = isSerigrafiaMode();

    const wrapSwitchHtml = `
      <div class="sec-block" style="margin-bottom:2px;">
        <div class="sec-hdr">
          <span>${l === "it" ? "TIPO RIVESTIMENTO PRIMARIO" : "PRIMARY DECORATION TYPE"}</span>
        </div>
        <div class="${isCanVessel ? "grid-3" : "grid-2"}">
          <button class="opt-pill ${state.wrapType === "sleeve" ? "active" : ""}" onclick="setWrapType('sleeve')">
            Sleeve 360°
            <small>${l === "it" ? "Termoretratta attorno" : "Heat-shrunk around"}</small>
          </button>
          <button class="opt-pill ${state.wrapType === "label" ? "active" : ""}" onclick="setWrapType('label')">
            ${l === "it" ? "Etichetta Adesiva" : "Adhesive Label"}
            <small>${l === "it" ? "Incollata sopra" : "Glued on surface"}</small>
          </button>
          ${isCanVessel ? `
            <button class="opt-pill ${serigActive ? "active" : ""}" onclick="setWrapType('serigrafia')">
              ${l === "it" ? "Serigrafia" : "Silk-Screen"}
              <small>${l === "it" ? "Diretta su lattina" : "Direct 360° ink"}</small>
            </button>
          ` : ""}
        </div>
      </div>
    `;

    if (!hasWrap()) {
      box.innerHTML = `
        ${wrapSwitchHtml}
        <div class="sec-block${animCls}" style="font-size:11.5px; color:var(--slate); background:var(--bg-subtle); border:1px solid var(--border); border-radius:6px; padding:11px;">
          ${l === "it"
            ? "Nessun rivestimento applicato al contenitore. Seleziona un'opzione qui sopra per aggiungerlo al modello 3D (clicca di nuovo sullo stesso tasto per rimuoverlo)."
            : "No wrap applied to container. Select an option above to add it to the 3D model (re-click to remove)."}
        </div>
      `;
      return;
    }

    if (serigActive) {
      const inkPills = SERIGRAFIA_INKS.map(ik => `
        <button class="opt-pill ${ik.id === state.serigrafiaInkId ? "active" : ""}" onclick="state.serigrafiaInkId='${ik.id}'; renderSleeveUVTexture(); renderAllUI();">
          ${ik.name}
          <small>${l === "it" ? ik.descIt : ik.descEn}</small>
        </button>
      `).join("");

      box.innerHTML = `
        ${wrapSwitchHtml}
        <div class="sec-block${animCls}">
          <div class="sec-hdr"><span>${l === "it" ? "INCHIOSTRI SERIGRAFIA DIRETTA SU LATTINA" : "DIRECT-TO-CAN SCREEN INKS"}</span></div>
          <div class="grid-2">${inkPills}</div>
        </div>

        <div class="sec-block${animCls}">
          <div class="sec-hdr"><span>${l === "it" ? "GRAFICHE BRAND" : "BRAND GRAPHICS"}</span></div>
          <div class="prod-list">${skinPills}</div>
          ${addCustomGraphicBtn}
        </div>
      `;
      return;
    }

    if (isLabelMode()) {
      const labelPaperPills = LABEL_PAPERS.map(p => `
        <button class="opt-pill ${p.id === state.labelMatId ? "active" : ""}" onclick="state.labelMatId='${p.id}'; rebuild3DProduct(); renderAllUI();">
          ${p.name}
          <small>${l === "it" ? p.descIt : p.descEn}</small>
        </button>
      `).join("");

      box.innerHTML = `
        ${wrapSwitchHtml}

        <div class="sec-block${animCls}">
          <div class="sec-hdr"><span>${l === "it" ? "CARTA E FILM ADESIVO ETICHETTA" : "ADHESIVE LABEL SUBSTRATE"}</span></div>
          <div class="grid-2">${labelPaperPills}</div>
        </div>

        <div class="sec-block${animCls}">
          <div class="sec-hdr"><span>${l === "it" ? "GRAFICHE BRAND" : "BRAND GRAPHICS"}</span></div>
          <div class="prod-list">${skinPills}</div>
          ${addCustomGraphicBtn}
        </div>
      `;
      return;
    }

    // SHRINK SLEEVE 360° MODE
    const filmPills = FILMS.map(f => `
      <button class="opt-pill ${f.id === state.filmId ? "active" : ""}" onclick="state.filmId='${f.id}'; rebuild3DProduct(); renderAllUI();">
        ${f.name}
        <small>${l === "it" ? f.descIt : f.descEn}</small>
      </button>
    `).join("");

    box.innerHTML = `
      ${wrapSwitchHtml}
      <div class="sec-block${animCls}">
        <div class="sec-hdr"><span>${l === "it" ? "MATERIALE FILM TERMORETRAIBILE" : "SHRINK SLEEVE FILM MATERIAL"}</span></div>
        <div class="grid-2">${filmPills}</div>
      </div>
      <div class="sec-block${animCls}">
        <div class="sec-hdr"><span>${l === "it" ? "GRAFICHE BRAND" : "BRAND GRAPHICS"}</span></div>
        <div class="prod-list">${skinPills}</div>
        ${addCustomGraphicBtn}
      </div>
    `;
  } else {
    // PACKAGING STEP: BOX CONFIGURATOR HxLxP (no "1./2./3.", no val-pills, no "(Solo Flaconi Plastica)", no "Astuccio", no "&")
    const plasticAllowed = isPlasticBottle(v);
    const isBulk = plasticAllowed && state.boxMode === "bulk";
    const qtys = [
      { q: 1, sub: "1×1" },
      { q: 2, sub: "2×1" },
      { q: 3, sub: "3×1" },
      { q: 6, sub: "3×2" },
      { q: 12, sub: "4×3" }
    ];
    const qtyButtons = qtys.map(item => `
      <button class="qty-btn ${!isBulk && state.boxQty === item.q ? "active" : ""}" onclick="state.boxMode='grid'; state.boxQty=${item.q}; renderAllUI();">
        ${item.q} pz
        <small>${item.sub}</small>
      </button>
    `).join("");

    const bulkQtys = [50, 100, 150, 200];
    const bulkHtml = !plasticAllowed ? "" : `
      <div style="margin-top:6px;">
        <div style="font-size:10px; font-weight:800; color:var(--slate); margin-bottom:5px; text-transform:uppercase; letter-spacing:0.06em;">
          ${l === "it" ? "Oppure sparsi nello scatolone" : "Or loose bulk carton"}
        </div>
        <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:5px;">
          ${bulkQtys.map(bq => `
            <button class="qty-btn ${isBulk && state.bulkQty === bq ? "active" : ""}" onclick="state.boxMode='bulk'; state.bulkQty=${bq}; renderAllUI();">
              ${bq} pz
              <small>${l === "it" ? "Sparsi" : "Loose"}</small>
            </button>
          `).join("")}
        </div>
      </div>
    `;

    const boardBlockHtml = isBulk ? "" : `
      <div class="sec-block${animCls}">
        <div class="sec-hdr"><span>${l === "it" ? "SPESSORE CARTONE E ALVEARE" : "BOARD GRADE AND PARTITION"}</span></div>
        <div class="grid-2">
          <button class="opt-pill ${state.boxBoard === "teso" ? "active" : ""}" onclick="state.boxBoard='teso'; renderAllUI();">
            ${l === "it" ? "Cartoncino Teso 350g" : "Solid Board 350g"}
            <small>+2 mm ${l === "it" ? "tolleranza" : "tolerance"}</small>
          </button>
          <button class="opt-pill ${state.boxBoard === "eflute" ? "active" : ""}" onclick="state.boxBoard='eflute'; renderAllUI();">
            ${l === "it" ? "Microonda E-Flute" : "E-Flute Corrugated"}
            <small>+6 mm ${l === "it" ? "rinforzato" : "heavy duty"}</small>
          </button>
        </div>
        <button class="opt-pill ${state.boxDivider ? "active" : ""}" style="width:100%; margin-top:2px;" onclick="state.boxDivider=!state.boxDivider; renderAllUI();">
          ${l === "it" ? "Inserisci Alveare Divisorio Interno" : "Add Internal Protective Divider"}
          <small>${l === "it" ? "+4 mm ingombro · Protezione antiurto" : "+4 mm clearance · Impact protection"}</small>
        </button>
      </div>
    `;

    box.innerHTML = `
      <div class="sec-block${animCls}">
        <div class="sec-hdr">
          <span>${l === "it" ? "ORDINATI PER SCATOLA" : "ORDERED PER BOX"}</span>
        </div>
        <div class="qty-grid">${qtyButtons}</div>
        ${bulkHtml}
      </div>

      ${boardBlockHtml}

      <div class="sec-block${animCls}">
        <div class="sec-hdr">
          <span>${isBulk
            ? (l === "it" ? "SCHEMA SCATOLONE E QUOTE H×L×P" : "MASTER CARTON AND H×W×D")
            : (l === "it" ? "SCHEMA IN PIANTA E QUOTE H×L×P" : "TOP-DOWN PACK LAYOUT AND H×W×D")}</span>
        </div>
        <div class="box-preview-card" id="boxSvgContainer"></div>
      </div>

      <div class="diag-card weight-red">
        <div class="diag-card-top">
          <span class="diag-card-k">${l === "it" ? "PESO LORDO STIMATO" : "ESTIMATED GROSS WEIGHT"}</span>
          <span class="diag-card-v" style="color:var(--crimson);">${(phys.grossWeightG / 1000).toFixed(2)} kg</span>
        </div>
        <div class="diag-card-s">${isBulk
          ? (l === "it"
              ? `Scatolone da ${phys.packQty} pz sparsi alla rinfusa (${phys.cartonH} × ${phys.cartonW} × ${phys.cartonD} mm).`
              : `Master carton with ${phys.packQty} loose pcs (${phys.cartonH} × ${phys.cartonW} × ${phys.cartonD} mm).`)
          : (l === "it"
              ? `Contiene ${phys.packQty}× ${v.it} in matrice ${phys.layout.cols}×${phys.layout.rows} (${phys.cartonH} × ${phys.cartonW} × ${phys.cartonD} mm).`
              : `Holds ${phys.packQty}× ${v.en} in ${phys.layout.cols}×${phys.layout.rows} grid (${phys.cartonH} × ${phys.cartonW} × ${phys.cartonD} mm).`)}</div>
      </div>
    `;
    setTimeout(renderMultiPackBoxSVG, 10);
  }
}

function renderMultiPackBoxSVG() {
  const wrap = document.getElementById("boxSvgContainer");
  if (!wrap) return;
  const v = getVessel();
  const l = state.lang;
  const phys = evaluateLivePhysics();

  if (phys.isBulk) {
    const ox = 66, oy = 24, boxW = 194, boxH = 116;
    wrap.innerHTML = `
      <svg width="100%" height="168" viewBox="0 0 308 168">
        <rect x="${ox}" y="${oy}" width="${boxW}" height="${boxH}" rx="4" fill="#EDE8DF" stroke="#121110" stroke-width="2.2"/>
        <rect x="${ox + 6}" y="${oy + 6}" width="${boxW - 12}" height="${boxH - 12}" rx="2" fill="none" stroke="#8C857C" stroke-width="1" stroke-dasharray="4 3"/>
        <text x="${ox + boxW / 2}" y="${oy + 44}" text-anchor="middle" font-size="10.5" font-weight="800" fill="#121110">${l === "it" ? "PRODOTTI SPARSI" : "LOOSE BULK"}</text>
        <text x="${ox + boxW / 2}" y="${oy + 58}" text-anchor="middle" font-size="10.5" font-weight="800" fill="#121110">${l === "it" ? "NELLO SCATOLONE" : "IN MASTER CARTON"}</text>
        <text x="${ox + boxW / 2}" y="${oy + 80}" text-anchor="middle" font-size="11" font-weight="700" fill="#C2180E">${phys.packQty} ${l === "it" ? "pezzi alla rinfusa" : "loose units"}</text>
        <text x="${ox + boxW / 2}" y="${oy - 6}" text-anchor="middle" font-size="10.5" font-weight="800" fill="#C2180E">L ${phys.cartonW} mm</text>
        <text x="${ox - 8}" y="${oy + boxH / 2 + 4}" text-anchor="end" font-size="10.5" font-weight="800" fill="#121110">P ${phys.cartonD} mm</text>
        <text x="${ox + boxW / 2}" y="${oy + boxH + 15}" text-anchor="middle" font-size="10" font-weight="700" fill="#69635D">H scatolone: ${phys.cartonH} mm · ${phys.packQty} unità</text>
      </svg>
    `;
    return;
  }

  const { cols, rows } = phys.layout;
  const padX = 24, padY = 20;
  const availW = 260, availH = 128;
  const wallPad = 3;
  const cellW = Math.min(46, (availW - wallPad * 2) / cols);
  const cellH = Math.min(38, (availH - wallPad * 2) / rows);
  const boxW = cols * cellW + wallPad * 2;
  const boxH = rows * cellH + wallPad * 2;
  const ox = padX + (availW - boxW) / 2;
  const oy = padY + (availH - boxH) / 2;

  let shapesSvg = "";
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const cx = ox + wallPad + c * cellW + cellW / 2;
      const cy = oy + wallPad + r * cellH + cellH / 2;
      if (v.shape === "doypack") {
        shapesSvg += `<rect x="${cx - cellW * 0.47}" y="${cy - cellH * 0.30}" width="${cellW * 0.94}" height="${cellH * 0.60}" rx="6" fill="#F3EFE6" stroke="#261811" stroke-width="1.4"/>`;
      } else if (v.shape === "square_soft") {
        shapesSvg += `<rect x="${cx - cellW * 0.45}" y="${cy - cellH * 0.44}" width="${cellW * 0.90}" height="${cellH * 0.88}" rx="4" fill="#F3EFE6" stroke="#261811" stroke-width="1.4"/>`;
      } else {
        const rad = Math.min(cellW, cellH) * 0.465;
        shapesSvg += `<circle cx="${cx}" cy="${cy}" r="${rad}" fill="#F3EFE6" stroke="#261811" stroke-width="1.4"/>`;
      }
    }
  }
  if (state.boxDivider && (cols > 1 || rows > 1)) {
    for (let c = 1; c < cols; c++) {
      const lx = ox + wallPad + c * cellW;
      shapesSvg += `<line x1="${lx}" y1="${oy + 2}" x2="${lx}" y2="${oy + boxH - 2}" stroke="#C2180E" stroke-width="1.2" stroke-dasharray="3 2"/>`;
    }
    for (let r = 1; r < rows; r++) {
      const ly = oy + wallPad + r * cellH;
      shapesSvg += `<line x1="${ox + 2}" y1="${ly}" x2="${ox + boxW - 2}" y2="${ly}" stroke="#C2180E" stroke-width="1.2" stroke-dasharray="3 2"/>`;
    }
  }

  wrap.innerHTML = `
    <svg width="100%" height="168" viewBox="0 0 308 168">
      <rect x="${ox}" y="${oy}" width="${boxW}" height="${boxH}" rx="2.5" fill="${state.boxBoard === "eflute" ? "#EDE8DF" : "#FAF8F4"}" stroke="#121110" stroke-width="2"/>
      ${shapesSvg}
      <text x="${ox + boxW / 2}" y="${oy - 6}" text-anchor="middle" font-size="10.5" font-weight="800" fill="#C2180E">L ${phys.cartonW} mm</text>
      <text x="${ox - 8}" y="${oy + boxH / 2 + 4}" text-anchor="end" font-size="10.5" font-weight="800" fill="#121110">P ${phys.cartonD}</text>
      <text x="${ox + boxW / 2}" y="${oy + boxH + 15}" text-anchor="middle" font-size="10" font-weight="700" fill="#69635D">H scatola: ${phys.cartonH} mm · ${phys.packQty} unità</text>
    </svg>
  `;
}

function formatEuro(val) {
  return "€" + val.toLocaleString("en-US");
}

const VESSEL_ALLOWED_FILL_MAP = {
  alu_can: [],
  wine_bordeaux: ["Liquidi"],
  cyl_tall: ["Liquidi"],
  square_soft: ["Liquidi", "Polveri"],
  jar_lux: ["Polveri", "Capsule", "Pillole"],
  doypack: ["Polveri", "Capsule", "Pillole"]
};

function isFillingPossibleForState(v) {
  const vessel = v || getVessel();
  if (vessel.shape === "alu_can") return false;
  if (isPlasticBottle(vessel) && state.boxMode === "bulk") return false;
  if (vessel.shape === "doypack") return true;
  return state.closureId !== "none";
}

function getAllowedFillTypes(v) {
  const vessel = v || getVessel();
  const ids = VESSEL_ALLOWED_FILL_MAP[vessel.shape] || [];
  return FILL_TYPES.filter(ft => ids.includes(ft.id));
}

function ensureValidCopackerFillType(v) {
  const vessel = v || getVessel();
  const allowed = getAllowedFillTypes(vessel);
  if (allowed.length === 0 || !isFillingPossibleForState(vessel)) {
    state.copackerFilling = false;
    return allowed;
  }
  if (!allowed.some(ft => ft.id === state.copackerFillType)) {
    state.copackerFillType = allowed[0].id;
  }
  return allowed;
}

function getCopackerFillCost(v) {
  const vessel = v || getVessel();
  const allowed = ensureValidCopackerFillType(vessel);
  if (!state.copackerFilling || !isFillingPossibleForState(vessel) || allowed.length === 0) return 0;
  const fObj = allowed.find(f => f.id === state.copackerFillType) || allowed[0];
  return fObj.cost;
}

function selectStepSupplier(stepKey, idx) {
  state.selectedSuppliers[stepKey] = idx;
  const listEl = document.getElementById("activeSupplierList");
  if (listEl) {
    const l = state.lang;
    const phys = evaluateLivePhysics();
    const chain = getActiveSupplyChain(phys);
    const step = chain.steps.find(s => s.key === stepKey);
    [...listEl.querySelectorAll(".supplier-rich-opt")].forEach((btn, bIdx) => {
      const isSel = bIdx === idx;
      btn.classList.toggle("selected", isSel);
      const tag = btn.querySelector(".sup-sel-tag");
      if (tag) {
        tag.className = "spec-tag sup-sel-tag" + (isSel ? " ok" : "");
        tag.textContent = isSel ? (l === "it" ? "SELEZIONATO ✓" : "SELECTED ✓") : (l === "it" ? "SELEZIONA →" : "SELECT →");
      }
    });
    const hdrBadge = document.getElementById("filieraStepStatusBadge");
    if (hdrBadge) {
      hdrBadge.className = "spec-tag ok";
      hdrBadge.textContent = l === "it" ? "AZIENDA SELEZIONATA ✓" : "SUPPLIER SELECTED ✓";
    }
    const nextBtn = document.getElementById("btnFilieraNext");
    if (nextBtn) nextBtn.disabled = false;
    const topTot = document.getElementById("filieraTopTotal");
    if (topTot && step) topTot.textContent = formatEuro(chain.totalCost);
    return;
  }
  renderPillarsView();
}

function toggleCopackerFilling() {
  const vessel = getVessel();
  const allowed = ensureValidCopackerFillType(vessel);
  if (!isFillingPossibleForState(vessel) || allowed.length === 0) return;
  state.copackerFilling = !state.copackerFilling;
  renderPillarsView();
  updateFastTelemetryUI();
}

function setCopackerFillMode(enabled) {
  const vessel = getVessel();
  const allowed = ensureValidCopackerFillType(vessel);
  if (!isFillingPossibleForState(vessel) || allowed.length === 0) {
    state.copackerFilling = false;
  } else {
    state.copackerFilling = !!enabled;
  }
  renderPillarsView();
  updateFastTelemetryUI();
}

function setCopackerFillType(ft) {
  const vessel = getVessel();
  if (!isFillingPossibleForState(vessel)) return;
  const allowed = getAllowedFillTypes(vessel);
  if (!allowed.some(item => item.id === ft)) return;
  state.copackerFillType = ft;
  state.copackerFilling = true;
  renderPillarsView();
  updateFastTelemetryUI();
}

function getFilieraMaxUnlocked(steps) {
  let maxStep = 1;
  for (let i = 0; i < steps.length; i++) {
    const s = steps[i];
    if (s.lockedFixed || state.selectedSuppliers[s.key] !== undefined) {
      maxStep = i + 2;
    } else {
      break;
    }
  }
  return Math.min(steps.length + 1, maxStep);
}

function nextFilieraStep() {
  const phys = evaluateLivePhysics();
  const steps = buildSupplyChainSteps(phys);
  const totalSteps = steps.length + 1;
  const maxUnlocked = getFilieraMaxUnlocked(steps);
  if (state.filieraStep < Math.min(totalSteps, maxUnlocked)) {
    state.filieraStep += 1;
    renderPillarsView();
    syncBrowserHistory(false);
    if (window.scrollY !== 0) window.scrollTo(0, 0);
  }
}

function prevFilieraStep() {
  if (state.filieraStep > 1) {
    const newCur = state.filieraStep - 1;
    const phys = evaluateLivePhysics();
    const steps = buildSupplyChainSteps(phys);
    state.copackerFilling = false;
    for (let i = Math.max(0, newCur - 1); i < steps.length; i++) {
      if (!steps[i].lockedFixed) delete state.selectedSuppliers[steps[i].key];
    }
    state.filieraStep = newCur;
    renderPillarsView();
    updateFastTelemetryUI();
    syncBrowserHistory(false);
    if (window.scrollY !== 0) window.scrollTo(0, 0);
  }
}

// Build sequential selectable supply-chain steps & active companies from live 3D config
function buildSupplyChainSteps(phys) {
  const l = state.lang;
  const v = getVessel();
  const cl = getClosure();
  const fm = getFilm();
  const lp = getLabelPaper();
  const ink = getSerigrafiaInk();
  const pouchMode = isDoypack();
  const labelMode = isLabelMode();
  const serigMode = isSerigrafiaMode();
  const bcStatCls = phys.ansiGrade === "F" ? "err" : (phys.ansiGrade === "C" ? "warn" : "ok");

  const steps = [];

  const vendorProfiles = {
    "PoliPlast Lombardia Srl (BG)": {
      it: "Azienda bergamasca specializzata nello soffiaggio di flaconi in PET lucido e HDPE per cosmetica, detergenza e cura personale.",
      en: "Bergamo manufacturer specialized in glossy PET and HDPE blow-molded bottles for personal care and household lines."
    },
    "Emilia BlowMold SpA (BO)": {
      it: "Stabilimento bolognese per stampaggio a estrusione-soffiaggio di contenitori sagomati in HDPE opaco riciclabile.",
      en: "Bologna industrial extrusion blow-molding plant producing shaped recyclable matte HDPE containers."
    },
    "Vetreria Padana SpA (BS)": {
      it: "Vetreria storica bresciana dedicata alla formatura di bottiglie in vetro cavo per bevande, oli e specialità liquide.",
      en: "Historic Brescia glassworks producing hollow glass bottles for beverages, oils, and liquid specialties."
    },
    "Vetreria Brianza Srl (MB)": {
      it: "Produttore brianzolo di vasi in vetro spesso e finiture satinate per cosmesi, alimentare gourmet e farmaceutica.",
      en: "Brianza producer of heavy-wall and frosted glass jars for skincare, gourmet food, and pharma."
    },
    "AluCan Packaging Italia SpA (MI)": {
      it: "Impianto milanese ad alta velocità specializzato in lattine trafilate in alluminio alimentare per il mercato europeo.",
      en: "High-speed Milan plant producing drawn food-grade aluminum cans for the European market."
    },
    "FlexPack Lombardia Srl (MI)": {
      it: "Trasformatore milanese di imballaggi flessibili stand-up ad alta barriera per polveri, integratori e prodotti secchi.",
      en: "Milan flexible packaging converter producing high-barrier stand-up pouches for dry goods and powders."
    }
  };
  const vProf = vendorProfiles[v.vendor] || {
    it: "Produttore europeo certificato di contenitori primari con controllo dimensionale in linea.",
    en: "Certified European primary container manufacturer with inline dimensional control."
  };

  // STEP 1 (LOCKED / NON-MODIFICABILE): Container Factory already selected in Marketplace
  steps.push({
    key: "container",
    lockedFixed: true,
    tagIt: "CONTENITORE PRIMARIO",
    tagEn: "PRIMARY CONTAINER",
    labelIt: "Contenitore primario",
    labelEn: "Primary container",
    cls: "ok",
    badge: `${v.neck} · ${v.vol}`,
    title: l === "it" ? v.it : v.en,
    spec: `${l === "it" ? v.matIt : v.matEn} · ${l === "it" ? v.subIt : v.subEn}`,
    options: [
      {
        name: v.vendor,
        sponsored: false,
        price: 260,
        rating: "4.9",
        reviews: 128,
        cert: "ISO 9001 · ISO 15378 · BRCGS",
        leadIt: "5 gg",
        leadEn: "5 days",
        sub: l === "it" ? vProf.it : vProf.en
      }
    ]
  });

  // STEP 2 (if closure selected): [0]=Sponsored, [1]=Lowest Price, [2..3]=Others
  if (cl.id !== "none" && !pouchMode && v.shape !== "alu_can") {
    const capOpt2 = cl.vendor;
    const capOpt3 = cl.vendor.includes("Emilia") ? "PlastChiusure Nord Srl (VA)" : "CapMold Emilia Srl (MO)";
    steps.push({
      key: "closure",
      lockedFixed: false,
      tagIt: "CHIUSURA E TAPPO",
      tagEn: "CLOSURE AND CAP",
      labelIt: "Chiusura e tappo",
      labelEn: "Closure and cap",
      cls: phys.neckMatch ? "ok" : "err",
      badge: phys.neckMatch ? `${cl.neck} ✓` : `${cl.neck} ≠ ${v.neck} ✕`,
      title: l === "it" ? cl.it : cl.en,
      spec: l === "it" ? `Filettatura ${cl.neck} · Accoppiamento ${v.neck}` : `Thread ${cl.neck} · Fit ${v.neck}`,
      options: [
        {
          name: `${v.vendor} — Div. Chiusure`,
          sponsored: true,
          price: 210,
          rating: "4.9",
          reviews: 96,
          cert: "ISO 9001 · ISO 15378",
          leadIt: "4 gg",
          leadEn: "4 days",
          sub: l === "it"
            ? "Divisione interna dedicata allo stampaggio di chiusure accoppiate direttamente agli stampi del contenitore."
            : "In-house closure molding division engineered to match the container plant molds directly."
        },
        {
          name: "Tecnocap Lombardia Srl (BG)",
          sponsored: false,
          price: 165,
          rating: "4.6",
          reviews: 49,
          cert: "ISO 9001 · ISO 14001",
          leadIt: "6 gg",
          leadEn: "6 days",
          sub: l === "it"
            ? "Produttore lombardo di tappi a vite, flip-top e dispenser in polipropilene per piccole e medie serie."
            : "Lombardy producer of polypropylene screw caps, flip-tops, and dispensers for short and mid runs."
        },
        {
          name: capOpt2,
          sponsored: false,
          price: 195,
          rating: "4.8",
          reviews: 84,
          cert: "BRCGS Packaging · ISO 9001",
          leadIt: "5 gg",
          leadEn: "5 days",
          sub: l === "it"
            ? "Specialista italiano di sistemi di erogazione, pompe cosmetiche e chiusure tecniche ad alta tenuta."
            : "Italian specialist in dispensing systems, cosmetic pumps, and precision tight-seal closures."
        },
        {
          name: capOpt3,
          sponsored: false,
          price: 180,
          rating: "4.7",
          reviews: 61,
          cert: "ISO 9001 · ISO 22000",
          leadIt: "6 gg",
          leadEn: "6 days",
          sub: l === "it"
            ? "Officina di stampaggio a iniezione multi-cavità per tappi standard e su misura con test tenuta."
            : "Multi-cavity injection molding workshop for standard and custom caps with leak verification."
        }
      ]
    });
  }

  // STEP 3 (unified decoration & printing step; [0]=Sponsored, [1]=Lowest Price)
  if (hasWrap()) {
    if (pouchMode) {
      const pTechIt = state.pouchPrintType === "flexo" ? "Stampa Flessografica" : "Stampa Digitale";
      const pTechEn = state.pouchPrintType === "flexo" ? "Flexographic Print" : "Digital Print";
      steps.push({
        key: "pouchPrint",
        lockedFixed: false,
        tagIt: "STAMPA BUSTA",
        tagEn: "POUCH PRINTING",
        labelIt: "Stampa busta",
        labelEn: "Pouch printing",
        cls: bcStatCls,
        badge: `${pTechIt} · GRADE ${phys.ansiGrade}`,
        title: l === "it" ? pTechIt : pTechEn,
        spec: `Barcode ${state.bcDoypackSide.toUpperCase()} · Grade ${phys.ansiGrade}`,
        options: [
          {
            name: "Rotoflex Packaging Srl (BG)",
            sponsored: true,
            price: 210,
            rating: "4.9",
            reviews: 104,
            cert: "BRCGS Packaging · ISO 9001",
            leadIt: "5 gg",
            leadEn: "5 days",
            sub: l === "it"
              ? "Converter flessibile bergamasco dotato di linee flessografiche e digitali fino a 10 colori per buste stand-up."
              : "Bergamo flexible converter running up to 10-color flexo and digital lines for stand-up pouches."
          },
          {
            name: "FlexoPrint Emilia Srl (RE)",
            sponsored: false,
            price: 165,
            rating: "4.6",
            reviews: 47,
            cert: "ISO 9001 · ISO 14001",
            leadIt: "6 gg",
            leadEn: "6 days",
            sub: l === "it"
              ? "Stamperia flessografica emiliana focalizzata su imballaggi flessibili, vernici opache e lotti test."
              : "Emilian flexographic print house focused on flexible pouches, matte finishes, and pilot batches."
          },
          {
            name: `${v.vendor} — Reparto Stampa`,
            sponsored: false,
            price: 195,
            rating: "4.8",
            reviews: 88,
            cert: "ISO 9001 · BRCGS",
            leadIt: "5 gg",
            leadEn: "5 days",
            sub: l === "it"
              ? "Reparto grafico integrato nello stesso impianto di saldatura buste per ridurre passaggi logistici."
              : "In-house printing department integrated inside the pouch converting plant to minimize transit."
          },
          {
            name: "Laminati Nord Italia SpA (NO)",
            sponsored: false,
            price: 180,
            rating: "4.7",
            reviews: 63,
            cert: "BRCGS Packaging · FSC",
            leadIt: "6 gg",
            leadEn: "6 days",
            sub: l === "it"
              ? "Azienda piemontese specializzata in stampa digitale su bobine flessibili senza costi di impianti stampa."
              : "Piedmont converter specialized in zero-plate digital roll printing for agile pre-series launches."
          }
        ]
      });
    } else if (serigMode) {
      steps.push({
        key: "serigrafia",
        lockedFixed: false,
        tagIt: "SERIGRAFIA DIRETTA 360°",
        tagEn: "360° DIRECT SILK-SCREEN",
        labelIt: "Serigrafia diretta 360°",
        labelEn: "360° direct silk-screen",
        cls: bcStatCls,
        badge: `GRADE ${phys.ansiGrade} · ${ink.id}`,
        title: ink.name,
        spec: l === "it" ? `Stampa diretta su alluminio · Barcode ${state.bcAngleDeg}° Grade ${phys.ansiGrade}` : `Direct print on aluminum · Barcode Grade ${phys.ansiGrade}`,
        options: [
          {
            name: "SeriCan Lombardia Srl (BG)",
            sponsored: true,
            price: 240,
            rating: "4.9",
            reviews: 89,
            cert: "ISO 9001 · BRCGS",
            leadIt: "5 gg",
            leadEn: "5 days",
            sub: l === "it"
              ? "Impresa specializzata nella decorazione diretta UV a 360° su lattine e corpi cilindrici in alluminio."
              : "Specialist plant for 360° direct UV screen decoration on aluminum cans and cylinders."
          },
          {
            name: "CromoCan Veneto Srl (VR)",
            sponsored: false,
            price: 190,
            rating: "4.6",
            reviews: 44,
            cert: "ISO 9001 · ISO 14001",
            leadIt: "6 gg",
            leadEn: "6 days",
            sub: l === "it"
              ? "Stabilimento veneto di stampa cilindrica diretta con polimerizzazione LED per tirature pilota."
              : "Veneto direct cylindrical printing facility with LED curing tailored to pilot runs."
          },
          {
            name: `${v.vendor} — Reparto Litografia`,
            sponsored: false,
            price: 220,
            rating: "4.8",
            reviews: 76,
            cert: "ISO 9001 · FSSC 22000",
            leadIt: "5 gg",
            leadEn: "5 days",
            sub: l === "it"
              ? "Linea litografica e serigrafica interna al produttore della lattina, con spedizione diretta al co-packer."
              : "In-plant lithography and screen line inside the can factory for seamless handoff."
          },
          {
            name: "DecoMetalli Piemonte Srl (TO)",
            sponsored: false,
            price: 205,
            rating: "4.7",
            reviews: 58,
            cert: "ISO 9001 · ISO 14001",
            leadIt: "6 gg",
            leadEn: "6 days",
            sub: l === "it"
              ? "Decoratore industriale su metallo specializzato in vernici tattili, finiture opache e inchiostri metallizzati."
              : "Industrial metal decorator specialized in tactile coatings, matte finishes, and metallic inks."
          }
        ]
      });
    } else if (labelMode) {
      steps.push({
        key: "label",
        lockedFixed: false,
        tagIt: "ETICHETTA ADESIVA",
        tagEn: "ADHESIVE LABEL",
        labelIt: "Etichetta adesiva",
        labelEn: "Adhesive label",
        cls: phys.sleeveStatus,
        badge: `Curva ${phys.sleeveTD}% · GRADE ${phys.ansiGrade}`,
        title: lp.name,
        spec: `${l === "it" ? lp.descIt : lp.descEn} · Barcode integrato (${state.sleeveAngleDeg}°)`,
        options: [
          {
            name: "Etichettificio Lombardo Srl (MI)",
            sponsored: true,
            price: 290,
            rating: "4.9",
            reviews: 118,
            cert: "BRCGS · FSC · ISO 9001",
            leadIt: "4 gg",
            leadEn: "4 days",
            sub: l === "it"
              ? "Etichettificio milanese attivo dal 1984 con linee rotative e digitali per etichette in bobina ad alta nobilitazione."
              : "Milan label house operating since 1984 with rotary and digital roll-label finishing lines."
          },
          {
            name: "LabelTech Emilia Srl (BO)",
            sponsored: false,
            price: 235,
            rating: "4.6",
            reviews: 51,
            cert: "ISO 9001 · ISO 14001",
            leadIt: "6 gg",
            leadEn: "6 days",
            sub: l === "it"
              ? "Produttore bolognese di etichette autoadesive tecniche resistenti a umidità, oli e lavaggi industriali."
              : "Bologna producer of technical self-adhesive labels resistant to moisture, oils, and abrasion."
          },
          {
            name: "Grafiche Adesive Brianza Srl (MB)",
            sponsored: false,
            price: 270,
            rating: "4.8",
            reviews: 92,
            cert: "ISO 9001 · FSC",
            leadIt: "5 gg",
            leadEn: "5 days",
            sub: l === "it"
              ? "Azienda grafica specializzata nella stampa digitale HP Indigo su bobina per lotti test e multi-referenza."
              : "Print specialist focused on HP Indigo digital roll labels for pilot runs and multi-SKU batches."
          },
          {
            name: "StampaPack Veneto Srl (TV)",
            sponsored: false,
            price: 250,
            rating: "4.7",
            reviews: 67,
            cert: "ISO 9001 · BRCGS",
            leadIt: "5 gg",
            leadEn: "5 days",
            sub: l === "it"
              ? "Converter veneto di etichette su carte naturali, PP e film trasparenti con fustellatura laser di precisione."
              : "Veneto roll-label converter working on natural papers, PP, and clear films with laser die-cutting."
          }
        ]
      });
    } else {
      steps.push({
        key: "sleeve",
        lockedFixed: false,
        tagIt: "SLEEVE 360°",
        tagEn: "360° SLEEVE",
        labelIt: "Stampa e film sleeve 360°",
        labelEn: "360° sleeve film and print",
        cls: bcStatCls === "err" || phys.sleeveStatus === "err" ? "err" : (bcStatCls === "warn" || phys.sleeveStatus === "warn" ? "warn" : "ok"),
        badge: `TD ${phys.sleeveTD}% · GRADE ${phys.ansiGrade}`,
        title: fm.name,
        spec: `Stampa Sleeve e Cucitura · Barcode (${state.bcAngleDeg}° · Grade ${phys.ansiGrade})`,
        options: [
          {
            name: "SleevePrint Milano Srl (MI)",
            sponsored: true,
            price: 340,
            rating: "4.9",
            reviews: 142,
            cert: "BRCGS · ISO 9001",
            leadIt: "5 gg",
            leadEn: "5 days",
            sub: l === "it"
              ? "Stabilimento specializzato in sleeve termoretraibili con reparto prestampa anamorfica e saldatura tubolare laser."
              : "Dedicated shrink-sleeve plant with in-house anamorphic prepress and laser tubular seaming."
          },
          {
            name: "PoliFilm Grafica Lombarda Srl (MB)",
            sponsored: false,
            price: 275,
            rating: "4.6",
            reviews: 54,
            cert: "FSC · ISO 14001",
            leadIt: "7 gg",
            leadEn: "7 days",
            sub: l === "it"
              ? "Trasformatore brianzolo agile per campionature e pre-serie rapide su film termoretraibili PETG, OPS e rPET."
              : "Agile Brianza converter delivering rapid pre-series shrink-sleeve samples in PETG, OPS, and rPET."
          },
          {
            name: "TermoPack Bergamo Srl (BG)",
            sponsored: false,
            price: 315,
            rating: "4.8",
            reviews: 115,
            cert: "ISO 9001 · BRCGS",
            leadIt: "5 gg",
            leadEn: "5 days",
            sub: l === "it"
              ? "Impresa industriale bergamasca con tunnel di prova vapore interno per validare la retrazione su contenitori sagomati."
              : "Bergamo industrial converter equipped with in-house steam shrink tunnels for shaped containers."
          },
          {
            name: "Rotocalco Emiliana Srl (PR)",
            sponsored: false,
            price: 295,
            rating: "4.7",
            reviews: 78,
            cert: "ISO 9001 · ISO 14001",
            leadIt: "6 gg",
            leadEn: "6 days",
            sub: l === "it"
              ? "Stamperia rotocalco emiliana ad alta definizione specializzata in sleeve integrali e bande di garanzia."
              : "Emilian high-definition rotogravure printer focused on full-body shrink sleeves and tamper bands."
          }
        ]
      });
    }
  }

  // STEP 4: CARTON BOX MAKER STEP ([0]=Sponsored, [1]=Lowest Price)
  steps.push({
    key: "carton",
    lockedFixed: false,
    tagIt: "CARTOTECNICA IMBALLO",
    tagEn: "CARTON PACKAGING",
    labelIt: "Cartotecnica imballo",
    labelEn: "Carton packaging",
    cls: "ok",
    badge: phys.isBulk ? `Sparsi ${phys.packQty} pz` : `${phys.packQty} pz (${phys.layout.cols}×${phys.layout.rows})`,
    title: phys.isBulk
      ? (l === "it" ? `Scatolone Master ${phys.cartonStr}` : `Bulk Master Carton ${phys.cartonStr}`)
      : (l === "it" ? `Scatola ${phys.cartonStr}` : `Carton Box ${phys.cartonStr}`),
    spec: phys.isBulk
      ? (l === "it" ? `Allestimento sparso ${phys.packQty} pz · Peso ${(phys.grossWeightG / 1000).toFixed(2)} kg` : `Loose bulk ${phys.packQty} pcs · ${(phys.grossWeightG / 1000).toFixed(2)} kg`)
      : `${state.boxBoard === "eflute" ? "Microonda E-Flute" : "Cartoncino Teso 350g"}${state.boxDivider ? " + Alveare" : ""} · ${(phys.grossWeightG / 1000).toFixed(2)} kg`,
    options: [
      {
        name: "Scatolificio Nord Milano Srl (MB)",
        sponsored: true,
        price: 195,
        rating: "4.9",
        reviews: 134,
        cert: "FSC · ISO 9001",
        leadIt: "4 gg",
        leadEn: "4 days",
        sub: l === "it"
          ? "Cartotecnica storica dell'area milanese con fustellatrici automatiche per scatole su misura in cartone teso e microonda."
          : "Established Milan box-maker operating automated die-cutters for custom solid and E-flute cartons."
      },
      {
        name: "PackBox Veneto Srl (PD)",
        sponsored: false,
        price: 150,
        rating: "4.6",
        reviews: 59,
        cert: "FSC · ISO 14001",
        leadIt: "6 gg",
        leadEn: "6 days",
        sub: l === "it"
          ? "Scatolificio padovano specializzato in campionature CAD e piccoli lotti di imballi in cartone certificato FSC."
          : "Padua box factory focused on CAD-cut prototypes and short runs in FSC-certified board."
      },
      {
        name: "Cartotecnica Emiliana SpA (MO)",
        sponsored: false,
        price: 180,
        rating: "4.8",
        reviews: 98,
        cert: "BRCGS · FSC · ISO 9001",
        leadIt: "5 gg",
        leadEn: "5 days",
        sub: l === "it"
          ? "Gruppo cartotecnico emiliano dedicato a scatole multipack, scatoloni logistici e soluzioni antiurto per GDO."
          : "Emilian carton group producing multipack boxes, master shippers, and retail-ready protective packs."
      },
      {
        name: "Ondulati Lombardia SpA (BS)",
        sponsored: false,
        price: 165,
        rating: "4.7",
        reviews: 74,
        cert: "ISO 9001 · FSC",
        leadIt: "5 gg",
        leadEn: "5 days",
        sub: l === "it"
          ? "Produttore bresciano di cartone ondulato, microonda e alveari protettivi fustellati per spedizioni sicure."
          : "Brescia corrugated producer supplying micro-flute cartons and custom protective dividers."
      }
    ]
  });

  // STEP 5: CO-PACKER FINALE ([0]=Sponsored, [1]=Lowest Price)
  steps.push({
    key: "copacker",
    lockedFixed: false,
    isCopacker: true,
    tagIt: "CO-PACKER FINALE",
    tagEn: "FINAL CO-PACKER",
    labelIt: "Co-Packer finale",
    labelEn: "Final Co-Packer",
    cls: "ok",
    badge: "CONVERGENZA LOTTO",
    title: l === "it" ? "Assemblaggio, Confezionamento e Consegna" : "Assembly, Packaging and Trial Delivery",
    spec: l === "it" ? "Convergenza materiali dai produttori, applicazione rivestimento e imballo" : "Multi-plant convergence, wrap application and trial boxing",
    options: [
      {
        name: "Greas Sleeves Srl (MI)",
        sponsored: true,
        price: 280,
        rating: "5.0",
        reviews: 210,
        cert: "ISO 9001 · BRCGS",
        leadIt: "4 gg",
        leadEn: "4 days",
        sub: l === "it"
          ? "Co-packer milanese specializzato nella convergenza multi-fornitore, applicazione sleeve o etichette e allestimento lotti prova."
          : "Milan co-packer specialized in multi-supplier convergence, sleeving/labeling, and pilot batch assembly."
      },
      {
        name: "EuroPack Terzisti Srl (VR)",
        sponsored: false,
        price: 230,
        rating: "4.6",
        reviews: 64,
        cert: "ISO 9001 · ISO 14001",
        leadIt: "6 gg",
        leadEn: "6 days",
        sub: l === "it"
          ? "Impresa veronese di confezionamento conto terzi flessibile per piccoli lotti, assemblaggi manuali e inscatolatura."
          : "Verona contract packer offering agile small-batch assembly, kitting, and retail boxing."
      },
      {
        name: "Lombarda Co-Packing SpA (BG)",
        sponsored: false,
        price: 260,
        rating: "4.8",
        reviews: 112,
        cert: "ISO 9001 · GMP ISO 22716",
        leadIt: "5 gg",
        leadEn: "5 days",
        sub: l === "it"
          ? "Polo logistico e produttivo bergamasco con linee automatiche di etichettatura, termoretrazione e riempimento."
          : "Bergamo contract packaging hub equipped with automatic labeling, steam shrinking, and filling lines."
      },
      {
        name: "PackService Emilia Srl (BO)",
        sponsored: false,
        price: 245,
        rating: "4.7",
        reviews: 86,
        cert: "ISO 9001 · HACCP",
        leadIt: "6 gg",
        leadEn: "6 days",
        sub: l === "it"
          ? "Operatore bolognese di confezionamento conto terzi multi-formato con reparti dedicati a polveri, capsule e inscatolatura."
          : "Bologna multi-format contract packer operating dedicated rooms for powders, capsules, and boxing."
      }
    ]
  });

  steps.forEach(s => {
    const prices = s.options.map(o => o.price);
    s.minCost = Math.min(...prices);
    const selIdx = state.selectedSuppliers[s.key];
    s.selectedCost = (selIdx !== undefined && s.options[selIdx]) ? s.options[selIdx].price : s.minCost;
    s.cost = s.selectedCost;
  });

  return steps;
}

function getActiveSupplyChain(phys) {
  const steps = buildSupplyChainSteps(phys);
  const fillExtra = getCopackerFillCost(getVessel());
  const minBaseCost = steps.reduce((acc, s) => acc + s.minCost, 0);
  const minFactoryShare = Math.round(minBaseCost * 0.80);
  const minVcFee = minBaseCost - minFactoryShare;
  const baseCost = steps.reduce((acc, s) => acc + s.selectedCost, 0);
  const totalCost = baseCost + fillExtra;
  const factoryShare = Math.round(totalCost * 0.80);
  const vcFee = totalCost - factoryShare;
  return { actors: steps, steps, fillExtra, minBaseCost, minFactoryShare, minVcFee, baseCost, totalCost, factoryShare, vcFee };
}

function updateFastTelemetryUI() {
  const l = state.lang;
  const t = TXT[l];
  const v = getVessel();
  const cl = getClosure();
  const fm = getFilm();
  const lp = getLabelPaper();
  const ink = getSerigrafiaInk();
  const pouchMode = isDoypack();
  const labelMode = isLabelMode();
  const serigMode = isSerigrafiaMode();
  const wrapActive = hasWrap();
  const hasClosure = vesselHasClosureStep(v);
  const phys = evaluateLivePhysics();
  const chain = getActiveSupplyChain(phys);

  // Update 3D Pin Cards (no CLASH text, no &, no Ladder)
  const dimLabel = l === "it" ? "Dimensioni" : "Dimensions";
  const pNeckCard = document.getElementById("pinNeckCard");
  pNeckCard.className = "pin-card " + (phys.neckMatch ? "ok" : "err");
  document.getElementById("pinNeckTitle").textContent = phys.isNoCap
    ? `${v.neck} · ${l === "it" ? "ASSENTE" : "ABSENT"}`
    : (phys.neckMatch ? `${v.neck} OK ✓` : `${cl.neck} ≠ ${v.neck} ✕`);
  document.getElementById("pinNeckSub").textContent = phys.isNoCap
    ? (l === "it" ? "Nessuna chiusura selezionata" : "No closure selected")
    : (phys.neckMatch
        ? (l === "it" ? "Filetto e tenuta validati" : "Thread and seal locked")
        : (l === "it" ? "Filettatura incompatibile" : "Incompatible thread"));
  const neckDimEl = document.getElementById("pinNeckDim");
  if (neckDimEl) {
    neckDimEl.style.display = phys.isNoCap ? "none" : "block";
    if (!phys.isNoCap) neckDimEl.textContent = `${dimLabel}: ${getClosureRealDimensionsMm(cl)}`;
  }

  const dims = getWrapRealDimensionsMm(v);
  const pSlCard = document.getElementById("pinSleeveCard");
  if (pSlCard && !pouchMode && (state.wrapType === "sleeve" || state.wrapType === "label")) {
    pSlCard.className = "pin-card " + phys.sleeveStatus;
    const slTag = phys.sleeveStatus === "err" ? "GRADE F" : (phys.sleeveStatus === "warn" ? "GRADE C" : "GRADE A");
    if (labelMode) {
      document.getElementById("pinSlTitle").textContent = `ETICHETTA 3D · ${slTag}`;
      document.getElementById("pinSlSub").textContent = phys.sleeveStatus === "ok"
        ? (l === "it" ? `Stesura piana ${phys.sleeveTD}% (max ${lp.maxTD}%) · ${lp.id}` : `Flat adhesion ${phys.sleeveTD}% · ${lp.id}`)
        : (phys.sleeveStatus === "warn"
            ? (l === "it" ? `Curva spalla / spigolo (${phys.sleeveTD}%) · ${lp.id}` : `Shoulder / corner warning (${phys.sleeveTD}%)`)
            : (l === "it" ? `Grinze su doppia curvatura (${phys.sleeveTD}%)` : `Creasing on double curve (${phys.sleeveTD}%)`));
    } else {
      document.getElementById("pinSlTitle").textContent = `SLEEVE 3D · ${slTag}`;
      document.getElementById("pinSlSub").textContent = phys.sleeveStatus === "ok"
        ? (l === "it" ? `TD ${phys.sleeveTD}% · Corpo piano · ${fm.id}` : `TD ${phys.sleeveTD}% · Flat body · ${fm.id}`)
        : (phys.sleeveStatus === "warn"
            ? (l === "it" ? `TD ${phys.sleeveTD}% · Spalla curva (${fm.id})` : `TD ${phys.sleeveTD}% · Shoulder warp (${fm.id})`)
            : (l === "it" ? `TD ${phys.sleeveTD}% · Oltre limite ${fm.id}` : `TD ${phys.sleeveTD}% · Exceeds ${fm.id} limit`));
    }
    const slDimEl = document.getElementById("pinSlDim");
    if (slDimEl) slDimEl.textContent = `${dimLabel}: ${dims.wrapDimStr}`;
  }

  const pBcCard = document.getElementById("pinBarcodeCard");
  const bcStateCls = phys.ansiGrade === "F" ? "err" : (phys.ansiGrade === "C" ? "warn" : "ok");
  if (wrapActive) {
    pBcCard.className = "pin-card " + bcStateCls;
    document.getElementById("pinBcTitle").textContent = `EAN-13 · GRADE ${phys.ansiGrade}`;
    if (pouchMode) {
      document.getElementById("pinBcSub").textContent = l === "it" ? phys.bcReasonIt : phys.bcReasonEn;
    } else if (serigMode) {
      document.getElementById("pinBcSub").textContent = `${ink.id} · ${dims.wrapDimStr}`;
    } else if (labelMode) {
      document.getElementById("pinBcSub").textContent = phys.ansiGrade === "A"
        ? (l === "it" ? `Zona bassa piana (${phys.localTD}%)` : `Flat lower zone (${phys.localTD}%)`)
        : (l === "it" ? `Deformazione barre su curva (${phys.localTD}%)` : `Curve distortion on bars (${phys.localTD}%)`);
    } else {
      document.getElementById("pinBcSub").textContent = phys.ansiGrade === "F"
        ? (l === "it" ? `TD ${phys.localTD}% · Compressione barre!` : `TD ${phys.localTD}% · Bar compression!`)
        : (phys.ansiGrade === "C"
            ? (l === "it" ? `TD ${phys.localTD}% · Zona vicina a spalla` : `TD ${phys.localTD}% · Approaching shoulder`)
            : (l === "it" ? `TD ${phys.localTD}% · Zona cilindrica piana` : `TD ${phys.localTD}% · Flat cylinder zone`));
    }
    const bcDimEl = document.getElementById("pinBcDim");
    if (bcDimEl) bcDimEl.textContent = `${dimLabel}: ${dims.bcDimStr}`;
  }

  // Right Traffic Light Header
  const diagHost = document.getElementById("diagDetails");
  const banner = document.getElementById("tlBanner");
  banner.className = "traffic-banner " + phys.status;
  document.getElementById("bulbR").classList.toggle("active", phys.status === "r");
  document.getElementById("bulbY").classList.toggle("active", phys.status === "y");
  document.getElementById("bulbG").classList.toggle("active", phys.status === "g");

  document.getElementById("tlTitle").textContent = phys.status === "g" ? t.tlGreenT : (phys.status === "y" ? t.tlAmberT : t.tlRedT);
  document.getElementById("tlDesc").textContent = phys.status === "g" ? t.tlGreenD : (phys.status === "y" ? t.tlAmberD : t.tlRedD);

  // Unified Single-Pass Diagnostic Details (idle neutral grey when absent, no Box check 04, no Closure row on Can/Doypack)
  const absentLabel = l === "it" ? "Assente" : "Absent";
  const slCls = wrapActive ? phys.sleeveStatus : "idle";
  const bcRowCls = wrapActive ? bcStateCls : "idle";

  const d2K = pouchMode
    ? (l === "it" ? "STAMPA BUSTA" : "POUCH PRINTING")
    : (serigMode
        ? (l === "it" ? "SERIGRAFIA DIRETTA 360°" : "360° DIRECT SILK-SCREEN")
        : (labelMode ? (l === "it" ? "ETICHETTA ADESIVA" : "ADHESIVE LABEL") : (l === "it" ? "RIVESTIMENTO SLEEVE E FILM" : "SLEEVE WRAP AND FILM")));
  const d2Badge = !wrapActive
    ? absentLabel
    : (pouchMode
        ? (state.pouchPrintType === "flexo" ? "FLEXO ✓" : "DIGITALE ✓")
        : (serigMode
            ? `${ink.id} 360°`
            : (labelMode ? `${phys.sleeveTD}% / max ${lp.maxTD}%` : `TD ${phys.sleeveTD}% / max ${fm.maxTD}%`)));
  const d2Title = !wrapActive
    ? (l === "it" ? "Nessun rivestimento" : "No wrap")
    : (pouchMode
        ? (state.pouchPrintType === "flexo" ? (l === "it" ? "Stampa Flessografica" : "Flexographic Print") : (l === "it" ? "Stampa Digitale" : "Digital Print"))
        : (serigMode ? ink.name : (labelMode ? lp.name : fm.name)));
  const d2Sub = !wrapActive
    ? (l === "it" ? "Contenitore neutro privo di grafica o pellicola: nessun fornitore stampa aggiunto in filiera." : "Bare neutral vessel with no graphics or film: no printer added to supply chain.")
    : (pouchMode
        ? (l === "it" ? "Stampa diretta sulla superficie della busta pronta per il confezionamento." : "Direct surface printing ready for pouch converting.")
        : (serigMode
            ? (l === "it" ? "Inchiostri polimerizzati direttamente sull'alluminio senza pellicole né giunte." : "Inks cured directly onto aluminum with zero seam.")
            : (labelMode
                ? (slCls === "ok"
                    ? (l === "it" ? "Aderenza regolare sulla fascia piana senza formazione di bolle o grinze." : "Clean flat-zone adhesion with zero bubbles or wrinkles.")
                    : (slCls === "warn"
                        ? (l === "it" ? "Bordo vicino alla curvatura: possibile formazione di leggere grinze." : "Edge approaches taper: mild wrinkle risk.")
                        : (l === "it" ? "Curvatura oltre la tolleranza del supporto rigido: abbassa verso la zona piana." : "Curve exceeds substrate tolerance: move down to flat zone.")))
                : (slCls === "ok"
                    ? (l === "it" ? "Conformabilità regolare sulla superficie del flacone entro i limiti del film." : "Smooth conformability across bottle body within film limits.")
                    : (slCls === "warn"
                        ? (l === "it" ? `Grafica sulla spalla curva: richiesta pre-distorsione per ${fm.id}.` : `Upper copy enters shoulder curve: ${fm.id} pre-warp required.`)
                        : (l === "it" ? `Retrazione oltre il limite fisico di ${fm.id}: cambia film o abbassa la fascia.` : `Shrink exceeds ${fm.id} physical limit: switch film or lower wrap.`))))));

  const bcTitle = !wrapActive
    ? (l === "it" ? "Nessun codice a barre" : "No barcode")
    : (pouchMode
        ? `${l === "it" ? "EAN-13 Busta" : "Pouch EAN-13"} · ${dims.bcDimStr}`
        : (labelMode
            ? `${l === "it" ? "Integrato in fustella" : "Die-cut integrated"} · ${dims.bcDimStr}`
            : `EAN-13 · ${dims.bcDimStr} (TD ${phys.localTD}%)`));

  const bcSubText = !wrapActive
    ? (l === "it" ? "Viene generato e controllato automaticamente applicando un rivestimento grafico." : "Generated and verified automatically once a graphic wrap is applied.")
    : (pouchMode
        ? (l === "it" ? phys.bcReasonIt : phys.bcReasonEn)
        : (bcStateCls === "ok"
            ? (l === "it" ? "Leggibilità ottimale GS1 sulla zona bassa piana nella posizione attuale." : "Optimal GS1 retail readability on the flat lower zone.")
            : (bcStateCls === "warn"
                ? (l === "it" ? "Zona barcode vicina a una curvatura o spigolo: consigliata verifica in prestampa." : "Barcode zone near curve or edge: prepress check advised.")
                : (l === "it" ? "Deformazione eccessiva sulle barre: sposta il rivestimento verso la zona piana." : "Excessive bar distortion: move wrap onto flat zone."))));

  const rowData = [];
  if (hasClosure) {
    const capCls = phys.isNoCap ? "idle" : (phys.neckMatch ? "ok" : "err");
    rowData.push({
      cls: capCls,
      ico: capCls === "idle" ? "–" : (phys.neckMatch ? "✓" : "✕"),
      k: t.chk1,
      pill: phys.isNoCap ? absentLabel : `${v.neck} ↔ ${cl.neck}`,
      title: phys.isNoCap ? (l === "it" ? "Nessuna chiusura" : "No closure") : (l === "it" ? cl.it : cl.en),
      sub: phys.isNoCap
        ? (l === "it" ? "Contenitore aperto senza tappo: nessun fornitore chiusure aggiunto in filiera." : "Open container without cap: no closure supplier added to supply chain.")
        : (phys.neckMatch
            ? (l === "it" ? "Filettatura e tenuta meccanica compatibili con il collo del contenitore." : "Thread geometry and mechanical seal match the container neck.")
            : (l === "it" ? `Filettatura incompatibile: seleziona un componente con attacco ${v.neck}.` : `Incompatible thread: select a closure matching ${v.neck}.`))
    });
  }

  rowData.push({
    cls: slCls,
    ico: slCls === "idle" ? "–" : (slCls === "ok" ? "✓" : (slCls === "warn" ? "!" : "✕")),
    k: d2K,
    pill: d2Badge,
    title: d2Title,
    sub: d2Sub
  });

  rowData.push({
    cls: bcRowCls,
    ico: bcRowCls === "idle" ? "–" : (bcRowCls === "ok" ? "✓" : (bcRowCls === "warn" ? "!" : "✕")),
    k: t.chk3,
    pill: wrapActive ? `GRADE ${phys.ansiGrade}` : absentLabel,
    title: bcTitle,
    sub: bcSubText
  });

  rowData.forEach((r, idx) => { r.num = String(idx + 1).padStart(2, "0"); });

  const existingBoard = diagHost.querySelector(".diag-board");
  const existingRows = existingBoard ? [...existingBoard.children] : [];
  if (existingRows.length === rowData.length) {
    rowData.forEach((r, idx) => {
      const rowEl = existingRows[idx];
      rowEl.className = "diag-row " + r.cls;
      rowEl.querySelector(".diag-pillar-num").textContent = r.num;
      rowEl.querySelector(".diag-pillar-ico").textContent = r.ico;
      rowEl.querySelector(".diag-card-k").textContent = r.k;
      const pillEl = rowEl.querySelector(".diag-pill");
      pillEl.className = "diag-pill " + r.cls;
      pillEl.textContent = r.pill;
      rowEl.querySelector(".diag-card-t").textContent = r.title;
      rowEl.querySelector(".diag-card-s").textContent = r.sub;
    });
  } else {
    diagHost.innerHTML = `
      <div class="diag-board">
        ${rowData.map(r => `
          <div class="diag-row ${r.cls}">
            <div class="diag-pillar">
              <span class="diag-pillar-num">${r.num}</span>
              <span class="diag-pillar-ico">${r.ico}</span>
            </div>
            <div class="diag-body">
              <div class="diag-row-top">
                <span class="diag-card-k">${r.k}</span>
                <span class="diag-pill ${r.cls}">${r.pill}</span>
              </div>
              <div class="diag-card-t">${r.title}</div>
              <div class="diag-card-s">${r.sub}</div>
            </div>
          </div>
        `).join("")}
      </div>
    `;
  }

  // Dynamic Starting Price Footer (large clean "Da €..." with no boxes)
  const prefix = l === "it" ? "Da " : "From ";
  document.getElementById("ui_chk_hdr").textContent = t.chkHdr;
  document.getElementById("ui_ship_note").textContent = t.shipNote;
  document.getElementById("val_sp_lot").textContent = `${prefix}${formatEuro(chain.minBaseCost)}`;

  const btnChk = document.getElementById("btnCheckout");
  if (phys.status === "r") {
    btnChk.disabled = true;
    btnChk.textContent = t.ctaBlock;
  } else if (phys.status === "y") {
    btnChk.disabled = false;
    btnChk.textContent = t.ctaWarn;
  } else {
    btnChk.disabled = false;
    btnChk.textContent = t.ctaOk;
  }
}

// ==================== VIEW 01: CONTAINER MARKETPLACE (STEP 1 — BARE CONTAINERS!) ====================
function renderCatalogThumbSVG(v) {
  if (v.shape === "doypack") {
    return `<svg width="96" height="126" viewBox="0 0 96 126">
      <path d="M18,16 L78,16 L82,110 Q48,118 14,110 Z" fill="#FAF8F4" stroke="#121110" stroke-width="2"/>
      <line x1="18" y1="28" x2="78" y2="28" stroke="#D5CFC4" stroke-width="1.4"/>
      <ellipse cx="48" cy="110" rx="28" ry="3.5" fill="#EAE4D8" stroke="#121110" stroke-width="1.2"/>
      <path d="M26,42 Q32,76 28,102" fill="none" stroke="rgba(18,17,16,0.08)" stroke-width="3" stroke-linecap="round"/>
    </svg>`;
  }
  if (v.shape === "wine_bordeaux") {
    return `<svg width="96" height="126" viewBox="0 0 96 126">
      <rect x="41" y="10" width="14" height="5" rx="1.5" fill="#1D4B31" stroke="#0B1D13" stroke-width="1.4"/>
      <path d="M42,15 L42,40 C42,50 28,54 28,66 L28,114 Q48,118 68,114 L68,66 C68,54 54,50 54,40 L54,15 Z" fill="#173A26" stroke="#0B1D13" stroke-width="2"/>
      <path d="M34,66 L34,106" fill="none" stroke="rgba(255,255,255,0.18)" stroke-width="2.5" stroke-linecap="round"/>
    </svg>`;
  }
  if (v.shape === "jar_lux") {
    return `<svg width="96" height="110" viewBox="0 0 96 110">
      <rect x="28" y="34" width="40" height="13" rx="2" fill="#E6E1D7" stroke="#121110" stroke-width="1.6"/>
      <line x1="29" y1="38" x2="67" y2="38" stroke="#9A9286" stroke-width="1.2"/>
      <line x1="29" y1="42" x2="67" y2="42" stroke="#9A9286" stroke-width="1.2"/>
      <rect x="22" y="47" width="52" height="45" rx="7" fill="#F3EFE6" stroke="#121110" stroke-width="2"/>
      <path d="M29,55 L29,84" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
    </svg>`;
  }
  if (v.shape === "square_soft") {
    return `<svg width="96" height="126" viewBox="0 0 96 126">
      <rect x="40" y="13" width="16" height="13" rx="1.5" fill="#F3EFE7" stroke="#121110" stroke-width="1.6"/>
      <line x1="41" y1="17" x2="55" y2="17" stroke="#8C857C" stroke-width="1.2"/>
      <line x1="41" y1="21" x2="55" y2="21" stroke="#8C857C" stroke-width="1.2"/>
      <path d="M22,36 Q24,26 38,26 L58,26 Q72,26 74,36 L74,110 Q74,116 68,116 L28,116 Q22,116 22,110 Z" fill="#FAF8F5" stroke="#121110" stroke-width="2"/>
      <path d="M29,40 L29,106" fill="none" stroke="rgba(0,0,0,0.06)" stroke-width="2.5" stroke-linecap="round"/>
    </svg>`;
  }
  if (v.shape === "alu_can") {
    return `<svg width="96" height="126" viewBox="0 0 96 126">
      <path d="M26,20 L70,20 L74,28 L74,108 L70,115 L26,115 L22,108 L22,28 Z" fill="#D8DCE0" stroke="#121110" stroke-width="2"/>
      <ellipse cx="48" cy="20" rx="22" ry="4" fill="#E9ECEF" stroke="#121110" stroke-width="1.5"/>
      <ellipse cx="48" cy="20" rx="6" ry="2.2" fill="#9AA1A8" stroke="#121110" stroke-width="1"/>
      <line x1="33" y1="32" x2="33" y2="108" stroke="rgba(255,255,255,0.55)" stroke-width="4" stroke-linecap="round"/>
      <line x1="63" y1="32" x2="63" y2="108" stroke="rgba(0,0,0,0.10)" stroke-width="2.5" stroke-linecap="round"/>
    </svg>`;
  }
  // Cylindrical Glossy PET bottle: bare transparent-look plastic, no cap & no sleeve
  return `<svg width="96" height="126" viewBox="0 0 96 126">
    <rect x="41" y="16" width="14" height="15" rx="1.5" fill="#EAF4FA" stroke="#121110" stroke-width="1.6"/>
    <line x1="41" y1="20" x2="55" y2="20" stroke="#7A8F9E" stroke-width="1.2"/>
    <line x1="41" y1="24" x2="55" y2="24" stroke="#7A8F9E" stroke-width="1.2"/>
    <ellipse cx="48" cy="16" rx="7" ry="2" fill="#FFFFFF" stroke="#121110" stroke-width="1.2"/>
    <path d="M26,46 Q28,31 41,31 L55,31 Q68,31 70,46 L70,110 Q70,116 64,116 L32,116 Q26,116 26,110 Z" fill="#EAF4FA" stroke="#121110" stroke-width="2"/>
    <path d="M32,48 Q34,40 36,40 L36,108" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>
  </svg>`;
}

const VESSEL_REALISTIC_THUMBS = {};

function createPackshotEnvironment(offRenderer) {
  const pmrem = new THREE.PMREMGenerator(offRenderer);
  pmrem.compileEquirectangularShader();
  const envScene = new THREE.Scene();
  // Dark studio room with bright softbox vertical diffusers gives crystal glass, clear PET, brushed aluminum & satin HDPE strong realistic Fresnel edge contrast
  envScene.background = new THREE.Color(0x232933);

  const boxGeo = new THREE.BoxGeometry(1, 1, 1);
  const addCard = (col, sx, sy, sz, px, py, pz) => {
    const m = new THREE.Mesh(boxGeo, new THREE.MeshBasicMaterial({ color: col }));
    m.scale.set(sx, sy, sz);
    m.position.set(px, py, pz);
    envScene.add(m);
  };
  addCard(0xFFFFFF, 8.5, 0.25, 8.5, 0, 7.0, 0);      // Overhead studio scrim
  addCard(0xFFFFFF, 0.3, 9.5, 3.0, -5.0, 1.5, 3.8);  // Key vertical softbox left
  addCard(0xF8FAFC, 0.3, 9.5, 2.2, 5.2, 1.8, 3.2);   // Secondary softbox right
  addCard(0x0B0E14, 0.3, 10.5, 4.5, -5.4, 0.5, -1.5);// Crisp black negative fill left
  addCard(0x0B0E14, 0.3, 10.5, 4.5, 5.4, 0.5, -1.5); // Crisp black negative fill right
  addCard(0x94A3B8, 12, 0.25, 12, 0, -5.0, 0);       // Cool studio floor bounce

  const tex = pmrem.fromScene(envScene, 0.024).texture;
  pmrem.dispose();
  return tex;
}

function createThumbDoypackTexture() {
  const c = document.createElement("canvas");
  c.width = 512;
  c.height = 512;
  const ctx = c.getContext("2d");
  const g = ctx.createLinearGradient(0, 0, 0, 512);
  g.addColorStop(0, "#FAFAFB");
  g.addColorStop(0.50, "#ECEFF3");
  g.addColorStop(1, "#D8DDE6");
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, 512, 512);

  // Subtle side heat-seal border sheen + dark zip groove
  ctx.fillStyle = "rgba(15, 23, 42, 0.08)";
  ctx.fillRect(0, 0, 512, 66);
  ctx.fillStyle = "rgba(15, 23, 42, 0.24)";
  ctx.fillRect(0, 64, 512, 5);
  ctx.fillRect(0, 74, 512, 3);

  [0.25, 0.75].forEach(u => {
    const sx = u * 512;
    const sg = ctx.createLinearGradient(sx - 20, 0, sx + 20, 0);
    sg.addColorStop(0, "rgba(15, 23, 42, 0)");
    sg.addColorStop(0.5, "rgba(15, 23, 42, 0.16)");
    sg.addColorStop(1, "rgba(15, 23, 42, 0)");
    ctx.fillStyle = sg;
    ctx.fillRect(sx - 20, 0, 40, 512);
  });

  const tex = new THREE.CanvasTexture(c);
  tex.encoding = THREE.sRGBEncoding;
  tex.wrapS = THREE.RepeatWrapping;
  tex.wrapT = THREE.ClampToEdgeWrapping;
  return tex;
}

function generatePhotorealisticVesselThumbnails() {
  if (typeof THREE === "undefined") return;
  try {
    const W = 440, H = 440;
    const offCanvas = document.createElement("canvas");
    offCanvas.width = W;
    offCanvas.height = H;
    const offRenderer = new THREE.WebGLRenderer({ canvas: offCanvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
    offRenderer.setPixelRatio(1);
    offRenderer.setSize(W, H, false);
    offRenderer.toneMapping = THREE.ACESFilmicToneMapping;
    offRenderer.toneMappingExposure = 1.08;
    offRenderer.outputEncoding = THREE.sRGBEncoding;

    const offScene = new THREE.Scene();
    offScene.environment = createPackshotEnvironment(offRenderer);

    // Sculptural studio key/rim ratio (low ambient preserves deep 3D edge shading on white HDPE & Doypack!)
    const amb = new THREE.AmbientLight(0xF1F5F9, 0.20);
    offScene.add(amb);
    const key = new THREE.DirectionalLight(0xFFFFFF, 1.32);
    key.position.set(4.8, 6.2, 5.2);
    offScene.add(key);
    const fillLeft = new THREE.DirectionalLight(0x94A3B8, 0.42);
    fillLeft.position.set(-5.2, 1.8, 2.4);
    offScene.add(fillLeft);
    const rim = new THREE.DirectionalLight(0xE2E8F0, 0.92);
    rim.position.set(-4.5, 4.2, -5.0);
    offScene.add(rim);

    // Grounded contact shadow beneath vessel
    const shC = document.createElement("canvas");
    shC.width = 256; shC.height = 256;
    const shCtx = shC.getContext("2d");
    const shG = shCtx.createRadialGradient(128, 128, 12, 128, 128, 120);
    shG.addColorStop(0, "rgba(15, 23, 42, 0.34)");
    shG.addColorStop(0.55, "rgba(15, 23, 42, 0.11)");
    shG.addColorStop(1, "rgba(15, 23, 42, 0)");
    shCtx.fillStyle = shG;
    shCtx.fillRect(0, 0, 256, 256);
    const shTex = new THREE.CanvasTexture(shC);
    const shPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(2.5, 2.1),
      new THREE.MeshBasicMaterial({ map: shTex, transparent: true, depthWrite: false })
    );
    shPlane.rotation.x = -Math.PI / 2;
    shPlane.position.y = -1.26;
    offScene.add(shPlane);

    const offCam = new THREE.PerspectiveCamera(28, W / H, 0.1, 40);
    const doypackTex = createThumbDoypackTexture();

    VESSELS.forEach(v => {
      const grp = new THREE.Group();
      const totalH = getVesselTotalHeight(v);
      const pouchMode = v.shape === "doypack";
      const vGeo = createParametricVesselGeometry(v, pouchMode ? 112 : 96, pouchMode ? 84 : 110, 0.0, 1.0, 1.0, false);

      function addStudioFresnelRim(mat, rimHex, strength, rimOpacityBoost) {
        mat.onBeforeCompile = shader => {
          shader.uniforms.uRimColor = { value: new THREE.Color(rimHex) };
          shader.uniforms.uRimStrength = { value: strength };
          shader.uniforms.uRimAlpha = { value: rimOpacityBoost };
          shader.fragmentShader = shader.fragmentShader
            .replace(
              "#include <common>",
              `#include <common>
uniform vec3 uRimColor;
uniform float uRimStrength;
uniform float uRimAlpha;`
            )
            .replace(
              "#include <dithering_fragment>",
              `vec3 _vN = normalize(vNormal);
vec3 _vV = normalize(vViewPosition);
float _fr = pow(1.0 - clamp(abs(dot(_vN, _vV)), 0.0, 1.0), 1.9);
gl_FragColor.rgb = mix(gl_FragColor.rgb, uRimColor, _fr * uRimStrength);
gl_FragColor.a = clamp(gl_FragColor.a + _fr * uRimAlpha, 0.0, 1.0);
#include <dithering_fragment>`
            );
        };
      }

      let vMat;
      if (pouchMode) {
        vMat = new THREE.MeshPhysicalMaterial({
          map: doypackTex,
          color: 0xECEFF4,
          roughness: 0.58,
          metalness: 0.02,
          clearcoat: 0.16,
          envMapIntensity: 0.68,
          side: THREE.DoubleSide
        });
        addStudioFresnelRim(vMat, 0x475569, 0.42, 0.0);
      } else if (v.defaultFinish === "pet_gloss") {
        vMat = new THREE.MeshPhysicalMaterial({
          color: 0xD2E4F3,
          transparent: true,
          opacity: 0.72,
          roughness: 0.05,
          metalness: 0.05,
          reflectivity: 1.0,
          clearcoat: 1.0,
          clearcoatRoughness: 0.03,
          envMapIntensity: 1.15,
          side: THREE.DoubleSide
        });
        addStudioFresnelRim(vMat, 0x334155, 0.68, 0.28);
      } else if (v.defaultFinish === "hdpe_white") {
        vMat = new THREE.MeshPhysicalMaterial({
          color: 0xEDF0F5,
          roughness: 0.44,
          metalness: 0.03,
          clearcoat: 0.22,
          clearcoatRoughness: 0.26,
          envMapIntensity: 0.58
        });
        addStudioFresnelRim(vMat, 0x64748B, 0.44, 0.0);
      } else if (v.defaultFinish === "wine_green") {
        vMat = new THREE.MeshPhysicalMaterial({
          color: 0x062311,
          transparent: true,
          opacity: 0.96,
          roughness: 0.06,
          metalness: 0.06,
          clearcoat: 1.0,
          clearcoatRoughness: 0.03,
          envMapIntensity: 0.72,
          side: THREE.DoubleSide
        });
        addStudioFresnelRim(vMat, 0x031209, 0.55, 0.04);
      } else if (v.defaultFinish === "alu_brushed") {
        vMat = new THREE.MeshStandardMaterial({
          color: 0xCFD5DD,
          roughness: 0.20,
          metalness: 0.92,
          envMapIntensity: 1.18,
          side: THREE.DoubleSide
        });
        addStudioFresnelRim(vMat, 0x334155, 0.36, 0.0);
      } else {
        vMat = new THREE.MeshPhysicalMaterial({
          color: 0xE2DFD7,
          transparent: true,
          opacity: 0.88,
          roughness: 0.36,
          metalness: 0.02,
          clearcoat: 0.42,
          clearcoatRoughness: 0.22,
          envMapIntensity: 0.78,
          side: THREE.DoubleSide
        });
        addStudioFresnelRim(vMat, 0x475569, 0.52, 0.14);
      }

      grp.add(new THREE.Mesh(vGeo, vMat));

      // Molded neck lip on open rigid glass/plastic vessels
      if (!pouchMode && v.shape !== "alu_can") {
        const lipGeo = v.shape === "jar_lux"
          ? new THREE.TorusGeometry(0.676, 0.024, 14, 64)
          : (v.shape === "wine_bordeaux"
              ? new THREE.TorusGeometry(0.160, 0.023, 14, 48)
              : new THREE.TorusGeometry(0.214, 0.019, 14, 48));
        lipGeo.rotateX(Math.PI / 2);
        const lipMesh = new THREE.Mesh(lipGeo, vMat);
        lipMesh.position.y = -1.25 + totalH;
        grp.add(lipMesh);
      }

      // Rich internal formula core inside transparent / frosted glass & PET vessels
      if (!pouchMode && v.shape !== "alu_can" && v.defaultFinish !== "hdpe_white") {
        const liqTop = (v.shape === "jar_lux" || v.shape === "wine_bordeaux") ? 0.64 : 0.62;
        const liqGeo = createParametricVesselGeometry(v, 56, 40, 0.03, liqTop, 0.89, true);
        const liqCol = v.defaultFinish === "pet_gloss" ? 0x7BA9D1 : (v.defaultFinish === "frosted" ? 0xDDBB93 : 0x3A0A12);
        const liqMat = new THREE.MeshPhysicalMaterial({
          color: new THREE.Color(liqCol),
          transparent: true,
          opacity: v.defaultFinish === "wine_green" ? 0.85 : (v.defaultFinish === "frosted" ? 0.74 : 0.62),
          roughness: 0.16,
          clearcoat: 0.85
        });
        grp.add(new THREE.Mesh(liqGeo, liqMat));
      }

      // Metallic SOT 202 pull-tab deck on aluminum can
      if (v.shape === "alu_can") {
        const botDisk = new THREE.Mesh(
          new THREE.CylinderGeometry(0.50, 0.50, 0.02, 48),
          new THREE.MeshStandardMaterial({ color: 0xC8CDD2, roughness: 0.26, metalness: 0.88 })
        );
        botDisk.position.y = -1.24;
        grp.add(botDisk);

        const canTopY = -1.25 + 0.965 * totalH;
        const rimMat = new THREE.MeshStandardMaterial({ color: 0xE6E9ED, roughness: 0.16, metalness: 0.94 });
        const deckMat = new THREE.MeshStandardMaterial({ color: 0xCBD0D6, roughness: 0.26, metalness: 0.90 });
        const chime = new THREE.Mesh(new THREE.TorusGeometry(0.516, 0.022, 16, 64), rimMat);
        chime.rotation.x = Math.PI / 2;
        chime.position.y = canTopY;
        grp.add(chime);
        const deck = new THREE.Mesh(new THREE.CylinderGeometry(0.495, 0.495, 0.018, 64), deckMat);
        deck.position.y = canTopY - 0.022;
        grp.add(deck);
        const rivet = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.03, 24), rimMat);
        rivet.position.y = canTopY;
        grp.add(rivet);
        const pullRing = new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.014, 12, 32), rimMat);
        pullRing.rotation.x = Math.PI / 2;
        pullRing.position.set(0, canTopY + 0.008, -0.14);
        grp.add(pullRing);
        const tabBlade = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.016, 0.18), rimMat);
        tabBlade.position.set(0, canTopY + 0.008, 0.04);
        grp.add(tabBlade);
      }

      offScene.add(grp);

      const centerY = -1.25 + totalH * 0.5;
      let dist = 5.95, phi = 1.32, theta = 0.34;
      if (v.shape === "jar_lux") { dist = 5.15; phi = 1.18; theta = 0.38; }
      else if (v.shape === "wine_bordeaux") { dist = 6.75; phi = 1.38; theta = 0.28; }
      else if (v.shape === "doypack") { dist = 6.45; phi = 1.34; theta = 0.36; }
      else if (v.shape === "alu_can") { dist = 5.95; phi = 1.22; theta = 0.32; }
      else if (v.shape === "square_soft") { dist = 6.05; phi = 1.32; theta = 0.48; }

      offCam.position.set(
        dist * Math.sin(phi) * Math.sin(theta),
        centerY + dist * Math.cos(phi),
        dist * Math.sin(phi) * Math.cos(theta)
      );
      offCam.lookAt(0, centerY, 0);
      offRenderer.clear();
      offRenderer.render(offScene, offCam);

      VESSEL_REALISTIC_THUMBS[v.id] = offCanvas.toDataURL("image/png");
      offScene.remove(grp);
      grp.traverse(obj => {
        if (obj.geometry) obj.geometry.dispose();
        if (obj.material) obj.material.dispose();
      });
    });

    doypackTex.dispose();
    shTex.dispose();
    offRenderer.dispose();
  } catch (e) {
    console.warn("Thumb renderer fallback:", e);
  }
}

function getVesselRealisticThumb(v) {
  return VESSEL_REALISTIC_THUMBS[v.id] || "";
}

function renderCatalogView() {
  const l = state.lang;
  const pills = [
    { id: "all", it: "Tutti", en: "All" },
    { id: "cylindrical", it: "Flacone Cilindrico", en: "Cylindrical Bottle" },
    { id: "square", it: "Flacone Quadro", en: "Square Bottle" },
    { id: "wine", it: "Bottiglia", en: "Bottle" },
    { id: "jars", it: "Vaso", en: "Jar" },
    { id: "cans", it: "Lattina", en: "Can" },
    { id: "flexibles", it: "Doypack", en: "Doypack" }
  ];
  const eyeEl = document.getElementById("ui_cat_eye");
  if (eyeEl) eyeEl.textContent = l === "it" ? "SELEZIONE CONTENITORE CERTIFICATO" : "CERTIFIED CONTAINER SELECTION";
  const titleEl = document.getElementById("ui_cat_title");
  if (titleEl) titleEl.textContent = l === "it" ? "Marketplace Contenitori" : "Container Marketplace";
  const catCodeEl = document.getElementById("ui_cat_code");
  if (catCodeEl) catCodeEl.textContent = "06 ARCHETIPI PRIMARI · QUOTE 1:1";
  const statEl = document.getElementById("ui_cat_stat");
  if (statEl) statEl.textContent = l === "it" ? "Scegli il contenitore per avviare lo Studio 3D" : "Pick a vessel to launch the 3D Studio";
  const customBtn = document.getElementById("btnCustomVessel");
  if (customBtn) customBtn.textContent = l === "it" ? "Continua con il mio contenitore" : "Continue with my container";

  document.getElementById("catPillarPills").innerHTML = pills.map(p => `
    <button class="p-pill ${state.activeCatGroup === p.id ? "active" : ""}" onclick="state.activeCatGroup='${p.id}'; renderCatalogView();">
      ${l === "it" ? p.it : p.en}
    </button>
  `).join("");

  const filtered = VESSELS.filter(v => state.activeCatGroup === "all" || v.catGroup === state.activeCatGroup);
  document.getElementById("catGrid").innerHTML = filtered.map(v => {
    const isFav = isVesselFavorite(v.id);
    const thumbUrl = getVesselRealisticThumb(v);
    const visualMarkup = thumbUrl
      ? `<img class="cat-real-img" src="${thumbUrl}" alt="${l === "it" ? v.it : v.en}">`
      : renderCatalogThumbSVG(v);
    return `
      <div class="cat-card" onclick="selectVesselFromMarketplace('${v.id}')">
        <div class="cat-stage">
          ${visualMarkup}
        </div>
        <div class="cat-meta-body">
          <div class="cat-title-row">
            <div class="cat-meta-title">${l === "it" ? v.it : v.en}</div>
            <button type="button" class="fav-heart-btn ${isFav ? "active" : ""}" data-fav-vid="${v.id}" onclick="toggleFavoriteVessel('${v.id}', event)" title="${l === "it" ? (isFav ? "Rimuovi dai preferiti" : "Salva nei preferiti") : (isFav ? "Remove from favorites" : "Save to favorites")}" aria-label="${l === "it" ? "Preferiti" : "Favorite"}">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="${isFav ? "currentColor" : "none"}" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            </button>
          </div>
          ${renderVesselTwoColSpecs(v, l)}
          <div class="cat-meta-footer">
            <button type="button" class="cat-select-btn" onclick="event.stopPropagation(); selectVesselFromMarketplace('${v.id}')">
              ${l === "it" ? "Seleziona" : "Select"}
            </button>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// ==================== VIEW 03: STEP-BY-STEP SUPPLY CHAIN WIZARD ====================
function renderPillarsView() {
  const l = state.lang;
  const v = getVessel();
  const phys = evaluateLivePhysics();
  const chain = getActiveSupplyChain(phys);
  const steps = chain.steps;
  const totalSteps = steps.length + 1; // Production Steps (1..N) + Extra Step (N+1): Riempimento Lotto Prova
  const allowedFillTypes = ensureValidCopackerFillType(v);
  const canFill = isFillingPossibleForState(v) && allowedFillTypes.length > 0;
  const isCan = v.shape === "alu_can";
  if (!canFill && state.copackerFilling) state.copackerFilling = false;
  const fillingConflict = phys.isBulk && state.copackerFilling;

  // Step 1 (container) is always fixed/pre-selected at index 0
  if (state.selectedSuppliers.container === undefined) state.selectedSuppliers.container = 0;

  const maxUnlocked = getFilieraMaxUnlocked(steps);
  if (!state.filieraStep || state.filieraStep < 1) state.filieraStep = 1;
  if (state.filieraStep > maxUnlocked) state.filieraStep = maxUnlocked;
  if (state.filieraStep > totalSteps) state.filieraStep = totalSteps;

  const cur = state.filieraStep;

  // 1. Top Progress Stepper Bar (read-only indicator pills)
  const stepperHtml = [
    ...steps.map((s, idx) => {
      const n = idx + 1;
      const isDone = n < cur;
      const isCur = n === cur;
      const cls = isCur ? "fstep-pill active" : (isDone ? "fstep-pill done" : "fstep-pill upcoming");
      return `
        <div class="${cls}">
          <span class="fstep-num">${isDone && !isCur ? "✓" : String(n).padStart(2, "0")}</span>
          <span>${l === "it" ? s.tagIt : s.tagEn}</span>
        </div>
      `;
    }),
    (() => {
      const n = totalSteps;
      const isCur = cur === n;
      const cls = isCur ? "fstep-pill active" : "fstep-pill upcoming";
      return `
        <div class="${cls}">
          <span class="fstep-num">${String(n).padStart(2, "0")}</span>
          <span>${l === "it" ? "RIEMPIMENTO E RICHIESTA" : "FILLING AND REQUEST"}</span>
        </div>
      `;
    })()
  ].join("");

  // 2. Confirmed Suppliers Summary Bar (Steps 2..N+1; non-clickable chips, keeps same label across all steps)
  let confirmedBarHtml = "";
  if (cur > 1) {
    const chipsHtml = steps.slice(0, cur - 1).map((s, idx) => {
      const chosen = s.options[state.selectedSuppliers[s.key] ?? 0];
      return `
        <div class="f-chip">
          <span>✓ ${String(idx + 1).padStart(2, "0")}: ${chosen ? chosen.name : s.title}</span>
          <span class="mono" style="color:var(--crimson);">€${s.cost}</span>
        </div>
      `;
    }).join("");
    confirmedBarHtml = `
      <div class="filiera-confirmed-bar">
        <div style="display:flex; flex-direction:column; gap:5px;">
          <span style="font-size:10px; font-weight:800; color:var(--slate); letter-spacing:0.08em;">${l === "it" ? "FORNITORI CONFERMATI FINORA" : "CONFIRMED SUPPLIERS SO FAR"}</span>
          <div class="filiera-confirmed-chips">${chipsHtml}</div>
        </div>
      </div>
    `;
  }

  // 3. Single Active Stage Card (ONLY Step cur!)
  let stageHtml = "";
  const isFinalFillingStep = (cur === totalSteps);
  const stageAnimStyle = (state._lastFilieraStep === cur) ? ' style="animation:none;"' : "";
  state._lastFilieraStep = cur;

  if (!isFinalFillingStep) {
    const step = steps[cur - 1];
    const selIdx = state.selectedSuppliers[step.key];
    const hasSel = (selIdx !== undefined);

    if (step.lockedFixed) {
      const opt = step.options[0];
      stageHtml = `
        <div class="filiera-stage-card"${stageAnimStyle}>
          <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; flex-wrap:wrap;">
            <div>
              <span style="font-family:var(--mono); font-size:10.5px; font-weight:800; color:var(--crimson);">STEP 01 / 0${totalSteps} · ${l === "it" ? step.tagIt : step.tagEn}</span>
              <h2 style="font-size:21px; font-weight:800; margin-top:4px; color:var(--ink);">${step.title}</h2>
              <p style="font-size:12.5px; color:var(--slate); margin-top:3px;">${step.spec} · ${step.badge}</p>
            </div>
            <span class="spec-tag ok">${l === "it" ? "PRODUTTORE PRE-SELEZIONATO ✓" : "PRE-SELECTED MANUFACTURER ✓"}</span>
          </div>

          <div class="supplier-list-rich">
            <div class="supplier-rich-opt selected" style="cursor:default;">
              <div style="flex:1;">
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                  <span class="sup-name" style="font-size:15.5px; font-weight:800; color:var(--ink);">${opt.name}</span>
                  <span class="rating-pill"><span class="rating-stars">★★★★★</span> ${opt.rating} <span class="rating-rev" style="font-weight:500; color:var(--slate);">(${opt.reviews} ${l === "it" ? "recensioni" : "reviews"})</span></span>
                </div>
                <div class="sup-desc" style="font-size:12px; color:var(--charcoal); margin-top:4px;">${opt.sub}</div>
                <div class="meta-tags-row">
                  <span class="meta-tag">${opt.cert}</span>
                  <span class="meta-tag">${l === "it" ? `Consegna prevista: ${opt.leadIt}` : `Estimated delivery: ${opt.leadEn}`}</span>
                </div>
              </div>
              <div class="supplier-rich-right">
                <strong class="sup-price" style="font-family:var(--mono); font-size:17px; color:var(--ink);">€${step.cost}</strong>
                <span class="sup-alloc" style="font-size:10.5px; font-weight:700; color:var(--green);">${l === "it" ? "Quota lotto prova" : "Trial allocation"}</span>
              </div>
            </div>
          </div>

          <p class="filiera-locked-red-text">
            ${l === "it"
              ? "Il produttore del contenitore è vincolato al modello scelto: per cambiarlo torna nel Marketplace (tasto &lt; in alto) e seleziona un altro flacone."
              : "The container manufacturer is tied to the chosen model: to change it, return to the Marketplace (&lt; button above) and select another vessel."}
          </p>

          <div class="filiera-nav-row" style="justify-content:flex-end;">
            <button id="btnFilieraNext" class="cta-btn" style="width:auto; min-width:220px; padding:0 24px;" onclick="nextFilieraStep()">
              ${l === "it" ? "Conferma" : "Confirm"}
            </button>
          </div>
        </div>
      `;
    } else {
      const optsHtml = step.options.map((opt, oIdx) => {
        const isSel = (selIdx === oIdx);
        const isLowest = (opt.price === step.minCost);
        const cls = `supplier-rich-opt${opt.sponsored ? " sponsored" : ""}${isSel ? " selected" : ""}`;
        return `
          <button class="${cls}" onclick="selectStepSupplier('${step.key}', ${oIdx})">
            <div style="flex:1;">
              <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                ${opt.sponsored ? `<span class="sponsored-badge">${l === "it" ? "SPONSORIZZATO" : "SPONSORED"}</span>` : ""}
                ${isLowest ? `<span class="lowest-price-badge">${l === "it" ? "PREZZO PIÙ BASSO" : "LOWEST PRICE"}</span>` : ""}
                <span class="sup-name" style="font-size:15px; font-weight:800; color:var(--ink);">${opt.name}</span>
                <span class="rating-pill"><span class="rating-stars">★★★★★</span> ${opt.rating} <span class="rating-rev" style="font-weight:500; color:var(--slate);">(${opt.reviews} ${l === "it" ? "recensioni" : "reviews"})</span></span>
              </div>
              <div class="sup-desc" style="font-size:12px; color:var(--charcoal); margin-top:4px;">${opt.sub}</div>
              <div class="meta-tags-row">
                <span class="meta-tag">${opt.cert}</span>
                <span class="meta-tag">${l === "it" ? `Consegna prevista: ${opt.leadIt}` : `Estimated delivery: ${opt.leadEn}`}</span>
              </div>
            </div>
            <div class="supplier-rich-right">
              <strong class="sup-price" style="font-family:var(--mono); font-size:17px; color:var(--ink);">€${opt.price}</strong>
              <span class="spec-tag sup-sel-tag ${isSel ? "ok" : ""}">${isSel ? (l === "it" ? "SELEZIONATO ✓" : "SELECTED ✓") : (l === "it" ? "SELEZIONA →" : "SELECT →")}</span>
            </div>
          </button>
        `;
      }).join("");

      stageHtml = `
        <div class="filiera-stage-card"${stageAnimStyle}>
          <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; flex-wrap:wrap;">
            <div>
              <span style="font-family:var(--mono); font-size:10.5px; font-weight:800; color:var(--crimson);">STEP 0${cur} / 0${totalSteps} · ${l === "it" ? step.tagIt : step.tagEn}</span>
              <h2 style="font-size:21px; font-weight:800; margin-top:4px; color:var(--ink);">${step.title}</h2>
              <p style="font-size:12.5px; color:var(--slate); margin-top:3px;">${step.spec} · ${step.badge}</p>
            </div>
            <span id="filieraStepStatusBadge" class="spec-tag ${hasSel ? "ok" : ""}">${hasSel ? (l === "it" ? "AZIENDA SELEZIONATA ✓" : "SUPPLIER SELECTED ✓") : (l === "it" ? "SCEGLI UN FORNITORE" : "CHOOSE A SUPPLIER")}</span>
          </div>

          <div class="supplier-list-rich" id="activeSupplierList">${optsHtml}</div>

          <div class="filiera-nav-row">
            <button id="btnFilieraPrev" class="cta-btn white" style="width:auto; min-width:200px; padding:0 24px;" onclick="prevFilieraStep()">${l === "it" ? "Torna indietro" : "Go back"}</button>
            <button id="btnFilieraNext" class="cta-btn" style="width:auto; min-width:220px; padding:0 24px;" ${hasSel ? "" : "disabled"} onclick="nextFilieraStep()">
              ${l === "it" ? "Conferma" : "Confirm"}
            </button>
          </div>
        </div>
      `;
    }
  } else {
    // EXTRA FINAL STEP (Step N+1): RIEMPIMENTO + SUMMARY + CHECKOUT
    const copackerChosen = steps[steps.length - 1]?.options[state.selectedSuppliers.copacker ?? 0];
    const fillExtra = chain.fillExtra;
    const summaryRows = steps.map(s => {
      const chosen = s.options[state.selectedSuppliers[s.key] ?? 0];
      return `
        <div class="supply-card" style="padding:8px 12px;">
          <span><strong>${l === "it" ? s.labelIt : s.labelEn}:</strong> ${chosen ? chosen.name : s.title}</span>
          <span class="spec-tag ok">€${s.cost} ✓</span>
        </div>
      `;
    }).join("");

    const allowedListTextIt = allowedFillTypes.length === 1
      ? `prodotti ${allowedFillTypes[0].it.toLowerCase()}`
      : (allowedFillTypes.length > 1
          ? `${allowedFillTypes.slice(0, -1).map(f => f.it.toLowerCase()).join(", ")} o ${allowedFillTypes[allowedFillTypes.length - 1].it.toLowerCase()}`
          : "");
    const allowedListTextEn = allowedFillTypes.length === 1
      ? `${allowedFillTypes[0].en.toLowerCase()} products`
      : (allowedFillTypes.length > 1
          ? `${allowedFillTypes.slice(0, -1).map(f => f.en.toLowerCase()).join(", ")}, or ${allowedFillTypes[allowedFillTypes.length - 1].en.toLowerCase()}`
          : "");
    const minFillCost = canFill ? Math.min(...allowedFillTypes.map(f => f.cost)) : 220;

    const fillingControlsHtml = `
      <div class="filling-mode-grid">
        <button id="btnFillNone" class="filling-mode-card ${!state.copackerFilling ? "active" : ""}" onclick="setCopackerFillMode(false)">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <strong style="font-size:14px; color:var(--ink);">${l === "it" ? "Solo Confezionamento Vuoto" : "Empty Assembly Only"}</strong>
            <span class="mono fill-price-green" style="font-weight:800; color:var(--green);">+€0</span>
          </div>
          <span class="fill-sub" style="font-size:11.5px; color:var(--slate); line-height:1.4;">
            ${l === "it" ? "Ricevi i contenitori vuoti, decorati e confezionati pronti per il test in linea." : "Receive decorated empty vessels packed for line testing."}
          </span>
        </button>

        <button id="btnFillAdd" class="filling-mode-card ${!canFill ? "disabled" : (state.copackerFilling ? "active" : "")}" ${canFill ? 'onclick="setCopackerFillMode(true)"' : "disabled"}>
          <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
            <strong style="font-size:14px; color:var(--ink);">${l === "it" ? "Aggiungi Riempimento" : "Add Filling"}</strong>
            ${canFill
              ? `<span class="mono fill-price-red" style="font-weight:800; color:var(--crimson);">${l === "it" ? `da ${minFillCost}€` : `from €${minFillCost}`}</span>`
              : `<span class="spec-tag" style="background:var(--bg-stone); color:var(--slate); border:1px solid var(--border);">${l === "it" ? "NON DISPONIBILE" : "UNAVAILABLE"}</span>`}
          </div>
          <span class="fill-sub" style="font-size:11.5px; color:var(--slate); line-height:1.4;">
            ${canFill
              ? (l === "it"
                  ? `Servizio aggiuntivo presso ${copackerChosen ? copackerChosen.name : "il Co-Packer"} su ${allowedListTextIt}.`
                  : `Added co-packer filling service for ${allowedListTextEn}.`)
              : (l === "it"
                  ? "Servizio non attivabile per questa configurazione."
                  : "Service not available for this configuration.")}
          </span>
        </button>
      </div>

      ${!canFill ? `
        <p class="filling-unavail-text">
          ${isCan
            ? (l === "it"
                ? "Riempimento non disponibile per le lattine: l'aggraffatura richiede linee dedicate; il co-packer esegue solo rivestimento e imballaggio."
                : "Filling unavailable for aluminum cans: seaming requires dedicated bottling lines; the co-packer handles decoration and packing only.")
            : (phys.isBulk && state.closureId === "none" && v.shape !== "doypack"
                ? (l === "it"
                    ? "Riempimento non disponibile: seleziona una chiusura e un'inscatolatura ordinata nello Studio 3D."
                    : "Filling unavailable: select a closure and ordered boxing in the 3D Studio.")
                : (phys.isBulk
                    ? (l === "it"
                        ? "Riempimento non disponibile con confezionamento sparso: seleziona un'inscatolatura ordinata nello Studio 3D."
                        : "Filling unavailable with loose bulk packing: select ordered boxing in the 3D Studio.")
                    : (l === "it"
                        ? "Riempimento non disponibile: seleziona una chiusura nello Studio 3D per poter sigillare il contenitore."
                        : "Filling unavailable: select a closure in the 3D Studio to seal the container.")))}
        </p>
      ` : (state.copackerFilling ? `
        <div class="filling-box">
          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
            <span style="font-size:11.5px; font-weight:800; color:var(--ink);">${l === "it" ? "TIPOLOGIA CONTENUTO DA RIEMPIRE" : "PRODUCT TYPE FOR FILLING"}</span>
          </div>
          <div class="fill-types-grid" style="display:grid; grid-template-columns:repeat(4, 1fr); gap:8px;">
            ${FILL_TYPES.map(ft => {
              const isAllowed = allowedFillTypes.some(a => a.id === ft.id);
              return `
                <button class="qty-btn ${isAllowed ? (state.copackerFillType === ft.id ? "active" : "") : "disabled"}" style="padding:8px 6px; font-size:12px;" ${isAllowed ? `onclick="setCopackerFillType('${ft.id}')"` : "disabled"}>
                  ${l === "it" ? ft.it : ft.en}
                  <small>+€${ft.cost}</small>
                </button>
              `;
            }).join("")}
          </div>
          <div style="font-size:11.5px; color:var(--crimson-dark); line-height:1.4; background:#FFFFFF; border:1px solid var(--border-light); padding:8px 10px; border-radius:5px;">
            ${l === "it"
              ? `Nota operativa: dovrai spedire manualmente a <strong>${copackerChosen ? copackerChosen.name : "il Co-Packer"}</strong> il contenuto sfuso da imbottigliare/dosare.`
              : `Operational note: you must manually ship bulk contents to <strong>${copackerChosen ? copackerChosen.name : "Co-Packer"}</strong>.`}
          </div>
        </div>
      ` : "")}
    `;

    const allProdSelected = steps.every(s => s.lockedFixed || state.selectedSuppliers[s.key] !== undefined);
    const canOrder = isFinalFillingStep && allProdSelected && phys.status !== "r";

    stageHtml = `
      <div class="filiera-stage-card"${stageAnimStyle}>
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px; flex-wrap:wrap;">
          <div>
            <span style="font-family:var(--mono); font-size:10.5px; font-weight:800; color:var(--crimson);">STEP 0${cur} / 0${totalSteps} · ${l === "it" ? "RIEMPIMENTO E RICHIESTA" : "FILLING AND REQUEST"}</span>
            <h2 style="font-size:21px; font-weight:800; margin-top:4px; color:var(--ink);">${l === "it" ? "Riempimento e Richiesta Prova" : "Filling and Trial Request"}</h2>
            <p style="font-size:12.5px; color:var(--slate); margin-top:3px;">${l === "it" ? "Scegli se richiedere il solo lotto prova vuoto oppure aggiungere il riempimento presso il Co-Packer selezionato." : "Choose empty trial vessels or add product filling at the selected Co-Packer."}</p>
          </div>
        </div>

        ${fillingControlsHtml}

        <div class="filiera-nav-row filiera-final-nav-row" style="align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap;">
          <div class="filiera-final-total-box" style="display:flex; flex-direction:column; gap:2px;">
            <span style="font-size:10px; font-weight:800; color:var(--slate); letter-spacing:0.06em;">${l === "it" ? "TOTALE LOTTO PROVA · SPEDIZIONI ESCLUSE" : "TRIAL BATCH TOTAL · SHIPPING EXCLUDED"}</span>
            <div style="font-size:16px; font-weight:800; color:var(--ink); font-family:var(--mono);">
              ${formatEuro(chain.totalCost)} <span style="font-size:12px; color:var(--crimson); font-weight:700;">(${formatEuro(chain.vcFee)} fee)</span>
            </div>
          </div>
          <div class="filiera-final-actions" style="display:flex; align-items:center; gap:10px; margin-left:auto;">
            <button id="btnFilieraPrev" class="cta-btn white" style="width:auto; min-width:180px; padding:0 22px;" onclick="prevFilieraStep()">${l === "it" ? "Torna indietro" : "Go back"}</button>
            <button id="btnOpenCheckout" class="cta-btn" style="width:auto; min-width:220px; padding:0 24px;" ${canOrder ? "" : "disabled"} onclick="submitTrialRequest()">
              ${phys.status === "r"
                ? (l === "it" ? "Risolvi errori" : "Resolve errors")
                : (l === "it" ? "Invia richiesta" : "Send request")}
            </button>
          </div>
        </div>
      </div>
    `;
  }

  document.getElementById("pillarsPortalBody").innerHTML = `
    <div class="brown-hdr-bar">
      <div>
        <h1 class="brown-hdr-title">${l === "it" ? "Selezione Passo-Passo Fornitori" : "Step-by-Step Supplier Selection"}</h1>
        <p class="cat-sub-minimal">${l === "it" ? "Componi la filiera desiderata per richiedere la prova" : "Compose your desired supply chain to request a trial"}</p>
      </div>
      <div class="brown-hdr-total-wrap" style="text-align:right;">
        <div class="brown-hdr-muted">${l === "it" ? "TOTALE LOTTO IN CORSO" : "LIVE TRIAL TOTAL"}</div>
        <div id="filieraTopTotal" class="brown-hdr-total">${formatEuro(chain.totalCost)}</div>
      </div>
    </div>

    <div class="filiera-stepper">${stepperHtml}</div>
    ${confirmedBarHtml}
    ${stageHtml}
  `;
}

// ==================== SUBMIT TRIAL REQUEST -> SAVE IN PROFILE & RETURN TO MARKETPLACE ====================
function submitTrialRequest() {
  const l = state.lang;
  const v = getVessel();
  const cl = getClosure();
  const fm = getFilm();
  const lp = getLabelPaper();
  const ink = getSerigrafiaInk();
  const pouchMode = isDoypack();
  const labelMode = isLabelMode();
  const serigMode = isSerigrafiaMode();
  const phys = evaluateLivePhysics();
  const chain = getActiveSupplyChain(phys);
  const wrapDesc = !hasWrap()
    ? (l === "it" ? "Contenitore neutro" : "Bare container")
    : (pouchMode
        ? `${state.pouchPrintType === "flexo" ? "Stampa Flessografica" : "Stampa Digitale"}`
        : (serigMode
            ? `${ink.name} 360°`
            : (labelMode ? `${lp.name}` : `${fm.name}`)));

  const now = new Date();
  const createdAt = `${String(now.getDate()).padStart(2, "0")}/${String(now.getMonth() + 1).padStart(2, "0")}/${now.getFullYear()} ${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;
  const reqNum = String(state.submittedRequests.length + 1).padStart(2, "0");
  const reqId = `#REQ-2026-${reqNum}`;

  const supplierItems = chain.steps.map(s => {
    const chosen = s.options[state.selectedSuppliers[s.key] ?? 0];
    return {
      name: chosen ? chosen.name : s.title,
      roleIt: s.labelIt,
      roleEn: s.labelEn,
      spec: s.title,
      cost: s.cost,
      status: "pending"
    };
  });
  if (chain.fillExtra > 0) {
    const copackerChosen = chain.steps[chain.steps.length - 1]?.options[state.selectedSuppliers.copacker ?? 0];
    supplierItems.push({
      name: copackerChosen ? copackerChosen.name : "Co-Packer",
      roleIt: "Riempimento",
      roleEn: "Filling",
      spec: state.copackerFillType,
      cost: chain.fillExtra,
      status: "pending"
    });
  }

  const savedReq = {
    id: reqId,
    createdAt,
    vesselIt: v.it,
    vesselEn: v.en,
    summaryLine: `${v.neck}${cl.id !== "none" ? ` + ${l === "it" ? cl.it : cl.en}` : ""} · ${wrapDesc} · Imballo ${phys.packQty} pz (${phys.cartonStr})`,
    totalCost: chain.totalCost,
    vcFee: chain.vcFee,
    acceptDays: ACCEPTANCE_DEADLINE_DAYS,
    suppliers: supplierItems
  };

  state.submittedRequests.unshift(savedReq);
  saveSubmittedRequests();
  updateProfileBadge();

  document.getElementById("checkoutModalBody").innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:1.5px solid var(--ink); padding-bottom:12px;">
      <div>
        <div style="font-size:10px; font-weight:800; color:var(--green); letter-spacing:0.12em;">${reqId} · ${l === "it" ? "SALVATA NEL TUO PROFILO" : "SAVED IN YOUR PROFILE"}</div>
        <h2 style="font-size:21px; font-weight:800; margin-top:3px; color:var(--ink);">${l === "it" ? "Richiesta inviata ✓" : "Request sent ✓"}</h2>
      </div>
    </div>

    <p style="font-size:12.5px; color:var(--charcoal); margin:12px 0; line-height:1.48;">
      ${l === "it"
        ? `La tua richiesta per <strong>${v.it}</strong> è stata inviata a tutti i fornitori selezionati ed è ora visibile nel tuo <strong>Profilo</strong>. Ogni azienda ha <strong>${ACCEPTANCE_DEADLINE_DAYS} giorni</strong> per accettare la lavorazione: il pagamento verrà richiesto solo se e quando tutti i fornitori confermeranno.`
        : `Your request for <strong>${v.en}</strong> has been sent to all selected suppliers and saved in your <strong>Profile</strong>. Every company has <strong>${ACCEPTANCE_DEADLINE_DAYS} days</strong> to accept: payment is requested only if and when all suppliers confirm.`}
    </p>

    <div style="display:flex; flex-direction:column; gap:6px; margin-bottom:14px; max-height:310px; overflow-y:auto;">
      ${supplierItems.map(sup => `
        <div class="req-sup-row">
          <div>
            <div style="font-weight:800; color:var(--ink);">${sup.name}</div>
            <div style="font-size:11px; color:var(--slate);">${l === "it" ? sup.roleIt : sup.roleEn} · ${sup.spec}</div>
          </div>
          <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
            <span class="req-deadline-pill">${l === "it" ? `Limite: ${ACCEPTANCE_DEADLINE_DAYS} gg` : `Limit: ${ACCEPTANCE_DEADLINE_DAYS}d`}</span>
            <span class="req-status-pill">${l === "it" ? "IN ATTESA" : "PENDING"}</span>
          </div>
        </div>
      `).join("")}
    </div>

    <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap; border-top:1px solid var(--border-light); padding-top:12px;">
      <button class="cta-btn white" style="width:auto; padding:0 18px;" onclick="document.getElementById('checkoutModal').classList.remove('open'); resetVesselConfigState('serum_250'); openProfileView();">
        ${l === "it" ? "Visualizza nel Profilo" : "View in Profile"}
      </button>
      <button id="btnReturnMarketplace" class="cta-btn" style="width:auto; min-width:210px; padding:0 22px;" onclick="returnToMarketplaceAfterSubmit(false)">
        ${l === "it" ? "Torna alla pagina iniziale" : "Return to home page"}
      </button>
    </div>
  `;
  document.getElementById("checkoutModal").classList.add("open");
}

function openCheckoutModal() {
  submitTrialRequest();
}

// ==================== BOOTSTRAP & QUERY PARAM SUPPORT ====================
window.addEventListener("DOMContentLoaded", () => {
  loadSubmittedRequests();
  loadFavoriteVessels();
  initWebGL();
  generatePhotorealisticVesselThumbnails();
  updateFavoritesBadges();
  const qs = new URLSearchParams(window.location.search);
  resetVesselConfigState(qs.get("vessel") || "serum_250");
  if (qs.get("custom") === "1") state.customVesselMode = true;
  if (qs.get("customgraphic") === "1") state.customGraphicMode = true;
  if (qs.get("wrap")) {
    state.wrapType = qs.get("wrap");
    if (state.wrapType === "pouch" && state.pouchPrintType === "none") state.pouchPrintType = qs.get("pouchprint") || "digital";
    if (state.wrapType !== "none" && state.skinId === "none") {
      state.skinId = qs.get("skin") || ((state.wrapType === "sleeve" || state.wrapType === "label") ? "neutral" : "lumina");
    }
  }
  if (qs.get("skin")) {
    state.skinId = qs.get("skin");
    if (getVessel().shape === "doypack" && state.wrapType === "none" && state.skinId !== "none") {
      state.wrapType = "pouch";
      state.pouchPrintType = qs.get("pouchprint") || "digital";
    }
  }
  if (qs.get("slang")) state.sleeveAngleDeg = Number(qs.get("slang"));
  if (qs.get("side") === "back") {
    state.bcDoypackSide = "back";
    camSpherical.theta = Math.PI + 0.22;
  }
  if (qs.get("bcx")) state.bcDoypackX = Number(qs.get("bcx"));
  if (qs.get("closure")) state.closureId = qs.get("closure");
  if (qs.get("tool") && qs.get("tool") !== "barcode") state.pointerTool = qs.get("tool");
  if (qs.get("slh")) state.sleeveHeightPct = Number(qs.get("slh"));
  if (qs.get("bch")) state.bcHeightPct = Number(qs.get("bch"));
  if (qs.get("boxmode") === "bulk" && isPlasticBottle(getVessel())) state.boxMode = "bulk";
  if (qs.get("bulkqty")) state.bulkQty = Number(qs.get("bulkqty"));
  if (qs.get("qty")) state.boxQty = Number(qs.get("qty"));
  if (qs.get("filling") === "1" && isFillingPossibleForState(getVessel())) state.copackerFilling = true;
  if (qs.get("filltype")) state.copackerFillType = qs.get("filltype");
  if (qs.get("exploded") === "1" && !evaluateLivePhysics().isNoCap) state.exploded = true;
  if (!evaluateLivePhysics().neckMatch) {
    state.exploded = true;
    state.explodeProgress = 1.0;
    const shp = getVessel().shape;
    if (shp === "wine_bordeaux") clampAndSetZoom(8.35, true);
    else if (shp === "jar_lux") clampAndSetZoom(5.45, true);
  } else if (state.exploded) {
    state.explodeProgress = 1.0;
  }
  if (qs.get("heatmap") === "1") state.heatmap = true;
  if (qs.get("tab")) state.inspTab = Number(qs.get("tab"));
  if (qs.get("lang")) state.lang = qs.get("lang");
  if (qs.get("fstep")) {
    const fTarget = Math.max(1, Number(qs.get("fstep")) || 1);
    const previewSteps = buildSupplyChainSteps(evaluateLivePhysics());
    previewSteps.slice(0, Math.max(0, fTarget - 1)).forEach(s => {
      if (state.selectedSuppliers[s.key] === undefined) state.selectedSuppliers[s.key] = 0;
    });
    state.filieraStep = fTarget;
  }
  const rawView = qs.get("view") || "catalog";
  let initialView = rawView;
  if (rawView === "custom-vessel") {
    state.customVesselMode = true;
    initialView = "studio";
  } else if (rawView === "custom-graphic") {
    state.customGraphicMode = true;
    initialView = "studio";
  }
  document.addEventListener("click", e => {
    if (!state.infoPopoverOpen) return;
    const pop = document.getElementById("vesselInfoPopover");
    const btn = document.getElementById("btnVesselInfo");
    if (pop && !pop.contains(e.target) && btn && !btn.contains(e.target)) {
      state.infoPopoverOpen = false;
      renderVesselInfoPopover();
    }
  });
  rebuild3DProduct();
  isApplyingHistoryState = true;
  switchMainView(initialView);
  isApplyingHistoryState = false;
  syncBrowserHistory(true);
  if (qs.get("modal") === "1") openCheckoutModal();
  animateWebGL();
});
</script>
</body>
</html>
"""
    html = html.replace("__VC_LOGO__", logo_b64).replace("__VC_FAVICON__", favicon_b64).replace("__THREE_JS__", three_js)
    out_file = BASE_DIR / "index.html"
    out_file.write_text(html, encoding="utf-8")
    print(f"Wrote {out_file} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
