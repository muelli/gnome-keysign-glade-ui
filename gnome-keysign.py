#!/usr/bin/env python

import signal
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio


data = {
    'key1' : {'id':'2048R/ED8312A2 2014-04-08',
              'fpr':'BEFDD433DCF8956D0D36011B4B032D3DED8312A2',
              'uids':[
                    {'uid':'John Doe john.doe@test.com',
                     'sigs':['ED8312A2', '6FB8DCCE']
                    },
                    {'uid':'John Foo (Test Key) john.foe@test.com',
                     'sigs':['ED8312A2']
                    }
                    ],
              'expire':'2016-12-12',
              'nsigs':3
             },
    'key2' : {'id':'2048R/D32DFCFB 2015-08-20',
              'fpr':'B870D356F7ECD46CF2CEDF933BF372D3D32DFCFB',
              'uids':[
                    {'uid':'Foo Bar foo.bar@test.com',
                     'sigs':['D32DFCFB','6FB8DCCE']
                    }
                    ],
              'expire':'2016-05-20',
              'nsigs':2
             },
}


def formatListboxKeydata(keydata):
    keyid = keydata['id']
    uids = keydata['uids']
    expire = keydata['expire']
    nsigs = keydata['nsigs']

    result = "<b>{0}</b>\t\t\t{1}\n".format(keyid, nsigs)
    for uid in uids:
        result += "{}\n".format(uid['uid'])
    result += "\n"
    result += "<small>Expires {}</small>".format(expire)

    return result

def formatDetailsKeydata(keydata):
    result = "{0}\n".format(keydata['id'])
    for uid in keydata['uids']:
        result += "{}\n".format(uid['uid'])

    return result


class Handler:

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onDeleteKeyPresentWindow(self, *args):
        keyPresentWindow = args[0]
        keyPresentWindow.close()

    def onDeleteKeyConfirmWindow(self, *args):
        keyConfirmWindow = args[0]
        keyConfirmWindow.close()

    def onDeleteInvalidDialog(self, *args):
        pass

    def onListRowActivated(self, widget, row, *args):
        print "ListRow activated!Key '{}'' selected".format(row.keyid)

        keyPresentWindow = KeyPresentWindow(row.keyid)
        keyPresentWindow.show()

    def onListRowSelected(self, widget, row, *args):
        print "ListRow selected!Key '{}'' selected".format(row.keyid)

    def onTextChanged(self, widget):
        print "Gtk.Entry text changed: {}".format(widget.get_text())
        for key,val in data.items():
            if val['fpr'] == widget.get_text():
                keyConfirmWindow = KeyConfirmWindow(key)
                keyConfirmWindow.show_confirm_window()


# TODO split the signal handlers into different classes
global_handler = Handler()


class ListBoxRowWithKeyData(Gtk.ListBoxRow):

    def __init__(self, keyid, keydata):
        super(Gtk.ListBoxRow, self).__init__()
        self.keyid = keyid
        self.data = keydata

        label = Gtk.Label()
        label.set_markup(keydata)
        self.add(label)



class KeysignApp:

    def __init__(self):

        self.builder = Gtk.Builder()
        self.builder.add_from_file("MainWindow.glade")
        # self.builder.add_from_file("MainWindowNotebook.glade")
        self.builder.connect_signals(global_handler)

        self.app = self.builder.get_object("applicationwindow1")
        self.data = data


    def show(self):
        # notebook = self.builder.get_object("notebook1")
        listBox = self.builder.get_object('listbox1')

        for key,val in data.items():
            listBox.add(ListBoxRowWithKeyData(key, formatListboxKeydata(val)))

        self.app.show_all()


class KeyPresentWindow:

    def __init__(self, keyid):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("KeyPresentWindow.glade")
        self.builder.connect_signals(global_handler)

        self.window = self.builder.get_object("window1")
        self.key = data[keyid]

    def show(self):
        keyDetailsLabel = self.builder.get_object("keyDetailsLabel")
        keyDetailsLabel.set_markup(formatDetailsKeydata(self.key))

        fpr = "<b>{}</b>".format(self.key['fpr'])
        keyFingerprintLabel = self.builder.get_object("keyFingerprintLabel")
        keyFingerprintLabel.set_markup(fpr)

        self.window.show_all()


class KeyConfirmWindow:

    def __init__(self, keyid):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("KeyConfirmWindow.glade")
        self.builder.connect_signals(global_handler)

        self.confirm_window = self.builder.get_object("confirm_window")
        self.invalid_dialog = self.builder.get_object("invalid_dialog")
        self.key = data[keyid]

    def show_confirm_window(self):
        keyIdsLabel = self.builder.get_object("key_ids_label")
        keyIdsLabel.set_markup(self.key['id'])

        uidsLabel = self.builder.get_object("uids_label")
        markup = ""
        for uid in self.key['uids']:
            markup += uid['uid'] + "\n"
        uidsLabel.set_markup(markup)

        self.confirm_window.show_all()

    def show_invalid_dialog(self):
        pass


def main():
    keysignApp = KeysignApp()
    keysignApp.show()

    Gtk.main()

if __name__ == '__main__':
    main()