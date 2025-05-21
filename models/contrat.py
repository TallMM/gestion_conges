# models/contrat.py
from odoo import models, fields, api

class Contrat(models.Model):
    _name = 'gestion_conges.contrat'
    _description = 'Contrat de travail'

    name = fields.Char(string="Référence")
    candidat_id = fields.Many2one('hr.applicant', string="Candidat")
    date_signature = fields.Date(string="Date de signature")
    is_signed = fields.Boolean(string="Signé", default=False)

    @api.onchange('is_signed')
    def _onchange_is_signed(self):
        for rec in self:
            if rec.is_signed and rec.candidat_id and not rec.candidat_id.emp_id:
                # Créer automatiquement l'employé depuis le candidat
                employee = rec.candidat_id.create_employee_from_applicant()
                rec.candidat_id.emp_id = employee

                # Créer automatiquement un planning de congé
                self.env['gestion.conge'].create({
                    'employe_id': employee.id,
                    'dernier_depart': fields.Date.today(),
                    'nombre_jours': 0,
                    'date_prevue': fields.Date.today(),
                })
