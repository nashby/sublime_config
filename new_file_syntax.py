'''
Stores syntax file from last activated view and reuses this for a new view.

@author: Oktay Acikalin <ok@ryotic.de>

@license: MIT (http://www.opensource.org/licenses/mit-license.php)

@since: 2011-03-05

@todo: Remove odd workaround below when/if "on_deactivated", "on_new" and
       "on_activated" events get fired in correct order.
'''

import sublime_plugin


class NewFileSyntaxListener(sublime_plugin.EventListener):

    def __init__(self, *args, **kwargs):
        super(NewFileSyntaxListener, self).__init__(*args, **kwargs)
        self.last_syntax = None
        self.new_buffers = []

    def on_new(self, view):
        # print 'on_new', self.last_syntax, view.buffer_id()
        self.new_buffers.append(view.buffer_id())

    def on_activated(self, view):
        # print 'on_activated', self.last_syntax, view.buffer_id()
        if view.buffer_id() in self.new_buffers:
            if self.last_syntax:
                view.set_syntax_file(self.last_syntax)
            self.new_buffers.remove(view.buffer_id())

    def on_deactivated(self, view):
        # print 'on_deactivated', self.last_syntax, view.buffer_id()
        if view.buffer_id() not in self.new_buffers:
            self.last_syntax = view.settings().get('syntax')
