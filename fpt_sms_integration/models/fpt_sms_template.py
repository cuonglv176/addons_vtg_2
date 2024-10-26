from odoo import api, fields, models
import requests
import json

class FptSmsTemplate(models.Model):
    _name = 'fpt.sms.template'
    _description = 'FPT SMS Template'

    name = fields.Char("Template Name", required=True)
    content = fields.Text("Message Content", required=True)
    template_type = fields.Selection([('otp', 'OTP'), ('marketing', 'Marketing')], "Type", required=True)

    def send_sms(self, recipient, template_id):
        # Fetch API credentials from Odoo configuration
        api_key = self.env['ir.config_parameter'].sudo().get_param('fpt_sms.api_key')
        brandname = self.env['ir.config_parameter'].sudo().get_param('fpt_sms.brandname')

        if not api_key or not brandname:
            raise ValueError("API key or Brandname not configured.")

        template = self.browse(template_id)
        message_content = template.content

        # Sending SMS through FPT API
        url = "https://api.fpt.net/sms-brandname/v2.1/send"
        payload = {
            "brandname": brandname,
            "message": message_content,
            "phone": recipient,
            "type": "1" if template.template_type == 'otp' else "2"
        }
        headers = {
            'Content-Type': 'application/json',
            'api-key': api_key
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()

        # Save history of sent message
        self.env['fpt.sms.history'].create({
            'recipient': recipient,
            'message_content': message_content,
            'status': result.get('status'),
            'send_date': fields.Datetime.now()
        })

        return result


class FptSmsHistory(models.Model):
    _name = 'fpt.sms.history'
    _description = 'FPT SMS History'

    recipient = fields.Char("Recipient Number", required=True)
    message_content = fields.Text("Message Content", required=True)
    status = fields.Char("Status")
    send_date = fields.Datetime("Sent Date", default=fields.Datetime.now)
