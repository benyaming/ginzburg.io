from trumbowyg.widgets import TrumbowygWidget
from django.utils.safestring import mark_safe
from django.urls import reverse

from trumbowyg.widgets import get_trumbowyg_language


class ContentWidget(TrumbowygWidget):
    """
    Custom realisation of trumbowyg widget.
    """
    class Media:
        css = {
            'all': (
                'trumbowyg/ui/trumbowyg.css',
                'trumbowyg/admin.css',
            )
        }
        js = [
            '//ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js',
            'trumbowyg/trumbowyg.min.js',
            'trumbowyg/plugins/upload/trumbowyg.upload.js',
            f'trumbowyg/langs/{get_trumbowyg_language()}.min.js',
            'trumbowyg/dist/plugins/preformatted/trumbowyg.preformatted.min.js'
        ]

    def render(self, name, value, attrs=None, renderer=None):
        output = super(TrumbowygWidget, self).render(name, value, attrs)
        script = f'''
            <script>
            $("#id_{name}").trumbowyg({{
                lang: "{get_trumbowyg_language()}",
                semantic: true,
                resetCss: true,
                autogrow: true,
                removeformatPasted: true,
                btnsDef: {{
                    image: {{
                        dropdown: ['upload', 'insertImage', 'base64', 'noembed'],
                        ico: 'insertImage'
                    }}
                }},
                btns: [
                       ['formatting'],
                       'btnGrp-semantic',
                       ['link'],
                       ['image'],
                       'btnGrp-justify',
                       'btnGrp-lists',
                       ['horizontalRule'],
                       ['removeformat'],
                       ['fullscreen'],
                       ['viewHTML'],
                       ['preformatted'],
                ],
                plugins: {{
                    upload: {{
                        serverPath: '{reverse('trumbowyg_upload_image')}',
                        fileFieldName: 'image',
                        statusPropertyName: 'message',
                        urlPropertyName: 'file'
                    }}
                }}
            }});
            </script>
        '''
        output += mark_safe(script)
        return output
