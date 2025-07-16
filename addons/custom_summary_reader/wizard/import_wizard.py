import json
import requests
from odoo import models, fields, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class ImportSummaryWizard(models.TransientModel):
    _name = "import.summary.wizard"
    _description = "Import Summaries via API"

    token = fields.Char(required=True, string="API Token")

    def action_import(self):
        base_url = f"http://host.docker.internal:3001/template/token/{self.token}"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise UserError(_("API request failed: %s") % str(e))

        templates = response.json()
        Template = self.env["summary.template"]

        created = 0
        updated = 0
        skipped = 0

        qtype_map = {
            "OPEN": "open",
            "NUMERICAL": "number",
            "MULTICHOICE": "multichoice",
            "CLOSE": "close",
        }

        for template_data in templates:
            external_id = template_data.get("id")
            if not external_id:
                skipped += 1
                continue

            questions_data = template_data.get("Question") or template_data.get("questions") or []
            questions = []

            for q in questions_data:
                answers_data = q.get("Answer", [])
                answers = []
                for a in answers_data:
                    answers.append((0, 0, {
                        "answer": a.get("answer"),
                        "sequence": a.get("sequence", 0),
                        "user_id": a.get("userId"),
                        "user_name": a.get("username"),
                        "form_id": a.get("formId"),
                        "external_answer_id": a.get("id"),
                    }))

                questions.append((0, 0, {
                    "text": q.get("title", ""),
                    "qtype": qtype_map.get(q.get("type"), "text"),
                    "sequence": q.get("sequence", 0),
                    "external_question_id": q.get("id"),
                    "answers": answers,
                }))

            vals = {
                "title": template_data.get("title", "No title"),
                "author": template_data.get("userId"),
                "description": template_data.get("description"),
                "type": template_data.get("type"),
                "topic": template_data.get("topic"),
                "external_id": external_id,
            }

            existing = Template.search([("external_id", "=", external_id)], limit=1)
            if existing:
                vals["questions"] = [(5, 0, 0)] + questions
                existing.write(vals)
                updated += 1
            else:
                vals["questions"] = questions
                Template.create(vals)
                created += 1

        self.env.cr.commit()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Import completed"),
                "message": _("Created: %d, Updated: %d, Skipped: %d") % (created, updated, skipped),
                "type": "success",
                "sticky": False,
            }
        }
