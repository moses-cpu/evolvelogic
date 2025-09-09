{
    'name': 'Disable Copy-Paste in Survey',
    'version': '1.0',
    'category': 'Survey',
    'summary': 'Prevents copy-paste actions in the Survey module',
    'author': 'Your Name',
    'depends': ['base','web','survey'],
    'data': [
        'views/survey_templates.xml',
	'views/views.xml'
    ],
    'assets': {
#    'web.assets_backend': [
#            'disable_copy_paste_survey/static/src/js/video_preview.js',  # JavaScript file
#            'disable_copy_paste_survey/views/video_preview.xml',  # OWL XML template
#        ],
    'web.assets_backend': [
            'disable_copy_paste_survey/static/src/video_field.xml',
            'disable_copy_paste_survey/static/src/video_field.js',
            
        ],
    'web.assets_frontend': [
        'disable_copy_paste_survey/static/src/js/disable_copy_paste.js',
    	],

	},

    'installable': True,
    'application': False,
}
