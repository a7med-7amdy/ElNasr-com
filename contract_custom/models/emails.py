from odoo import api, fields, models

from odoo import models, fields, api, _


class ContractNotification(models.Model):
    _inherit = 'contract.contract'


    
    
    def start_end_date_notification(self):

        current_day = fields.Date.today()

        # Avoid sending notifications on Friday or Saturday
        # if current_day.weekday() in [4, 5]:
        #     print("❌ No notifications sent today (Friday/Saturday).")
        #     return

        records = self.sudo().search([
            ('state', '=', 'confirmed'), ('contract_type', '!=', 'general'),
            ('contract_admin', '!=', False)
        ])
        print(f"✅ Found {len(records)} contracts")


        for rec in records:
            manager_partners = rec.contract_admin.mapped('partner_id')
            email_3 = manager_partners.mapped('email')
            message_lines_2 = []
            if rec.contract_lines:
                print("contract_lines",rec.contract_lines)
                for line in rec.contract_lines:
                    print(f"Checking contract line: {line.id}, End Date: {line.contract_end_date}")

                    if line.contract_end_date:
                        print(f"End Date exists: {line.contract_end_date}, Today: {current_day}")
                        if line.contract_end_date and line.contract_end_date < current_day:
                            print("✅ Condition met: Contract End Date is after or equal to today.")
                        else:
                            print("❌ Condition NOT met: Contract End Date is before today.")
                        msg_2 = _(
                            "🔹 Contract: {contract}\n"
                            "🔹 has End Date Od : {end_date}\n"
                            "🔹 Old Than Today: {current_day}\n\n"
                            "Please take the necessary action."
                        ).format(
                            contract=rec.name,
                            end_date=line.contract_end_date,
                            current_day=current_day
                        )
                        print("######################",msg_2)

                        message_lines_2.append(msg_2)

            if message_lines_2:
                full_message = "Hello,\n\n" + "\n\n".join(message_lines_2)

                # ✅ Ensure `message_post` runs on a single record
                rec.sudo().message_post(
                    body=full_message,
                    subject="Contract Date Notification",
                    partner_ids=manager_partners.ids,
                    message_type='notification',
                )
                if email_3:
                    mail_values = {
                        'subject': "Contract Date Notification",
                        'body_html': f"<p>{full_message.replace('\n', '<br>')}</p>",
                        'email_to': ",".join(email_3),
                        'email_from': rec.env.user.company_id.email or rec.env.user.email,
                    }
                    mail = rec.env['mail.mail'].create(mail_values)
                    mail.sudo().send()
                    
                    
    def start_general_end_date_notification(self):

        current_day = fields.Date.today()

        # Avoid sending notifications on Friday or Saturday
        # if current_day.weekday() in [4, 5]:
        #     print("❌ No notifications sent today (Friday/Saturday).")
        #     return

        records = self.sudo().search([
            ('state', '=', 'confirmed'), ('contract_type', '=', 'general'),('contract_end_date', '!=', False),
            ('contract_admin', '!=', False)
        ])
        print(f"✅ Found {len(records)} contracts")


        for rec in records:
            manager_partners = rec.contract_admin.mapped('partner_id')
            email_3 = manager_partners.mapped('email')
            message_lines_2 = []
            if rec.contract_end_date < current_day:
                print("✅ Condition met: Contract End Date is after or equal to today.")
                msg_2 = _(
                    "🔹 General Contract: {contract}\n"
                    "🔹 has End Date Od : {end_date}\n"
                    "🔹 Old Than Today: {current_day}\n\n"
                    "Please take the necessary action."
                ).format(
                    contract=rec.name,
                    end_date=rec.contract_end_date,
                    current_day=current_day
                )
                print("######################",msg_2)

                message_lines_2.append(msg_2)

                if message_lines_2:
                    full_message = "Hello,\n\n" + "\n\n".join(message_lines_2)

                    # ✅ Ensure `message_post` runs on a single record
                    rec.sudo().message_post(
                        body=full_message,
                        subject="Contract Date Notification",
                        partner_ids=manager_partners.ids,
                        message_type='notification',
                    )
                    if email_3:
                        mail_values = {
                            'subject': "General Contract Date Notification",
                            'body_html': f"<p>{full_message.replace('\n', '<br>')}</p>",
                            'email_to': ",".join(email_3),
                            'email_from': rec.env.user.company_id.email or rec.env.user.email,
                        }
                        mail = rec.env['mail.mail'].create(mail_values)
                        mail.sudo().send()

    def start_email_notification(self, *args, **kwargs):
        print("🔔 start_email_notification triggered")

        current_day = fields.Date.today()

        # Avoid sending notifications on Friday or Saturday
        # if current_day.weekday() in [4, 5]:
        #     print("❌ No notifications sent today (Friday/Saturday).")
        #     return

        records = self.sudo().search([
            ('state', '=', 'confirmed'),
            ('contract_admin', '!=', False)
        ])

        print(f"✅ Found {len(records)} contracts")

        for rec in records:
            manager_partners = rec.contract_admin.mapped('partner_id')
            email_3 = manager_partners.mapped('email')
            message_lines = []
            if rec.contract_lines:
                for line in rec.contract_lines:
                    if line.max_qty >= line.withdrawn_quantity:
                        msg = _(
                            "🔹 Contract: {contract}\n"
                            "🔹 Max Quantity Reached: {max_qty}\n"
                            "🔹 Product: {product}\n\n"
                            "Please take the necessary action."
                        ).format(
                            contract=rec.name,
                            max_qty=line.max_qty,
                            product=line.product_id.name
                        )

                        message_lines.append(msg)

            if message_lines:
                full_message = "Hello,\n\n" + "\n\n".join(message_lines)

                # ✅ Ensure `message_post` runs on a single record
                rec.sudo().message_post(
                    body=full_message,
                    subject="Contract Quantity Notification",
                    partner_ids=manager_partners.ids,
                    message_type='notification',
                )
                if email_3:
                    mail_values = {
                        'subject': "Contract Quantity Notification",
                        'body_html': f"<p>{full_message.replace('\n', '<br>')}</p>",
                        'email_to': ",".join(email_3),
                        'email_from': rec.env.user.company_id.email or rec.env.user.email,
                    }
                    mail = rec.env['mail.mail'].create(mail_values)
                    mail.sudo().send()
