from odoo import models, fields


class SummaryAnswer(models.Model):
    _name = "summary.answer"
    _description = "Summary Answer"
    _order = "sequence, id"

    question_id = fields.Many2one(
        "summary.question",
        string="Question",
        required=True,
        ondelete="cascade",
        readonly=True,
    )
    sequence = fields.Integer(default=0, readonly=True)
    answer = fields.Text(readonly=True)
    user_id = fields.Char(string="User ID", readonly=True)
    user_name = fields.Char(string="User", readonly=True)
    form_id = fields.Char(string="Form ID", readonly=True)
    external_answer_id = fields.Char(string="External Answer ID", readonly=True)
