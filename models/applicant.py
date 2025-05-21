from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        for rec in self:
            if rec.stage_id.name == 'Contrat signé' and not rec.employee_id:
                # Créer l’employé automatiquement
                employee = self.env['hr.employee'].create({
                    'name': rec.partner_name or rec.name,
                    'job_id': rec.job_id.id,
                    'department_id': rec.department_id.id,
                    'work_email': rec.email_from,
                    'work_phone': rec.partner_phone,
                    'date_embauche': fields.Date.today(),  # facultatif ici si tu ne gères pas le contrat
                })

                rec.employee_id = employee.id

                # Créer automatiquement un planning de congé
                self.env['gestion.conge'].create({
                    'employe_id': employee.id,
                   # 'dernier_depart': fields.Date.today(),
                    'nombre_jours': 0,
                    #'date_prevue': fields.Date.today(),
                })

    def create_employee_from_applicant(self):
        for rec in self:
            # Vérifier s’il y a un contrat signé
            contrat = self.env['hr.contract'].search([
                ('employee_id.partner_id', '=', rec.partner_id.id),
                ('state', '=', 'open')
            ], limit=1)

            if not contrat:
                raise ValidationError("Le candidat n'a pas encore signé de contrat !")

            # Créer l'employé si pas encore créé
            if not rec.employee_id:
                employee = self.env['hr.employee'].create({
                    'name': rec.partner_name or rec.name,
                    'job_id': rec.job_id.id,
                    'department_id': rec.department_id.id,
                    'date_embauche': contrat.date_start,
                })

                rec.write({
                    'employee_id': employee.id,
                    'stage_id': self.env.ref('hr_recruitment.stage_employee').id
                })

                # Créer planning congé
                self.env['gestion.conge'].create({
                    'employe_id': employee.id,
                    #'dernier_depart': fields.Date.today(),
                    'nombre_jours': 0,
                    #'date_prevue': fields.Date.today(),
                })
