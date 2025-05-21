from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class GestionConge(models.Model):
    _name = 'gestion.conge'
    _description = "Gestion des Congés"
    _order = 'prochain_depart asc'

    _sql_constraints = [
        ('unique_employee_leave', 'UNIQUE(employe_id, date_embauche)',
         'Un employé ne peut pas avoir plusieurs congés à la même date.')
    ]

    # -------------------------
    # CHAMPS
    # -------------------------

    employe_id = fields.Many2one('hr.employee', string="Employé", required=True)
    matricule = fields.Char(string="Matricule", related='employe_id.matricule', required=True, copy=False)
    departement = fields.Many2one(string="Département", related='employe_id.department_id', store=True, readonly=True)
    poste = fields.Many2one(string="Poste", related='employe_id.job_id', store=True, readonly=True)
    date_embauche = fields.Date(string="Date d'embauche", related='employe_id.date_embauche', store=True)

    dernier_depart = fields.Date(string="Dernier départ en congé")
    nombre_jours = fields.Integer(string="Nbr de jours", default=0)
    reliquat = fields.Integer(string="Reliquat", compute='_compute_reliquat_et_prochain_depart', store=True, readonly=True)
    prochain_depart = fields.Date(string="Prochain départ en congé", compute='_compute_reliquat_et_prochain_depart', store=True, readonly=True)
    date_prevue = fields.Date(string="Date Prévue")

    is_current_month = fields.Boolean(
        string="Mois en cours",
        compute='_compute_is_current_month',
        store=True
    )

    # -------------------------
    # CALCUL : MOIS EN COURS
    # -------------------------

    @api.depends('prochain_depart')
    def _compute_is_current_month(self):
        """Calcule si la date de prochain départ est dans le mois courant"""
        today = fields.Date.today()
        for rec in self:
            rec.is_current_month = bool(
                rec.prochain_depart and
                rec.prochain_depart.month == today.month and
                rec.prochain_depart.year == today.year
            )

    # -------------------------
    # CALCUL : RELIQUAT & PROCHAIN DÉPART
    # -------------------------

    @api.depends('date_embauche', 'dernier_depart', 'nombre_jours')
    def _compute_reliquat_et_prochain_depart(self):
        for rec in self:
            rec.reliquat = 0
            rec.prochain_depart = False
            today = fields.Date.today()

            if rec.date_embauche:
                date_1_an = rec.date_embauche + timedelta(days=365)
                if today >= date_1_an:
                    rec.reliquat = max(30 - rec.nombre_jours, 0)

            if rec.dernier_depart:
                try:
                    rec.prochain_depart = (rec.dernier_depart + timedelta(days=rec.nombre_jours)).replace(
                        year=rec.dernier_depart.year + 1)
                except ValueError:
                    rec.prochain_depart = rec.dernier_depart.replace(year=rec.dernier_depart.year + 1, day=28)
            elif rec.date_embauche:
                try:
                    rec.prochain_depart = rec.date_embauche.replace(year=rec.date_embauche.year + 1)
                except ValueError:
                    rec.prochain_depart = rec.date_embauche.replace(year=rec.date_embauche.year + 1, day=28)

    # -------------------------
    # CONTRAINTE : Congé unique par date
    # -------------------------

    @api.constrains('employe_id', 'date_embauche')
    def _check_unique_leave(self):
        for record in self:
            count = self.env['gestion.conge'].search_count([
                ('employe_id', '=', record.employe_id.id),
                ('date_embauche', '=', record.date_embauche)
            ])
            if count > 1:
                raise ValidationError(
                    f"L'employé {record.employe_id.name} a déjà un congé prévu à cette date !"
                )

    # -------------------------
    # CONTRAINTE : Nombre de jours max/min
    # -------------------------

    @api.constrains('nombre_jours')
    def _check_nombre_jours_maximum(self):
        for record in self:
            if record.nombre_jours > 30:
                raise ValidationError("Le nombre de jours de congé ne peut pas dépasser 30.")
            if record.nombre_jours < 0:
                raise ValidationError("Le nombre de jours de congé ne peut pas être négatif.")

    # -------------------------
    # ACTION : Impression
    # -------------------------

    def action_print_report(self):
        return self.env.ref('gestion_conges.action_report_planning_conge').report_action(self.id)


# -------------------------
# CRON : Mise à jour automatique du reliquat
# -------------------------

@api.model
def update_reliquat_anciennete(self):
    """
    Cron : recalcul uniquement du reliquat et du prochain départ pour tous les congés.
    """
    conges = self.search([])
    for conge in conges:
        conge._compute_reliquat_et_prochain_depart()

    self.env['ir.logging'].create({
        'name': "Recalcul reliquats",
        'type': 'server',
        'dbname': self._cr.dbname,
        'level': 'info',
        'message': "Recalcul automatique des reliquats effectué.",
        'path': __name__,
        'line': '0',
        'func': 'update_reliquat_anciennete',
    })
