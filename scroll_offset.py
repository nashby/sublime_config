'''
Simulate vim's scroll offset functionality.

Vim has a very nice feature called 'scrolloff' which allows to define a minimal
number of lines to keep above and below the cursor when scrolling. It makes it
very convenient to work with files where there's already content below the
cursor.

Configurable file settings:
* scroll_offset_top: Minimum number of lines to keep above cursor.
* scroll_offset_top_treshold: When to move (1 = always, 3 = every 3 rows).
* scroll_offset_bottom: Minimum number of lines to keep below cursor.
* scroll_offset_bottom_treshold: When to move (1 = always, 3 = every 3 rows).

@author: Oktay Acikalin <ok@ryotic.de>

@license: MIT (http://www.opensource.org/licenses/mit-license.php)

@since: 2011-02-14
'''

import sublime
import sublime_plugin

from support.view import view_is_widget


DEFAULT_OFFSET_TOP = 5
DEFAULT_OFFSET_BOTTOM = 5
DEFAULT_OFFSET_TOP_TRESHOLD = 1
DEFAULT_OFFSET_BOTTOM_TRESHOLD = 1


class ScrollOffsetListener(sublime_plugin.EventListener):
    '''
    An event listener to keep the cursor from the top and bottom of the view.
    '''

    def on_selection_modified(self, view):
        '''
        Checks and eventually scrolls the view to keep the cursor in the middle
        of the view.

        @type  view: sublime.View
        @param view: View to work with.

        @return: None
        '''
        if getattr(self, 'paused', False):
            return
        
        if view_is_widget(view):
            return
        
        get = view.settings().get
        offset_top = get('scroll_offset_top', DEFAULT_OFFSET_TOP)
        offset_top_treshold = get('scroll_offset_top_treshold',
                                  DEFAULT_OFFSET_TOP_TRESHOLD)
        offset_bottom = get('scroll_offset_bottom', DEFAULT_OFFSET_BOTTOM)
        offset_bottom_treshold = get('scroll_offset_bottom_treshold',
                                     DEFAULT_OFFSET_BOTTOM_TRESHOLD)

        file_region = view.size()
        file_begin = 0
        file_end = view.rowcol(file_region)[0]

        visible_region = view.visible_region()
        view_begin = view.rowcol(visible_region.begin())[0]
        view_end = view.rowcol(visible_region.end())[0]

        view_size = view_end - view_begin
        offset_sum = offset_top + offset_bottom
        while view_size <= offset_sum:
            # print view_size
            # print offset_sum
            offset_top /= 2
            offset_bottom /= 2
            offset_sum = offset_top + offset_bottom
            if offset_sum < 1:
                # print 'view is too small.'
                return

        selected_region = view.sel()[0]
        selection_end = view.rowcol(selected_region.b)[0]

        diff_top = (selection_end - view_begin)
        diff_bottom = (view_end - selection_end)

        # print 'file:', file_begin, file_end
        # print 'view:', view_begin, view_end
        # print 'selection:', selection_end
        # print 'diff:', diff_top, diff_bottom

        if diff_top < offset_top:
            amount = offset_top - diff_top
            amount_is_enough = amount >= offset_top_treshold
            if view_begin - amount >= file_begin and amount_is_enough:
                # print 'move up:', amount
                if amount > 1 and selected_region.size() > 0:
                    self.paused = True
                    def _move_up():
                        view.run_command('scroll_lines', {'amount': 1})
                        self.paused = False
                    sublime.set_timeout(_move_up, 100)
                else:
                    view.run_command('scroll_lines', {'amount': amount})
        if diff_bottom < offset_bottom:
            amount = offset_bottom - diff_bottom
            amount_is_enough = amount >= offset_bottom_treshold
            if view_end + amount <= file_end + 1 and amount_is_enough:
                # print 'move down:', amount
                if amount > 1 and selected_region.size() > 0:
                    self.paused = True
                    def _move_down():
                        view.run_command('scroll_lines', {'amount': -1})
                        self.paused = False
                    sublime.set_timeout(_move_down, 100)
                else:
                    view.run_command('scroll_lines', {'amount': -amount})
