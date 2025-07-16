import requests
import json
from odoo import models, fields, _
from odoo.exceptions import UserError


class SummaryQuestion(models.Model):
    _name = "summary.question"
    _description = "Summary Question"
    _order = "sequence,id"

    template_id = fields.Many2one(
        "summary.template",
        string="Template",
        required=True,
        ondelete="cascade",
        readonly=True,
    )
    text = fields.Char(string="Question Text", required=True, readonly=True)
    qtype = fields.Selection(
        [
            ("number", "Number"),
            ("open", "Open"),
            ("close", "Close"),
            ("multichoice", "Multichoice"),
        ],
        string="Type",
        required=True,
        readonly=True,
    )
    sequence = fields.Integer(default=10, readonly=True)
    external_question_id = fields.Char(string="External Question ID", readonly=True)
    answers = fields.One2many(
        "summary.answer", "question_id", string="Answers", readonly=True
    )

    def action_view_analysis(self):
        self.ensure_one()
        base_url = (
            f"http://host.docker.internal:3001/analyze/{self.external_question_id}"
        )
        headers = {
            "Authorization": f"Bearer {self.env.context.get('token') or 'demo_token'}"
        }

        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise UserError(_("Failed to fetch analysis: %s") % str(e))

        data = response.json()
        content = json.dumps(data, indent=2)
        res_text = ""

        if data.get("questionType") == "CLOSE":
            res_text = f"YES: {data.get('YES', 0)}%, NO: {data.get('NO', 0)}%"
        elif data.get("questionType") == "MULTICHOICE":
            stats = data.get("stats", [])
            lines = [
                f"{item.get('title', 'Unknown')}: {item.get('percentage', 0)}%"
                for item in stats
            ]
            res_text = "\n".join(lines)
        elif data.get("questionType") == "NUMERICAL":
            answers = data.get("answers", [])
            numbers = []

            for ans in answers:
                try:
                    value = float(ans.get("answer", 0))
                    numbers.append(value)
                except (ValueError, TypeError):
                    continue

            if numbers:
                max_val = max(numbers)
                min_val = min(numbers)
                avg_val = round(sum(numbers) / len(numbers), 2)
                res_text = f"Max: {max_val}\nMin: {min_val}\nAvg: {avg_val}"
            else:
                res_text = "No valid numeric answers found."
        elif data.get("questionType") == "OPEN":
            res_text = 'You can check answers on previouse section for OPEN questions'
        return {
            "type": "ir.actions.act_window",
            "name": _("Analysis"),
            "res_model": "summary.analysis.popup",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_result_text": res_text.strip(),
                "default_json_data": content,
            },
        }
