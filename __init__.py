# -*- coding: utf-8 -*-

# Highlight Search Results in the Browser Add-on for Anki
#
# Copyright (C) 2017-2023  Aristotelis P. <https://glutanimate.com/>
#           (C) 2024 CravingCrates <https://github.com/CravingCrates>
#           (c) 2024 Shigeyuki  <https://github.com/shigeyukey>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.



#############
# This add-on is based on an idea requested by Anking and developed by CravingCrates
# based on Glutanimate “Highlight Search”, then debugged and forked by me(Shigeyuki).
#
# [ AnkiForums ] Suggestion : highlight cloze in card when selected in browser
# https://forums.ankiweb.net/t/suggestion-highlight-cloze-in-card-when-selected-in-browser/45726


import re
from typing import List
from bs4 import BeautifulSoup

from anki.consts import MODEL_CLOZE
from aqt import mw, gui_hooks, QWebEngineFindTextResult
from aqt.webview import AnkiWebView
from aqt.browser import Browser

from .popup.popup_config import set_gui_hook_change_log
set_gui_hook_change_log()

REGULAR_EXPRESSION_A = r"(\{\{c(\d+)::(.+?)(::(.*?))?\}\})"
    # -> select "{{c0:: ... }}"
REGULAR_EXPRESSION_B = r"(\{\{c(\d+)::)"
    # -> select only "{{c0::"

MAX_NUMBER_OF_ITERATIONS = 40
    # Cloze supports up to 20 (Field 20 + HTML Field 20 = 40 )

def handle_find_result(webview: AnkiWebView, term: str, matches: QWebEngineFindTextResult, count=0):
    # Re-search until the currently selected highlight(Orange) is at the top (activeMatch()==1)
        # Q. Why does it need loops?
            # 1. There is no function to select it in Qt. Highlighted in sequence, so need to update it until it reaches 1.
            # 2. Auto-scroll to the highlighted position, so if the text below is highlighted, the card is difficult to edit.
    if hasattr(matches, 'activeMatch'):
        if matches.activeMatch() != 1 and count < MAX_NUMBER_OF_ITERATIONS:
            # NOTE :When the number of Cloze is too many, flickering will occur.
            webview.findText(term, resultCallback=lambda matches: handle_find_result(webview, term, matches, count+1))
    else:
        pass

def highlight_terms(webview: AnkiWebView, terms: List[str]):
    # Highlight by "QWebEngineView.findText"
    if terms:
        webview.findText(terms[0], resultCallback=lambda matches: handle_find_result(webview, terms[0], matches))
    # "findText" can only select one.
        # Currently selected text -> Orange
        # Exact match text -> Yellow
    # Q. Why cannot all text be highlighted at once?
        # 1. Multiple selections are not possible because of Qt limitations ¯\_(ツ)_/¯
        # 2. Highlighting with JavaScript breaks the card template.
        # 3. It may be possible to enclose all the Cloze with <span> and color it with JavaScript and CSS?
                # (But that's an add-on to another mechanism.)


def on_browser_did_change_row(browser: Browser, *args, **kwargs):
    """
    Highlight cloze deletions in Editor pane on selecting a cloze card
    """

    selected_cards = browser.selected_cards()
    if not selected_cards or len(selected_cards) > 1:
        # When no card or two or more cards are selected.
        return

    card_id = browser.selected_cards()[0]
    card = mw.col.get_card(card_id)
    note = card.note()

    if note.note_type()["type"] != MODEL_CLOZE:
        return

    if not note.cloze_numbers_in_fields():
        return

    cloze_number = card.ord + 1
    cloze_list = []

    for field in note.fields:
        # Exclude HTML by beautifulSoup.
        field = BeautifulSoup(field, "html.parser").get_text()
        cloze_deletions = re.findall(REGULAR_EXPRESSION_A, field, re.DOTALL)
        if cloze_deletions == []:
            continue

        for cloze in cloze_deletions:
            # Only Cloze with matching numbers will be listed.
            if int(cloze[1]) == cloze_number:
                cloze_list.append(cloze[0])

        if len(cloze_list) >= 2:
            # If there are two or more clozes, select only "{{c0::"
                # Q. Why?
                    # 1. Exact match text is highlighted in yellow.
                    # 2. If there are multiple Cloze, the text will not exact match.
                    # 3. So only “{{c0:::” can highlight everything in the exact match.
            cloze_deletions = re.findall(REGULAR_EXPRESSION_B, field, re.DOTALL)
            cloze_list = [] # Reset regular expression.
            for cloze in cloze_deletions:
                if int(cloze[1]) == cloze_number:
                    cloze_list.append(cloze[0])

    highlight_terms(browser.editor.web, cloze_list)


gui_hooks.browser_did_change_row.append(on_browser_did_change_row)
