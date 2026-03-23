(() => {
  function getSelectionSafe() {
    return window.getSelection ? window.getSelection() : null;
  }

  function getRange() {
    const sel = getSelectionSafe();
    if (!sel || sel.rangeCount === 0) {
      return null;
    }
    return sel.getRangeAt(0);
  }

  function isBlockElement(tagName) {
    return /^(DIV|P|LI|BLOCKQUOTE|TD|TH|H1|H2|H3|H4|H5|H6|UL|OL|PRE)$/i.test(tagName);
  }

  function editableRootFrom(node) {
    let cur = node;
    while (cur) {
      if (cur.nodeType === Node.ELEMENT_NODE && cur.isContentEditable) {
        return cur;
      }
      cur = cur.parentNode;
    }
    return document.body;
  }

  function closestBlock(node) {
    let cur = node && node.nodeType === Node.TEXT_NODE ? node.parentNode : node;
    while (cur && cur !== document.body) {
      if (cur.nodeType === Node.ELEMENT_NODE && isBlockElement(cur.tagName)) {
        return cur;
      }
      cur = cur.parentNode;
    }
    return document.body;
  }

  function setCaretAfter(node) {
    const range = document.createRange();
    range.setStartAfter(node);
    range.collapse(true);
    const sel = getSelectionSafe();
    if (!sel) return;
    sel.removeAllRanges();
    sel.addRange(range);
  }

  function placeCaretInside(node) {
    const sel = getSelectionSafe();
    if (!sel) return;

    let targetTextNode = null;
    if (node.lastChild && node.lastChild.nodeType === Node.TEXT_NODE) {
      targetTextNode = node.lastChild;
    } else {
      targetTextNode = document.createTextNode("\u200b");
      node.appendChild(targetTextNode);
    }

    const range = document.createRange();
    range.setStart(targetTextNode, targetTextNode.textContent.length);
    range.collapse(true);
    sel.removeAllRanges();
    sel.addRange(range);
  }

  function notifyEditorChanged() {
    let target = document.activeElement;
    const range = getRange();

    if (!target || target === document.body) {
      const baseNode = range ? range.startContainer : document.body;
      target = editableRootFrom(baseNode);
    }

    try {
      if (target && typeof target.dispatchEvent === "function") {
        target.dispatchEvent(new Event("input", { bubbles: true }));
        target.dispatchEvent(new Event("change", { bubbles: true }));
      }
    } catch (_e) {
      // ignore
    }

    try {
      if (typeof triggerChanges === "function") {
        triggerChanges();
      }
    } catch (_e) {
      // ignore
    }

    try {
      if (typeof saveNow === "function") {
        saveNow(1);
      }
    } catch (_e) {
      // ignore
    }

    return true;
  }

  function textToFragment(text) {
    const frag = document.createDocumentFragment();
    const normalized = String(text || "").replace(/\r\n/g, "\n");
    const parts = normalized.split("\n");

    parts.forEach((part, index) => {
      if (part.length > 0) {
        frag.appendChild(document.createTextNode(part));
      }
      if (index < parts.length - 1) {
        frag.appendChild(document.createElement("br"));
      }
    });

    return frag;
  }

  function insertFragment(fragment) {
    const range = getRange();
    if (!range) return false;

    const lastNode = fragment.lastChild;
    range.deleteContents();
    range.insertNode(fragment);

    if (lastNode) {
      setCaretAfter(lastNode);
    }

    notifyEditorChanged();
    return true;
  }

  function insertNode(node) {
    const range = getRange();
    if (!range) return false;

    range.deleteContents();
    range.insertNode(node);
    setCaretAfter(node);
    notifyEditorChanged();
    return true;
  }

  function htmlToFragment(html) {
    const template = document.createElement("template");
    template.innerHTML = html;
    return template.content;
  }

  function insertHTML(html) {
    if (!html) return false;
    return insertFragment(htmlToFragment(html));
  }

  function insertText(text) {
    return insertFragment(textToFragment(text));
  }

  function wrapTag(tagName) {
    const range = getRange();
    if (!range || !tagName) return false;

    const el = document.createElement(tagName);

    if (range.collapsed) {
      el.appendChild(document.createTextNode("\u200b"));
      range.insertNode(el);
      placeCaretInside(el);
      notifyEditorChanged();
      return true;
    }

    try {
      range.surroundContents(el);
    } catch (_e) {
      const frag = range.extractContents();
      el.appendChild(frag);
      range.insertNode(el);
    }
    setCaretAfter(el);
    notifyEditorChanged();
    return true;
  }

  function applyStyle(style) {
    const range = getRange();
    if (!range) return false;

    const span = document.createElement("span");
    Object.assign(span.style, style || {});

    if (range.collapsed) {
      span.appendChild(document.createTextNode("\u200b"));
      range.insertNode(span);
      placeCaretInside(span);
      notifyEditorChanged();
      return true;
    }

    try {
      range.surroundContents(span);
    } catch (_e) {
      const frag = range.extractContents();
      span.appendChild(frag);
      range.insertNode(span);
    }
    setCaretAfter(span);
    notifyEditorChanged();
    return true;
  }

  function blockStyle(style) {
    const range = getRange();
    if (!range) return false;

    let block = closestBlock(range.startContainer);
    if (block === document.body) {
      block = document.createElement("div");

      if (range.collapsed) {
        block.appendChild(document.createElement("br"));
        range.insertNode(block);
        Object.assign(block.style, style || {});
        placeCaretInside(block);
        notifyEditorChanged();
        return true;
      }

      const frag = range.extractContents();
      block.appendChild(frag);
      range.insertNode(block);
      Object.assign(block.style, style || {});
      setCaretAfter(block);
      notifyEditorChanged();
      return true;
    }

    Object.assign(block.style, style || {});
    notifyEditorChanged();
    return true;
  }

  function insertLink(url) {
    const range = getRange();
    if (!range || !url) return false;

    const selectedText = range.toString();
    const a = document.createElement("a");
    a.href = url;
    a.textContent = selectedText || url;

    range.deleteContents();
    range.insertNode(a);
    setCaretAfter(a);
    notifyEditorChanged();
    return true;
  }

  function insertImage(url) {
    if (!url) return false;
    const img = document.createElement("img");
    img.src = url;
    img.alt = "";
    return insertNode(img);
  }

  function insertBlockquote() {
    const range = getRange();
    if (!range) return false;

    const bq = document.createElement("blockquote");

    if (range.collapsed) {
      bq.appendChild(document.createElement("br"));
      range.insertNode(bq);
      placeCaretInside(bq);
      notifyEditorChanged();
      return true;
    }

    const frag = range.extractContents();
    bq.appendChild(frag);
    range.insertNode(bq);
    setCaretAfter(bq);
    notifyEditorChanged();
    return true;
  }

  function indent() {
    const range = getRange();
    if (!range) return false;
    const block = closestBlock(range.startContainer);
    const current = parseInt(block.style.marginLeft || "0", 10) || 0;
    block.style.marginLeft = `${current + 40}px`;
    notifyEditorChanged();
    return true;
  }

  function outdent() {
    const range = getRange();
    if (!range) return false;
    const block = closestBlock(range.startContainer);
    const current = parseInt(block.style.marginLeft || "0", 10) || 0;
    block.style.marginLeft = `${Math.max(0, current - 40)}px`;
    notifyEditorChanged();
    return true;
  }

  function insertList(ordered) {
    const range = getRange();
    if (!range) return false;

    const list = document.createElement(ordered ? "ol" : "ul");
    const lines = (range.toString() || "")
      .replace(/\r\n/g, "\n")
      .split("\n")
      .filter((line) => line.length > 0);

    const items = lines.length > 0 ? lines : ["\u200b"];

    for (const line of items) {
      const li = document.createElement("li");
      li.appendChild(textToFragment(line));
      list.appendChild(li);
    }

    range.deleteContents();
    range.insertNode(list);
    setCaretAfter(list);
    notifyEditorChanged();
    return true;
  }

  function selectAll() {
    const sel = getSelectionSafe();
    if (!sel) return false;

    const active = document.activeElement || document.body;
    const root = editableRootFrom(active);

    const range = document.createRange();
    range.selectNodeContents(root);
    sel.removeAllRanges();
    sel.addRange(range);
    return true;
  }

  function getSelectedText() {
    const sel = getSelectionSafe();
    return sel ? sel.toString() : "";
  }

  function getSelectedContent() {
    const range = getRange();
    if (!range || range.collapsed) {
      return { html: "", text: "" };
    }

    const container = document.createElement("div");
    container.appendChild(range.cloneContents());
    return {
      html: container.innerHTML,
      text: getSelectedText(),
    };
  }

  function deleteSelection() {
    const range = getRange();
    if (!range) return false;
    range.deleteContents();
    notifyEditorChanged();
    return true;
  }

  function plainTextFromNode(node) {
    if (!node) return "";

    if (node.nodeType === Node.TEXT_NODE) {
      return node.nodeValue || "";
    }

    if (node.nodeType !== Node.ELEMENT_NODE && node.nodeType !== Node.DOCUMENT_FRAGMENT_NODE) {
      return "";
    }

    if (node.nodeType === Node.ELEMENT_NODE && node.tagName === "BR") {
      return "\n";
    }

    let text = "";
    const isBlock = node.nodeType === Node.ELEMENT_NODE && isBlockElement(node.tagName);

    for (const child of node.childNodes) {
      text += plainTextFromNode(child);
    }

    if (isBlock && text && !text.endsWith("\n")) {
      text += "\n";
    }

    return text;
  }

  function clearFormat() {
    const range = getRange();
    if (!range) return false;

    const cloned = range.cloneContents();
    const text = plainTextFromNode(cloned).replace(/\n+$/, "");
    return insertFragment(textToFragment(text));
  }

  function wordCount() {
    const text = getSelectedText();
    const trimmed = text.trim();
    return {
      words: trimmed ? trimmed.split(/\s+/).length : 0,
      characters: text.length,
    };
  }

  function cleanEmptyStyleAttribute(el) {
    if (!el || el.nodeType !== Node.ELEMENT_NODE) return;
    const style = el.getAttribute("style");
    if (style !== null && style.trim() === "") {
      el.removeAttribute("style");
    }
  }

  function walkElements(root, callback) {
    if (!root) return;

    const stack = [root];
    while (stack.length > 0) {
      const node = stack.pop();

      if (node.nodeType === Node.ELEMENT_NODE) {
        callback(node);
      }

      const children = Array.from(node.childNodes || []);
      for (let i = children.length - 1; i >= 0; i--) {
        stack.push(children[i]);
      }
    }
  }

  function unwrapElement(el) {
    const parent = el && el.parentNode;
    if (!parent) return;

    while (el.firstChild) {
      parent.insertBefore(el.firstChild, el);
    }
    parent.removeChild(el);
  }

  function closestAncestorTag(node, tagName) {
    let cur = node && node.nodeType === Node.TEXT_NODE ? node.parentNode : node;
    while (cur && cur !== document.body) {
      if (cur.nodeType === Node.ELEMENT_NODE && cur.tagName === tagName) {
        return cur;
      }
      cur = cur.parentNode;
    }
    return null;
  }

  function reinsertExtractedFragment(range, fragment) {
    const lastNode = fragment.lastChild;
    range.insertNode(fragment);
    if (lastNode) {
      setCaretAfter(lastNode);
    }
    return true;
  }

  function removeStylePropertiesFromElement(el, properties) {
    if (!el || el.nodeType !== Node.ELEMENT_NODE) return false;

    let changed = false;

    properties.forEach((prop) => {
      if (el.style && el.style[prop]) {
        el.style[prop] = "";
        changed = true;
      }

      if (prop === "color" && el.hasAttribute("color")) {
        el.removeAttribute("color");
        changed = true;
      }

      if (prop === "backgroundColor" && el.hasAttribute("bgcolor")) {
        el.removeAttribute("bgcolor");
        changed = true;
      }
    });

    cleanEmptyStyleAttribute(el);

    if (
      el.parentNode &&
      (el.tagName === "SPAN" || el.tagName === "FONT") &&
      !el.getAttribute("style") &&
      !el.hasAttribute("color") &&
      !el.hasAttribute("bgcolor") &&
      el.attributes.length === 0
    ) {
      unwrapElement(el);
      changed = true;
    }

    return changed;
  }

  function removeLink() {
    const range = getRange();
    if (!range) return false;

    if (range.collapsed) {
      const anchor = closestAncestorTag(range.startContainer, "A");
      if (!anchor) return false;
      unwrapElement(anchor);
      notifyEditorChanged();
      return true;
    }

    const frag = range.extractContents();
    const anchors = [];

    walkElements(frag, (el) => {
      if (el.tagName === "A") {
        anchors.push(el);
      }
    });

    anchors.forEach(unwrapElement);
    reinsertExtractedFragment(range, frag);
    notifyEditorChanged();
    return true;
  }

  function clearStyleProperties(properties) {
    const range = getRange();
    if (!range || !Array.isArray(properties) || properties.length === 0) {
      return false;
    }

    if (range.collapsed) {
      let node =
        range.startContainer.nodeType === Node.TEXT_NODE
          ? range.startContainer.parentNode
          : range.startContainer;

      while (node && node !== document.body) {
        if (removeStylePropertiesFromElement(node, properties)) {
          notifyEditorChanged();
          return true;
        }
        node = node.parentNode;
      }

      return false;
    }

    const frag = range.extractContents();
    let changed = false;
    const elements = [];

    walkElements(frag, (el) => {
      elements.push(el);
    });

    elements.reverse().forEach((el) => {
      if (removeStylePropertiesFromElement(el, properties)) {
        changed = true;
      }
    });

    reinsertExtractedFragment(range, frag);

    if (changed) {
      notifyEditorChanged();
    }
    return changed;
  }

  function compatCommand(command) {
    if (!command) return false;
    try {
      if (document.queryCommandSupported && !document.queryCommandSupported(command)) {
        return false;
      }
    } catch (_e) {
      // ignore
    }

    try {
      return document.execCommand(command);
    } catch (_e) {
      return false;
    }
  }

  window.CMTT = {
    exec(payload) {
      if (!payload || !payload.op) return null;

      switch (payload.op) {
        case "insertText":
          return insertText(payload.text || "");
        case "insertHTML":
          return insertHTML(payload.html || "");
        case "wrapTag":
          return wrapTag(payload.tag || "");
        case "applyStyle":
          return applyStyle(payload.style || {});
        case "blockStyle":
          return blockStyle(payload.style || {});
        case "insertLink":
          return insertLink(payload.url || "");
        case "insertImage":
          return insertImage(payload.url || "");
        case "insertBlockquote":
          return insertBlockquote();
        case "indent":
          return indent();
        case "outdent":
          return outdent();
        case "insertList":
          return insertList(!!payload.ordered);
        case "selectAll":
          return selectAll();
        case "getSelectedText":
          return getSelectedText();
        case "getSelectedContent":
          return getSelectedContent();
        case "deleteSelection":
          return deleteSelection();
        case "clearFormat":
          return clearFormat();
        case "wordCount":
          return wordCount();
        case "removeLink":
          return removeLink();
        case "clearStyleProperties":
          return clearStyleProperties(payload.properties || []);
        case "compatCommand":
          return compatCommand(payload.command || "");
        default:
          return null;
      }
    },
  };
})();
