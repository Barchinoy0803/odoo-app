from odoo import models, fields, api

class SummaryTemplate(models.Model):
    _name = "summary.template"
    _description = "External Template Summary"
    _rec_name = "title"

    _sql_constraints = [
        ('external_id_unique', 'unique(external_id)', 'External ID must be unique!')
    ]

    title = fields.Char(required=True, readonly=True)
    author = fields.Char(readonly=True)
    description = fields.Char(readonly=True)
    type = fields.Char(readonly=True)
    topic = fields.Char(readonly=True)
    external_id = fields.Char(string="External ID", required=True, index=True, readonly=True)
    questions = fields.One2many("summary.question", "template_id", string="Questions")
    question_count = fields.Integer(string="Question Count", compute="_compute_question_count", readonly=True)

    average_values = fields.Text(string="Average Values", compute="_compute_aggregated_results", readonly=True)
    min_values = fields.Text(string="Minimum Values", compute="_compute_aggregated_results", readonly=True)
    max_values = fields.Text(string="Maximum Values", compute="_compute_aggregated_results", readonly=True)
    popular_answers = fields.Text(string="Popular Answers", compute="_compute_aggregated_results", readonly=True)

    def _compute_question_count(self):
        for record in self:
            record.question_count = len(record.questions)

    def _compute_aggregated_results(self):
        for record in self:
            record.average_values = "N/A"
            record.min_values = "N/A"
            record.max_values = "N/A"
            record.popular_answers = "N/A"

    def action_open_token_popup(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'import.summary.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_template_id': self.id},
        }