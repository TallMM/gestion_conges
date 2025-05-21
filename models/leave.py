from odoo import models

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def action_print_report(self):
        return self.env.ref('gestion_conges.report_conge_planning').report_action(self)
