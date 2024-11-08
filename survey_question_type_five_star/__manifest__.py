# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Survey five stars question type",
    "summary": """
        This module add five stars rating as question type for survey page""",
    "version": "14.0.1.0.1",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/survey",
    "depends": ["survey"],
    "data": ["views/survey_question.xml", "templates/survey_template.xml"],
    "demo": [],
    'assets': {
        'web.assets_frontend': [
            'survey_question_type_five_star/static/src/js/survey.js',
            'survey_question_type_five_star/static/src/scss/parameters.scss',
            'survey_question_type_five_star/static/src/scss/survey.scss',
        ],
    },
}
