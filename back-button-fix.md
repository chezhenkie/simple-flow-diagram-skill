# Toolbar back button

The toolbar starts with a back button that returns to the page which linked here and is disabled when the tab has no earlier page. Three signals decide the state: the Navigation API, an arrival marker on generated links, and `history.length`.

## History length alone

`history.length` counts every entry in the tab: entries behind, entries ahead and entries from child frames. Only 1 proves that nothing is behind. A larger value proves nothing, and after Back to the first entry the length still counts the entry ahead, so the button stays active with no page to return to.

## The Navigation API

`navigation.canGoBack` is exact for same-origin contiguous history and follows every traversal. Firefox gives each `file://` document its own origin, so a page opened from a local link reports `canGoBack` false, `entries().length` 1 and `currentEntry.index` 0, while `history.back()` still returns to the linking page. Chromium treats all `file:` URLs as one origin, so the same read works there.

## The arrival marker

Every local `.html` link written by the toolbar carries `?mode=...&dark=...&light=...&via=1`. The mode and theme names keep the reader's state; `via=1` records that the page arrived through a generated link. On a `file:` page where the API reports no earlier entry, `via=1` plus a `history.length` above 1 proves that a Back entry exists. A new tab has `via=1` but a length of 1, so it stays grey, which is correct for that tab. A theme or mode pick rewrites the current entry and keeps the marker, so a reload and Back keep the state. No storage is used.

## State by case

| Case | Button |
| --- | --- |
| The Navigation API reports an earlier entry | active |
| `file:` page, API reports none, `via=1`, length above 1 | active |
| `file:` page opened in a new tab with `via=1`, length 1 | disabled |
| Index page, typed URL or bookmark without `via` | disabled |
| Browser without the Navigation API | length above 1, with the after-Back false positive |

The click calls `history.back()`, not `navigation.back()`, because a Navigation API traversal stays within the same origin and would not cross the Firefox file origin.

## Limits

A page reached by typing its URL in a tab that already has history, from a bookmark, or from a page that does not write the marker has a Back entry but no proof of it, so a local file in Firefox greys. A page opened from a link in a new tab carries the marker but has no earlier entry, so it is grey. Browsers without the API keep the false positive after Back. On a hosted site the API sees only same-origin entries, so an arrival from another site greys the first page; internal links then carry the marker.
