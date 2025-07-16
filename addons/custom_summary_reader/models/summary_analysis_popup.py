from odoo import models, fields


class SummaryAnalysisPopup(models.TransientModel):
    _name = "summary.analysis.popup"
    _description = "Popup to show analysis of a question"

    result_text = fields.Text(string="Analysis Result", readonly=True)
    json_data = fields.Text(string="Raw JSON", readonly=True)
