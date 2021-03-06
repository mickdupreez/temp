from powerline import Powerline
from powerline.lib.dict import mergedicts


class LemonbarPowerline(Powerline):
    def init(self):
        super(LemonbarPowerline, self).init(ext='wm', renderer_module='lemonbar')

    get_encoding = staticmethod(lambda: 'utf-8')

    def get_local_themes(self, local_themes):
        if not local_themes:
            return {}

        return dict((
            (key, {'config': self.load_theme_config(val)})
            for key, val in local_themes.items()
        ))

INTERNAL_BAR_COMMAND = b"#bar;"
SEGMENT_NAME = b"#sname;"
