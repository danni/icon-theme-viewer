#!/usr/bin/env python
#
# Icon Theme Viewer
#
# Authors:
#   Danielle Madeley <danielle.madeley@collabora.co.uk>
#

import gtk
import gtk.gdk as gdk

PIXBUF, NAME = range(2)
model = gtk.TreeStore(gdk.Pixbuf, str)

theme = gtk.icon_theme_get_default()

for context in theme.list_contexts():
    if context == 'Animations': continue # do not want

    iter = model.append(None, (None, context))

    for name in theme.list_icons(context):
        pixbuf = theme.load_icon(name, 48, 0)

        model.append(iter, (pixbuf, name))

window = gtk.Window()

sw = gtk.ScrolledWindow()
window.add(sw)

treeview = gtk.TreeView(model)
column = gtk.TreeViewColumn("Icon")
treeview.append_column(column)

renderer = gtk.CellRendererPixbuf()
column.pack_start (renderer, expand = False)
column.set_attributes (renderer, pixbuf = PIXBUF)

renderer = gtk.CellRendererText()
column.pack_start (renderer, expand = True)
column.set_attributes (renderer, text = NAME)

sw.add(treeview)

window.show_all()
window.connect('destroy', lambda w: gtk.main_quit())
gtk.main()
