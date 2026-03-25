import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    custom_fields = {
        "Customer": [
            dict(
                fieldname="custom_multi_partner_section",
                label="Partner Hierarchy",
                fieldtype="Section Break",
                insert_before="defaults_tab",
                collapsible=1
            ),
            dict(
                fieldname="custom_is_parent_partner",
                label="Is Parent Partner?",
                fieldtype="Check",
                insert_after="custom_multi_partner_section",
                description="Check if this company is a designated Parent Company for other companies."
            ),
            dict(
                fieldname="custom_parent_partner",
                label="Parent Partner",
                fieldtype="Link",
                options="Customer",
                insert_after="custom_is_parent_partner",
                depends_on="eval:!doc.custom_is_parent_partner",
                description="Link to the Parent Company if this is a child entity."
            )
        ],
        "Supplier": [
            dict(
                fieldname="custom_multi_partner_section",
                label="Partner Hierarchy",
                fieldtype="Section Break",
                insert_before="defaults_section",
                collapsible=1
            ),
            dict(
                fieldname="custom_is_parent_partner",
                label="Is Parent Partner?",
                fieldtype="Check",
                insert_after="custom_multi_partner_section",
                description="Check if this company is a designated Parent Company for other companies."
            ),
            dict(
                fieldname="custom_parent_partner",
                label="Parent Partner",
                fieldtype="Link",
                options="Supplier",
                insert_after="custom_is_parent_partner",
                depends_on="eval:!doc.custom_is_parent_partner",
                description="Link to the Parent Company if this is a child entity."
            )
        ]
    }
    
    create_custom_fields(custom_fields, ignore_validate=True)
    frappe.clear_cache()
