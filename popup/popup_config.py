

from aqt import QAction, QDialog, QHBoxLayout, QIcon, QMenu, QTextBrowser, Qt, qconnect
from aqt import QVBoxLayout, QLabel, QPushButton
from aqt import mw
from os.path import join, dirname
from aqt import QPixmap,gui_hooks
from aqt.utils import openLink


CHANGE_LOG = "is_change_log"
CHANGE_LOG_DAY = "2024_06_26-"

# mini-pupup
SIZE_MINI_WIDTH = 400
SIZE_MINI_HEIGHT = 350

# Large-popup
SIZE_BIG_WIDTH = 600
SIZE_BIG_HEIGHT = 500

POKEBALL_PATH = r"popup_icon.png"

THE_ADDON_NAME = "🖌️Auto Highlight Cloze in Browser (Fork by Shige)"
SHORT_ADDON_NAME = "🖌️Auto Highlight"
IS_CHANGE_LOG = None
GITHUB_URL = "https://github.com/shigeyukey/Auto-Highlight-Cloze-in-Browser-Fork-by-Shige/issues"




ANKI_WEB_URL = ""
RATE_THIS_URL = ""

ADDON_PACKAGE = mw.addonManager.addonFromModule(__name__)
# ｱﾄﾞｵﾝのURLが数値であるか確認
if (isinstance(ADDON_PACKAGE, (int, float))
    or (isinstance(ADDON_PACKAGE, str)
    and ADDON_PACKAGE.isdigit())):
    ANKI_WEB_URL = f"https://ankiweb.net/shared/info/{ADDON_PACKAGE}"
    RATE_THIS_URL = f"https://ankiweb.net/shared/review/{ADDON_PACKAGE}"





IS_CHANGE_LOG = True
PATREON_URL = "http://patreon.com/Shigeyuki"
REDDIT_URL = "https://www.reddit.com/r/Anki/comments/1b0eybn/simple_fix_of_broken_addons_for_the_latest_anki/"

POPUP_PNG = r"popup_shige.png"


NEW_FEATURE = """
2024_06_26
[1] Fixed a bug
    - Support for PyQt5
"""

CHANGE_LOG_TEXT = """
[ Change log : {addon} ]

Shigeyuki :
Hello, thank you for using this add-on!😆
I updated this Add-on.
{new_feature}
If you like this Add-on, please support
my activities on Patreon. Thank you!



2024_06_12
[1] First Release
    - It works with Cloze note type from the Browser.
    - Please report any problems.

""".format(addon=SHORT_ADDON_NAME,new_feature=NEW_FEATURE)



CHANGE_LOG_TEXT_B = """
{addon}
Shigeyuki :
Hello, thank you for using this add-on!😆
Options are still under development.

If you like this Add-on, please support
my activities on Patreon. Thank you!

[ Change log ]

2024_06_26
[1] Fixed a bug
    - Support for PyQt5

2024_06_12
[1] First Release
    - It works with Cloze note type from the Browser.
    - Please report any problems.

[ Contribution ]
This add-on is based on an idea requested by Anking and developed
by CravingCrates based on Glutanimate “Highlight Search”,
then debugged, forked and customized by me (Shigeyuki).

Copyright (C) 2017-2023  Aristotelis P. <https://glutanimate.com/>
(C) 2024 CravingCrates <https://github.com/CravingCrates>
(c) 2024 Shigeyuki  <https://github.com/shigeyukey>

[ Patreon ] Special thanks
Without the support of my Patrons, I would never have been
able to develop this. Thank you very much!🙏

Arthur Bookstein, Haruka, Luis Alberto, Letona Quispe, Haley Schwarz, GP O'Byrne, Oleksandr Pashchenko, Alba Grecia Suárez Recuay, Douglas Beeman, Renoaldo Costa Silva Junior, Felipe Dias, Tobias Klös, 07951350313540, Ernest Chan, Corentin, Yitzhak Bar Geva, 龍星 武田, Muneeb Khan, Kurt Grabow, Daniel Kohl-Fink, Gabriel Vinicio Guedes, Ansel Ng, Maik C., Ricardo Escobar, Daniel Valcárcel Málaga, Lerner Alcala, Alex D, Blake, Hikori, Ketan Pal, Kyle Mondlak, Natalia Ostaszewska, Lily, Wa sup, Victor Evangelista, NamelessGO, Tim, Knightwalker, Lukas Hammerschmidt, as cam, Richard Fernandez, K Chuong Dang, Jason Liu, Hashem Hanaktah, Justin Skariah, Marli, Ella Schultz, Ali Abid, Siva Garapati, Nitin Chetla, hubert tuyishime, J, Dan S, Salman Majid, C, Maduka Gunasinghe, Marcin Skic, Andreas China, Lê Hoàng Phúc, anonymous, Jesse Asiedu, Chanho Youne, Dhenis Ferisco, Wave
""".format(addon=SHORT_ADDON_NAME,new_feature=NEW_FEATURE)



# ------- Rate This PopUp ---------------

def set_gui_hook_change_log():
    gui_hooks.main_window_did_init.append(change_log_popup)
    gui_hooks.main_window_did_init.append(add_config_button)

def change_log_popup(*args,**kwargs):
    try:
        config = mw.addonManager.getConfig(__name__)
        # if (config[IS_RATE_THIS] == False and config[CHANGE_LOG] == False):
        if (config.get(CHANGE_LOG, False) != CHANGE_LOG_DAY):

            dialog = CustomDialog(None,CHANGE_LOG_TEXT,size_mini=True)
            if hasattr(dialog, 'exec'):result = dialog.exec() # Qt6
            else:result = dialog.exec_() # Qt5

            if result == QDialog.DialogCode.Accepted:
                openLink(PATREON_URL)
                toggle_rate_this()
            elif  result == QDialog.DialogCode.Rejected:
                toggle_changelog()

    except Exception as e:
        print(e)
        pass



def change_log_popup_B(*args,**kwargs):
    try:
        dialog = CustomDialog(None,CHANGE_LOG_TEXT_B,True)
        if hasattr(dialog, 'exec'):result = dialog.exec() # Qt6
        else:result = dialog.exec_() # Qt5

        if result == QDialog.DialogCode.Accepted:
            openLink(PATREON_URL)
            toggle_rate_this()
        elif  result == QDialog.DialogCode.Rejected:
            toggle_changelog()
    except Exception as e:
        print(e)
        pass



# ----- add-onのconfigをｸﾘｯｸしたら設定ｳｨﾝﾄﾞｳを開く -----
def add_config_button():
    mw.addonManager.setConfigAction(__name__, change_log_popup_B)
    # ----- ﾒﾆｭｰﾊﾞｰに追加 -----
    action = QAction(THE_ADDON_NAME, mw)
    qconnect(action.triggered, change_log_popup_B)
    mw.form.menuTools.addAction(action)

# ================================================



class CustomDialog(QDialog):
    def __init__(self, parent=None,change_log_text=CHANGE_LOG_TEXT,more_button=False,size_mini=False):
        super().__init__(parent)

        addon_path = dirname(__file__)
        icon = QPixmap(join(addon_path, POPUP_PNG))
        layout = QVBoxLayout()
        if size_mini:
            self.resize(SIZE_MINI_WIDTH, SIZE_MINI_HEIGHT)
        else:
            self.resize(SIZE_BIG_WIDTH, SIZE_BIG_HEIGHT)

        pokeball_icon = QIcon(join(addon_path, POKEBALL_PATH))
        self.setWindowIcon(pokeball_icon)

        self.setWindowTitle(THE_ADDON_NAME)

        icon_label = QLabel()
        icon_label.setPixmap(icon)

        hbox = QHBoxLayout()

        change_log_label = QTextBrowser()
        change_log_label.setReadOnly(True)
        change_log_label.setOpenExternalLinks(True)

        change_log_label.setPlainText(change_log_text)

        hbox.addWidget(icon_label)
        hbox.addWidget(change_log_label)

        layout.addLayout(hbox)


        if more_button:
            button_layout = QVBoxLayout()
        else:
            button_layout = QHBoxLayout()

        self.yes_button = QPushButton("💖Patreon")
        self.yes_button.clicked.connect(self.accept)
        self.yes_button.setFixedWidth(120)


        if more_button:
            row1_layout = QHBoxLayout()
            row1_layout.addWidget(self.yes_button)
        else:
            button_layout.addWidget(self.yes_button)

        if more_button:
            self.rate_button = QPushButton("👍️RateThis")
            self.rate_button.clicked.connect(lambda : openLink(RATE_THIS_URL))
            self.rate_button.setFixedWidth(120)
            row1_layout.addWidget(self.rate_button)
            if RATE_THIS_URL == "":
                self.rate_button.setEnabled(False)

            self.ankiweb_button = QPushButton("🌟AnkiWeb")
            self.ankiweb_button.clicked.connect(lambda : openLink(ANKI_WEB_URL))
            self.ankiweb_button.setFixedWidth(120)
            row1_layout.addWidget(self.ankiweb_button)
            if ANKI_WEB_URL == "":
                self.ankiweb_button.setEnabled(False)

            button_layout.addLayout(row1_layout)

            row2_layout = QHBoxLayout()

            self.reddit_button = QPushButton("👨‍🚀Reddit")
            self.reddit_button.clicked.connect(lambda : openLink(REDDIT_URL))
            self.reddit_button.setFixedWidth(120)
            row2_layout.addWidget(self.reddit_button)

            self.github_button = QPushButton("🐈️Github")
            self.github_button.clicked.connect(lambda : openLink(GITHUB_URL))
            self.github_button.setFixedWidth(120)
            row2_layout.addWidget(self.github_button)

        self.no_button = QPushButton("Close")
        self.no_button.clicked.connect(self.reject)
        self.no_button.setFixedWidth(120)
        if more_button:
            row2_layout.addWidget(self.no_button)
            button_layout.addLayout(row2_layout)
        else:
            button_layout.addWidget(self.no_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        layout.addLayout(button_layout)
        self.setLayout(layout)

def toggle_rate_this():
    config = mw.addonManager.getConfig(__name__)
    # config[IS_RATE_THIS] = True
    config[CHANGE_LOG] = CHANGE_LOG_DAY
    mw.addonManager.writeConfig(__name__, config)

def toggle_changelog():
    config = mw.addonManager.getConfig(__name__)
    config[CHANGE_LOG] = CHANGE_LOG_DAY
    mw.addonManager.writeConfig(__name__, config)

# -----------------------------------

# class CustomDialog(QDialog):
#     def __init__(self, parent=None,change_log_text=CHANGE_LOG_TEXT,more_button=False):
#         super().__init__(parent)

#         addon_path = dirname(__file__)
#         icon = QPixmap(join(addon_path, POPUP_PNG))
#         layout = QVBoxLayout()

#         pokeball_icon = QIcon(join(addon_path, POKEBALL_PATH))
#         self.setWindowIcon(pokeball_icon)

#         self.setWindowTitle(THE_ADDON_NAME)

#         icon_label = QLabel()
#         icon_label.setPixmap(icon)

#         hbox = QHBoxLayout()

#         rate_this_label = QLabel(change_log_text)
#         rate_this_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
#         hbox.addWidget(icon_label)
#         hbox.addWidget(rate_this_label)

#         layout.addLayout(hbox)


#         if more_button:
#             button_layout = QVBoxLayout()
#         else:
#             button_layout = QHBoxLayout()

#         self.yes_button = QPushButton("💖Patreon")
#         self.yes_button.clicked.connect(self.accept)
#         self.yes_button.setFixedWidth(120)


#         if more_button:
#             row1_layout = QHBoxLayout()
#             row1_layout.addWidget(self.yes_button)
#         else:
#             button_layout.addWidget(self.yes_button)

#         if more_button:
#             self.rate_button = QPushButton("👍️RateThis")
#             self.rate_button.clicked.connect(lambda : openLink(RATE_THIS_URL))
#             self.rate_button.setFixedWidth(120)
#             row1_layout.addWidget(self.rate_button)
#             if RATE_THIS_URL == "":
#                 self.rate_button.setEnabled(False)

#             self.ankiweb_button = QPushButton("🌟AnkiWeb")
#             self.ankiweb_button.clicked.connect(lambda : openLink(ANKI_WEB_URL))
#             self.ankiweb_button.setFixedWidth(120)
#             row1_layout.addWidget(self.ankiweb_button)
#             if ANKI_WEB_URL == "":
#                 self.ankiweb_button.setEnabled(False)

#             button_layout.addLayout(row1_layout)

#             row2_layout = QHBoxLayout()

#             self.reddit_button = QPushButton("👨‍🚀Reddit")
#             self.reddit_button.clicked.connect(lambda : openLink(REDDIT_URL))
#             self.reddit_button.setFixedWidth(120)
#             row2_layout.addWidget(self.reddit_button)

#             self.github_button = QPushButton("🐈️Github")
#             self.github_button.clicked.connect(lambda : openLink(GITHUB_URL))
#             self.github_button.setFixedWidth(120)
#             row2_layout.addWidget(self.github_button)

#         self.no_button = QPushButton("Close")
#         self.no_button.clicked.connect(self.reject)
#         self.no_button.setFixedWidth(120)
#         if more_button:
#             row2_layout.addWidget(self.no_button)
#             button_layout.addLayout(row2_layout)
#         else:
#             button_layout.addWidget(self.no_button)

#         layout.addLayout(button_layout)
#         self.setLayout(layout)

#         layout.addLayout(button_layout)
#         self.setLayout(layout)

# def toggle_rate_this():
#     config = mw.addonManager.getConfig(__name__)
#     # config[IS_RATE_THIS] = True
#     config[CHANGE_LOG] = CHANGE_LOG_DAY
#     mw.addonManager.writeConfig(__name__, config)

# def toggle_changelog():
#     config = mw.addonManager.getConfig(__name__)
#     config[CHANGE_LOG] = CHANGE_LOG_DAY
#     mw.addonManager.writeConfig(__name__, config)

# # -----------------------------------
