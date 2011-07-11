'''
Shows current filename in status bar when the view gets activated.

@author: Oktay Acikalin <ok@ryotic.de>

@license: MIT (http://www.opensource.org/licenses/mit-license.php)

@since: 2011-02-28

@todo: Remove odd workaround below when/if "on_deactivated", "on_new" and
       "on_activated" events get fired in correct order.
'''

import os.path

import sublime
import sublime_plugin

from support.view import view_is_widget


class ShowFilenameOnActivateListener(sublime_plugin.EventListener):

    def on_activated(self, view):
        if view_is_widget(view):
            return
        def _func():
            filename = view.file_name() or view.name()
            syntax = view.settings().get('syntax', 'unknown')
            if syntax:
                syntax = os.path.basename(syntax)
                syntax = os.path.splitext(syntax)[0]
            sublime.status_message('Current view: %s (%s)' % (filename, syntax))
        sublime.set_timeout(_func, 10)  # Workaround for wrong event order.
