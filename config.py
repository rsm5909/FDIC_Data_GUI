import os

LARGE_FONT = ('Verdana', 20)
REG_FONT = ('Verdana', 12, 'bold')
REG_BOLD = ('Verdana', 14, 'bold')
REG_LIGHT = ('Verdana', 12)

green = '#00694d'
tan = '#e3bb83'
grey = '#f4f4f3'
grey2 = '#ececec'

database = os.path.dirname(os.path.realpath(__file__)) + '/bhc_database.db'
views = os.path.dirname(os.path.realpath(__file__)) + '/viewnames.json'
dupku = os.path.dirname(os.path.realpath(__file__)) + '/dupku.json'
comm = os.path.dirname(os.path.realpath(__file__)) + '/common.json'
exclude = os.path.dirname(os.path.realpath(__file__)) + '/exclude.json'

show = os.path.dirname(os.path.realpath(__file__)) + '/show.png'
hide = os.path.dirname(os.path.realpath(__file__)) + '/hide.png'
excel = os.path.dirname(os.path.realpath(__file__)) + '/excel.png'
chart = os.path.dirname(os.path.realpath(__file__)) + '/chart.png'