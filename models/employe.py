from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    date_embauche = fields.Date(string="Date d'embauche")
    matricule = fields.Char(string="Matricule", required=True, copy=False)
    dernier_depart = fields.Date(string="Dernier départ en congé")
    prochain_depart = fields.Date(string="Prochain départ en congé")
    reliquat_conges = fields.Integer(string="Reliquat de congés")

    _sql_constraints = [
        ('matricule_unique', 'unique(matricule)', 'Le matricule doit être unique pour chaque employé.')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Générer un matricule automatiquement si non fourni
            if not vals.get('matricule'):
                vals['matricule'] = self.env['ir.sequence'].next_by_code('hr.employee.matricule') or '/'
        
        employees = super(HrEmployee, self).create(vals_list)

        leave_type = self.env['hr.leave.type'].search([('name', '=', 'Legal Leaves')], limit=1)

        

        if leave_type:
            for employee in employees:
                self.env['hr.leave'].create({
                    'employee_id': employee.id,
                    'holiday_status_id': leave_type.id,
                    'name': 'Congé automatique',
                    'request_date_from': date.today(),
                    'request_date_to': date.today(),
                    'request_unit_half': False,
                })

        return employees
    

    
    def print_leave_report(self):
        # Récupère tous les congés associés à cet employé
        leave_ids = self.env['hr.leave'].search([('employee_id', '=', self.id)])
        
        # Appelle l'action du rapport avec les congés filtrés
        return self.env.ref('gestion_conges.leave_report_template').report_action(leave_ids)