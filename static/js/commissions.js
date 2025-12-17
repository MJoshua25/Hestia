(function() {
    const { createApp } = Vue;

    createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            eventId: null,
            csrfToken: null,
            apiUrl: null,
            autoAssignUrl: null,
            manualAssignUrl: null,
            commissions: [],
            availableMembers: [], // List of {id, name, ...}
            
            // UI States
            loading: true,
            assigning: false,
            
            // Modals
            showAssignModal: false,
            showManualModal: false,
            showMoveModal: false,
            showExportDropdown: false,
            
            // Selection for Auto Assign
            selectedMembers: [], 
            
            // Context for Actions
            currentCommissionId: null,
            currentMemberId: null,
            searchQuery: ''
        }
    },
    mounted() {
        // Init from DOM data attributes
        const appEl = document.getElementById('commission-app');
        this.eventId = appEl.dataset.eventId;
        this.csrfToken = appEl.dataset.csrfToken;
        this.apiUrl = appEl.dataset.apiUrl;
        this.autoAssignUrl = appEl.dataset.autoAssignUrl;
        this.manualAssignUrl = appEl.dataset.manualAssignUrl;
        
        this.loadData();
    },
    computed: {
        assignedCount() {
            return this.commissions.reduce((acc, c) => acc + c.current_count, 0);
        },
        totalMembers() {
            return this.availableMembers.length;
        },
        fillRate() {
            if (this.totalMembers === 0) return 0;
            return Math.round((this.assignedCount / this.totalMembers) * 100);
        },
        allSelected() {
            return this.availableMembers.length > 0 && this.selectedMembers.length === this.availableMembers.length;
        },
        filteredMembers() {
            // For Manual Add: Filter by search + exclude already assigned (unless we want to allow stealing?)
            // PRD says: "Members already assigned ... are grayed out"
            // We'll show all but indicate status
            const query = this.searchQuery.toLowerCase();
            return this.availableMembers.filter(m => 
                m.name.toLowerCase().includes(query) &&
                !m.is_assigned // Only show unassigned for addition? Or show all? 
                // Let's filter to unassigned for simplicity in "Add Member" context
            );
        },
        currentCommission() {
            return this.commissions.find(c => c.id === this.currentCommissionId);
        }
    },
    methods: {
        async loadData() {
            this.loading = true;
            try {
                const response = await fetch(this.apiUrl);
                if (!response.ok) throw new Error("Erreur chargement");
                const data = await response.json();
                
                this.commissions = data.commissions;
                this.availableMembers = data.members;
                
                // Pre-select all members for auto-assign by default if none selected?
                // Or preserve selection?
                // Default: Select ALL unassigned members + those currently assigned (if re-running)
                // Actually simple approach: Select ALL members by default.
                this.selectedMembers = this.availableMembers.map(m => m.id);
                
            } catch (error) {
                console.error(error);
                this.showToast("Erreur lors du chargement des données", "error");
            } finally {
                this.loading = false;
            }
        },
        
        toggleSelectAll() {
            if (this.allSelected) {
                this.selectedMembers = [];
            } else {
                this.selectedMembers = this.availableMembers.map(m => m.id);
            }
        },
        
        toggleExportDropdown() {
            this.showExportDropdown = !this.showExportDropdown;
        },
        
        async runAutoAssign(force = false) {
            if (typeof force !== 'boolean') force = false;
            
            if (this.selectedMembers.length === 0) {
                this.showToast("Veuillez sélectionner au moins un membre", "warning");
                return;
            }
            
            this.assigning = true;
            try {
                const response = await fetch(this.autoAssignUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.csrfToken
                    },
                    body: JSON.stringify({
                        member_ids: this.selectedMembers,
                        force: force
                    })
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    this.showToast(result.message || "Attribution réussie !", "success");
                    this.showAssignModal = false;
                    await this.loadData();
                } else if (result.status === 'warning_min_capacity') {
                    // Show confirmation for force
                    if (confirm(`⚠️ ATTENTION : ${result.message}\n\nVoulez-vous forcer l'attribution (certains minimums ne seront pas respectés) ?`)) {
                        await this.runAutoAssign(true);
                    }
                } else {
                    this.showToast(result.message || "Erreur lors de l'attribution", "error");
                }
            } catch (error) {
                this.showToast("Erreur serveur", "error");
            } finally {
                this.assigning = false;
            }
        },
        
        async manualAssign(commissionId) {
            this.currentCommissionId = commissionId;
            this.searchQuery = '';
            this.showManualModal = true;
        },
        
        async confirmManualAdd(memberId) {
            await this.performAction(this.currentCommissionId, memberId, 'add');
            this.showManualModal = false;
        },
        
        async removeMember(memberId, commissionId) {
            if (!confirm("Voulez-vous retirer ce membre ?")) return;
            await this.performAction(commissionId, memberId, 'remove');
        },
        
        moveMember(memberId, fromCommissionId) {
            this.currentMemberId = memberId;
            this.currentCommissionId = fromCommissionId; // Source
            this.showMoveModal = true;
        },
        
        async confirmMove(targetCommissionId) {
            // Action: 'move', commission_id is target
            await this.performAction(targetCommissionId, this.currentMemberId, 'move');
            this.showMoveModal = false;
        },
        
        async performAction(commissionId, memberId, action) {
            try {
                const response = await fetch(this.manualAssignUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.csrfToken
                    },
                    body: JSON.stringify({
                        commission_id: commissionId,
                        member_id: memberId,
                        action: action
                    })
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    this.showToast("Action effectuée", "success");
                    await this.loadData();
                } else {
                    this.showToast(result.message, "error");
                }
            } catch (error) {
                this.showToast("Erreur de connexion", "error");
            }
        },
        
        showToast(message, type = 'info') {
            // Simple alert for now, or use a custom toast if available in base.html logic
            // Base template has toast display for Django messages, but here we are client side.
            // We can append a toast to the DOM or just alert.
            // For MVP: Alert for errors, subtle console or temporary div for success.
            if (type === 'error') alert("❌ " + message);
            else console.log(message);
        }
    }
}).mount('#commission-app');
})();
