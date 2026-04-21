import frappe
from typing import List, Union

@frappe.whitelist()
def get_related_parties(party_type: str, parties: Union[str, List[str]]):
    """
    Given a list of parties (or a single party), find and return the entire 'family'.
    If the requested party is a Parent, returns the Parent + all its Children.
    If the requested party is a Child, returns the Parent + the requesting Child + all sibling Children.
    """
    if isinstance(parties, str):
        try:
            import json
            parties = json.loads(parties)
        except Exception:
            parties = [parties]
            
    if not parties:
        return []
        
    family_members = set()

    for party in parties:
        # Check if this party acts as a parent and if it has a linked parent
        parent_partner, is_parent = frappe.db.get_value(
            party_type, 
            party, 
            ["custom_parent_partner", "custom_is_parent_partner"]
        ) or (None, 0)
        
        target_parent = None
        
        if is_parent:
            target_parent = party
        elif parent_partner:
            target_parent = parent_partner
        else:
            # It's an isolated node, just append itself
            family_members.add(party)
            continue
            
        # Add the parent to the family
        family_members.add(target_parent)
        
        # Add all children of this parent to the family
        children = frappe.get_all(
            party_type,
            filters={
                "custom_parent_partner": target_parent
            },
            pluck="name"
        )
        
        for child in children:
            family_members.add(child)
            
    return list(family_members)
