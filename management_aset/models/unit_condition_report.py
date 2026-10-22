from odoo import fields, models,api, _ 

class UnitConditionReport(models.Model):
    _name="unit.condition.report"
    _description="Define the Unit Condition Report"
    _rec_name="customer_id"

    customer_id=fields.Many2one('res.partner', 
                                string="Client Name", 
                                required=True)
    employee_id=fields.Many2many('employee.name', 
                                 string='Engineer')
    job_no=fields.Many2one('sale.order', 
                           string="Job No", domain=[('state', '=','sale')])
    platform_vessel_id=fields.Many2one('platform.vessel',
                                       string="Name of Installation, Vessel/Rig/Platform")
    start_date=fields.Date(string="Inspection Date")
    end_date=fields.Date(string="End Date")
    location=fields.Char(string="Location", 
                         related="platform_vessel_id.country_id.name", 
                         store=True,
                         readonly=True)
    client_name_ids=fields.One2many('client.name', 
                                    'unit_condition_id', 
                                    string='Client Visit Name')
    crane_registration_id=fields.Many2one('crane.registration', 
                                          string="Serial Number")
    make=fields.Char(string="Make", 
                     related="crane_registration_id.make",
                     store=True,
                     readonly=True)
    model=fields.Char(string='Model', 
                      related="crane_registration_id.model_id.crane_model",
                      store=True, 
                      readonly=True)
    year_built=fields.Char(string='Year Manufactured',
                           related="crane_registration_id.year_built",
                           store=True,
                           readonly=True)
    boom_length=fields.Char(string= "Boom Length")
    swl_main=fields.Char(string="SWL Main")
    min_radius=fields.Char(string="Min. Radius")
    max_radius=fields.Char(string="Max. Radius")
    swl_whip_aux=fields.Char(string="SWL Whip / Aux")
    engine_hours=fields.Char(string="Engine Hours")

    spec_wire_id=fields.One2many(
        "wire.rope.result",
        "unit_condition_id",
        string="Wire Rope Specification"
    )
    result_ids = fields.One2many(
        "unit.condition.result",
        "unit_condition_id",
        string="Inspection Results",
    )

    result_ids2 = fields.One2many(
            "unit.condition.result2",
            "unit_condition_id",
            string="Inspection Results 2",
    )
    result_ids3=fields.One2many(
        "unit.condition.result3",
        "unit_condition_id",
        string="Inspection Results 3"
    )
    
    result_ids4=fields.One2many(
            "unit.condition.result4",
            "unit_condition_id",
            string="Inspection Results 4"
    )

    result_ids5=fields.One2many(
        "unit.condition.result5",
        "unit_condition_id",
        string="Inspection Results 5"
    )

    result_ids6=fields.One2many(
        "unit.condition.result6",
        "unit_condition_id",
        string="Inspection Results 6"
    )

    result_ids7=fields.One2many(
        "unit.condition.result7",
        "unit_condition_id",
        string="Inspection Result 7"
    )
    result_ids8=fields.One2many(
        "unit.condition.result8",
        "unit_condition_id",
        string="Inspection Result 8"
    )

    result_ids9=fields.One2many(
        "unit.condition.result9",
        "unit_condition_id",
        string="Inspection Result 9"
    )
    result_ids10=fields.One2many(
        "unit.condition.result10",
        "unit_condition_id",
        "SUITABILITY OF CRANE FOR MANRIDING DUTIES"
    )
    @api.model
    def default_get(self, fields_list):

        vals = super().default_get(fields_list)

        wire_specification=self.env[
            "wire.rope.specification"
        ].search(
            [("active", "=", True)],
            order="sort_order, id"
        )

        vals['spec_wire_id']=[
            (
                0,
                0,
                {
                    "wire_rope_id":spec_wire.id,
                    "location":spec_wire.location,
                    "sort_order":spec_wire.sort_order
                },
            )
            for spec_wire in wire_specification
        ]

        specifications = self.env[
            "specification.report"
        ].search(
            [("active", "=", True)],
            order="sort_order, id",
        )

        vals["result_ids"] = [
            (
                0,
                0,
                {
                    "specification_id": specification.id,
                    "sequence": specification.sequence,
                    "item_detail": specification.item_detail,
                    "is_section": specification.is_section,
                    "sort_order": specification.sort_order,
                },
            )
            for specification in specifications
        ]


        general_check = self.env[
            "general.visual.report"
        ].search(
            [("active", "=", True)],
            order="sort_order, id",
        )

        vals["result_ids2"] = [
            (
                0,
                0,
                {
                    "general_visual_id": general.id,
                    "sequence": general.sequence,
                    "item_detail": general.item_detail,
                    "is_section":general.is_section,
                    "sort_order": general.sort_order,
                },
            )
            for general in general_check
        ]


        inspection_control=self.env[
            "instrumentation.control.report"
        ].search(
             [("active", "=", True)],
             order="sort_order, id",
        )

        vals["result_ids3"] = [
            (
                0,
                0,
                {
                    "instrumentation_control_id": inspection.id,
                    "sequence": inspection.sequence,
                    "item_detail": inspection.item_detail,
                    "is_section":inspection.is_section,
                    "sort_order": inspection.sort_order,
                },
            )
            for inspection in inspection_control
        ]

        
        structure_primary=self.env[
            "structure.primary.report"
        ].search(
                [("active", "=", True)],
                order="sort_order, id",
        )

        vals["result_ids4"] = [
            (
                0,
                0,
                {
                    "structure_primary_id": structure.id,
                    "sequence": structure.sequence,
                    "item_detail": structure.item_detail,
                    "is_section": structure.is_section,
                    "sort_order": structure.sort_order,
                },
            )
            for structure in structure_primary
        ]


        wire_hook=self.env[
            "wire.hooks.report"
        ].search(
                [("active", "=", True)],
                order="sort_order, id",
        )

        vals["result_ids5"] = [
            (
                0,
                0,
                {
                    "wire_hook_id":wire.id,
                    "sequence": wire.sequence,
                    "item_detail": wire.item_detail,
                    "is_section":wire.is_section,
                    "sort_order": wire.sort_order,
                },
            )
            for wire in wire_hook
        ]

        hoist_slew=self.env[
            "hoist.slew.report"
        ].search(
                [("active", "=", True)],
                order="sort_order, id",
        )

        vals["result_ids6"] = [
            (
                0,
                0,
                {
                    "hoist_slew_id":hoist.id,
                    "sequence": hoist.sequence,
                    "item_detail": hoist.item_detail,
                    "is_section":hoist.is_section,
                    "sort_order": hoist.sort_order,
                },
            )
            for hoist in hoist_slew
        ]

        prime_mover=self.env[
            "prime.mover.report"
        ].search(
                [("active", "=", True)],
                order="sort_order, id",
        )

        vals["result_ids7"] = [
            (
                0,
                0,
                {
                    "power_mover_id":prime.id,
                    "sequence": prime.sequence,
                    "item_detail": prime.item_detail,
                    "is_section":prime.is_section,
                    "sort_order": prime.sort_order,
                },
            )
            for prime in prime_mover
        ]

        hydraulic_pneumatic=self.env[
            "hydraulic.pneumatic.report"
        ].search(
                [("active", "=", True)],
                order="sort_order, id",
        )

        vals["result_ids8"] = [
            (
                0,
                0,
                {
                    "hydraulic_pneumatic_id":hydraulic.id,
                    "sequence": hydraulic.sequence,
                    "item_detail": hydraulic.item_detail,
                    "is_section":hydraulic.is_section,
                    "sort_order": hydraulic.sort_order,
                },
            )
            for hydraulic in hydraulic_pneumatic
        ]

        electrical_system=self.env[
            "electrical.system.report"
        ].search(
                [("active", "=", True)],
                order="sort_order, id",
        )

        vals["result_ids9"] = [
            (
                0,
                0,
                {
                    "electrical_system_id":electrical.id,
                    "sequence": electrical.sequence,
                    "item_detail": electrical.item_detail,
                    "is_section":electrical.is_section,
                    "sort_order": electrical.sort_order,
                },
            )
            for electrical in electrical_system
        ]

        suitability_crane=self.env[
            "suitability.crane.report"
        ].search(
                [("active", "=", True)],
                order="sort_order, id",
        )

        vals["result_ids10"] = [
            (
                0,
                0,
                {
                    "suitability_crane_id":suitability.id,
                    "sequence": suitability.sequence,
                    "item_detail": suitability.item_detail,
                    "is_section":suitability.is_section,
                    "sort_order": suitability.sort_order,
                },
            )
            for suitability in suitability_crane
        ]
        return vals


    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        self.platform_vessel_id=False
        self.crane_registration_id=False

    @api.onchange('platform_vessel_id')
    def _onchange_platform_vessel_id(self):
        self.crane_registration_id=False
