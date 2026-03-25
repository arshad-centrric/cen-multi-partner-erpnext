def get_customer_dashboard_data(data):
    if isinstance(data, dict):
        if "transactions" not in data:
            data["transactions"] = []
            
        data["transactions"].append({
            "label": "Child Companies",
            "items": ["Customer"]
        })
        
        if "non_standard_fieldnames" not in data:
            data["non_standard_fieldnames"] = {}
            
        data["non_standard_fieldnames"]["Customer"] = "custom_parent_partner"
        
    return data

def get_supplier_dashboard_data(data):
    if isinstance(data, dict):
        if "transactions" not in data:
            data["transactions"] = []
            
        data["transactions"].append({
            "label": "Child Companies",
            "items": ["Supplier"]
        })
        
        if "non_standard_fieldnames" not in data:
            data["non_standard_fieldnames"] = {}
            
        data["non_standard_fieldnames"]["Supplier"] = "custom_parent_partner"
        
    return data
