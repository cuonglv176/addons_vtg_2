from odoo import api, fields, models
import requests
import json

class FptConfig(models.Model):
    _name = 'fpt.config'
    _description = 'FPT SMS Config'

    name = fields.Char("Name", required=True)
    client_id = fields.Char("Client ID")
    client_secret = fields.Char("Client Secret")
    scope = fields.Char("Scope")
    grant_type = fields.Char("Grant Type")

