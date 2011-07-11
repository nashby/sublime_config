'''
Highlights trailing spaces.

You might want to override the following parameters within your file settings:
* highlight_trailing_spaces_max_file_size
  Restrict this to a sane size in order not to DDOS your editor.
* highlight_trailing_spaces_color_name
  Change this to a valid scope name, which has to be defined within your theme.

@author: Oktay Acikalin <ok@ryotic.de>

@license: MIT (http://www.opensource.org/licenses/mit-license.php)

@since: 2011-02-11
'''

import sublime

from support.view import DeferedViewListener


DEFAULT_MAX_FILE_SIZE = 1048576
DEFAULT_COLOR_NAME = 'comment'


class HighlightTrailingSpacesListener(DeferedViewListener):
    '''
    An event listener to highlight trailing spaces.
    '''

    def __init__(self):
        super(HighlightTrailingSpacesListener, self).__init__()
        self.max_size_setting = 'highlight_trailing_spaces_max_file_size'
        self.default_max_file_size = DEFAULT_MAX_FILE_SIZE
        self.delay = 0

    def view_is_too_big_callback(self, view):
        view.erase_regions('HighlightTrailingSpacesListener')

    def update(self, view):
        '''
        Searches for trailing spaces and highlights them.

        @type  view: sublime.View
        @param view: View to work with.

        @return: None
        '''
        settings = view.settings()

        color_name = settings.get('highlight_trailing_spaces_color_name',
                                  DEFAULT_COLOR_NAME)
        trails = view.find_all('[ \t]+$')
        regions = []
        for trail in trails:
            regions.append(trail)
        view.add_regions('HighlightTrailingSpacesListener', regions, color_name,
                         sublime.DRAW_EMPTY_AS_OVERWRITE)
