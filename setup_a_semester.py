#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import argparse
import html
import shutil
import subprocess
import sys

ROOT = Path.cwd()
LESSON_COUNT = 13

GENERATED_MARK = "<!-- generated-by: setup_a_semester.py -->"

# ============================================================
# S semester review structure
# ============================================================

STAGES = [
    {
        "n": "01",
        "title": "文字・発音・名詞・冠詞",
        "desc": "スペイン語の読み方と、名詞の性・数、定冠詞・不定冠詞を整理する。",
        "points": [
            "スペイン語の文字と基本的な発音",
            "男性名詞・女性名詞",
            "単数形と複数形",
            "el / la / los / las",
            "un / una / unos / unas",
        ],
        "check": [
            ("「本」を表す libro は男性名詞？女性名詞？", "男性名詞。el libro / un libro。"),
            ("la casa の複数形は？", "las casas。"),
            ("unos libros の意味は？", "何冊かの本、いくつかの本。"),
        ],
        "files": [
            "2-1-alphabeto.html",
            "1-1.html",
            "1-1-words.html",
        ],
    },
    {
        "n": "02",
        "title": "形容詞と性・数一致",
        "desc": "名詞と形容詞の関係を整理し、語尾の変化を自然にできるようにする。",
        "points": [
            "形容詞は修飾する名詞の性・数に一致する",
            "-o / -a 型の基本変化",
            "-e 型など性で変化しない形容詞",
            "複数形",
            "基本的な語順",
        ],
        "check": [
            ("una casa + blanco はどうなる？", "una casa blanca"),
            ("libros + interesante の複数形は？", "libros interesantes"),
            ("chico alto の女性形は？", "chica alta"),
        ],
        "files": [
            "1-2.html",
            "1-3.html",
            "1-3-0.html",
        ],
    },
    {
        "n": "03",
        "title": "主語人称代名詞と ser",
        "desc": "yo / tú / él…と ser の活用を即答できる状態にする。",
        "points": [
            "yo / tú / él / ella / usted",
            "nosotros / vosotros / ellos / ustedes",
            "soy / eres / es",
            "somos / sois / son",
            "職業・出身・属性などの表現",
        ],
        "check": [
            ("Yo ___ estudiante.", "soy"),
            ("Nosotros ___ japoneses.", "somos"),
            ("María ___ profesora.", "es"),
        ],
        "files": [
            "1-4.html",
            "1-4-0.html",
            "1-5.html",
            "1-5-0.html",
            "1-5-1.html",
        ],
    },
    {
        "n": "04",
        "title": "ser・estar・hay",
        "desc": "日本語では同じ『〜である／いる／ある』に見える3表現を使い分ける。",
        "points": [
            "ser：属性・本質・職業・出身",
            "estar：状態・場所",
            "hay：不特定のものの存在",
            "estar の現在形",
            "場所を表す基本表現",
        ],
        "check": [
            ("Madrid ___ en España.", "está"),
            ("Mi padre ___ médico.", "es"),
            ("___ un libro en la mesa.", "Hay"),
        ],
        "files": [
            "1-6.html",
            "1-7.html",
            "test-04.html",
        ],
    },
    {
        "n": "05",
        "title": "規則動詞の現在形",
        "desc": "-ar / -er / -ir 動詞の現在形をまとめて復習する。",
        "points": [
            "-ar：hablo / hablas / habla…",
            "-er：como / comes / come…",
            "-ir：vivo / vives / vive…",
            "主語に応じた語尾変化",
            "主語省略",
        ],
        "check": [
            ("hablar の nosotros 形は？", "hablamos"),
            ("comer の tú 形は？", "comes"),
            ("vivir の ellos 形は？", "viven"),
        ],
        "files": [
            "1-8.html",
            "1-8-0.html",
            "1-9.html",
            "1-10.html",
            "1-10-0.html",
        ],
    },
    {
        "n": "06",
        "title": "不規則動詞",
        "desc": "Aセメ以降でも頻出する現在形の不規則活用を重点的に固める。",
        "points": [
            "tener",
            "venir",
            "hacer",
            "ir",
            "語幹母音変化",
            "一人称単数だけ不規則な動詞",
        ],
        "check": [
            ("tener の yo 形は？", "tengo"),
            ("ir の nosotros 形は？", "vamos"),
            ("hacer の yo 形は？", "hago"),
        ],
        "files": [
            "1-11.html",
            "2-1.html",
            "2-2.html",
            "2-2-words.html",
        ],
    },
    {
        "n": "07",
        "title": "所有・指示・疑問表現",
        "desc": "文を具体的にするための所有表現・疑問詞などをまとめる。",
        "points": [
            "mi / tu / su",
            "nuestro / vuestro",
            "qué / quién",
            "dónde / cuándo",
            "cómo / cuánto",
        ],
        "check": [
            ("『私の本』は？", "mi libro"),
            ("『どこ？』に対応する疑問詞は？", "dónde"),
            ("『誰？』に対応する疑問詞は？", "quién"),
        ],
        "files": [
            "2-3.html",
            "2-3-words.html",
            "2-4.html",
            "2-4-0.html",
            "2-4-words.html",
            "2-5.html",
            "2-5-words.html",
        ],
    },
    {
        "n": "08",
        "title": "否定・疑問・文の組み立て",
        "desc": "単語や活用を、実際のスペイン語の文に組み上げる練習。",
        "points": [
            "no を使った否定",
            "疑問文",
            "主語を省略した文",
            "語順",
            "日本語からスペイン語への変換",
        ],
        "check": [
            ("『私はスペイン語を話しません』の基本形は？", "No hablo español."),
            ("主語代名詞は常に必要？", "不要なことが多い。動詞の活用から主語が分かるため。"),
            ("¿Dónde vives? の意味は？", "どこに住んでいますか。"),
        ],
        "files": [
            "2-6.html",
            "2-6-words.html",
            "2-7.html",
            "2-7-words.html",
            "2-8.html",
            "2-8-0.html",
            "2-8-words.html",
        ],
    },
    {
        "n": "09",
        "title": "会話・読解",
        "desc": "個別文法ではなく、複数の知識を同時に使って文章を理解する。",
        "points": [
            "短い会話を読む",
            "質問にスペイン語で答える",
            "文脈から意味を判断する",
            "既習文法を混ぜて使う",
            "長めの文章に慣れる",
        ],
        "check": [
            ("会話問題で最初に確認するものは？", "誰が誰に話しているか、場面、動詞。"),
            ("未知語が1語あったら全文を止める？", "止めずに文脈と既知の文法から推測する。"),
            ("読解で動詞を先に探す利点は？", "文の骨格と主語・時制を把握しやすい。"),
        ],
        "files": [
            "2-9.html",
            "2-9-0.html",
            "2-9-words.html",
            "2-10.html",
            "2-10-words.html",
            "2-11.html",
            "2-11-words.html",
            "1-game.html",
        ],
    },
    {
        "n": "10",
        "title": "Sセメ総合",
        "desc": "単元別ではなく、Sセメスターの内容を混ぜて最終確認する。",
        "points": [
            "冠詞・名詞・形容詞",
            "ser / estar / hay",
            "規則・不規則動詞",
            "疑問・否定",
            "会話・読解",
            "苦手分野をStage 1〜9へ戻って復習",
        ],
        "check": [
            ("総合問題で活用を間違えた場合は？", "Stage 5〜6へ戻って活用を再確認する。"),
            ("ser / estar の判断に迷った場合は？", "Stage 4へ戻る。"),
            ("最終目標は暗記だけ？", "文脈の中で正しい形を自然に選べる状態。"),
        ],
        "files": [
            "test-00.html",
            "test-01.html",
            "test-02.html",
            "test-03.html",
            "test-0304ex.html",
            "test-04.html",
            "test-05.html",
            "test-06.html",
            "test-07.html",
            "test-radio.html",
            "index.html",
        ],
    },
]


# ============================================================
# Helpers
# ============================================================

def backup_if_needed(path: Path):
    if not path.exists():
        return

    try:
        old = path.read_text(encoding="utf-8")
    except Exception:
        return

    if GENERATED_MARK in old:
        return

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = path.with_name(path.name + f".bak-{stamp}")
    shutil.copy2(path, dst)
    print(f"backup: {path} -> {dst}")


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_if_needed(path)
    path.write_text(GENERATED_MARK + "\n" + content, encoding="utf-8")
    print("write:", path.relative_to(ROOT))


def shell(cmd):
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def existing_archive_links(files):
    out = []
    for name in files:
        p = ROOT / "archive" / "spanish" / name
        if p.exists():
            out.append(
                f'<a class="archive-link" href="../../archive/spanish/{html.escape(name)}">'
                f'{html.escape(name)}</a>'
            )
    return "\n".join(out)


def head(title, css_path):
    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{css_path}">
</head>
"""


# ============================================================
# CSS
# ============================================================

CSS = r"""
:root {
    --bg: #f5f6f8;
    --card: #ffffff;
    --text: #17191d;
    --sub: #686d76;
    --line: #e2e5e9;
    --accent: #3157d5;
    --accent-soft: #eef2ff;
    --good: #18864b;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family:
        -apple-system, BlinkMacSystemFont,
        "Segoe UI", "Noto Sans JP",
        "Hiragino Sans", sans-serif;
    line-height: 1.7;
}

a {
    color: inherit;
}

header {
    background: rgba(255,255,255,.92);
    border-bottom: 1px solid var(--line);
    position: sticky;
    top: 0;
    z-index: 10;
    backdrop-filter: blur(10px);
}

.nav {
    max-width: 1000px;
    margin: auto;
    padding: 13px 20px;
    display: flex;
    gap: 18px;
    align-items: center;
}

.nav a {
    text-decoration: none;
    font-size: 14px;
    color: var(--sub);
}

.nav .brand {
    color: var(--text);
    font-weight: 750;
    margin-right: auto;
}

main {
    max-width: 1000px;
    margin: auto;
    padding: 42px 20px 80px;
}

.hero {
    margin-bottom: 32px;
}

.eyebrow {
    color: var(--accent);
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
}

h1 {
    margin: 4px 0 7px;
    font-size: clamp(32px, 7vw, 52px);
    line-height: 1.18;
}

h2 {
    margin-top: 38px;
    font-size: 24px;
}

h3 {
    margin-top: 5px;
}

p.sub {
    color: var(--sub);
    margin-top: 4px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(245px, 1fr));
    gap: 15px;
}

.card {
    display: block;
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 17px;
    padding: 20px;
    text-decoration: none;
    transition: .15s ease;
}

a.card:hover {
    transform: translateY(-2px);
    border-color: #bfc8e9;
    box-shadow: 0 7px 24px rgba(0,0,0,.06);
}

.card-number {
    color: var(--accent);
    font-weight: 800;
    font-size: 13px;
}

.card-title {
    font-weight: 750;
    font-size: 18px;
    margin: 5px 0 4px;
}

.card-desc {
    color: var(--sub);
    font-size: 14px;
}

.badge {
    display: inline-block;
    border-radius: 999px;
    padding: 3px 9px;
    font-size: 12px;
    background: #eceef2;
    color: var(--sub);
}

.badge.done {
    background: #e3f7eb;
    color: var(--good);
}

.progress {
    height: 10px;
    overflow: hidden;
    border-radius: 99px;
    background: #e9ebef;
    margin: 11px 0 6px;
}

.progress > div {
    height: 100%;
    width: 0;
    background: var(--accent);
    transition: width .25s ease;
}

.big-progress {
    background: var(--card);
    padding: 20px;
    border: 1px solid var(--line);
    border-radius: 17px;
    margin: 20px 0 26px;
}

.section {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 17px;
    padding: 22px;
    margin: 16px 0;
}

ul {
    padding-left: 23px;
}

li {
    margin: 5px 0;
}

details {
    background: #fafafa;
    border: 1px solid var(--line);
    border-radius: 11px;
    padding: 11px 14px;
    margin: 9px 0;
}

summary {
    cursor: pointer;
    font-weight: 650;
}

.archive-links {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.archive-link {
    display: inline-block;
    padding: 7px 11px;
    border: 1px solid var(--line);
    border-radius: 10px;
    background: #fafafa;
    text-decoration: none;
    font-size: 13px;
}

.archive-link:hover {
    border-color: var(--accent);
}

button {
    border: 0;
    border-radius: 11px;
    background: var(--accent);
    color: white;
    padding: 11px 18px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
}

button.secondary {
    background: #e9ecf4;
    color: var(--text);
}

.stage-nav {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin-top: 30px;
}

.stage-nav a {
    text-decoration: none;
    padding: 10px 14px;
    border-radius: 10px;
    background: var(--card);
    border: 1px solid var(--line);
}

textarea,
input[type=text] {
    width: 100%;
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 12px;
    background: white;
    color: var(--text);
    font: inherit;
}

textarea {
    min-height: 160px;
    resize: vertical;
}

label {
    display: block;
    font-weight: 700;
    margin: 18px 0 7px;
}

.lesson-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(155px, 1fr));
    gap: 10px;
}

.lesson-list a {
    background: white;
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 14px;
    text-decoration: none;
}

.small {
    font-size: 13px;
    color: var(--sub);
}

footer {
    color: var(--sub);
    font-size: 12px;
    text-align: center;
    padding: 30px;
}
"""


# ============================================================
# JS
# ============================================================

JS = r"""
(() => {
    const PROGRESS_KEY = "study.spanish.review.v1";

    function getDone() {
        try {
            const v = JSON.parse(localStorage.getItem(PROGRESS_KEY) || "[]");
            return Array.isArray(v) ? v : [];
        } catch {
            return [];
        }
    }

    function setDone(stage, value) {
        const s = new Set(getDone());

        if (value) s.add(stage);
        else s.delete(stage);

        localStorage.setItem(PROGRESS_KEY, JSON.stringify([...s].sort()));
        update();
    }

    function update() {
        const done = getDone();

        document.querySelectorAll("[data-stage-card]").forEach(card => {
            const n = card.dataset.stageCard;
            const badge = card.querySelector("[data-stage-badge]");

            if (!badge) return;

            if (done.includes(n)) {
                badge.textContent = "✓ 完了";
                badge.classList.add("done");
            } else {
                badge.textContent = "未完了";
                badge.classList.remove("done");
            }
        });

        const count = done.length;
        const pct = Math.min(100, count * 10);

        document.querySelectorAll("[data-progress-bar]").forEach(x => {
            x.style.width = pct + "%";
        });

        document.querySelectorAll("[data-progress-text]").forEach(x => {
            x.textContent = `${count} / 10 completed`;
        });

        document.querySelectorAll("[data-stage-toggle]").forEach(btn => {
            const n = btn.dataset.stageToggle;
            const finished = done.includes(n);

            btn.textContent = finished ? "✓ 完了済み — 未完了に戻す" : "このStageを完了にする";
            btn.classList.toggle("secondary", finished);
        });
    }

    document.addEventListener("click", e => {
        const btn = e.target.closest("[data-stage-toggle]");
        if (!btn) return;

        const n = btn.dataset.stageToggle;
        const done = getDone();

        setDone(n, !done.includes(n));
    });

    document.querySelectorAll("[data-persist]").forEach(el => {
        const key = el.dataset.persist;
        const old = localStorage.getItem(key);

        if (old !== null) {
            el.value = old;
        }

        el.addEventListener("input", () => {
            localStorage.setItem(key, el.value);
        });
    });

    update();
})();
"""


# ============================================================
# Root index
# ============================================================

def root_index():
    return head("Study", "assets/site.css") + """
<body>
<header>
<div class="nav">
<a class="brand" href="./">Study</a>
<a href="spanish/">Spanish</a>
<a href="archive/">Archive</a>
</div>
</header>

<main>
<div class="hero">
<div class="eyebrow">2026 A Semester</div>
<h1>Study</h1>
<p class="sub">今学期の学習ページと、過去の教材をまとめた入口。</p>
</div>

<div class="grid">
<a class="card" href="spanish/">
<div class="card-number">CURRENT</div>
<div class="card-title">🇪🇸 Spanish — A Semester</div>
<div class="card-desc">
Aセメスターの授業・復習・学習メモ。
</div>
</a>

<a class="card" href="spanish/review/">
<div class="card-number">REVIEW</div>
<div class="card-title">Sセメ総復習</div>
<div class="card-desc">
Sセメスターの内容を10段階で総復習。
</div>
</a>

<a class="card" href="archive/">
<div class="card-number">ARCHIVE</div>
<div class="card-title">Archive</div>
<div class="card-desc">
過去の教材・演習・テストを見る。
</div>
</a>
</div>
</main>

<footer>28q Study</footer>
<script src="assets/site.js"></script>
</body>
</html>
"""


# ============================================================
# Archive
# ============================================================

def archive_index():
    archive = ROOT / "archive" / "spanish"

    files = sorted(
        p.name for p in archive.iterdir()
        if p.is_file() and p.suffix.lower() in {".html", ".json"}
    )

    tests = [x for x in files if x.startswith("test-")]
    words = [x for x in files if "words" in x]
    normal = [
        x for x in files
        if x not in tests and x not in words and x != "index.html"
    ]

    def links(items):
        return "\n".join(
            f'<a class="archive-link" href="spanish/{html.escape(x)}">{html.escape(x)}</a>'
            for x in items
        )

    return head("Archive", "../assets/site.css") + f"""
<body>
<header>
<div class="nav">
<a class="brand" href="../">Study</a>
<a href="../spanish/">Spanish</a>
<a href="./">Archive</a>
</div>
</header>

<main>
<div class="hero">
<div class="eyebrow">Archive</div>
<h1>過去の教材</h1>
<p class="sub">今まで作った教材をそのまま残して参照できる場所。</p>
</div>

<a class="card" href="spanish/index.html">
<div class="card-number">2026 S SEMESTER</div>
<div class="card-title">🇪🇸 Spanish</div>
<div class="card-desc">Sセメスターで使用したスペイン語教材。</div>
</a>

<h2>通常教材</h2>
<div class="archive-links">
{links(normal)}
</div>

<h2>単語</h2>
<div class="archive-links">
{links(words)}
</div>

<h2>テスト</h2>
<div class="archive-links">
{links(tests)}
</div>

</main>

<footer>Archive</footer>
<script src="../assets/site.js"></script>
</body>
</html>
"""


# ============================================================
# Spanish A semester top
# ============================================================

def spanish_index():
    return head("Spanish — A Semester", "../assets/site.css") + """
<body>
<header>
<div class="nav">
<a class="brand" href="../">Study</a>
<a href="./">Spanish</a>
<a href="../archive/">Archive</a>
</div>
</header>

<main>

<div class="hero">
<div class="eyebrow">2026 A Semester</div>
<h1>🇪🇸 Español</h1>
<p class="sub">
Aセメスターの学習拠点。
最初にSセメ総復習を終わらせ、その後Aセメの授業内容を蓄積していく。
</p>
</div>

<div class="big-progress">
<strong>Sセメ総復習</strong>
<div class="progress"><div data-progress-bar></div></div>
<div class="small" data-progress-text>0 / 10 completed</div>
<br>
<a href="review/">10段階復習を開く →</a>
</div>

<div class="grid">

<a class="card" href="lesson/">
<div class="card-number">A SEMESTER</div>
<div class="card-title">授業</div>
<div class="card-desc">
各回の授業内容・宿題・重要事項を保存。
</div>
</a>

<a class="card" href="review/">
<div class="card-number">PREPARATION</div>
<div class="card-title">Sセメ総復習</div>
<div class="card-desc">
Aセメに入る前に10 Stageで基礎を再構成。
</div>
</a>

<a class="card" href="../archive/spanish/index.html">
<div class="card-number">REFERENCE</div>
<div class="card-title">Sセメ Archive</div>
<div class="card-desc">
以前の問題・単語・テストをそのまま参照。
</div>
</a>

</div>

<h2>学習メモ</h2>

<div class="section">
<p class="small">
この欄はブラウザに自動保存されます。
</p>
<textarea
    data-persist="study.spanish.asem.dashboard.memo"
    placeholder="今週やること、苦手な部分、授業予定など..."
></textarea>
</div>

</main>

<footer>Español — 2026 A</footer>
<script src="../assets/site.js"></script>
</body>
</html>
"""


# ============================================================
# Review index
# ============================================================

def review_index():
    cards = []

    for s in STAGES:
        cards.append(f"""
<a class="card" data-stage-card="{s['n']}" href="{s['n']}.html">
<div class="card-number">STAGE {s['n']}</div>
<div class="card-title">{html.escape(s['title'])}</div>
<div class="card-desc">{html.escape(s['desc'])}</div>
<br>
<span class="badge" data-stage-badge>未完了</span>
</a>
""")

    return head("Sセメ総復習", "../../assets/site.css") + f"""
<body>

<header>
<div class="nav">
<a class="brand" href="../../">Study</a>
<a href="../">Spanish</a>
<a href="../../archive/spanish/">S Archive</a>
</div>
</header>

<main>

<div class="hero">
<div class="eyebrow">Preparation</div>
<h1>Sセメ総復習</h1>
<p class="sub">
Aセメスターに入る前に、Sセメの内容を依存関係順に10段階で整理する。
</p>
</div>

<div class="big-progress">
<strong>Progress</strong>
<div class="progress"><div data-progress-bar></div></div>
<div class="small" data-progress-text>0 / 10 completed</div>
</div>

<div class="grid">
{''.join(cards)}
</div>

</main>

<footer>S Semester Review</footer>
<script src="../../assets/site.js"></script>
</body>
</html>
"""


# ============================================================
# Review pages
# ============================================================

def review_page(stage):
    i = int(stage["n"])

    points = "\n".join(
        f"<li>{html.escape(x)}</li>"
        for x in stage["points"]
    )

    checks = "\n".join(
        f"""
<details>
<summary>{html.escape(q)}</summary>
<p>{html.escape(a)}</p>
</details>
"""
        for q, a in stage["check"]
    )

    links = existing_archive_links(stage["files"])

    prev_link = ""
    next_link = ""

    if i > 1:
        prev_link = f'<a href="{i-1:02d}.html">← Stage {i-1:02d}</a>'

    if i < 10:
        next_link = f'<a href="{i+1:02d}.html">Stage {i+1:02d} →</a>'
    else:
        next_link = '<a href="../">Aセメへ →</a>'

    return head(
        f"Stage {stage['n']} — {stage['title']}",
        "../../assets/site.css"
    ) + f"""
<body>

<header>
<div class="nav">
<a class="brand" href="../../">Study</a>
<a href="../">Spanish</a>
<a href="./">Review</a>
</div>
</header>

<main>

<div class="hero">
<div class="eyebrow">Stage {stage['n']} / 10</div>
<h1>{html.escape(stage['title'])}</h1>
<p class="sub">{html.escape(stage['desc'])}</p>
</div>

<div class="section">
<h2>このStageで整理すること</h2>
<ul>
{points}
</ul>
</div>

<div class="section">
<h2>セルフチェック</h2>
<p class="small">
一度自分で答えてから「答えを見る」を開く。
</p>
{checks}
</div>

<div class="section">
<h2>Sセメ教材</h2>
<p class="small">
このStageに関連する元の教材。
</p>
<div class="archive-links">
{links}
</div>
</div>

<div class="section">
<button data-stage-toggle="{stage['n']}">
このStageを完了にする
</button>
</div>

<div class="stage-nav">
<div>{prev_link}</div>
<div>{next_link}</div>
</div>

</main>

<footer>Stage {stage['n']}</footer>
<script src="../../assets/site.js"></script>

</body>
</html>
"""


# ============================================================
# Lessons
# ============================================================

def lesson_index():
    links = "\n".join(
        f'<a href="{i:02d}.html"><strong>第{i}回</strong><br>'
        f'<span class="small">授業メモ</span></a>'
        for i in range(1, LESSON_COUNT + 1)
    )

    return head("Aセメ授業", "../../assets/site.css") + f"""
<body>

<header>
<div class="nav">
<a class="brand" href="../../">Study</a>
<a href="../">Spanish</a>
<a href="../review/">Review</a>
</div>
</header>

<main>

<div class="hero">
<div class="eyebrow">2026 A Semester</div>
<h1>授業</h1>
<p class="sub">
各回の内容・宿題・語彙を記録する。入力内容はブラウザに自動保存。
</p>
</div>

<div class="lesson-list">
{links}
</div>

</main>

<footer>A Semester Lessons</footer>
<script src="../../assets/site.js"></script>
</body>
</html>
"""


def lesson_page(i):
    n = f"{i:02d}"

    prev_link = (
        f'<a href="{i-1:02d}.html">← 第{i-1}回</a>'
        if i > 1 else ""
    )

    next_link = (
        f'<a href="{i+1:02d}.html">第{i+1}回 →</a>'
        if i < LESSON_COUNT else ""
    )

    return head(f"Spanish 第{i}回", "../../assets/site.css") + f"""
<body>

<header>
<div class="nav">
<a class="brand" href="../../">Study</a>
<a href="../">Spanish</a>
<a href="./">授業一覧</a>
</div>
</header>

<main>

<div class="hero">
<div class="eyebrow">2026 A Semester</div>
<h1>第{i}回</h1>
<p class="sub">授業内容をここに蓄積する。</p>
</div>

<div class="section">

<label>タイトル / 日付</label>
<input
    type="text"
    data-persist="study.spanish.asem.lesson.{n}.title"
    placeholder="例: 10/3 第1回"
/>

<label>授業メモ</label>
<textarea
    data-persist="study.spanish.asem.lesson.{n}.notes"
    placeholder="文法・例文・先生の説明など..."
></textarea>

<label>重要語彙</label>
<textarea
    data-persist="study.spanish.asem.lesson.{n}.words"
    placeholder="単語 : 意味..."
></textarea>

<label>宿題 / 次回まで</label>
<textarea
    data-persist="study.spanish.asem.lesson.{n}.homework"
    placeholder="宿題、暗記、復習内容..."
></textarea>

</div>

<div class="stage-nav">
<div>{prev_link}</div>
<div>{next_link}</div>
</div>

</main>

<footer>Spanish Lesson {n}</footer>
<script src="../../assets/site.js"></script>
</body>
</html>
"""


# ============================================================
# Generate
# ============================================================

def generate():
    if not (ROOT / ".git").exists():
        print(
            "ERROR: study リポジトリのルートで実行してください。",
            file=sys.stderr
        )
        print("現在:", ROOT, file=sys.stderr)
        sys.exit(1)

    if not (ROOT / "archive" / "spanish").is_dir():
        print(
            "ERROR: archive/spanish が見つかりません。",
            file=sys.stderr
        )
        sys.exit(1)

    write(ROOT / "assets" / "site.css", CSS)
    write(ROOT / "assets" / "site.js", JS)

    write(ROOT / "index.html", root_index())
    write(ROOT / "archive" / "index.html", archive_index())

    write(ROOT / "spanish" / "index.html", spanish_index())

    write(
        ROOT / "spanish" / "review" / "index.html",
        review_index()
    )

    for stage in STAGES:
        write(
            ROOT / "spanish" / "review" / f"{stage['n']}.html",
            review_page(stage)
        )

    write(
        ROOT / "spanish" / "lesson" / "index.html",
        lesson_index()
    )

    for i in range(1, LESSON_COUNT + 1):
        write(
            ROOT / "spanish" / "lesson" / f"{i:02d}.html",
            lesson_page(i)
        )

    print()
    print("==========================================")
    print("生成完了")
    print("==========================================")
    print()
    print("トップ:")
    print("  /index.html")
    print()
    print("Aセメ:")
    print("  /spanish/index.html")
    print()
    print("10段階復習:")
    print("  /spanish/review/index.html")
    print()
    print("Archive:")
    print("  /archive/index.html")
    print()


# ============================================================
# Main / Git
# ============================================================

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--commit",
        action="store_true",
        help="git add + commit も行う"
    )

    parser.add_argument(
        "--push",
        action="store_true",
        help="commit 後に git push も行う"
    )

    args = parser.parse_args()

    generate()

    if args.push:
        args.commit = True

    if args.commit:
        shell(["git", "add", "-A"])

        diff = subprocess.run(
            ["git", "diff", "--cached", "--quiet"]
        )

        if diff.returncode == 0:
            print("変更がないため commit は不要です。")
        else:
            shell([
                "git",
                "commit",
                "-m",
                "Create A semester study pages"
            ])

    if args.push:
        shell(["git", "push"])

    print()
    print("done.")


if __name__ == "__main__":
    main()