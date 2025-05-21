from odoo import models, fields;

class PlanningConge(models.Model):
    _name = 'gestion_conges.planning'
    
    employe_id = fields.Many2one('hr.employee', string="Employé")
    date_embauche = fields.Date(related="employe_id.date_embauche", store=True)
