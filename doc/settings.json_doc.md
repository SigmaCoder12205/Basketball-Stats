# VSCode settings.json Configuration Documentation

## Window & Layout

### Activity Bar
```json
"workbench.activityBar.location": "hidden"
```
Removes the vertical icon bar on the left side containing Explorer, Search, Source Control, Run, and Extensions icons.

### Editor Tabs
```json
"workbench.editor.showTabs": "single"
```
Displays only the active editor tab. Other open files are hidden from tab bar.

### Status Bar
```json
"workbench.statusBar.visible": false
```
Hides the bottom status bar showing line/column numbers, language mode, Git branch, errors/warnings.

### Sidebar
```json
"workbench.sideBar.location": "right"
```
Moves the file explorer and other sidebar panels to the right side of the window.

### Startup
```json
"workbench.startupEditor": "none"
```
Opens VSCode with a blank window instead of the Welcome page or previous session.

```json
"workbench.tips.enabled": false"
```
Disables tips and tricks notifications.

### Window Controls
```json
"window.zoomLevel": 3
```
Sets interface zoom to 300%. Affects all UI elements and text.

```json
"window.customTitleBarVisibility": "never"
```
Hides the custom title bar.

```json
"window.titleBarStyle": "native"
```
Uses the OS native title bar instead of VSCode's custom one.

## Theme & Icons

```json
"workbench.colorTheme": "Aura Dracula Spirit (Soft)"
```
Sets the color scheme. Requires Aura Theme extension.

```json
"workbench.iconTheme": "material-icon-theme"
```
Uses Material Icon Theme for file/folder icons. Requires extension.

```json
"material-icon-theme.hidesExplorerArrows": true
```
Removes expand/collapse arrows next to folders in file explorer.

## Tree View

```json
"workbench.tree.enableStickyScroll": false
```
Disables sticky scroll in tree views (file explorer, outline).

```json
"workbench.tree.renderIndentGuides": "none"
```
Removes vertical indent guide lines in tree structures.

```json
"workbench.tree.indent": 8
```
Sets indentation spacing for nested items to 8 pixels.

## Explorer

```json
"explorer.compactFolders": false
```
Shows each folder level separately instead of compacting single-child folders into one line.

```json
"explorer.confirmDragAndDrop": false
```
Disables confirmation dialog when dragging and dropping files.

```json
"explorer.confirmDelete": false
```
Disables confirmation dialog when deleting files.

```json
"explorer.decorations.badges": false
```
Hides badges showing file status (modified, ignored, etc.).

```json
"breadcrumbs.enabled": false
```
Hides the breadcrumb navigation at the top of the editor showing file path.

## Editor Core

### Minimap
```json
"editor.minimap.enabled": false
```
Disables the code minimap preview on the right edge of the editor.

### Line Numbers
```json
"editor.lineNumbers": "relative"
```
Shows relative line numbers. Current line shows absolute number, others show distance from cursor.

### Font
```json
"editor.fontFamily": "Dank Mono"
```
Sets editor font to Dank Mono, a monospaced font with coding ligatures.

```json
"editor.fontSize": 14
```
Font size in pixels.

```json
"editor.fontLigatures": true
```
Enables font ligatures. Combines character sequences like `=>`, `!=`, `>=` into single glyphs.

```json
"editor.lineHeight": 2.5
```
Line height multiplier. Each line is 2.5× the font size in height.

### Cursor
```json
"editor.cursorBlinking": "solid"
```
Cursor does not blink. Remains solid/visible at all times.

```json
"editor.cursorStyle": "block"
```
Block cursor that covers the character underneath.

```json
"editor.multiCursorModifier": "ctrlCmd"
```
Adds additional cursors with Cmd (Mac) or Ctrl (Windows/Linux) + Click.

### Indentation
```json
"editor.tabSize": 2
```
Sets tab width to 2 spaces.

```json
"editor.detectIndentation": false
```
Disables automatic detection of indentation from file content. Always uses configured tab size.

## Editor Visual Elements

### Highlighting
```json
"editor.renderLineHighlight": "none"
```
Disables highlighting of the current line.

```json
"editor.occurrencesHighlight": "off"
```
Disables automatic highlighting of matching symbols when cursor is on them.

```json
"editor.selectionHighlight": false
```
Disables highlighting of text matching the current selection.

### Guides & Whitespace
```json
"editor.showFoldingControls": "never"
```
Hides code folding chevrons/arrows in the gutter.

```json
"editor.guides.indentation": false
```
Removes vertical indentation guide lines.

```json
"editor.renderWhitespace": "none"
```
Does not display dots/symbols for spaces and tabs.

### Scrollbars
```json
"editor.scrollbar.horizontal": "hidden"
```
Hides horizontal scrollbar.

```json
"editor.scrollbar.vertical": "hidden"
```
Hides vertical scrollbar. Content still scrollable via trackpad/mouse wheel.

```json
"editor.scroll.decoration": "display: none"
```
Applied via CSS. Removes scroll position indicator shadow at top of editor.

### Overview Ruler
```json
"editor.overviewRulerBorder": false
```
Removes border around the overview ruler (thin column on right edge showing marks).

```json
"editor.hideCursorInOverviewRuler": true
```
Hides cursor position indicator in overview ruler.

All `editorOverviewRuler.*` settings in `workbench.colorCustomizations` set to `#0000` (transparent) to hide all marks in the overview ruler including:
- Word highlights
- Selection highlights
- Range highlights
- Bracket matches
- Find matches
- Modified/deleted/added lines
- Warnings/errors/info marks

### Sticky Scroll
```json
"editor.stickyScroll.enabled": false
```
Disables sticky scroll that keeps function/class headers visible at top when scrolling.

### Decorators & Hints
```json
"editor.colorDecorators": false
```
Hides inline color previews next to color codes.

```json
"editor.codeLens": false
```
Disables CodeLens (inline annotations showing references, implementations, etc.).

```json
"editor.links": false
```
Disables clickable links in editor.

```json
"editor.matchBrackets": "never"
```
Disables bracket pair highlighting.

```json
"editor.parameterHints.enabled": false
```
Disables parameter hints popup when typing function calls.

```json
"editor.lightbulb.enabled": "off"
```
Hides lightbulb icon for quick fixes and refactorings.

```json
"editor.hover.enabled": "off"
```
Disables hover tooltips when mousing over code.

## IntelliSense & Suggestions

```json
"editor.quickSuggestions": {
  "other": "off"
}
```
Disables automatic suggestion popup while typing.

```json
"editor.suggestOnTriggerCharacters": false
```
Disables suggestions when typing trigger characters like `.` or `(`.

```json
"editor.tabCompletion": "on"
```
Enables tab completion. Pressing Tab accepts the top suggestion.

```json
"editor.snippetSuggestions": "top"
```
Places code snippets at the top of suggestion list.

```json
"emmet.triggerExpansionOnTab": true
```
Enables Emmet abbreviation expansion with Tab key.

## Token Customization

```json
"editor.tokenColorCustomizations": {
  "textMateRules": [
    {
      "scope": "comment",
      "settings": {
        "fontStyle": "italic"
      }
    }
  ]
}
```
Sets all code comments to display in italic font style.

## Files

```json
"files.trimTrailingWhitespace": true
```
Automatically removes trailing whitespace from lines when saving.

```json
"files.insertFinalNewline": true
```
Automatically adds a newline at the end of files when saving.

```json
"files.autoSave": "afterDelay"
```
Automatically saves files after a delay (default 1000ms) of no typing.

## Git/SCM

```json
"git.decorations.enabled": false
```
Hides Git status decorations (colors, badges) in file explorer.

```json
"scm.diffDecorations": "none"
```
Removes inline diff decorations (added/modified/deleted line indicators) in editor gutter.

## Extensions & Updates

```json
"update.mode": "none"
```
Disables automatic VSCode updates. Must update manually.

```json
"extensions.ignoreRecommendations": true
```
Disables extension recommendation notifications.

## Custom UI Styling

### Title Bar (macOS)
```json
"custom-ui-style.electron": {
  "titleBarStyle": "hiddenInset",
  "trafficLightPosition": {
    "x": 20,
    "y": 16
  }
}
```
Requires Custom UI Style extension. Hides title bar with inset style and positions traffic light buttons (close/minimize/maximize) at coordinates (20, 16).

### Font
```json
"custom-ui-style.font.sansSerif": "Dank Mono"
```
Sets UI elements to use Dank Mono font.

### CSS Overrides
```json
"custom-ui-style.stylesheet": { ... }
```
Applies custom CSS rules to VSCode interface. Key modifications:

**Notifications & Dialogs**
- `.notification-toast`: Removes box shadow from notification toasts
- `.quick-input-widget.show-file-icons`: Removes box shadow from quick input
- `.quick-input-widget`: Positions quick input at 25% from top
- `.quick-input-list .scrollbar`: Hides scrollbar in quick input list
- `.monaco-action-bar.quick-input-inline-action-bar`: Hides inline action bar
- `.quick-input-titlebar`: Sets background color to `#100B15`

**Editor Widget**
- `.editor-widget.find-widget`: Removes box shadow and adds 4px border radius to find widget

**Editor Tabs**
- `.monaco-workbench .part.editor > .content .editor-group-container > .title.title-border-bottom:after`: Removes bottom border from tab bar
- `.title-actions`: Hides tab action buttons
- `.title .monaco-icon-label:after`: Removes right margin from icon label
- `.monaco-workbench .part.editor > .content .editor-group-container > .title > .label-container > .title-label`: Adds 60px left padding to title label
- `.title .monaco-icon-label.file-icon`: Centers icon with 60px horizontal margins
- `.title.show-file-icons .label-container .monaco-icon-label.file-icon`: Centers file icon with no padding

**Sidebar**
- `.sidebar .title-label`: Removes padding from sidebar title label
- `.sidebar`: Removes border from sidebar
- `.monaco-scrollable-element > .shadow.top`: Hides top shadow on scrollable elements

**Lists & Focus**
- `.monaco-workbench .monaco-list:not(.element-focused):focus:before`: Removes outline from unfocused lists
- `.monaco-list-row.focused`: Removes outline from focused list rows

**Scroll Decoration**
- `.monaco-editor .scroll-decoration`: Hides scroll position indicator

**Cursor**
- `.monaco-editor .cursors-layer .cursor`: Applies gradient background (pink to orchid) to cursor

## Color Customizations

```json
"workbench.colorCustomizations": {
  "editorCursor.background": "#000000",
  "[Aura Dracula Spirit (Soft)]": {
    "editorSuggestWidget.selectedBackground": "#3A334B",
    "sideBar.background": "#191521"
  }
}
```

**Global**
- `editorCursor.background`: Sets cursor inner color to black

**Theme-Specific (Aura Dracula Spirit Soft)**
- `editorSuggestWidget.selectedBackground`: Sets selected suggestion background to `#3A334B`
- `sideBar.background`: Sets sidebar background to `#191521`

All overview ruler colors set to transparent (`#0000`) to completely hide the overview ruler marks.

## Dependencies

**Required Extensions:**
- Aura Theme
- Material Icon Theme
- Custom UI Style

**Required Font:**
- Dank Mono
