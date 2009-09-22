#!/usr/bin/env python
#
# Icon Theme Viewer
#
# Authors:
#   Danielle Madeley <danielle.madeley@collabora.co.uk>
#

import gtk
import gtk.gdk as gdk

PIXBUF, NAME, CONTEXT = range(3)
model = gtk.TreeStore(gdk.Pixbuf, str, str)

theme = gtk.icon_theme_get_default()

for context in theme.list_contexts():
    if context == 'Animations': continue # do not want

    iter = model.append(None, (None, context, None))

    for name in theme.list_icons(context):
        pixbuf = theme.load_icon(name, 48, 0)

        model.append(iter, (pixbuf, name, context))

window = gtk.Window()

vbox = gtk.VBox()
window.add(vbox)

entry = gtk.Entry()
vbox.pack_start(entry, expand = False)

filter = model.filter_new()
def filter_func(model, iter):
    name, context = model.get(iter, NAME, CONTEXT)
    if context is None: return True
    needle = entry.get_text()
    if needle == "": return True
    else: return needle in name

filter.set_visible_func(filter_func)

entry.connect('activate', lambda e: filter.refilter())

sw = gtk.ScrolledWindow()
vbox.pack_start(sw)

treeview = gtk.TreeView(filter)
column = gtk.TreeViewColumn("Icon")
treeview.append_column(column)

renderer = gtk.CellRendererPixbuf()
column.pack_start (renderer, expand = False)
column.set_attributes (renderer, pixbuf = PIXBUF)

renderer = gtk.CellRendererText()
column.pack_start (renderer, expand = True)
def name_data_func(column, renderer, model, iter):
    name, context = model.get(iter, NAME, CONTEXT)
    if context is None: # this is a context row
        nchildren = model.iter_n_children(iter)
        renderer.set_property('markup', '<b>%s</b> (%i)' % (name, nchildren))
    else:
        renderer.set_property('text', name)
column.set_cell_data_func(renderer, name_data_func)

sw.add(treeview)

window.show_all()
window.connect('destroy', lambda w: gtk.main_quit())
gtk.main()
