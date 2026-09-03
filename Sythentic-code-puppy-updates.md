\# TASK-001: Synthetic.new 90x Plan Optimization & Agent Re-pinning

\#\# 1\. Overview & Objectives  
\* **\*\*Goal:\*\*** Re-pin Code Puppy agents to eliminate premature quota exhaustion on the Synthetic.new 90x plan.  
\* **\*\*Problem:\*\*** Heavyweight models (\`Kimi-K3\` at 3.0×) are exhausting weekly credits and the 5-hour pool within minutes under continuous multi-agent execution.  
\* **\*\*Target State:\*\*** Shift text-only reasoning to \`GLM-5.2\` (1.0×), fan-out tasks to \`GLM-4.7-Flash\` (0.1×), and route RAG/embeddings to \`nomic-embed-text-v1.5\` (0.0×).

\---

\#\# 2\. Agent Assignments & Multiplier Matrix

| Agent ID | Old Model / Pin | New Model / Pin | Multiplier | Role / Rationale |  
| :--- | :--- | :--- | :---: | :--- |  
| \`code-puppy\` | \`syn:large:vision\` | \`syn:large:text\` | **\*\*1.0×\*\*** | Main driving seat; shift reasoning off 3.0× Kimi-K3 |  
| \`husky\` | \`syn:large:vision\` | \`syn:large:text\` | **\*\*1.0×\*\*** | Long-horizon planning (text-first, no vision needed) |  
| \`job-application-architect\` | \`syn:large:text\` | \`syn:small:text\` | **\*\*0.1×\*\*** | Fan-out & template processing |  
| \`tenantfleet-scanner\` | \`syn:small:text\` | \`syn:small:text\` | **\*\*0.1×\*\*** | Bulk scanning on lightweight weights |  
| \`solutions-architect\` | \`syn:large:text\` | \`syn:large:text\` | **\*\*1.0×\*\*** | Deep architectural reasoning |  
| \`web-puppy\` | \`hf:zai-org/GLM-4.7-Flash\` | \`syn:small:text\` | **\*\*0.1×\*\*** | Scraping and DOM parsing |

\---

\#\# 3\. Configuration & Overrides

\#\#\# A. \`puppy.cfg\` Updates  
\`\`\`ini  
\[agents\]  
\# Re-pin core python agents from 3.0x to 1.0x  
agent\_model\_code\_puppy \= syn:large:text  
agent\_model\_husky \= syn:large:text

\# Re-pin fan-out agents to Flash (0.1x)  
agent\_model\_job\_application\_architect \= syn:small:text  
agent\_model\_tenantfleet\_scanner \= syn:small:text

### **B. Agent JSON Overrides (agents/\*.json)**

JSON

{  
  "agent\_id": "job-application-architect",  
  "model": "syn:small:text"  
}

## ---

**4\. Execution Workflow (Dolt / Beads DB \+ Code Puppy CLI)**

### **Step 1: Initialize Task in Beads Database**

Bash

\# Create and track the optimization task in local Dolt DB  
bd create task "Optimize Synthetic.new agent model pins" \\  
  \--description "Re-pin code-puppy, husky, and fan-out agents to reduce multiplier burn" \\  
  \--label "infrastructure" \--label "quota-optimization"

\# Assign active task context  
bd start TASK-001

### **Step 2: Apply Config Changes & Refresh Telemetry**

Bash

\# Apply configuration changes via Code Puppy CLI  
code-puppy config apply \--file puppy.cfg

\# Execute database migrations for telemetry tracking  
code-puppy db migrate

### **Step 3: Rebuild Documentation Page**

Bash

\# Regenerate dashboard and update GitHub Pages content  
python tools/synthetic-report.py \--update-docs \--output-dir docs/

### **Step 4: Commit Changes & Close Beads Task**

Bash

\# Record completed changes in Dolt/Beads ledger  
bd commit TASK-001 \-m "Updated puppy.cfg, agent JSON pins, and index.html"  
bd close TASK-001

\# Git commit and deploy to GitHub Pages  
git add puppy.cfg agents/\*.json docs/index.html synthetic-90x-cockpit.html  
git commit \-m "feat(quota): optimize agent pins and refresh 90x cockpit"  
git push origin main  
