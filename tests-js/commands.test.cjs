const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

const { JSDOM } = require("jsdom");

const COMMANDS_JS = fs.readFileSync(
  path.join(__dirname, "..", "Text-Tools", "web", "commands.js"),
  "utf8",
);

function createHarness(editorHtml) {
  const dom = new JSDOM(
    `<!doctype html><html><body><div id="editor" contenteditable="true">${editorHtml}</div></body></html>`,
    {
      pretendToBeVisual: true,
      runScripts: "dangerously",
    },
  );

  const { window } = dom;
  const editor = window.document.getElementById("editor");
  let triggerChangesCount = 0;
  const saveNowCalls = [];

  window.triggerChanges = () => {
    triggerChangesCount += 1;
  };
  window.saveNow = (...args) => {
    saveNowCalls.push(args);
  };

  window.eval(COMMANDS_JS);

  return {
    dom,
    editor,
    saveNowCalls,
    window,
    triggerChangesCount: () => triggerChangesCount,
  };
}

function selectNode(window, node) {
  const range = window.document.createRange();
  range.selectNode(node);
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
}

function selectNodeContents(window, node) {
  const range = window.document.createRange();
  range.selectNodeContents(node);
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
}

function placeCaretInsideText(window, textNode, offset) {
  const range = window.document.createRange();
  range.setStart(textNode, offset);
  range.collapse(true);
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
}

function toPlainObject(value) {
  return JSON.parse(JSON.stringify(value));
}

test("getSelectedContent returns both html and text", () => {
  const { editor, window } = createHarness("<b>Hello</b> <i>world</i>");

  selectNode(window, editor.querySelector("b"));

  assert.deepEqual(toPlainObject(window.CMTT.exec({ op: "getSelectedContent" })), {
    html: "<b>Hello</b>",
    text: "Hello",
  });
});

test("clearFormat preserves visible line breaks while removing markup", () => {
  const { editor, saveNowCalls, triggerChangesCount, window } = createHarness(
    '<span style="color: red;">Hello<br>World</span>',
  );

  selectNode(window, editor.querySelector("span"));

  assert.equal(window.CMTT.exec({ op: "clearFormat" }), true);
  assert.equal(editor.innerHTML, "Hello<br>World");
  assert.equal(triggerChangesCount(), 1);
  assert.deepEqual(saveNowCalls, [[1]]);
});

test("removeLink unwraps a selected link while keeping its text", () => {
  const { editor, window } = createHarness('<a href="https://example.com">Hello</a>');

  selectNode(window, editor.querySelector("a"));

  assert.equal(window.CMTT.exec({ op: "removeLink" }), true);
  assert.equal(editor.innerHTML, "Hello");
});

test("removeLink also works with a collapsed caret inside a link", () => {
  const { editor, window } = createHarness('<a href="https://example.com">Hello</a>');
  const textNode = editor.querySelector("a").firstChild;

  placeCaretInsideText(window, textNode, 2);

  assert.equal(window.CMTT.exec({ op: "removeLink" }), true);
  assert.equal(editor.innerHTML, "Hello");
});

test("clearStyleProperties removes requested styles and unwraps empty spans", () => {
  const { editor, window } = createHarness(
    '<span style="color: red; background-color: yellow;">Hello</span>',
  );

  selectNode(window, editor.querySelector("span"));

  assert.equal(
    window.CMTT.exec({
      op: "clearStyleProperties",
      properties: ["color", "backgroundColor"],
    }),
    true,
  );
  assert.equal(editor.innerHTML, "Hello");
});

test("clearStyleProperties keeps unrelated styles intact", () => {
  const { editor, window } = createHarness('<span style="color: red; font-weight: bold;">Hello</span>');

  selectNode(window, editor.querySelector("span"));

  assert.equal(
    window.CMTT.exec({
      op: "clearStyleProperties",
      properties: ["color"],
    }),
    true,
  );
  assert.equal(editor.innerHTML, '<span style="font-weight: bold;">Hello</span>');
});

test("insertList turns multiline text into separate list items", () => {
  const { editor, window } = createHarness("Alpha\nBeta");

  selectNodeContents(window, editor);

  assert.equal(window.CMTT.exec({ op: "insertList", ordered: false }), true);
  assert.equal(editor.innerHTML, "<ul><li>Alpha</li><li>Beta</li></ul>");
});

test("wordCount counts selected words and characters", () => {
  const { editor, window } = createHarness("Alpha Beta");

  selectNodeContents(window, editor);

  assert.deepEqual(toPlainObject(window.CMTT.exec({ op: "wordCount" })), {
    words: 2,
    characters: 10,
  });
});
