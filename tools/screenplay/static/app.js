"use strict";

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

function h(tag, attrs, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else if (k === "html") node.innerHTML = v;
    else node.setAttribute(k, v === true ? "" : v);
  }
  for (const c of children.flat()) {
    if (c === null || c === undefined || c === false) continue;
    node.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return node;
}

const state = {
  story: null,
  version: null,
  flags: loadFlags(),
  order: null,          // порядок сцен, ещё не применённый к файлам
  editing: null,
  busy: false,
  search: "",
  marks: [],
  markIndex: -1,
  byKey: new Map(),
};

const TRANSPARENT = new Set(["pause", "audio", "jump"]);

function loadFlags() {
  const def = { slides: true, tech: false, en: false };
  try {
    return Object.assign(def, JSON.parse(localStorage.getItem("screenplay-flags") || "{}"));
  } catch (e) {
    return def;
  }
}

function saveFlags() {
  try {
    localStorage.setItem("screenplay-flags", JSON.stringify(state.flags));
  } catch (e) { /* приватное окно */ }
}

async function api(path, body) {
  const opts = body === undefined ? {} : {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  };
  let res;
  try {
    res = await fetch(path, opts);
  } catch (e) {
    throw new Error("Сервер не отвечает — запущен ли server.py?");
  }
  const data = await res.json().catch(() => ({ error: "Некорректный ответ сервера" }));
  if (!res.ok) {
    const err = new Error(data.error || res.statusText);
    err.status = res.status;
    throw err;
  }
  return data;
}

let toastTimer = null;
function toast(msg, isError) {
  const t = $("#toast");
  t.textContent = msg;
  t.className = "toast" + (isError ? " error" : "");
  t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { t.hidden = true; }, isError ? 5000 : 2200);
}

// ------------------------------------------------------------------ загрузка и якорь прокрутки

function captureAnchor(key) {
  let el = key ? document.querySelector(`[data-key="${CSS.escape(key)}"]`) : null;
  if (!el) {
    for (const c of $$("[data-key]")) {
      if (c.getBoundingClientRect().bottom > 80) { el = c; break; }
    }
  }
  return el ? { key: el.dataset.key, top: el.getBoundingClientRect().top } : null;
}

function restoreAnchor(anchor, key) {
  if (!anchor) return null;
  const el = document.querySelector(`[data-key="${CSS.escape(key || anchor.key)}"]`);
  if (el) window.scrollBy(0, el.getBoundingClientRect().top - anchor.top);
  return el;
}

async function load(anchor, focusKey) {
  const story = await api("/api/story");
  state.story = story;
  state.version = story.version;
  if (state.order && !sameSceneSet(state.order)) state.order = null;
  render();
  updateUndo(story.undo);
  const el = restoreAnchor(anchor, focusKey);
  if (el && focusKey) {
    el.classList.add("flash");
    setTimeout(() => el.classList.remove("flash"), 1300);
  }
  return el;
}

function sameSceneSet(order) {
  return order.every((n) => n in state.story.scenes);
}

function updateUndo(list) {
  const b = $("#undo");
  b.disabled = !list || !list.length;
  b.title = list && list.length ? "Отменить: " + list[0] : "";
}

// ------------------------------------------------------------------ форматирование текста

function escapeHtml(s) {
  return s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function highlight(plain) {
  const esc = escapeHtml(plain);
  if (!state.search) return esc;
  const q = escapeHtml(state.search).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return esc.replace(new RegExp(q, "gi"), (m) => `<mark>${m}</mark>`);
}

/** Текст реплики: теги {…} и подстановки […] приглушены, совпадения поиска подсвечены. */
function fmt(text) {
  const parts = text.split(/(\{[^{}]*\}|\[[^\[\]]*\])/);
  return parts.map((p, i) => {
    if (i % 2 === 0) return highlight(p);
    const cls = p.startsWith("{") ? "tag" : "interp";
    return `<span class="${cls}">${escapeHtml(p)}</span>`;
  }).join("").replace(/\n/g, "<br>");
}

function vscodeLink(file, line) {
  return `vscode://file/${state.story.game_dir}/${file}:${line}`;
}

// ------------------------------------------------------------------ рендер

function currentOrder() {
  const s = state.story;
  if (!state.order) return { chain: s.chain, orphans: s.orphans };
  const all = Object.keys(s.scenes);
  return {
    chain: state.order,
    orphans: all.filter((n) => !state.order.includes(n)),
  };
}

function render() {
  const s = state.story;
  const main = $("#manuscript");
  state.byKey.clear();
  main.innerHTML = "";
  const { chain, orphans } = currentOrder();

  chain.forEach((name, i) => main.append(renderScene(s.scenes[name], i + 1, chain[i + 1] || null)));
  if (orphans.length) {
    main.append(h("div", { class: "orphans-sep" },
      "Вне цепочки — в игре до этих сцен сейчас не дойти"));
    orphans.forEach((name) => main.append(renderScene(s.scenes[name], null, null)));
  }

  renderToc(chain, orphans);
  const words = chain.reduce((sum, n) => sum + s.scenes[n].words, 0);
  $("#stats").textContent = `${chain.length} сцен · ${words.toLocaleString("ru-RU")} слов`;
  collectMarks();
  spy();
}

function renderScene(sc, num, nextName) {
  const sec = h("section", { class: "scene" + (num ? "" : " orphan"), id: "scene-" + sc.label });
  sec.append(h("div", { class: "scene-head" },
    h("div", { class: "scene-kicker" }, num ? `Сцена ${String(num).padStart(2, "0")}` : "Вне цепочки"),
    h("h2", {}, sc.title),
    h("div", { class: "scene-meta" },
      sc.label, " · ",
      h("a", { href: vscodeLink(sc.file, sc.line), title: "Открыть в VS Code" }, `${sc.file}:${sc.line}`),
      ` · ${sc.words} слов`),
    sc.synopsis ? h("p", { class: "synopsis" }, sc.synopsis) : null));

  let group = [];
  const flush = () => {
    if (group.length) sec.append(renderVisuals(group, sc));
    group = [];
  };

  sc.elements.forEach((el, idx) => {
    if (el.type === "visual") {
      group.push(el);
      return;
    }
    const node = renderElement(el, sc, idx);
    if (!node) return;
    flush();
    sec.append(node);
  });
  flush();

  const s = state.story;
  let exit;
  if (nextName) {
    exit = h("div", { class: "scene-exit" }, "→ дальше: ",
      h("a", { href: "#scene-" + nextName }, s.scenes[nextName].title));
  } else if (num) {
    exit = h("div", { class: "scene-exit" }, "■ конец цепочки");
  }
  if (exit) sec.append(exit);
  return sec;
}

function keyOf(sc, el) {
  return `${sc.file}:${el.line}`;
}

function depthStyle(el) {
  return el.depth ? `margin-left:${el.depth * 26}px` : null;
}

function renderVisuals(group, sc) {
  const fulls = group.filter((v) => v.full && !v.black);
  const main = fulls[fulls.length - 1];
  const rest = group.filter((v) => v !== main && !v.black);
  const last = group[group.length - 1];
  const key = keyOf(sc, last);
  const names = group.map((v) => `${v.kind} ${v.name}`);

  if (!state.flags.slides) {
    const node = h("div", { class: "vis-compact", "data-key": key },
      group.map((v) => h("span", {}, "▣ " + v.name)));
    return node;
  }

  if (!main) {
    if (!rest.length) return h("div", { class: "black-bar", "data-key": key });
    return h("div", { class: "sprite-row", "data-key": key }, rest.map(thumb));
  }

  const frame = h("div", { class: "slide-frame", onclick: () => lightbox(main, names) },
    main.url ? h("img", { src: encodeURI(main.url), loading: "lazy", alt: main.name })
      : h("div", { class: "slide-missing" }, main.name));
  if (rest.length) frame.append(h("div", { class: "slide-strip" }, rest.map(thumb)));

  const add = h("button", {
    class: "btn slide-add",
    title: "Новая строка под этим кадром",
    onclick: (e) => { e.stopPropagation(); startPhantom(last, sc, { afterNode: fig }); },
  }, "+ текст");
  frame.append(add);

  const fig = h("figure", { class: "slide", "data-key": key }, frame,
    state.flags.tech ? h("figcaption", { class: "slide-caption" }, names.join(" · ")) : null);
  state.byKey.set(key, { el: last, sc, node: fig });
  return fig;
}

function thumb(v) {
  return h("div", { class: "thumb", title: `${v.kind} ${v.name}` },
    v.url ? h("img", { src: encodeURI(v.url), loading: "lazy", alt: v.name }) : v.name);
}

function renderElement(el, sc, idx) {
  const tech = state.flags.tech;
  switch (el.type) {
    case "say": return renderLine(el, sc, idx, "say");
    case "choice": return renderLine(el, sc, idx, "choice");
    case "title": return renderLine(el, sc, idx, "title");
    case "menu":
      return h("div", { class: "menu-head", style: depthStyle(el), "data-key": keyOf(sc, el) }, "Выбор");
    case "sublabel":
      return h("div", { class: "sublabel", id: "sub-" + el.label, "data-key": keyOf(sc, el) }, el.title);
    case "call":
      return h("div", { class: "card", style: depthStyle(el), "data-key": keyOf(sc, el) },
        h("b", {}, /minigame/.test(el.target) ? "Мини-игра" : "Вставка"), el.target);
    case "interact":
      return h("div", { class: "card", style: depthStyle(el), "data-key": keyOf(sc, el) },
        h("b", {}, "Интерактив"), el.target);
    case "audio":
      if (el.kind === "mplay") {
        return h("div", { class: "music", style: depthStyle(el), "data-key": keyOf(sc, el) }, el.text);
      }
      return tech ? h("div", { class: "tech", "data-key": keyOf(sc, el) }, `${el.kind} ${el.text}`) : null;
    case "pause":
      return tech ? h("div", { class: "tech", style: depthStyle(el) }, `pause ${el.text}`) : null;
    case "cond":
      return tech ? h("div", { class: "tech", style: depthStyle(el), "data-key": keyOf(sc, el) }, el.text) : null;
    case "jump":
      return tech ? h("div", { class: "tech", style: depthStyle(el) }, "jump " + el.target) : null;
    case "return":
      return tech ? h("div", { class: "tech", style: depthStyle(el) }, "return") : null;
    default:
      return null;
  }
}

function renderLine(el, sc, idx, kind) {
  const key = keyOf(sc, el);
  const chars = state.story.characters;
  let cls = "line ";
  if (kind === "say") cls += el.who ? "speech" : "narr";
  else cls += kind === "choice" ? "choice" : "title-card";

  const node = h("div", { class: cls, "data-key": key, style: depthStyle(el) });
  if (kind === "say" && el.who) node.append(h("div", { class: "who" }, chars[el.who] || el.who));
  const text = h("div", { class: "text", html: fmt(el.text) || "&nbsp;" });
  text.addEventListener("click", () => startEdit(node, el, sc, kind));
  node.append(text);
  if (state.flags.en) {
    node.append(h("div", { class: "en" + (el.en ? "" : " missing") }, el.en || "нет перевода"));
  }
  node.append(lineTools(node, el, sc, idx, kind));
  state.byKey.set(key, { el, sc, node, kind, idx });
  return node;
}

/** Соседняя реплика того же уровня, с которой можно поменяться местами. */
function neighbor(sc, idx, dir) {
  const el = sc.elements[idx];
  for (let i = idx + dir; i >= 0 && i < sc.elements.length; i += dir) {
    const o = sc.elements[i];
    if (TRANSPARENT.has(o.type) && o.depth >= el.depth) continue;
    return o.type === "say" && o.depth === el.depth ? o : null;
  }
  return null;
}

function lineTools(node, el, sc, idx, kind) {
  const box = h("div", { class: "tools" });
  if (kind === "say") {
    const up = neighbor(sc, idx, -1);
    const down = neighbor(sc, idx, 1);
    box.append(
      h("button", { class: "tool", title: "Выше", disabled: !up, onclick: () => swap(sc, el, up) }, "↑"),
      h("button", { class: "tool", title: "Ниже", disabled: !down, onclick: () => swap(sc, el, down) }, "↓"),
      h("button", { class: "tool", title: "Новая строка ниже (Ctrl+Enter)",
        onclick: () => startPhantom(el, sc, { afterNode: node, who: el.who }) }, "+"),
      h("button", { class: "tool danger", title: "Удалить строку", onclick: () => removeLine(sc, el) }, "✕"));
  } else if (kind === "choice") {
    box.append(h("button", { class: "tool", title: "Новая строка в начале ветки",
      onclick: () => startPhantom(el, sc, { afterNode: node, intoBlock: true, depth: el.depth + 1 }) }, "+"));
  }
  box.append(h("a", { class: "tool", href: vscodeLink(sc.file, el.line), title: "Открыть в VS Code" }, "⧉"));
  return box;
}

// ------------------------------------------------------------------ правка

function autosize(ta) {
  ta.style.height = "auto";
  ta.style.height = ta.scrollHeight + 2 + "px";
}

function speakerSelect(current) {
  const sel = h("select", { title: "Кто говорит" },
    h("option", { value: "" }, "— рассказ (без имени) —"));
  for (const [v, name] of Object.entries(state.story.characters)) {
    sel.append(h("option", { value: v }, `${name} (${v})`));
  }
  if (current && !(current in state.story.characters)) sel.append(h("option", { value: current }, current));
  sel.value = current || "";
  return sel;
}

/** Открывает поле правки внутри узла строки. ctx.phantom — строка, которой ещё нет в файле. */
function openEditor(node, ctx) {
  state.editing = ctx;
  node.classList.add("editing");
  const textDiv = $(".text", node);
  const ta = h("textarea", { class: "editor", rows: 1, spellcheck: "true" });
  ta.value = ctx.text;
  textDiv.replaceWith(ta);
  ctx.node = node;
  ctx.ta = ta;
  ctx.textDiv = textDiv;

  const bar = h("div", { class: "edit-bar" });
  if (ctx.kind === "say") {
    ctx.sel = speakerSelect(ctx.who);
    bar.append(h("label", {}, "Говорит: ", ctx.sel));
  }
  bar.append(h("span", {}, "Enter — сохранить · Shift+Enter — перенос · Ctrl+Enter — ещё строка · Esc — отмена"));
  ta.after(bar);
  ctx.bar = bar;

  ta.addEventListener("input", () => autosize(ta));
  ta.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      e.preventDefault();
      finishEdit(ctx, false);
    } else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      finishEdit(ctx, true, true);
    } else if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      finishEdit(ctx, true);
    }
  });
  node.addEventListener("focusout", () => {
    setTimeout(() => {
      if (state.editing === ctx && !node.contains(document.activeElement)) finishEdit(ctx, true);
    }, 0);
  });

  autosize(ta);
  ta.focus();
  ta.setSelectionRange(ta.value.length, ta.value.length);
}

/** Сохраняет открытую правку. false — запись ушла на сервер и страница вот-вот перерисуется. */
function releaseEditor() {
  if (state.editing) finishEdit(state.editing, true);
  return !state.busy;
}

function startEdit(node, el, sc, kind) {
  if (state.editing && state.editing.node === node) return;
  if (!releaseEditor()) return;
  openEditor(node, { el, sc, kind, text: el.text, who: el.who || "" });
}

/** Новая строка: в файл попадает только после Enter, пустая — исчезает. */
function startPhantom(refEl, sc, opts) {
  if (!releaseEditor()) return;
  const who = opts.who || "";
  const node = h("div", {
    class: "line " + (who ? "speech" : "narr"),
    style: (opts.depth || refEl.depth) ? `margin-left:${(opts.depth || refEl.depth) * 26}px` : null,
  }, h("div", { class: "text" }));
  opts.afterNode.after(node);
  openEditor(node, { phantom: true, refEl, sc, kind: "say", text: "", who, intoBlock: !!opts.intoBlock });
}

function closeEditor(ctx) {
  if (ctx.phantom) {
    ctx.node.remove();
  } else {
    ctx.bar.remove();
    ctx.ta.replaceWith(ctx.textDiv);
    ctx.node.classList.remove("editing");
  }
  if (state.editing === ctx) state.editing = null;
}

async function finishEdit(ctx, save, andNew) {
  if (ctx.done) return;
  ctx.done = true;
  const text = ctx.ta.value;
  const who = ctx.sel ? ctx.sel.value : undefined;

  let req = null;
  if (save && ctx.phantom && text.trim()) {
    req = ["insert", {
      file: ctx.sc.file, line: ctx.refEl.line, expect: ctx.refEl.raw,
      into_block: ctx.intoBlock, who: who || null, text,
    }];
  } else if (save && !ctx.phantom) {
    const whoChanged = who !== undefined && who !== (ctx.el.who || "");
    if (text !== ctx.el.text || whoChanged) {
      req = ["edit", {
        file: ctx.sc.file, line: ctx.el.line, expect: ctx.el.raw,
        kind: ctx.kind, text, ...(whoChanged ? { who: who || null } : {}),
      }];
    }
  }

  if (!req) {
    closeEditor(ctx);
    if (andNew && !ctx.phantom && ctx.kind === "say") {
      startPhantom(ctx.el, ctx.sc, { afterNode: ctx.node, who: ctx.el.who });
    }
    return;
  }

  ctx.node.classList.add("saving");
  ctx.ta.readOnly = true;
  state.editing = null;
  const res = await runOp(req[0], req[1], ctx.node);
  if (res && andNew) {
    const reg = state.byKey.get(`${res.focus.file}:${res.focus.line}`);
    if (reg && reg.kind === "say") startPhantom(reg.el, reg.sc, { afterNode: reg.node, who: reg.el.who });
  }
}

/** Операция над файлами + перечитка сценария с сохранением позиции экрана. */
async function runOp(op, body, anchorNode) {
  if (state.busy) return null;
  state.busy = true;
  const anchor = anchorNode
    ? { key: anchorNode.dataset.key || "", top: anchorNode.getBoundingClientRect().top }
    : captureAnchor();
  try {
    const res = await api("/api/" + op, body);
    const focus = res.focus ? `${res.focus.file}:${res.focus.line}` : null;
    await load(anchor, focus);
    return res;
  } catch (e) {
    toast(e.message, true);
    await load(anchor).catch(() => {});
    return null;
  } finally {
    state.busy = false;
  }
}

function swap(sc, el, other) {
  runOp("swap", {
    file: sc.file, a: el.line, expect_a: el.raw, b: other.line, expect_b: other.raw,
  }, state.byKey.get(keyOf(sc, el)).node);
}

function removeLine(sc, el) {
  const preview = el.text.length > 60 ? el.text.slice(0, 60) + "…" : el.text;
  if (!confirm(`Удалить строку?\n\n${preview}`)) return;
  runOp("delete", { file: sc.file, line: el.line, expect: el.raw });
}

async function undo() {
  if (state.editing) return;
  const res = await runOp("undo", {});
  if (res) toast("Отменено: " + res.undone);
}

// ------------------------------------------------------------------ оглавление и порядок сцен

function renderToc(chain, orphans) {
  const s = state.story;
  const fill = (list, names, numbered) => {
    list.innerHTML = "";
    names.forEach((name, i) => {
      const sc = s.scenes[name];
      const subs = sc.elements.filter((e) => e.type === "sublabel");
      const li = h("li", { class: "toc-item", draggable: "true", "data-scene": name },
        h("div", { class: "toc-row" },
          h("span", { class: "toc-num" }, numbered ? String(i + 1) : "·"),
          h("span", { class: "toc-title" }, sc.title),
          h("span", { class: "toc-words" }, String(sc.words))),
        subs.length ? h("ul", { class: "toc-subs" },
          subs.map((e) => h("li", {
            onclick: (ev) => { ev.stopPropagation(); scrollToId("sub-" + e.label); },
          }, e.title))) : null);
      li.addEventListener("click", () => scrollToId("scene-" + name));
      bindDrag(li);
      list.append(li);
    });
  };
  fill($("#toc-chain"), chain, true);
  fill($("#toc-orphans"), orphans, false);
  $("#order-bar").hidden = !state.order;
}

function scrollToId(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
}

let dragName = null;

function bindDrag(li) {
  li.addEventListener("dragstart", (e) => {
    dragName = li.dataset.scene;
    li.classList.add("dragging");
    e.dataTransfer.effectAllowed = "move";
    e.dataTransfer.setData("text/plain", dragName);
  });
  li.addEventListener("dragend", () => {
    li.classList.remove("dragging");
    clearDropMarks();
    dragName = null;
  });
  li.addEventListener("dragover", (e) => {
    if (!dragName || dragName === li.dataset.scene) return;
    e.preventDefault();
    clearDropMarks();
    const r = li.getBoundingClientRect();
    li.classList.add(e.clientY < r.top + r.height / 2 ? "drop-before" : "drop-after");
  });
  li.addEventListener("drop", (e) => {
    e.preventDefault();
    if (!dragName) return;
    const before = li.classList.contains("drop-before");
    const moved = document.querySelector(`.toc-item[data-scene="${CSS.escape(dragName)}"]`);
    if (moved && moved !== li) li.parentNode.insertBefore(moved, before ? li : li.nextSibling);
    commitTocOrder();
  });
}

for (const list of [$("#toc-chain"), $("#toc-orphans")]) {
  list.addEventListener("dragover", (e) => {
    if (dragName && e.target === list) e.preventDefault();
  });
  list.addEventListener("drop", (e) => {
    if (!dragName || e.target !== list) return;
    e.preventDefault();
    const moved = document.querySelector(`.toc-item[data-scene="${CSS.escape(dragName)}"]`);
    if (moved) list.append(moved);
    commitTocOrder();
  });
}

function clearDropMarks() {
  $$(".drop-before, .drop-after").forEach((n) => n.classList.remove("drop-before", "drop-after"));
}

function commitTocOrder() {
  clearDropMarks();
  const order = $$("#toc-chain .toc-item").map((li) => li.dataset.scene);
  if (!order.length) {
    toast("В цепочке должна остаться хотя бы одна сцена", true);
    render();
    return;
  }
  const same = order.length === state.story.chain.length &&
    order.every((n, i) => n === state.story.chain[i]);
  state.order = same ? null : order;
  const anchor = captureAnchor();
  render();
  restoreAnchor(anchor);
}

async function previewOrder() {
  let res;
  try {
    res = await api("/api/reorder", { order: state.order, apply: false });
  } catch (e) {
    toast(e.message, true);
    return;
  }
  if (!res.changes.length) {
    toast("Файлы менять не нужно");
    state.order = null;
    render();
    return;
  }
  const dialog = h("div", { class: "dialog" },
    h("h3", {}, "Новый порядок сцен"),
    h("div", { class: "change-loc" }, "Меняются переходы jump в концах сцен:"),
    res.changes.map((c) => h("div", { class: "change" },
      h("div", { class: "change-note" }, c.note),
      h("div", { class: "change-loc" }, `${c.file}:${c.line}${c.mode === "insert" ? " (вставка после строки)" : ""}`),
      h("div", { class: "change-diff" },
        c.mode === "replace" ? h("div", { class: "del" }, "- " + c.old.trim()) : null,
        h("div", { class: "add" }, "+ " + c.new.trim())))),
    res.warnings.length ? h("div", { class: "warnings" }, res.warnings.map((w) => h("div", {}, "⚠ " + w))) : null,
    h("div", { class: "dialog-actions" },
      h("button", { class: "btn", onclick: closeModal }, "Отмена"),
      h("button", { class: "btn accent", onclick: applyOrder }, "Применить к файлам")));
  openModal(dialog);
}

async function applyOrder() {
  closeModal();
  const order = state.order;
  const res = await runOp("reorder", { order, apply: true });
  if (res) {
    state.order = null;
    render();
    toast("Порядок сцен записан");
  }
}

// ------------------------------------------------------------------ модалки, поиск, прокрутка

function openModal(content) {
  const m = $("#modal");
  m.innerHTML = "";
  m.append(content);
  m.hidden = false;
}

function closeModal() {
  $("#modal").hidden = true;
  $("#modal").innerHTML = "";
}

$("#modal").addEventListener("click", (e) => {
  if (e.target.id === "modal" || e.target.tagName === "IMG") closeModal();
});

function lightbox(v, names) {
  if (!v.url) return;
  openModal(h("div", {},
    h("img", { src: encodeURI(v.url), alt: v.name }),
    h("div", { class: "modal-cap" }, names.join(" · "))));
}

function collectMarks() {
  state.marks = $$("#manuscript mark");
  state.markIndex = -1;
  $("#search-count").textContent = state.search ? String(state.marks.length) : "";
}

function nextMark(dir) {
  if (!state.marks.length) return;
  if (state.markIndex >= 0) state.marks[state.markIndex].classList.remove("active");
  state.markIndex = (state.markIndex + dir + state.marks.length) % state.marks.length;
  const m = state.marks[state.markIndex];
  m.classList.add("active");
  m.scrollIntoView({ block: "center" });
  $("#search-count").textContent = `${state.markIndex + 1}/${state.marks.length}`;
}

let searchTimer = null;
$("#search").addEventListener("input", (e) => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    state.search = e.target.value.trim();
    if (state.editing) finishEdit(state.editing, true);
    const anchor = captureAnchor();
    render();
    restoreAnchor(anchor);
  }, 180);
});
$("#search").addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    nextMark(e.shiftKey ? -1 : 1);
  } else if (e.key === "Escape") {
    e.target.value = "";
    e.target.dispatchEvent(new Event("input"));
  }
});

let spyQueued = false;
function spy() {
  spyQueued = false;
  let current = null;
  for (const sec of $$(".scene")) {
    if (sec.getBoundingClientRect().top < 140) current = sec.id.slice(6);
    else break;
  }
  for (const li of $$(".toc-item")) li.classList.toggle("current", li.dataset.scene === current);
}
window.addEventListener("scroll", () => {
  if (!spyQueued) {
    spyQueued = true;
    requestAnimationFrame(spy);
  }
}, { passive: true });

// ------------------------------------------------------------------ переключатели, клавиши, опрос

for (const box of $$("[data-flag]")) {
  box.checked = !!state.flags[box.dataset.flag];
  box.addEventListener("change", () => {
    state.flags[box.dataset.flag] = box.checked;
    saveFlags();
    if (state.editing) finishEdit(state.editing, true);
    const anchor = captureAnchor();
    render();
    restoreAnchor(anchor);
  });
}

$("#undo").addEventListener("click", undo);
$("#order-preview").addEventListener("click", previewOrder);
$("#order-reset").addEventListener("click", () => {
  state.order = null;
  render();
});

document.addEventListener("keydown", (e) => {
  const typing = /^(TEXTAREA|INPUT|SELECT)$/.test(document.activeElement.tagName);
  if (e.key === "Escape" && !$("#modal").hidden) {
    closeModal();
  } else if (!typing && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "z") {
    e.preventDefault();
    undo();
  } else if (!typing && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "f") {
    e.preventDefault();
    $("#search").focus();
    $("#search").select();
  }
});

/** Правки из VS Code или самой игры подхватываются без перезагрузки страницы. */
async function poll() {
  if (!state.editing && !state.busy && !document.hidden && $("#modal").hidden && state.story) {
    try {
      const { version } = await api("/api/version");
      if (version !== state.version && !state.editing && !state.busy) {
        await load(captureAnchor());
        toast("Файлы изменились снаружи — обновлено");
      }
    } catch (e) { /* сервер перезапускается */ }
  }
  setTimeout(poll, 2000);
}

load(null).then(() => {
  const hash = decodeURIComponent(location.hash.slice(1));
  if (hash) scrollToId(hash);
  poll();
}).catch((e) => {
  $("#manuscript").innerHTML = "";
  $("#manuscript").append(h("div", { class: "loading" }, e.message));
});
