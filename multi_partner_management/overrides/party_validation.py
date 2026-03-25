import frappe
from frappe import _

def validate(doc, method):
    # Enforce 1-level hierarchy limiting and self-linking
    if doc.custom_is_parent_partner and doc.custom_parent_partner:
        frappe.throw(_("A Parent Company cannot have another Parent Company."))
        
    if doc.custom_parent_partner:
        if doc.custom_parent_partner == doc.name:
            frappe.throw(_("A company cannot be its own Parent Company."))
            
        parent_is_group = frappe.db.get_value(doc.doctype, doc.custom_parent_partner, "custom_is_parent_partner")
        if not parent_is_group:
            frappe.throw(_("The selected Parent Company must have 'Is Parent Partner' checked."))
