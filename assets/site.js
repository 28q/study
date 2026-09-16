<!-- generated-by: setup_a_semester.py -->

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
