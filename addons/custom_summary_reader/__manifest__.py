{
  "name": "Custom Summary Reader",
  "version": "17.0.1.0.0",
  "author": "Your Name",
  "depends": ["base"],
  "data": [
    "security/ir.model.access.csv",
    "views/summary_views.xml",
    "wizard/import_wizard_views.xml",
    "menu.xml",
    "security/summary_security.xml",
    "views/summary_question_views.xml",
  ],
  "installable": True,
  "application": True,
  "license": "LGPL-3",
}