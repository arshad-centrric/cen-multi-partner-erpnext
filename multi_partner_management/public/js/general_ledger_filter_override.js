frappe.provide('frappe.views');

frappe.router.on('change', () => {
    // Ensure we capture the prototype patch early if it hasn't been applied yet
    if (frappe.views.QueryReport && !frappe.views.QueryReport.prototype._custom_multi_partner_patched) {
        let orig_setup_filters = frappe.views.QueryReport.prototype.setup_filters;
        
        frappe.views.QueryReport.prototype.setup_filters = function() {
            if (this.report_name === "General Ledger") {
                let gl_report = frappe.query_reports["General Ledger"];
                if (gl_report && gl_report.filters && !gl_report.custom_multi_partner_injected) {
                    gl_report.custom_multi_partner_injected = true;
                    
                    let party_idx = gl_report.filters.findIndex(f => f.fieldname === 'party');
                    if (party_idx !== -1) {
                        gl_report.filters.splice(party_idx + 1, 0, {
                            fieldname: "custom_include_family",
                            label: __("Select Related Parties"),
                            fieldtype: "Check",
                            on_change: function() {
                                let is_checked = frappe.query_report.get_filter_value('custom_include_family');
                                if (!is_checked) {
                                    // When unchecked, automatically clear the selected parties
                                    frappe.query_report.set_filter_value('party', []);
                                    return;
                                }
                                
                                let parties = frappe.query_report.get_filter_value('party');
                                let party_type = frappe.query_report.get_filter_value('party_type');
                                
                                if (parties && parties.length > 0 && party_type) {
                                    // Call our custom backend API to fetch the full 1-level family cluster
                                    frappe.call({
                                        method: "multi_partner_management.api.get_related_parties",
                                        args: {
                                            party_type: party_type,
                                            parties: parties
                                        },
                                        callback: function(r) {
                                            if (r.message && r.message.length > 0) {
                                                // Update the native multi-select filter with the expanded set
                                                frappe.query_report.set_filter_value('party', r.message);
                                            }
                                        }
                                    });
                                }
                            }
                        });
                    }
                }
            }
            // Execute the core frappe logic with our injected JS active natively
            return orig_setup_filters.apply(this, arguments);
        };
        frappe.views.QueryReport.prototype._custom_multi_partner_patched = true;
    }
});
