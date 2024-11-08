# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import _, api, fields, models


class Message(models.Model):
    """ Messages model: system notification (replacing res.log notifications),
        comments (OpenChatter discussion) and incoming emails. """
    _inherit = 'mail.message'

    # message_type = fields.Selection(selection_add=[('system_notification', 'System Notification')])
    message_type = fields.Selection([
        ('email', 'Email'),
        ('comment', 'Comment'),
        ('notification', 'System notification'),
        ('user_notification', 'User Specific Notification'),
        ('system_notification', 'System Notification')
    ],
        'Type', required=True, default='email',
        help="Message type: email for email message, notification for system "
             "message, comment for other messages such as user replies",
    )
    active = fields.Boolean(string="Active", default=True)
    status = fields.Selection([('seen', 'Seen'), ('unseen', 'Unseen')], default='unseen')
    icon = fields.Char(string="Icon", help='Icon vector for system notification')
    url_portal = fields.Char(string="URL Portal")

    def update_status_message(self, *args, **kwargs):
        self.write({
            'status': 'seen'
        })
        # firebase_notification = self.env['firebase.notification'].sudo().search([('message_id','=',self.id)])
        # if len(firebase_notification) > 0:
        #     firebase_notification.mark_seen()
        # self.env['bus.bus'].sudo()._sendone(
        #     (self._cr.dbname, 'res.partner', self.author_id.id),
        #     {'type': 'notification_updated', 'notification_seen': True})

    def message_read_all(self):
        message_ids = self.env['mail.message'].sudo().search(
            [('active', '=', False), ('status', '=', 'unseen'), ('partner_ids', 'in', self.env.user.partner_id.ids)])
        for message in message_ids:
            message.update_status_message()
        # self.env['bus.bus'].sudo()._sendone(
        #     (self._cr.dbname, 'res.partner', self.author_id.id),
        #     {'type': 'notification_updated', 'notification_seen': True})

    def _push_system_notification(self, author_id, url_portal, recipients, subject_notification, model, res_id,
                                  icon='fa-user',
                                  body='', record_name='',
                                  timestamp=None, comment_id=False):
        """ Push system notification to recipients. Content's notification will be hidden on message log.
            Record has used for widget notification.

                   :param int author_id: author_id: object res.partner
                   :param list recipients: list recipients:  list id object res.partner
                   :param str subject_notification: subject's notification
                   :param str model: Model
                   :param int res_id: record of the model
                   :param str icon
                   :param str body
                   :param str record_name
                   :param datetime timestamp: time expected sent notification
               """
        partner_id = self.env['res.partner'].sudo().browse([author_id])
        subtype_id = self.env.ref('mail.mt_note').id
        # FirebaseNotificationObj = self.env['firebase.notification']
        message_ids = []
        for rc in recipients:
            values = {
                'url_portal': url_portal,
                'canned_response_ids': [],
                'author_id': author_id,
                'email_from': f'"{partner_id.name}" <{partner_id.email}>',
                'model': model,
                'create_date': timestamp if timestamp else datetime.now(),
                'res_id': res_id,
                'body': body,
                'subject': subject_notification,
                'message_type': 'system_notification',
                'partner_ids': [[6, 0, [rc]]],
                'active': False,
                'parent_id': False,
                'subtype_id': subtype_id,
                'status': 'unseen',
                'add_sign': True,
                'record_name': record_name,
                'icon': icon,
                'attachment_ids': []}

            message_id = self.env['mail.message'].sudo().create(values)
            message_ids.append(message_id)
        # if author_id:
        #     for at in recipients:
        #         user = self.env['res.users'].sudo().search([('partner_id', '=', at)], limit=1)
        #         if user:
        #             self.env['bus.bus'].sudo()._sendmany([[
        #                 'tcm_notification_%s' % user.id,
        #                 {'type': 'notification_updated', 'notification_unseen': True}]])
        #             user.sudo().notify_info(message=subject_notification)
        for message in message_ids:
            for partner in message.partner_ids:
                user = self.env['res.users'].sudo().search([('partner_id', '=', partner.id)], limit=1)
                if len(user) > 0:
                    model_type = {
                        'hr.express.delivery': 'express_delivery',
                        'hr.shuttle.bus': 'shuttle_bus',
                        'hr.leave': 'leave',
                        'hr.list.employee.going.on.business': 'list_going_on_business',
                        'hr.employee.going.on.business': 'list_going_on_business',
                        'hr.work.entry': 'timesheet',
                        'hr.employee.overtime.parent': 'overtime',
                        'hr.employee.have.child': 'have_child',
                        'hr.register.stationery': 'register_stationery',
                        'hr.register.meeting.room': 'meeting_room',
                        'hr.employee.dependant': 'dependant',
                    }
                    vals = {
                        'user_id': user.id,
                        'subject': 'Thông báo',
                        'message': message.subject,
                        'state': 'new',
                        'message_id': message.id,
                    }
                    # firebase_notification = FirebaseNotificationObj.sudo().create(vals)
                    # if message.model in model_type:
                    #     x_type = model_type[message.model]
                    # else:
                    #     x_type = ""
                    # firebase_notification.action_send(message.model, message.res_id, comment_id, x_type)

        return
