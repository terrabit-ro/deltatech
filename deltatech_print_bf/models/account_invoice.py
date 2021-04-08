# ©  2008-2021 Deltatech
#              Dorin Hongu <dhongu(@)gmail(.)com
# See README.rst file on addons root folder for license details


from odoo import _, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.move"

    receipt_print = fields.Boolean()  # bon fiscal tiparit

    def print_bf(self):
        wizard = self.env["account.invoice.export.bf"].with_context({"active_id": self.id}).create({})

        message = _("File receipt %s has been generated") % wizard.name
        self.message_post(body=message)
        wizard_download = self.env["wizard.download.file"].create(
            {"data_file": wizard.data_file, "file_name": wizard.name}
        )
        self.write({"receipt_print": True})
        return wizard_download.do_download_file()

    def action_switch_invoice_into_refund_credit_note(self):
        receipts = self.filtered(lambda m: m.type == "out_receipt")
        if receipts:
            receipts.write({"type": "out_invoice"})
        super(AccountInvoice, self).action_switch_invoice_into_refund_credit_note()
        if receipts:
            receipts.write({"type": "out_receipt"})
