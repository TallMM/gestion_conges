odoo.define('gestion_conges.nombre_jours_validation', function (require) {
    "use strict";
    const fieldRegistry = require('web.field_registry');
    const FieldInteger = fieldRegistry.get('integer');

    const NombreJoursField = FieldInteger.extend({
        _onInput: function () {
            this._super.apply(this, arguments);
            const value = parseInt(this.$input.val(), 10);
            if (value > 30) {
                alert("Le nombre de jours ne peut pas dépasser 30 !");
                this.$input.val(30);
            } else if (value < 0) {
                alert("Le nombre de jours ne peut pas être négatif !");
                this.$input.val(0);
            }
        },
    });

    fieldRegistry.add('nombre_jours_validated', NombreJoursField);
});
