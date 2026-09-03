window.FIELD_GUIDE_DATA = {
  "meta": {
    "generatedAt": "2026-09-01T14:55:41.008458+00:00",
    "repoPath": "/Users/tygranlund/code_puppy",
    "repoHead": "a12ed1f4",
    "branch": "main",
    "currentVersion": "code-puppy v0.0.808",
    "sourceUrl": "https://github.com/mpfaffenberger/code_puppy"
  },
  "stats": {
    "tools": 61,
    "agents": 22,
    "plugins": 65,
    "skills": 5,
    "commitsLast2Months": 952,
    "releases": 2
  },
  "tools": [
    {
      "name": "agent_run_shell_command",
      "category": "shell",
      "description": "Run a shell command with timeout, optional background execution, and output streaming. Your hands."
    },
    {
      "name": "agent_share_your_reasoning",
      "category": "shell",
      "description": "Record the agent's reasoning for observability in the TUI and logs."
    },
    {
      "name": "apply_patch",
      "category": "other",
      "description": ""
    },
    {
      "name": "ask_user_question",
      "category": "user",
      "description": "Ask the human multiple related questions in an interactive picker. Use when input is genuinely required."
    },
    {
      "name": "browser_check",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_clear_highlights",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_click",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_click_by_role",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_click_by_text",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_close",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_double_click",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_execute_js",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_find_buttons",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_find_by_label",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_find_by_placeholder",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_find_by_role",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_find_by_test_id",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_find_by_text",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_find_links",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_get_page_info",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_get_text",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_get_value",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_go_back",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_go_forward",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_highlight_element",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_hover",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_initialize",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_list_pages",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_list_workflows",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_navigate",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_new_page",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_page_snapshot",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_read_workflow",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_reload",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_save_workflow",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_screenshot_analyze",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_scroll",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_scroll_to_element",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_select_option",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_set_text",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_set_text_by_label",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_set_viewport",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_status",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_uncheck",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_wait_for_element",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_wait_for_load",
      "category": "browser",
      "description": ""
    },
    {
      "name": "browser_xpath_query",
      "category": "browser",
      "description": ""
    },
    {
      "name": "create_file",
      "category": "file",
      "description": "Create a new file or overwrite an existing one with full content."
    },
    {
      "name": "delete_file",
      "category": "file",
      "description": "Delete a file with a logged diff of what was removed. Use sparingly."
    },
    {
      "name": "delete_snippet",
      "category": "file",
      "description": "Remove the first occurrence of an exact text snippet from a file."
    },
    {
      "name": "edit",
      "category": "other",
      "description": ""
    },
    {
      "name": "edit_file",
      "category": "file",
      "description": "Deprecated compound tool; auto-expands to create/replace/delete. Prefer the specific tools."
    },
    {
      "name": "grep",
      "category": "file",
      "description": "Recursively search file contents with ripgrep regex. Fast way to find usages, definitions, and config."
    },
    {
      "name": "invoke_agent",
      "category": "agent",
      "description": "Delegate a task to a named sub-agent. Use this to hand off research, QA, or specialist work instead of doing it yourself."
    },
    {
      "name": "invoke_agent_with_model",
      "category": "agent",
      "description": "Delegate to a sub-agent while pinning a specific model for that run."
    },
    {
      "name": "list_agents",
      "category": "agent",
      "description": "List every sub-agent available for delegation, with what each one is good at."
    },
    {
      "name": "list_available_models",
      "category": "agent",
      "description": "Show the models configured in the model factory and which providers they route to."
    },
    {
      "name": "list_files",
      "category": "file",
      "description": "List files and directories with smart filtering (skips build artifacts, caches, and noise). Read-only."
    },
    {
      "name": "load_image_for_analysis",
      "category": "user",
      "description": "Load an image from disk so the model can see and analyze it."
    },
    {
      "name": "read_file",
      "category": "file",
      "description": "Read a file's contents, optionally a line range. Use before modifying anything."
    },
    {
      "name": "replace_in_file",
      "category": "file",
      "description": "Apply targeted find-and-replace edits. Prefer this over full rewrites; keeps diffs small."
    }
  ],
  "agents": [
    {
      "name": "agent-creator",
      "display_name": "Agent Creator 🏗️",
      "description": "Helps you create new JSON agent configurations with proper schema validation",
      "type": "python",
      "tools": [
        "list_files",
        "read_file",
        "create_file",
        "replace_in_file",
        "delete_snippet",
        "ask_user_question",
        "list_agents",
        "invoke_agent",
        "universal_constructor"
      ]
    },
    {
      "name": "benton-lead-orchestrator",
      "display_name": "Benton Lead Orchestrator ",
      "description": "Master orchestrator for the Benton Drones in-house lead ingestion pipeline. Evolves the local Python/SQLite MVP into a branded, multi-variant lead intake system with electronic consent/signature capture, admin dashboard with maps and analytics, and a production-ready deployment path. Coordinates specialist agents and custom tools to deliver the full pipeline plus a flat HTML explainer guide.",
      "type": "json",
      "tools": [
        "list_files",
        "read_file",
        "create_file",
        "replace_in_file",
        "delete_snippet",
        "list_agents",
        "invoke_agent",
        "shell_run",
        "universal_constructor",
        "ask_user_question",
        "kennel_recall",
        "kennel_remember"
      ]
    },
    {
      "name": "code-puppy",
      "display_name": "Code-Puppy 🐶",
      "description": "The most loyal digital puppy, helping with all coding tasks",
      "type": "python",
      "tools": [
        "list_agents",
        "invoke_agent",
        "list_files",
        "read_file",
        "grep",
        "create_file",
        "edit",
        "delete_snippet",
        "delete_file",
        "agent_run_shell_command",
        "ask_user_question",
        "activate_skill",
        "list_or_search_skills",
        "load_image_for_analysis"
      ]
    },
    {
      "name": "e2e-testing-expert",
      "display_name": "E2E Testing Expert",
      "description": "Analyzes any codebase to discover current features, then generates a complete, up-to-date end-to-end test suite. Works across web apps, Python backends, JS frontends, HTTP APIs, and CLI tools. Discovers, inventories, generates, executes, and reports.",
      "type": "json",
      "tools": [
        "list_files",
        "read_file",
        "grep",
        "create_file",
        "replace_in_file",
        "agent_run_shell_command",
        "agent_share_your_reasoning",
        "ask_user_question",
        "invoke_agent",
        "list_agents",
        "browser_initialize",
        "browser_close",
        "browser_status",
        "browser_new_page",
        "browser_list_pages",
        "browser_navigate",
        "browser_get_page_info",
        "browser_go_back",
        "browser_go_forward",
        "browser_reload",
        "browser_wait_for_load",
        "browser_find_by_role",
        "browser_find_by_text",
        "browser_find_by_label",
        "browser_find_by_placeholder",
        "browser_find_by_test_id",
        "browser_find_buttons",
        "browser_find_links",
        "browser_xpath_query",
        "browser_click",
        "browser_double_click",
        "browser_hover",
        "browser_set_text",
        "browser_get_text",
        "browser_get_value",
        "browser_select_option",
        "browser_check",
        "browser_uncheck",
        "browser_execute_js",
        "browser_scroll",
        "browser_scroll_to_element",
        "browser_set_viewport",
        "browser_wait_for_element",
        "browser_highlight_element",
        "browser_clear_highlights",
        "browser_save_workflow",
        "browser_list_workflows",
        "browser_read_workflow"
      ]
    },
    {
      "name": "emoji-artist",
      "display_name": "Emoji Artist 🎨",
      "description": "Designs and ships custom branded Microsoft Teams emojis (96x96, transparent PNG) using LLM-authored SVG rasterized via headless Chromium. Knows the HTT brand book and logo registry. No API keys needed — leverages the host model's native ability to write expressive SVG.",
      "type": "json",
      "tools": [
        "list_files",
        "read_file",
        "create_file",
        "replace_in_file",
        "delete_snippet",
        "delete_file",
        "grep",
        "agent_run_shell_command",
        "list_agents",
        "agent_share_your_reasoning",
        "ask_user_question",
        "load_image_for_analysis",
        "activate_skill",
        "list_or_search_skills"
      ]
    },
    {
      "name": "epistemic-architect",
      "display_name": "Epistemic Architect 🏛️🔬",
      "description": "Structured planning through evidence-based reasoning. Uses OODA loop and delegates to specialist agents for security, code review, QA, and implementation.",
      "type": "json",
      "tools": [
        "list_files",
        "read_file",
        "grep",
        "create_file",
        "replace_in_file",
        "delete_snippet",
        "delete_file",
        "agent_run_shell_command",
        "agent_share_your_reasoning",
        "list_agents",
        "invoke_agent",
        "ask_user_question"
      ]
    },
    {
      "name": "experience-architect",
      "display_name": "Experience Architect 🎨",
      "description": "Frontend and UX architect specializing in design systems, WCAG 2.2 accessibility, privacy-by-design (GDPR/CCPA/GPC), and frontend-backend integration contracts. Always researches via web-puppy.",
      "type": "json",
      "tools": [
        "list_files",
        "read_file",
        "grep",
        "agent_share_your_reasoning",
        "invoke_agent",
        "list_agents"
      ]
    },
    {
      "name": "helios",
      "display_name": "Helios ☀️",
      "description": "The Universal Constructor - a transcendent agent that can create any tool, any capability, any functionality",
      "type": "python",
      "tools": [
        "universal_constructor",
        "list_files",
        "read_file",
        "grep",
        "create_file",
        "replace_in_file",
        "delete_snippet",
        "delete_file",
        "agent_run_shell_command"
      ]
    },
    {
      "name": "job-application-architect",
      "display_name": "Job Application Architect",
      "description": "Ethical, human-in-the-loop job-application orchestrator. Discovers roles, classifies Experience- vs Solutions-Architect flavor, truthfully tailors ATS-safe resumes + cover letters per role, stages screening answers, fills out application forms via web-retriever (Playwright), uploads documents, and tracks everything in a durable ledger. Discovers live postings via public no-auth job-board APIs (Greenhouse/Lever/Ashby/SmartRecruiters/Workday CXS) with jobboard_discover and generates ATS-safe resume files (md/txt/html/docx) with ats_resume_build. Delegates research to web-puppy, form-filling + gated extraction to web-retriever, compensation & option-fit advisory analysis to solutions-architect, and tool-building to helios. Never solves CAPTCHAs, evades bot/AI detection, or fills EEO self-ID — a human clears every gate. Application submission happens only after Tyler explicitly reviews and approves; web-retriever executes the click.",
      "type": "json",
      "tools": [
        "list_agents",
        "invoke_agent",
        "jobapp_ledger",
        "jobboard_discover",
        "ats_resume_build",
        "ask_user_question",
        "read_file",
        "create_file",
        "replace_in_file",
        "grep"
      ]
    },
    {
      "name": "mail-researcher",
      "display_name": "Mail Researcher ",
      "description": "Parses, searches, and researches your local Mac Mail (Google + iCloud accounts). Pulls context/text/data/images from messages to support any initiative, and drafts plain-text or polished HTML emails saved as files and inserted as reviewable drafts in Mail.app — never auto-sends.",
      "type": "json",
      "tools": [
        "list_files",
        "read_file",
        "grep",
        "create_file",
        "replace_in_file",
        "agent_run_shell_command",
        "load_image_for_analysis",
        "ask_user_question",
        "universal_constructor",
        "browser_initialize",
        "browser_new_page",
        "browser_navigate",
        "browser_get_page_info",
        "browser_get_text",
        "browser_page_snapshot",
        "browser_find_by_text",
        "browser_find_links",
        "browser_scroll",
        "browser_screenshot_analyze",
        "browser_execute_js",
        "browser_close",
        "kennel_recent",
        "kennel_recall",
        "kennel_remember",
        "embed_text"
      ]
    },
    {
      "name": "model-judge",
      "display_name": "Model Judge ⚖️",
      "description": "Benchmark and compare models: run the same agent and prompt across multiple models, capture per-request token usage and latency, then produce a side-by-side comparison and a ranked verdict.",
      "type": "python",
      "tools": [
        "list_agents",
        "list_available_models",
        "invoke_agent",
        "invoke_agent_with_model",
        "ask_user_question",
        "agent_share_your_reasoning",
        "list_files",
        "read_file",
        "create_file"
      ]
    },
    {
      "name": "ops-comms-collie",
      "display_name": "Ops Comms Collie 🐕‍🦺",
      "description": "Reviews and refines drafts of business communications aimed at non-technical operations stakeholders (COOs, franchisee success leaders, ops analysts, finance). Herds technical findings into plain business English — does NOT write from scratch.",
      "type": "json",
      "tools": [
        "list_files",
        "read_file",
        "grep",
        "create_file",
        "replace_in_file",
        "delete_snippet",
        "agent_share_your_reasoning"
      ]
    },
    {
      "name": "planning-agent",
      "display_name": "Planning Agent 📋",
      "description": "Breaks down complex coding tasks into clear, actionable steps. Analyzes project structure, identifies dependencies, and creates execution roadmaps.",
      "type": "python",
      "tools": [
        "list_files",
        "read_file",
        "grep",
        "ask_user_question",
        "list_agents",
        "invoke_agent",
        "list_or_search_skills"
      ]
    },
    {
      "name": "prompt-sherpa",
      "display_name": "Prompt Sherpa 🏔️",
      "description": "Wraps your raw prompt: improves it, picks the right specialist agent, optionally validates time-sensitive facts, then executes the improved prompt against the chosen agent and returns the result. A single round-trip front door for getting better answers from the pack.",
      "type": "json",
      "tools": [
        "list_agents",
        "invoke_agent",
        "ask_user_question",
        "agent_share_your_reasoning"
      ]
    },
    {
      "name": "qa-kitten",
      "display_name": "Quality Assurance Kitten 🐱",
      "description": "Advanced web browser automation and quality assurance testing using Playwright with visual analysis capabilities",
      "type": "python",
      "tools": [
        "browser_initialize",
        "browser_close",
        "browser_status",
        "browser_new_page",
        "browser_list_pages",
        "browser_navigate",
        "browser_get_page_info",
        "browser_go_back",
        "browser_go_forward",
        "browser_reload",
        "browser_wait_for_load",
        "browser_page_snapshot",
        "browser_find_by_role",
        "browser_find_by_text",
        "browser_find_by_label",
        "browser_find_by_placeholder",
        "browser_find_by_test_id",
        "browser_find_buttons",
        "browser_find_links",
        "browser_xpath_query",
        "browser_click_by_role",
        "browser_click_by_text",
        "browser_set_text_by_label",
        "browser_click",
        "browser_double_click",
        "browser_hover",
        "browser_set_text",
        "browser_get_text",
        "browser_get_value",
        "browser_select_option",
        "browser_check",
        "browser_uncheck",
        "browser_execute_js",
        "browser_scroll",
        "browser_scroll_to_element",
        "browser_set_viewport",
        "browser_wait_for_element",
        "browser_highlight_element",
        "browser_clear_highlights",
        "browser_screenshot_analyze",
        "load_image_for_analysis",
        "browser_save_workflow",
        "browser_list_workflows",
        "browser_read_workflow"
      ]
    },
    {
      "name": "release-gate-arbiter",
      "display_name": "Release Gate Arbiter ⚔️",
      "description": "The final non-negotiable authorization gate for SDLC stage transitions at HTT Brands. Adversarial by default — assumes wrong until proven otherwise with receipts. Implements SLSA L3, Sigstore cosign verification, and 8-pillar validation for production releases across 200+ franchise locations.",
      "type": "json",
      "tools": [
        "list_files",
        "read_file",
        "grep",
        "create_file",
        "replace_in_file",
        "delete_snippet",
        "delete_file",
        "agent_run_shell_command",
        "list_agents",
        "invoke_agent",
        "agent_share_your_reasoning",
        "ask_user_question"
      ]
    },
    {
      "name": "slide-puppy",
      "display_name": "Slide-Puppy 🎞️🐶",
      "description": "Reverse-engineered gamma.app + beautiful.ai. Produces best-in-class presentations as Reveal.js, Tailwind/HTML, or Marp decks — with built-in FPO mockups, premium transitions, and visual QA via headless browser. Delegates UX research to experience-architect and tech decisions to solutions-architect.",
      "type": "json",
      "tools": [
        "list_files",
        "read_file",
        "create_file",
        "replace_in_file",
        "delete_snippet",
        "delete_file",
        "grep",
        "agent_run_shell_command",
        "list_agents",
        "agent_share_your_reasoning",
        "ask_user_question",
        "browser_initialize",
        "browser_close",
        "browser_new_page",
        "browser_navigate",
        "browser_wait_for_load",
        "browser_set_viewport",
        "browser_screenshot_analyze",
        "browser_execute_js",
        "browser_scroll",
        "browser_find_by_text",
        "browser_click",
        "load_image_for_analysis",
        "activate_skill",
        "list_or_search_skills",
        "universal_constructor"
      ]
    },
    {
      "name": "solutions-architect",
      "display_name": "Solutions Architect",
      "description": "Backend and infrastructure architect that conducts a two-dog research pack: delegates deep source evaluation to web-puppy and heavy scraping/login/form automation to web-retriever, while carrying web-retriever's full direct-action browser toolbelt itself. Produces MADR 4.0 ADRs with STRIDE analysis and fitness functions.",
      "type": "json",
      "tools": [
        "list_agents",
        "invoke_agent",
        "agent_share_your_reasoning",
        "ask_user_question",
        "list_files",
        "read_file",
        "grep",
        "create_file",
        "replace_in_file",
        "browser_initialize",
        "browser_close",
        "browser_status",
        "browser_new_page",
        "browser_list_pages",
        "browser_navigate",
        "browser_get_page_info",
        "browser_go_back",
        "browser_go_forward",
        "browser_reload",
        "browser_wait_for_load",
        "browser_page_snapshot",
        "browser_find_by_role",
        "browser_find_by_text",
        "browser_find_by_label",
        "browser_find_by_placeholder",
        "browser_find_by_test_id",
        "browser_find_buttons",
        "browser_find_links",
        "browser_xpath_query",
        "browser_click_by_role",
        "browser_click_by_text",
        "browser_set_text_by_label",
        "browser_click",
        "browser_double_click",
        "browser_hover",
        "browser_set_text",
        "browser_get_text",
        "browser_get_value",
        "browser_select_option",
        "browser_check",
        "browser_uncheck",
        "browser_execute_js",
        "browser_scroll",
        "browser_scroll_to_element",
        "browser_set_viewport",
        "browser_wait_for_element",
        "browser_highlight_element",
        "browser_clear_highlights",
        "browser_screenshot_analyze",
        "load_image_for_analysis",
        "browser_save_workflow",
        "browser_list_workflows",
        "browser_read_workflow"
      ]
    },
    {
      "name": "tenantfleet-architect",
      "display_name": "TenantFleet Architect ",
      "description": "Deep architectural synthesizer for multi-tenant identity frameworks. Excels at correlating patterns across disjoint repos and inferring system topology.",
      "type": "json",
      "tools": [
        "agent_share_your_reasoning",
        "agent_run_shell_command",
        "list_files",
        "read_file",
        "grep",
        "invoke_agent",
        "list_agents"
      ]
    },
    {
      "name": "tenantfleet-scanner",
      "display_name": "TenantFleet Scanner ",
      "description": "Massive-context repo scanner for multi-tenant identity frameworks. Ingests entire directory trees and correlates patterns across repos.",
      "type": "json",
      "tools": [
        "agent_share_your_reasoning",
        "agent_run_shell_command",
        "list_files",
        "read_file",
        "grep",
        "invoke_agent",
        "list_agents"
      ]
    },
    {
      "name": "web-puppy",
      "display_name": "Web-Puppy 🕵️‍♂️",
      "description": "Comprehensive web research agent that gathers, evaluates, and synthesizes information from reliable sources with multi-dimensional analysis and project-contextualized reporting",
      "type": "json",
      "tools": [
        "browser_initialize",
        "browser_navigate",
        "browser_new_page",
        "browser_list_pages",
        "browser_find_by_text",
        "browser_find_by_role",
        "browser_find_by_label",
        "browser_find_by_placeholder",
        "browser_find_by_test_id",
        "browser_find_links",
        "browser_xpath_query",
        "browser_get_text",
        "browser_get_value",
        "browser_scroll",
        "browser_scroll_to_element",
        "browser_screenshot_analyze",
        "browser_save_workflow",
        "browser_list_workflows",
        "browser_read_workflow",
        "browser_close",
        "list_files",
        "read_file",
        "edit_file",
        "agent_run_shell_command",
        "agent_share_your_reasoning"
      ]
    },
    {
      "name": "web-retriever",
      "display_name": "Web Retriever",
      "description": "Web scraping, browser automation, and data extraction specialist. Navigates websites, fills forms, clicks through multi-step flows, scrapes/crawls pages, and extracts structured data (to JSON/CSV/markdown) using Playwright. Use for: scrape this site, extract data from this page, automate this web workflow, crawl these URLs, fill out this form, log into this site and grab X. NOT for test assertions/visual QA - see qa-kitten for that.",
      "type": "python",
      "tools": [
        "browser_initialize",
        "browser_close",
        "browser_status",
        "browser_new_page",
        "browser_list_pages",
        "browser_navigate",
        "browser_get_page_info",
        "browser_go_back",
        "browser_go_forward",
        "browser_reload",
        "browser_wait_for_load",
        "browser_page_snapshot",
        "browser_find_by_role",
        "browser_find_by_text",
        "browser_find_by_label",
        "browser_find_by_placeholder",
        "browser_find_by_test_id",
        "browser_find_buttons",
        "browser_find_links",
        "browser_xpath_query",
        "browser_click_by_role",
        "browser_click_by_text",
        "browser_set_text_by_label",
        "browser_click",
        "browser_double_click",
        "browser_hover",
        "browser_set_text",
        "browser_get_text",
        "browser_get_value",
        "browser_select_option",
        "browser_check",
        "browser_uncheck",
        "browser_execute_js",
        "browser_scroll",
        "browser_scroll_to_element",
        "browser_set_viewport",
        "browser_wait_for_element",
        "browser_highlight_element",
        "browser_clear_highlights",
        "browser_screenshot_analyze",
        "load_image_for_analysis",
        "list_files",
        "read_file",
        "grep",
        "create_file",
        "replace_in_file",
        "browser_save_workflow",
        "browser_list_workflows",
        "browser_read_workflow",
        "ask_user_question"
      ]
    }
  ],
  "plugins": [
    {
      "name": "acp",
      "tier": "core-package",
      "description": "`acp` — Code Puppy as a native ACP agent  Run Code Puppy inside any ACP-capable editor's agent panel (e.g.",
      "hooks": [
        "handle_cli_args",
        "register_cli_args"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 8
        },
        {
          "name": "agent.py",
          "lines": 494
        },
        {
          "name": "bridge.py",
          "lines": 309
        },
        {
          "name": "capabilities.py",
          "lines": 73
        },
        {
          "name": "commands.py",
          "lines": 116
        },
        {
          "name": "content.py",
          "lines": 115
        },
        {
          "name": "io_delegation.py",
          "lines": 231
        },
        {
          "name": "mcp_config.py",
          "lines": 74
        },
        {
          "name": "permissions.py",
          "lines": 159
        },
        {
          "name": "persistence.py",
          "lines": 211
        },
        {
          "name": "register_callbacks.py",
          "lines": 110
        },
        {
          "name": "replay.py",
          "lines": 127
        },
        {
          "name": "session.py",
          "lines": 331
        },
        {
          "name": "session_config.py",
          "lines": 179
        },
        {
          "name": "state.py",
          "lines": 135
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "agent_creator_skill",
      "tier": "core-package",
      "description": "Register the bundled ``agent-creator`` delegation skill.",
      "hooks": [
        "register_skills"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "register_callbacks.py",
          "lines": 19
        }
      ],
      "hasReadme": false,
      "hasSkill": true
    },
    {
      "name": "agent_skills",
      "tier": "core-package",
      "description": "Agent Skills plugin - registers callbacks for skill integration.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "get_model_system_prompt",
        "register_skills",
        "register_tools"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 22
        },
        {
          "name": "config.py",
          "lines": 208
        },
        {
          "name": "discovery.py",
          "lines": 337
        },
        {
          "name": "downloader.py",
          "lines": 392
        },
        {
          "name": "enabled_skills.py",
          "lines": 82
        },
        {
          "name": "installer.py",
          "lines": 22
        },
        {
          "name": "metadata.py",
          "lines": 306
        },
        {
          "name": "prompt_builder.py",
          "lines": 49
        },
        {
          "name": "provider.py",
          "lines": 52
        },
        {
          "name": "register_callbacks.py",
          "lines": 309
        },
        {
          "name": "remote_catalog.py",
          "lines": 322
        },
        {
          "name": "skill_catalog.py",
          "lines": 277
        },
        {
          "name": "skill_commands.py",
          "lines": 102
        },
        {
          "name": "skills_install_menu.py",
          "lines": 609
        },
        {
          "name": "skills_menu.py",
          "lines": 682
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "auto_continue",
      "tier": "core-package",
      "description": "Register automatic continuation after routine permission requests.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "interactive_turn_end"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "classifier.py",
          "lines": 68
        },
        {
          "name": "register_callbacks.py",
          "lines": 100
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "aws_bedrock",
      "tier": "core-package",
      "description": "AWS Bedrock Plugin callbacks for Code Puppy CLI.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "register_model_type"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 14
        },
        {
          "name": "config.py",
          "lines": 101
        },
        {
          "name": "register_callbacks.py",
          "lines": 254
        },
        {
          "name": "utils.py",
          "lines": 186
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "azure_foundry",
      "tier": "core-package",
      "description": "Azure AI Foundry Plugin for Code Puppy  This plugin enables Code Puppy to use Anthropic Claude models hosted on Microsoft Azure AI Foundry with Azure AD (Entra...",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "register_model_type"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 15
        },
        {
          "name": "config.py",
          "lines": 126
        },
        {
          "name": "discovery.py",
          "lines": 189
        },
        {
          "name": "register_callbacks.py",
          "lines": 517
        },
        {
          "name": "token.py",
          "lines": 182
        },
        {
          "name": "utils.py",
          "lines": 375
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "btw",
      "tier": "core-package",
      "description": "Plugin: `/btw` — ask a quick side question without derailing the task.",
      "hooks": [
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "inline_view.py",
          "lines": 135
        },
        {
          "name": "register_callbacks.py",
          "lines": 106
        },
        {
          "name": "side_query.py",
          "lines": 91
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "chatgpt_oauth",
      "tier": "core-package",
      "description": "ChatGPT OAuth plugin callbacks aligned with ChatMock flow.",
      "hooks": [
        "agent_run_start",
        "custom_command",
        "custom_command_help",
        "load_models_config",
        "register_agent_tools",
        "register_model_type",
        "register_skills",
        "register_tools",
        "usage_status"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 8
        },
        {
          "name": "config.py",
          "lines": 55
        },
        {
          "name": "image_generation.py",
          "lines": 253
        },
        {
          "name": "image_tool.py",
          "lines": 70
        },
        {
          "name": "model_catalog.py",
          "lines": 77
        },
        {
          "name": "oauth_flow.py",
          "lines": 461
        },
        {
          "name": "register_callbacks.py",
          "lines": 301
        },
        {
          "name": "test_plugin.py",
          "lines": 683
        },
        {
          "name": "usage.py",
          "lines": 113
        },
        {
          "name": "utils.py",
          "lines": 578
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "claude_code_hooks",
      "tier": "core-package",
      "description": "Register callbacks for Claude Code hooks plugin.",
      "hooks": [
        "agent_run_end",
        "notification",
        "post_tool_call",
        "pre_compact",
        "pre_tool_call",
        "session_end",
        "startup",
        "user_prompt_submit"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "config.py",
          "lines": 140
        },
        {
          "name": "register_callbacks.py",
          "lines": 417
        },
        {
          "name": "trust.py",
          "lines": 339
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "claude_code_oauth",
      "tier": "core-package",
      "description": "Claude Code OAuth Plugin  This plugin adds OAuth authentication for Claude Code to Code Puppy, automatically importing available models into your configuration.",
      "hooks": [
        "agent_run_end",
        "agent_run_start",
        "check_claude_oauth_token_expiry",
        "claude_oauth_authenticate",
        "custom_command",
        "custom_command_help",
        "load_claude_oauth_models",
        "prepare_model_prompt",
        "refresh_claude_oauth_token",
        "register_model_type"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 25
        },
        {
          "name": "config.py",
          "lines": 59
        },
        {
          "name": "fast_mode.py",
          "lines": 121
        },
        {
          "name": "prompt_handler.py",
          "lines": 64
        },
        {
          "name": "register_callbacks.py",
          "lines": 725
        },
        {
          "name": "test_plugin.py",
          "lines": 285
        },
        {
          "name": "token_refresh_heartbeat.py",
          "lines": 240
        },
        {
          "name": "utils.py",
          "lines": 663
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "code_puppy_agent",
      "tier": "core-package",
      "description": "Register the built-in ``code-puppy-agent`` skill.",
      "hooks": [
        "register_skills"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 5
        },
        {
          "name": "register_callbacks.py",
          "lines": 46
        }
      ],
      "hasReadme": false,
      "hasSkill": true
    },
    {
      "name": "computer_use",
      "tier": "core-package",
      "description": "macOS Computer Use  This opt-in plugin lets Code Puppy inspect and operate the current macOS desktop through Apple's Accessibility APIs.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "load_prompt",
        "register_agent_tools",
        "register_tools",
        "startup"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "accessibility.py",
          "lines": 163
        },
        {
          "name": "activation.py",
          "lines": 75
        },
        {
          "name": "backend.py",
          "lines": 584
        },
        {
          "name": "backend_types.py",
          "lines": 5
        },
        {
          "name": "capture.py",
          "lines": 110
        },
        {
          "name": "commands.py",
          "lines": 62
        },
        {
          "name": "geometry.py",
          "lines": 81
        },
        {
          "name": "inline_image.py",
          "lines": 56
        },
        {
          "name": "keycodes.py",
          "lines": 47
        },
        {
          "name": "policy.py",
          "lines": 144
        },
        {
          "name": "register_callbacks.py",
          "lines": 96
        },
        {
          "name": "safety.py",
          "lines": 18
        },
        {
          "name": "settle.py",
          "lines": 64
        },
        {
          "name": "state.py",
          "lines": 86
        },
        {
          "name": "tools.py",
          "lines": 469
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "context_indicator",
      "tier": "core-package",
      "description": "Register callbacks for the ``context_indicator`` plugin.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "startup"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 14
        },
        {
          "name": "register_callbacks.py",
          "lines": 249
        },
        {
          "name": "usage.py",
          "lines": 40
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "copilot_auth",
      "tier": "core-package",
      "description": "GitHub Copilot auth plugin — callback registrations.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "register_model_type"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 11
        },
        {
          "name": "config.py",
          "lines": 93
        },
        {
          "name": "reasoning_client.py",
          "lines": 409
        },
        {
          "name": "register_callbacks.py",
          "lines": 456
        },
        {
          "name": "utils.py",
          "lines": 587
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "customizable_commands",
      "tier": "core-package",
      "description": "",
      "hooks": [
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 0
        },
        {
          "name": "register_callbacks.py",
          "lines": 464
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "dbos_durable_exec",
      "tier": "core-package",
      "description": "Wire the DBOS durable-execution plugin into core via callback hooks.",
      "hooks": [
        "agent_run_cancel",
        "agent_run_context",
        "custom_command",
        "custom_command_help",
        "feature_capability",
        "should_skip_fallback_render",
        "shutdown",
        "startup",
        "wrap_pydantic_agent"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "cancel.py",
          "lines": 15
        },
        {
          "name": "commands.py",
          "lines": 31
        },
        {
          "name": "config.py",
          "lines": 31
        },
        {
          "name": "lifecycle.py",
          "lines": 83
        },
        {
          "name": "register_callbacks.py",
          "lines": 45
        },
        {
          "name": "runtime.py",
          "lines": 60
        },
        {
          "name": "startup_lock.py",
          "lines": 155
        },
        {
          "name": "workflow_ids.py",
          "lines": 16
        },
        {
          "name": "wrapper.py",
          "lines": 58
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "destructive_command_guard",
      "tier": "core-package",
      "description": "Callback registration for the destructive command guard plugin.",
      "hooks": [
        "run_shell_command"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 14
        },
        {
          "name": "detector.py",
          "lines": 374
        },
        {
          "name": "register_callbacks.py",
          "lines": 165
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "emoji_filter",
      "tier": "core-package",
      "description": "Wire emoji_filter into the runtime.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "pre_tool_call",
        "startup",
        "stream_event"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 12
        },
        {
          "name": "config.py",
          "lines": 26
        },
        {
          "name": "register_callbacks.py",
          "lines": 309
        },
        {
          "name": "stripper.py",
          "lines": 45
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "empty_html_comment_filter",
      "tier": "core-package",
      "description": "Hide whitespace-only HTML comments from streamed thinking display.",
      "hooks": [
        "thinking_display_filter"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "register_callbacks.py",
          "lines": 116
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "example_custom_command",
      "tier": "core-package",
      "description": "Example Custom Command Plugin  > **Note**: This example demonstrates **custom commands** via the callback system.",
      "hooks": [
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "register_callbacks.py",
          "lines": 66
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "file_permission_handler",
      "tier": "core-package",
      "description": "File Permission Handler Plugin.",
      "hooks": [
        "file_permission",
        "load_prompt"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 4
        },
        {
          "name": "register_callbacks.py",
          "lines": 612
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "flux_bootstrap",
      "tier": "core-package",
      "description": "Flux bootstrap plugin.",
      "hooks": [
        "startup"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 5
        },
        {
          "name": "installer.py",
          "lines": 256
        },
        {
          "name": "register_callbacks.py",
          "lines": 71
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "force_push_guard",
      "tier": "core-package",
      "description": "Callback registration for the force push guard plugin.",
      "hooks": [
        "run_shell_command"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 5
        },
        {
          "name": "detector.py",
          "lines": 96
        },
        {
          "name": "register_callbacks.py",
          "lines": 161
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "fork",
      "tier": "core-package",
      "description": "``/fork`` — spawn a sub-agent in the background and keep working.",
      "hooks": [
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 7
        },
        {
          "name": "register_callbacks.py",
          "lines": 470
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "frontend_emitter",
      "tier": "core-package",
      "description": "Callback registration for frontend event emission.",
      "hooks": [
        "invoke_agent",
        "post_tool_call",
        "pre_tool_call",
        "stream_event"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 25
        },
        {
          "name": "emitter.py",
          "lines": 249
        },
        {
          "name": "register_callbacks.py",
          "lines": 412
        },
        {
          "name": "session_context.py",
          "lines": 50
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "grok_oauth",
      "tier": "core-package",
      "description": "Grok (x.ai) OAuth plugin callbacks.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "load_models_config",
        "register_model_type"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 6
        },
        {
          "name": "config.py",
          "lines": 49
        },
        {
          "name": "oauth_flow.py",
          "lines": 213
        },
        {
          "name": "register_callbacks.py",
          "lines": 132
        },
        {
          "name": "utils.py",
          "lines": 195
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "herdr",
      "tier": "core-package",
      "description": "herdr integration  Makes code-puppy a first-class citizen in [**herdr**](https://herdr.dev), a terminal workspace manager for coding agents.",
      "hooks": [
        "agent_run_cancel",
        "agent_run_end",
        "agent_run_start",
        "awaiting_user_input",
        "interactive_turn_cancel",
        "interactive_turn_end",
        "post_tool_call",
        "pre_tool_call",
        "session_end",
        "shutdown",
        "startup",
        "user_prompt_submit"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 9
        },
        {
          "name": "client.py",
          "lines": 339
        },
        {
          "name": "register_callbacks.py",
          "lines": 140
        },
        {
          "name": "reporter.py",
          "lines": 212
        },
        {
          "name": "smoke.py",
          "lines": 143
        },
        {
          "name": "sources.py",
          "lines": 133
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "hook_creator",
      "tier": "core-package",
      "description": "Hook Creator Plugin - Simple command that injects MCP prompt",
      "hooks": [
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "register_callbacks.py",
          "lines": 33
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "hook_manager",
      "tier": "core-package",
      "description": "Hook Manager plugin – registers callbacks for interactive hook management.",
      "hooks": [
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "config.py",
          "lines": 314
        },
        {
          "name": "hooks_menu.py",
          "lines": 493
        },
        {
          "name": "register_callbacks.py",
          "lines": 243
        },
        {
          "name": "trust_handler.py",
          "lines": 185
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "i_have_adhd",
      "tier": "user",
      "description": "i-have-adhd (Code Puppy port)  ADHD-friendly output mode, ported from [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) (MIT).",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "load_prompt",
        "register_skills"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 0
        },
        {
          "name": "register_callbacks.py",
          "lines": 141
        }
      ],
      "hasReadme": true,
      "hasSkill": true
    },
    {
      "name": "logfire_oauth",
      "tier": "core-package",
      "description": "Register the Logfire OAuth slash command.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "register_agent_tools",
        "register_tools",
        "startup"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "oauth.py",
          "lines": 439
        },
        {
          "name": "query_tool.py",
          "lines": 99
        },
        {
          "name": "register_callbacks.py",
          "lines": 166
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "logfire_sessions",
      "tier": "core-package",
      "description": "Register the Logfire session-mirroring plugin.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "post_autosave"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 7
        },
        {
          "name": "mirror.py",
          "lines": 108
        },
        {
          "name": "query.py",
          "lines": 119
        },
        {
          "name": "register_callbacks.py",
          "lines": 138
        },
        {
          "name": "sync.py",
          "lines": 153
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "logo_toolkit",
      "tier": "user",
      "description": "User plugin: /logo slash command for logo manipulation.",
      "hooks": [
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "logo_ops.py",
          "lines": 181
        },
        {
          "name": "register_callbacks.py",
          "lines": 361
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "meta_oauth",
      "tier": "core-package",
      "description": "Callbacks for Meta Muse OAuth authentication and model registration.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "load_models_config",
        "register_model_type"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "config.py",
          "lines": 55
        },
        {
          "name": "oauth_flow.py",
          "lines": 109
        },
        {
          "name": "register_callbacks.py",
          "lines": 154
        },
        {
          "name": "utils.py",
          "lines": 252
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "namespace_skill_search",
      "tier": "core-package",
      "description": "namespace_skill_search  Model-agnostic reimplementation of OpenAI's namespace + `tool_search` pattern, applied to Code Puppy's skill catalog.",
      "hooks": [
        "load_prompt",
        "register_agent_tools",
        "register_tools",
        "startup"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 15
        },
        {
          "name": "namespaces.py",
          "lines": 125
        },
        {
          "name": "register_callbacks.py",
          "lines": 99
        },
        {
          "name": "search_tool.py",
          "lines": 158
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "no_tools",
      "tier": "core-package",
      "description": "``--no-tools`` CLI flag (issue #182).",
      "hooks": [
        "handle_cli_args",
        "register_cli_args"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 0
        },
        {
          "name": "register_callbacks.py",
          "lines": 42
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "obsidian_agent",
      "tier": "core-package",
      "description": "Obsidian Agent  The Obsidian Agent adds a specialized Code Puppy agent for working with Obsidian vaults through the official `obsidian` CLI.",
      "hooks": [
        "register_agents"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 8
        },
        {
          "name": "agent_obsidian.py",
          "lines": 147
        },
        {
          "name": "register_callbacks.py",
          "lines": 13
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "ollama",
      "tier": "core-package",
      "description": "Ollama model type handler for OpenAI Chat Completions-compatible endpoints.",
      "hooks": [
        "register_model_type"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "register_callbacks.py",
          "lines": 126
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "ollama_setup",
      "tier": "core-package",
      "description": "Ollama cloud model setup — /ollama-setup command.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "register_completion_provider"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 5
        },
        {
          "name": "completer.py",
          "lines": 37
        },
        {
          "name": "register_callbacks.py",
          "lines": 419
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "openrouter_oauth",
      "tier": "core-package",
      "description": "OpenRouter OAuth plugin callbacks.",
      "hooks": [
        "provider_credential_flow"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 6
        },
        {
          "name": "config.py",
          "lines": 21
        },
        {
          "name": "oauth_flow.py",
          "lines": 242
        },
        {
          "name": "register_callbacks.py",
          "lines": 93
        },
        {
          "name": "test_plugin.py",
          "lines": 263
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "plugin_list",
      "tier": "core-package",
      "description": "``/plugins`` slash command -- manage plugins interactively or via subcommands.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "startup"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 0
        },
        {
          "name": "plugin_contributions.py",
          "lines": 348
        },
        {
          "name": "plugin_meta.py",
          "lines": 67
        },
        {
          "name": "plugin_text_utils.py",
          "lines": 183
        },
        {
          "name": "plugins_menu.py",
          "lines": 444
        },
        {
          "name": "plugins_menu_render.py",
          "lines": 431
        },
        {
          "name": "project_trust_flow.py",
          "lines": 162
        },
        {
          "name": "register_callbacks.py",
          "lines": 343
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "pop_command",
      "tier": "core-package",
      "description": "Plugin that adds /pop for trimming recent conversation history.",
      "hooks": [
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "register_callbacks.py",
          "lines": 191
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "prompt_newline",
      "tier": "core-package",
      "description": "Register callbacks for the prompt_newline plugin.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "startup"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 13
        },
        {
          "name": "config.py",
          "lines": 21
        },
        {
          "name": "register_callbacks.py",
          "lines": 164
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "prune",
      "tier": "core-package",
      "description": "Plugin that adds /prune for surgical history pruning.",
      "hooks": [
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "prune_menu.py",
          "lines": 211
        },
        {
          "name": "prune_model.py",
          "lines": 536
        },
        {
          "name": "prune_render.py",
          "lines": 354
        },
        {
          "name": "register_callbacks.py",
          "lines": 388
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "puppy_kennel",
      "tier": "core-package",
      "description": "Puppy Kennel  Local-first memory for Code Puppy.",
      "hooks": [
        "agent_run_end",
        "custom_command",
        "custom_command_help",
        "load_prompt",
        "register_agent_tools",
        "register_kennel_memory",
        "register_tools"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 6
        },
        {
          "name": "commands.py",
          "lines": 206
        },
        {
          "name": "config.py",
          "lines": 36
        },
        {
          "name": "kennel.py",
          "lines": 368
        },
        {
          "name": "packer.py",
          "lines": 152
        },
        {
          "name": "recorder.py",
          "lines": 83
        },
        {
          "name": "register_callbacks.py",
          "lines": 109
        },
        {
          "name": "retriever.py",
          "lines": 28
        },
        {
          "name": "schema.py",
          "lines": 78
        },
        {
          "name": "state.py",
          "lines": 68
        },
        {
          "name": "tools.py",
          "lines": 449
        },
        {
          "name": "wings.py",
          "lines": 110
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "puppy_spinner",
      "tier": "core-package",
      "description": "puppy_spinner  The bouncing-puppy spinner on the bottom bar's status-prefix slot — now with customizable styles.",
      "hooks": [
        "agent_run_end",
        "agent_run_start",
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 11
        },
        {
          "name": "builtin_frames.py",
          "lines": 172
        },
        {
          "name": "commands.py",
          "lines": 116
        },
        {
          "name": "picker.py",
          "lines": 312
        },
        {
          "name": "register_callbacks.py",
          "lines": 193
        },
        {
          "name": "spinners.py",
          "lines": 444
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "qa_kitten_skill",
      "tier": "core-package",
      "description": "Register the bundled ``qa-kitten`` delegation skill.",
      "hooks": [
        "register_skills"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "register_callbacks.py",
          "lines": 19
        }
      ],
      "hasReadme": false,
      "hasSkill": true
    },
    {
      "name": "quick_resume",
      "tier": "core-package",
      "description": "Quick-resume workspace observation hooks.",
      "hooks": [
        "post_tool_call"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 0
        },
        {
          "name": "register_callbacks.py",
          "lines": 77
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "review_pr",
      "tier": "core-package",
      "description": "Plugin: `/review-pr` — hand the agent a structured PR review mission.",
      "hooks": [
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "register_callbacks.py",
          "lines": 162
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "session_namer",
      "tier": "core-package",
      "description": "Register the session-namer plugin.",
      "hooks": [
        "post_autosave",
        "session_browser_open"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "namer.py",
          "lines": 255
        },
        {
          "name": "register_callbacks.py",
          "lines": 86
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "shell_safety",
      "tier": "core-package",
      "description": "Callback registration for shell command safety checking.",
      "hooks": [
        "run_shell_command"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 6
        },
        {
          "name": "classifier.py",
          "lines": 48
        },
        {
          "name": "command_cache.py",
          "lines": 156
        },
        {
          "name": "register_callbacks.py",
          "lines": 209
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "spill",
      "tier": "core-package",
      "description": "Plugin: spill oversized dict-shaped tool results to private files.",
      "hooks": [
        "post_tool_call",
        "startup"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "register_callbacks.py",
          "lines": 336
        },
        {
          "name": "store.py",
          "lines": 173
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "stack_dump",
      "tier": "core-package",
      "description": "Register callbacks for the ``stack_dump`` plugin.",
      "hooks": [
        "startup"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "register_callbacks.py",
          "lines": 79
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "statusline",
      "tier": "core-package",
      "description": "Wire up the statusline plugin.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "git_branch_provider",
        "startup"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 14
        },
        {
          "name": "config.py",
          "lines": 68
        },
        {
          "name": "payload.py",
          "lines": 138
        },
        {
          "name": "prompt_patch.py",
          "lines": 95
        },
        {
          "name": "register_callbacks.py",
          "lines": 45
        },
        {
          "name": "runner.py",
          "lines": 122
        },
        {
          "name": "statusline_command.py",
          "lines": 197
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "steer_queue",
      "tier": "core-package",
      "description": "Register callbacks for the ``steer_queue`` plugin.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "startup"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 10
        },
        {
          "name": "queue_menu.py",
          "lines": 359
        },
        {
          "name": "register_callbacks.py",
          "lines": 137
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "subagent_panel",
      "tier": "core-package",
      "description": "subagent_panel  A live, two-line status block for each running sub-agent, painted just above the bouncing puppy:  ```   INVOKE AGENT  pup-ticket-investigator...",
      "hooks": [
        "agent_run_cancel",
        "agent_run_end",
        "post_tool_call",
        "startup",
        "stream_event"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 24
        },
        {
          "name": "coalesce_patch.py",
          "lines": 242
        },
        {
          "name": "panel_render.py",
          "lines": 149
        },
        {
          "name": "register_callbacks.py",
          "lines": 544
        },
        {
          "name": "resume_repaint.py",
          "lines": 112
        },
        {
          "name": "state.py",
          "lines": 233
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "switch_agent_resume",
      "tier": "core-package",
      "description": "Register /switch-agent and /sa custom commands.",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "startup"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 5
        },
        {
          "name": "register_callbacks.py",
          "lines": 314
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "theme",
      "tier": "core-package",
      "description": "theme — `/theme` for Code Puppy  A friendlier `/theme` command with an **interactive picker**, **live preview**, and **four layers of theming** — banner header...",
      "hooks": [
        "custom_command",
        "custom_command_help",
        "prompt_text_color",
        "prompt_toolkit_style",
        "startup",
        "termflow_highlighter",
        "termflow_style"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "__init__.py",
          "lines": 14
        },
        {
          "name": "bundled_palettes.py",
          "lines": 34
        },
        {
          "name": "content_styles.py",
          "lines": 146
        },
        {
          "name": "osc_palette.py",
          "lines": 146
        },
        {
          "name": "picker.py",
          "lines": 259
        },
        {
          "name": "prompt_toolkit_theme.py",
          "lines": 113
        },
        {
          "name": "register_callbacks.py",
          "lines": 348
        },
        {
          "name": "rich_themes.py",
          "lines": 202
        },
        {
          "name": "themes.py",
          "lines": 720
        }
      ],
      "hasReadme": true,
      "hasSkill": false
    },
    {
      "name": "timestamp_heartbeat",
      "tier": "core-package",
      "description": "Plugin: timestamp heartbeat — stamp the current datetime into tool results.",
      "hooks": [
        "post_tool_call"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "register_callbacks.py",
          "lines": 114
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "token_ratio_learner",
      "tier": "core-package",
      "description": "Register callbacks for the token-ratio-learner plugin.",
      "hooks": [
        "startup"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 5
        },
        {
          "name": "ratios.py",
          "lines": 208
        },
        {
          "name": "register_callbacks.py",
          "lines": 218
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "universal_constructor",
      "tier": "core-package",
      "description": "Callback registration for the Universal Constructor plugin.",
      "hooks": [
        "register_tools",
        "startup"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 13
        },
        {
          "name": "models.py",
          "lines": 138
        },
        {
          "name": "provider.py",
          "lines": 62
        },
        {
          "name": "register_callbacks.py",
          "lines": 75
        },
        {
          "name": "registry.py",
          "lines": 302
        },
        {
          "name": "sandbox.py",
          "lines": 584
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "update_schedule",
      "tier": "user",
      "description": "User plugin: /update slash command for the code-puppy daily update schedule.",
      "hooks": [
        "custom_command",
        "custom_command_help"
      ],
      "hasCustomCommand": true,
      "files": [
        {
          "name": "register_callbacks.py",
          "lines": 198
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "web_retriever_skill",
      "tier": "core-package",
      "description": "Register the built-in ``web-retriever`` skill.",
      "hooks": [
        "register_skills"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "register_callbacks.py",
          "lines": 20
        }
      ],
      "hasReadme": false,
      "hasSkill": true
    },
    {
      "name": "wiggum",
      "tier": "core-package",
      "description": "Register the Wiggum looping slash commands and goal continuation policy.",
      "hooks": [
        "feature_capability",
        "interactive_turn_cancel",
        "interactive_turn_end"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "goal_runs.py",
          "lines": 91
        },
        {
          "name": "judge.py",
          "lines": 299
        },
        {
          "name": "judge_config.py",
          "lines": 249
        },
        {
          "name": "judges_menu.py",
          "lines": 607
        },
        {
          "name": "register_callbacks.py",
          "lines": 569
        },
        {
          "name": "state.py",
          "lines": 89
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    },
    {
      "name": "yolo_cli",
      "tier": "core-package",
      "description": "Expose a runtime-only YOLO override through the CLI.",
      "hooks": [
        "handle_cli_args",
        "register_cli_args"
      ],
      "hasCustomCommand": false,
      "files": [
        {
          "name": "__init__.py",
          "lines": 1
        },
        {
          "name": "register_callbacks.py",
          "lines": 41
        }
      ],
      "hasReadme": false,
      "hasSkill": false
    }
  ],
  "skills": [
    {
      "name": "agent-creator",
      "source": "core-package",
      "description": "Use before creating or revising a Code Puppy JSON agent. Delegates schema design, least-privilege tool selection, optional model and MCP bindings, validation, and per-agent Spill configuration to agent-creator.",
      "path": "code_puppy_core_plugins/agent_creator_skill/SKILL.md"
    },
    {
      "name": "code-puppy-agent",
      "source": "core-package",
      "description": "How Code Puppy itself is built — its internal architecture, structure, codebase layout, and source modules. Explains agents, tools, the plugin/callback hook system, models, MCP, sessions and history/context windows, skills (including skill namespaces for large catalogs), slash commands, config, messaging/UI, system-prompt assembly, and i18n. Activate for ANY question about how Code Puppy works internally, why it behaves a certain way, where something lives in the code, how a feature is implemented, or how to navigate, debug, or extend the codebase (add a tool, agent, plugin, command, skill, model, or MCP server).",
      "path": "code_puppy_core_plugins/code_puppy_agent/SKILL.md"
    },
    {
      "name": "i-have-adhd",
      "source": "user",
      "description": "Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state across turns, suppress tangents, give specific time estimates, make wins visible. Invoke with /adhd on; stays on until /adhd off.",
      "path": "/Users/tygranlund/.code_puppy/plugins/i_have_adhd/SKILL.md"
    },
    {
      "name": "qa-kitten",
      "source": "core-package",
      "description": "Use before testing a web application's behavior, accessibility, responsive layout, or visual rendering in a real browser. Delegates browser assertions and visual QA to qa-kitten; not for scraping, crawling, or general web retrieval.",
      "path": "code_puppy_core_plugins/qa_kitten_skill/SKILL.md"
    },
    {
      "name": "web-retriever",
      "source": "core-package",
      "description": "Use before handling web scraping, browser automation, crawling, structured data extraction, authenticated or interactive website workflows, monitoring pages for changes, or website screenshots. Delegates browser work to the web-retriever agent; not for test assertions or visual QA.",
      "path": "code_puppy_core_plugins/web_retriever_skill/SKILL.md"
    }
  ],
  "sdlc": [
    {
      "stage": "1. Ideate & Spec",
      "goal": "Turn a fuzzy idea into a crisp, testable plan.",
      "use": [
        "code-puppy to draft the design and spike options",
        "Agent Creator to spin up a domain-specialist sub-agent if the work repeats",
        "kennel memory to record decisions so the next session knows them"
      ],
      "output": "A written spec + acceptance criteria the agent can verify against."
    },
    {
      "stage": "2. Explore & Research",
      "goal": "Verify facts before writing code.",
      "use": [
        "web-puppy for docs, version compatibility, and API research",
        "web-retriever (via invoke_agent) for scraping/automation flows",
        "grep/read_file to ground decisions in the existing codebase"
      ],
      "output": "A citation-backed summary of constraints and known-good approaches."
    },
    {
      "stage": "3. Build",
      "goal": "Implement in small, reviewable diffs.",
      "use": [
        "replace_in_file over full rewrites (small diffs, easy review)",
        "Plugins over core edits (golden rule: new functionality = a plugin, not core)",
        "Helios / universal_constructor when you need a tool that doesn't exist"
      ],
      "output": "Working code that respects the repo's conventions (DRY, YAGNI, <600 lines/file)."
    },
    {
      "stage": "4. Test & QA",
      "goal": "Prove it works and looks right.",
      "use": [
        "agent_run_shell_command to run the test suite for real",
        "qa-kitten for visual/assertion QA on UIs",
        "Loop: run, read failures, fix, re-run. Don't stop at 'should work'."
      ],
      "output": "A green test run, not a promise."
    },
    {
      "stage": "5. Secure & Comply",
      "goal": "Ship something you won't regret.",
      "use": [
        "destructive_command_guard & force_push_guard plugins to block foot-guns",
        "Project plugin trust-gate so repo code can't silently self-approve",
        "Review diffs and secrets handling before commit"
      ],
      "output": "Code with guardrails active and no leaked secrets."
    },
    {
      "stage": "6. Ship & Polish",
      "goal": "Make it badass and beautiful, then deliver.",
      "use": [
        "Design-system tokens (like the CPU deck's tokens.css) for prompt-addressable theming",
        "The field guide itself to onboard collaborators",
        "dbos_durable_exec for long jobs that must survive crashes"
      ],
      "output": "A stable, documented artifact you're proud to demo."
    }
  ],
  "changelog": {
    "total_commits": 952,
    "releases": [
      {
        "month": "2026-08",
        "commit_count": 591,
        "commits": [
          {
            "hash": "a12ed1f4fc2924a20f54e6f2276895bddf165c50",
            "short_hash": "a12ed1f4",
            "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-27 15:34)",
            "author": "Tyler Granlund",
            "date": "2026-08-27",
            "month": "2026-08"
          },
          {
            "hash": "4d567a5751679a8b31828dd1aa96955635304b21",
            "short_hash": "4d567a57",
            "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-27 14:13)",
            "author": "Tyler Granlund",
            "date": "2026-08-27",
            "month": "2026-08"
          },
          {
            "hash": "eddff2414be887e8abc34838a2d25e78034d7849",
            "short_hash": "eddff241",
            "subject": "chore: auto-commit pre-update leftovers (2026-08-27 14:11)",
            "author": "Tyler Granlund",
            "date": "2026-08-27",
            "month": "2026-08"
          },
          {
            "hash": "dd9d44bb0e9ccf868b3aaf8cc8ca763fea3e617b",
            "short_hash": "dd9d44bb",
            "subject": "fix: remove shell from field guide (double-sidebar collision)",
            "author": "Tyler Granlund",
            "date": "2026-08-24",
            "month": "2026-08"
          },
          {
            "hash": "a1b20a8e8faa0f6e38454465b8d9a732a0f0620d",
            "short_hash": "a1b20a8e",
            "subject": "feat: left sidebar navigation across all pages, mobile-optimized",
            "author": "Tyler Granlund",
            "date": "2026-08-24",
            "month": "2026-08"
          },
          {
            "hash": "6cc0080332edc5a3e7a3227b5f07094aff57ecfd",
            "short_hash": "6cc00803",
            "subject": "fix: broken nav/sidebar logo — height:auto collapses in flex",
            "author": "Tyler Granlund",
            "date": "2026-08-24",
            "month": "2026-08"
          },
          {
            "hash": "de17cf215a4c95f2ac291970ac46fb61e4681bd8",
            "short_hash": "de17cf21",
            "subject": "fix(pages-hub): replace fake inline SVG silhouettes with real logo",
            "author": "Tyler Granlund",
            "date": "2026-08-24",
            "month": "2026-08"
          },
          {
            "hash": "d9e5346d693639dd6fb91b16587616ab667f9250",
            "short_hash": "d9e5346d",
            "subject": "fix(pages-hub): stats show real numbers locally (fetch -> script include)",
            "author": "Tyler Granlund",
            "date": "2026-08-24",
            "month": "2026-08"
          },
          {
            "hash": "48f5fc834450c6431638692049f9653a5afc734c",
            "short_hash": "48f5fc83",
            "subject": "fix(pages-hub): QA pass on landing page — 12 issues fixed",
            "author": "Tyler Granlund",
            "date": "2026-08-24",
            "month": "2026-08"
          },
          {
            "hash": "3cdb082574dec903cc89560097cb28a079f04bf3",
            "short_hash": "3cdb0825",
            "subject": "feat(field-guide): sortable, filterable plugin sidebar",
            "author": "Tyler Granlund",
            "date": "2026-08-24",
            "month": "2026-08"
          }
        ]
      },
      {
        "month": "2026-07",
        "commit_count": 361,
        "commits": [
          {
            "hash": "4305a354dc57fe0d83f61476189f00dffe5e01d0",
            "short_hash": "4305a354",
            "subject": "docs: CPU interactive curriculum web app + puppy mark",
            "author": "Tyler Granlund",
            "date": "2026-07-31",
            "month": "2026-07"
          },
          {
            "hash": "0d0efbad27ba9c9293a3788298cd3910128831cf",
            "short_hash": "0d0efbad",
            "subject": "docs: deck v3 — Acts IX/X, the internal + external university",
            "author": "Tyler Granlund",
            "date": "2026-07-31",
            "month": "2026-07"
          },
          {
            "hash": "3360b6e774075e489e653ce9a8b447226d9d7e35",
            "short_hash": "3360b6e7",
            "subject": "docs: deck v2.1 — token architecture, component registry, 42-test suite",
            "author": "Tyler Granlund",
            "date": "2026-07-30",
            "month": "2026-07"
          },
          {
            "hash": "49d49afebc643c61098915726521643327929746",
            "short_hash": "49d49afe",
            "subject": "docs: deck v2 — Cornerstone+ design system, Fireship beat, fact-check pass",
            "author": "Tyler Granlund",
            "date": "2026-07-30",
            "month": "2026-07"
          },
          {
            "hash": "e2a4ac48d44e7d94b1ef622518732d429a8bc235",
            "short_hash": "e2a4ac48",
            "subject": "docs: The Great Adpuppytion — Code-Puppy University founding deck",
            "author": "Tyler Granlund",
            "date": "2026-07-30",
            "month": "2026-07"
          },
          {
            "hash": "6a9f539bf7df86767f85a474f9a5fbe55dbd7ac6",
            "short_hash": "6a9f539b",
            "subject": "fix(mcp): a config can't be its own untrusted project twin (CWD == $HOME)",
            "author": "breedx",
            "date": "2026-07-31",
            "month": "2026-07"
          },
          {
            "hash": "0d7764e03a34959b2cea717521fc21c7f9d1692c",
            "short_hash": "0d7764e0",
            "subject": "chore: bump version [ci skip]",
            "author": "github-actions[bot]",
            "date": "2026-07-30",
            "month": "2026-07"
          },
          {
            "hash": "37f5a9adf736df41e6465e6979aaab9f19b7ff03",
            "short_hash": "37f5a9ad",
            "subject": "fix(computer-use): require explicit opt-in (#688)",
            "author": "mpfaffenberger",
            "date": "2026-07-30",
            "month": "2026-07"
          },
          {
            "hash": "baa95cefc63778c6320cad6654246e5d8102f503",
            "short_hash": "baa95cef",
            "subject": "chore: bump version [ci skip]",
            "author": "github-actions[bot]",
            "date": "2026-07-29",
            "month": "2026-07"
          },
          {
            "hash": "bfc4927f209493b8a97fc968cf9f38af5734c21d",
            "short_hash": "bfc4927f",
            "subject": "Merge pull request #685 from mpfaffenberger/awtilso/PUP-549",
            "author": "Andrew Tilson",
            "date": "2026-07-29",
            "month": "2026-07"
          }
        ]
      }
    ],
    "commits": [
      {
        "hash": "a12ed1f4fc2924a20f54e6f2276895bddf165c50",
        "short_hash": "a12ed1f4",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-27 15:34)",
        "author": "Tyler Granlund",
        "date": "2026-08-27"
      },
      {
        "hash": "4d567a5751679a8b31828dd1aa96955635304b21",
        "short_hash": "4d567a57",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-27 14:13)",
        "author": "Tyler Granlund",
        "date": "2026-08-27"
      },
      {
        "hash": "eddff2414be887e8abc34838a2d25e78034d7849",
        "short_hash": "eddff241",
        "subject": "chore: auto-commit pre-update leftovers (2026-08-27 14:11)",
        "author": "Tyler Granlund",
        "date": "2026-08-27"
      },
      {
        "hash": "dd9d44bb0e9ccf868b3aaf8cc8ca763fea3e617b",
        "short_hash": "dd9d44bb",
        "subject": "fix: remove shell from field guide (double-sidebar collision)",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "a1b20a8e8faa0f6e38454465b8d9a732a0f0620d",
        "short_hash": "a1b20a8e",
        "subject": "feat: left sidebar navigation across all pages, mobile-optimized",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "6cc0080332edc5a3e7a3227b5f07094aff57ecfd",
        "short_hash": "6cc00803",
        "subject": "fix: broken nav/sidebar logo — height:auto collapses in flex",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "de17cf215a4c95f2ac291970ac46fb61e4681bd8",
        "short_hash": "de17cf21",
        "subject": "fix(pages-hub): replace fake inline SVG silhouettes with real logo",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "d9e5346d693639dd6fb91b16587616ab667f9250",
        "short_hash": "d9e5346d",
        "subject": "fix(pages-hub): stats show real numbers locally (fetch -> script include)",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "48f5fc834450c6431638692049f9653a5afc734c",
        "short_hash": "48f5fc83",
        "subject": "fix(pages-hub): QA pass on landing page — 12 issues fixed",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "3cdb082574dec903cc89560097cb28a079f04bf3",
        "short_hash": "3cdb0825",
        "subject": "feat(field-guide): sortable, filterable plugin sidebar",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "dba4cd9412e366ac19aa314dd10653422ed6b04e",
        "short_hash": "dba4cd94",
        "subject": "feat(field-guide): master-detail plugin ecosystem explorer",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "25bd211ef9905480272b9d8eb339a7659fcd9fd0",
        "short_hash": "25bd211e",
        "subject": "feat(logo): white logo toolkit plugin + white logo for grove theme",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "dd4cca0fb7ab7e6a64e06eccb325add26340e668",
        "short_hash": "dd4cca0f",
        "subject": "design: migrate design system to Granlund-Grove forest palette",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "fbb2684fa5d9ff239fb19c158d6a95a35c0ff7df",
        "short_hash": "fbb2684f",
        "subject": "docs(field-guide+hub): use real Code Puppy logo across nav, favicon & shell",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "644a9782ada9ec69da86143ec884bc462887b5f7",
        "short_hash": "644a9782",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-24 10:56)",
        "author": "Tyler Granlund",
        "date": "2026-08-24"
      },
      {
        "hash": "a2394b7e63a84c87d27ccd4a801f46e95b7017ce",
        "short_hash": "a2394b7e",
        "subject": "docs(pages): bump version refs to v0.0.768 + rebuild offline wheel",
        "author": "Tyler Granlund",
        "date": "2026-08-22"
      },
      {
        "hash": "092679e065ee1ee980dd434e536754025a9c1480",
        "short_hash": "092679e0",
        "subject": "docs(field-guide+observatory): regenerate for v0.0.768 update",
        "author": "Tyler Granlund",
        "date": "2026-08-22"
      },
      {
        "hash": "5570df6104a95b7ade1becce784a6373dd5ef5cd",
        "short_hash": "5570df61",
        "subject": "chore: auto-commit pre-update leftovers (2026-08-22 21:55)",
        "author": "Tyler Granlund",
        "date": "2026-08-22"
      },
      {
        "hash": "4761214551d25f52f422545a31f22a313b6f6d1f",
        "short_hash": "47612145",
        "subject": "chore: rebuild offline wheel to v0.0.754, untrack NEWLog session log",
        "author": "Tyler Granlund",
        "date": "2026-08-21"
      },
      {
        "hash": "b202aac5ba31758ddbc64620c8a69ecd2878bee9",
        "short_hash": "b202aac5",
        "subject": "docs(pages): switch update_schedule to ad-hoc mode (no launchd)",
        "author": "Tyler Granlund",
        "date": "2026-08-21"
      },
      {
        "hash": "4b5fc66d116a619f8b395c9b801f2eadc347eedc",
        "short_hash": "4b5fc66d",
        "subject": "docs(pages): bump stale version refs to v0.0.754 (architecture.html, SOVEREIGNTY.md, FIELD_GUIDE_MAP snapshot)",
        "author": "Tyler Granlund",
        "date": "2026-08-21"
      },
      {
        "hash": "ba29310f8000a05d2084d3199dd4c37d07a4c1f2",
        "short_hash": "ba29310f",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-21 14:43)",
        "author": "Tyler Granlund",
        "date": "2026-08-21"
      },
      {
        "hash": "0902fedbdb99390979bddaa5c13f332ad0916e75",
        "short_hash": "0902fedb",
        "subject": "docs: fix stale version refs (v0.0.729/v0.0.709 -> v0.0.751) in architecture.html + SOVEREIGNTY.md",
        "author": "Tyler Granlund",
        "date": "2026-08-20"
      },
      {
        "hash": "902c3787fca395880491ff59dcf3e306f36535f8",
        "short_hash": "902c3787",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-20 18:47)",
        "author": "Tyler Granlund",
        "date": "2026-08-20"
      },
      {
        "hash": "66af571d78433eab2866e0a56280c15e236a8ff7",
        "short_hash": "66af571d",
        "subject": "chore: auto-commit pre-update leftovers (2026-08-20 18:46)",
        "author": "Tyler Granlund",
        "date": "2026-08-20"
      },
      {
        "hash": "b5933ecd8d4dfcd75ac79b1c3fad9726d3c9f160",
        "short_hash": "b5933ecd",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-20 18:42)",
        "author": "Tyler Granlund",
        "date": "2026-08-20"
      },
      {
        "hash": "adcb23881b0df3d79977e6420eddad8c7aeaed03",
        "short_hash": "adcb2388",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-20 18:36)",
        "author": "Tyler Granlund",
        "date": "2026-08-20"
      },
      {
        "hash": "ab5308ad72984898f50df06e9379131d125140cd",
        "short_hash": "ab5308ad",
        "subject": "chore: auto-commit pre-update leftovers (2026-08-20 18:34)",
        "author": "Tyler Granlund",
        "date": "2026-08-20"
      },
      {
        "hash": "209fe5529b890772d2332c166323e8948567bddf",
        "short_hash": "209fe552",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-20 18:04)",
        "author": "Tyler Granlund",
        "date": "2026-08-20"
      },
      {
        "hash": "dfb8deff3971ae2e507d43be04e635251593d4c9",
        "short_hash": "dfb8deff",
        "subject": "chore: auto-commit pre-update leftovers (2026-08-20 18:02)",
        "author": "Tyler Granlund",
        "date": "2026-08-20"
      },
      {
        "hash": "ee36dadb37c8686ea2350b4216af799b4c324857",
        "short_hash": "ee36dadb",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-19 07:02)",
        "author": "Tyler Granlund",
        "date": "2026-08-19"
      },
      {
        "hash": "b1d4599975ea301a80f4ca0a3e78ce1a7e522892",
        "short_hash": "b1d45999",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-18 20:02)",
        "author": "Tyler Granlund",
        "date": "2026-08-18"
      },
      {
        "hash": "95449e7fe15eac4a2189d7aa9bd8c911e0e5ae7c",
        "short_hash": "95449e7f",
        "subject": "chore: auto-commit pre-update leftovers (2026-08-18 20:00)",
        "author": "Tyler Granlund",
        "date": "2026-08-18"
      },
      {
        "hash": "39e07fe269d1f32025c0b3007fe22f7aa119aef1",
        "short_hash": "39e07fe2",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-18 12:01)",
        "author": "Tyler Granlund",
        "date": "2026-08-18"
      },
      {
        "hash": "7402d085a9d6a44cd80cc817437d3a784b6ca35b",
        "short_hash": "7402d085",
        "subject": "feat(a11y): sweep legacy page bodies to WCAG 2.2 AAA body-text contrast",
        "author": "Tyler Granlund",
        "date": "2026-08-18"
      },
      {
        "hash": "9fa89796e1eb5d69c55a253ed3668199fd9e5bea",
        "short_hash": "9fa89796",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-18 07:02)",
        "author": "Tyler Granlund",
        "date": "2026-08-18"
      },
      {
        "hash": "dbc1a405b573dbefe83d199bfb5184c53ca9eb25",
        "short_hash": "dbc1a405",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-17 20:02)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "8315767a7fc315c851eefbbcfd053e805b9b3650",
        "short_hash": "8315767a",
        "subject": "docs: build log + roadmap (what shipped, where, QA status, forward plan)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "1d07640a2fde45b1dfb12cfd6692ade801c63158",
        "short_hash": "1d07640a",
        "subject": "feat(ui): sidebar app-shell + reusable popover + design system, WCAG 2.2 AAA",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "8a9bfff77e9fb2f4697f8a1b6666b9eee96f863d",
        "short_hash": "8a9bfff7",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-17 17:21)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "762cb843f386fdf6b6dbd4c7e0b69b2eac9063cd",
        "short_hash": "762cb843",
        "subject": "fix(field-guide): flat-doc JSON corruption + responsive [mobile/tablet] layout",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "1a0d78173720327350a546237980ad50c759740f",
        "short_hash": "1a0d7817",
        "subject": "feat(brand): lucide icon pass + face-only mark, brand watermarks across site",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "c6dc217dc560ce41ebc643b50f14eb9d96274631",
        "short_hash": "c6dc217d",
        "subject": "feat(arch): wide-screen lane expansion + left-aligned navigation",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "83bf4660607066165158fcc85a9853bef85e3952",
        "short_hash": "83bf4660",
        "subject": "feat(pages): interactive architecture board - L-R flow, drilldown sheets, live inventory",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "a8a4b794ab184c5057670f6084781a2af1d8440b",
        "short_hash": "a8a4b794",
        "subject": "feat(brand): site-wide rebrand to periwinkle/cyan/mint design system",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "0cbf521fceed2aecce7ee05790832b48bdc4b276",
        "short_hash": "0cbf521f",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-17 12:00)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "157cd7c1f54c3d79b0d774d977917103c7628f62",
        "short_hash": "157cd7c1",
        "subject": "feat(pages): architecture diagram page - self-healing pipeline, Apple-internal-training treatment",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "d7e8d35d8ae38e41ab68d91bdbecc6aa9193afab",
        "short_hash": "d7e8d35d",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-17 10:48)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "04b6b60903d996269c5308cf9aec778f406a4f91",
        "short_hash": "04b6b609",
        "subject": "docs(sovereignty): profile backup now automated; curation cadence + restore path",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "f798c291bf1e631dc541983c43e0434c17061e79",
        "short_hash": "f798c291",
        "subject": "ci(pages): drop configure-pages (codeload 429 flake) - upload/deploy suffice",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "6b37d1dccf81c9b52b45d059549d43abaeaa747b",
        "short_hash": "6b37d1dc",
        "subject": "docs(field-guide+observatory): regenerate + post-update leftovers (2026-08-17 10:29)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "ca3c5c519d59cdc335ec6539657c2d486f8e1352",
        "short_hash": "ca3c5c51",
        "subject": "feat(pages): evergreen release observatory auto-regenerated by update pipeline",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "7e76b0975d5c0dde5e70c30943ff4f3a7c5b1d43",
        "short_hash": "7e76b097",
        "subject": "docs(sovereignty): update Pages URL structure for 4-section site",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "574222a2b0e03ce6e57facce5be9becebff642fd",
        "short_hash": "574222a2",
        "subject": "docs(pages): public site hub + release observatory for t-granlund fork Pages",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "920e74ad3db07f8900df44574e12f76d7fb97694",
        "short_hash": "920e74ad",
        "subject": "docs(field-guide): regenerate + post-update leftovers (2026-08-17 10:01)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "8b8f443c79131a1b58d71d67f965b105445d1f45",
        "short_hash": "8b8f443c",
        "subject": "docs(field-guide): regenerate + post-update leftovers (2026-08-17 09:59)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "6f7241534e52e95eaca21f70272502ce555c2da2",
        "short_hash": "6f724153",
        "subject": "docs(field-guide): regenerate + post-update leftovers (2026-08-17 09:58)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "565dd7e82033b69bbbb2a98fdd1114c586da38ca",
        "short_hash": "565dd7e8",
        "subject": "chore: auto-commit pre-update leftovers (2026-08-17 09:58)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "2927131211a9abaa43b06ce5531c5f171430331f",
        "short_hash": "29271312",
        "subject": "docs(sovereignty): reflect auto-sync updater + Pages field guide",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "d081f4481115d59a2e0106debcef0553a3db0868",
        "short_hash": "d081f448",
        "subject": "docs(field-guide): regenerate + post-update leftovers (2026-08-17 09:31)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "aaf68d8c7468d9e9b5343720f04250726df6859d",
        "short_hash": "aaf68d8c",
        "subject": "docs(field-guide): regenerate + post-update leftovers (2026-08-17 09:28)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "a647549a9fecc942c255283c36ceba210729a9fb",
        "short_hash": "a647549a",
        "subject": "docs(field-guide): regenerate + post-update leftovers (2026-08-17 09:28)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "a3db8c72bc465c1d135db42c4485f46654c8df64",
        "short_hash": "a3db8c72",
        "subject": "ci(pages): deploy field guide to GitHub Pages on docs changes",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "8ef4466b5aae8f5c0030566ba505544dd0c78641",
        "short_hash": "8ef4466b",
        "subject": "docs(field-guide): regenerate after upstream sync (2026-08-17)",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "93947d1cca577d9cdbbccbf4b375649e9d8cf8cc",
        "short_hash": "93947d1c",
        "subject": "docs: sovereignty playbook, weekly features page, changelog dir",
        "author": "Tyler Granlund",
        "date": "2026-08-17"
      },
      {
        "hash": "2890c1851d9dde3cb0aa758ce7188f8a24436d84",
        "short_hash": "2890c185",
        "subject": "docs(field-guide): regenerate with corrected skill labels",
        "author": "Tyler Granlund",
        "date": "2026-08-16"
      },
      {
        "hash": "1de4c0a7b420cf0d189ab713094f3cf8b13d6d1d",
        "short_hash": "1de4c0a7",
        "subject": "fix(field-guide): correct skill source labels and sanitize paths",
        "author": "Tyler Granlund",
        "date": "2026-08-16"
      },
      {
        "hash": "a8d9af404a9dbc3a40f66529f95c133ce57f1940",
        "short_hash": "a8d9af40",
        "subject": "docs(field-guide): regenerate with user plugins + i_have_adhd; app.js tier badges",
        "author": "Tyler Granlund",
        "date": "2026-08-16"
      },
      {
        "hash": "f3f85608d4dfc755a9a4a7f31d0d3c4e22d5a5c9",
        "short_hash": "f3f85608",
        "subject": "docs(field-guide): regenerate after core-plugins package scan support",
        "author": "Tyler Granlund",
        "date": "2026-08-16"
      },
      {
        "hash": "6ee7e37cdaed5d8e1e8f6485b4918cbcef460d43",
        "short_hash": "6ee7e37c",
        "subject": "feat(field-guide): scan installed core-plugins package + user plugins",
        "author": "Tyler Granlund",
        "date": "2026-08-16"
      },
      {
        "hash": "4305a354dc57fe0d83f61476189f00dffe5e01d0",
        "short_hash": "4305a354",
        "subject": "docs: CPU interactive curriculum web app + puppy mark",
        "author": "Tyler Granlund",
        "date": "2026-07-31"
      },
      {
        "hash": "0d0efbad27ba9c9293a3788298cd3910128831cf",
        "short_hash": "0d0efbad",
        "subject": "docs: deck v3 — Acts IX/X, the internal + external university",
        "author": "Tyler Granlund",
        "date": "2026-07-31"
      },
      {
        "hash": "3360b6e774075e489e653ce9a8b447226d9d7e35",
        "short_hash": "3360b6e7",
        "subject": "docs: deck v2.1 — token architecture, component registry, 42-test suite",
        "author": "Tyler Granlund",
        "date": "2026-07-30"
      },
      {
        "hash": "49d49afebc643c61098915726521643327929746",
        "short_hash": "49d49afe",
        "subject": "docs: deck v2 — Cornerstone+ design system, Fireship beat, fact-check pass",
        "author": "Tyler Granlund",
        "date": "2026-07-30"
      },
      {
        "hash": "e2a4ac48d44e7d94b1ef622518732d429a8bc235",
        "short_hash": "e2a4ac48",
        "subject": "docs: The Great Adpuppytion — Code-Puppy University founding deck",
        "author": "Tyler Granlund",
        "date": "2026-07-30"
      },
      {
        "hash": "9f0ba655eb3456f36a801ee8f976d42388be180c",
        "short_hash": "9f0ba655",
        "subject": "feat(field-guide): recreate changelog.py source from pycache analysis",
        "author": "Tyler Granlund",
        "date": "2026-08-13"
      },
      {
        "hash": "0f33ef03b2d84aee15001c90ae4f74b57ad14116",
        "short_hash": "0f33ef03",
        "subject": "feat(field-guide): deeper plugin/tool extraction + skills + SDLC lifecycle",
        "author": "Tyler Granlund",
        "date": "2026-08-13"
      },
      {
        "hash": "817455926afb15eb5d97e45d69137af7f1a18fc3",
        "short_hash": "81745592",
        "subject": "fix(field-guide): flat HTML no longer wipes DATA.plugins via JS escape reinterpretation",
        "author": "Tyler Granlund",
        "date": "2026-08-10"
      },
      {
        "hash": "91c99c4e1dfdc5e9a1afa2e5f3f11bb6ba4b1310",
        "short_hash": "91c99c4e",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-31"
      },
      {
        "hash": "2b3042ad4e80521ddce3648e0325125dec7bd2b3",
        "short_hash": "2b3042ad",
        "subject": "Fix AttributeError on newer mcp SDKs that renamed McpError to MCPError",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-31"
      },
      {
        "hash": "6f0c9af9a76e7d7e52bbb24353d3ab12f3f0a36e",
        "short_hash": "6f0c9af9",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-31"
      },
      {
        "hash": "5226fefab1d84d42439d590cdd846dc8ab2f9ac8",
        "short_hash": "5226fefa",
        "subject": "fix: default agency level to high (#898)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-31"
      },
      {
        "hash": "8442e7f144fbbb62f7bfa49ceba6ab030f85ac7f",
        "short_hash": "8442e7f1",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-31"
      },
      {
        "hash": "55f6311e5de950b4e0512c3de3a270cb7f9e1fe3",
        "short_hash": "55f6311e",
        "subject": "feat: make agency level a togglable setting (#897)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-31"
      },
      {
        "hash": "8f9504a0dd11f75199fe2465a892630e5550f5b9",
        "short_hash": "8f9504a0",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-31"
      },
      {
        "hash": "3b020d400b8f22e4ff6e5013759366e61497fc9f",
        "short_hash": "3b020d40",
        "subject": "chore: retire the shell_safety loader special case and safety_permission_level key (#895)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-31"
      },
      {
        "hash": "de7657eb09d0a01e09cde8632e4db5abb47798ac",
        "short_hash": "de7657eb",
        "subject": "feat(agents): add transform_mcp_toolsets extension seam to BaseAgent (#896)",
        "author": "Demise",
        "date": "2026-08-31"
      },
      {
        "hash": "582b4346128a48b7cd50351740e652c550eedcd0",
        "short_hash": "582b4346",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-30"
      },
      {
        "hash": "4597b01ea943d8eed49a4a8d73727a81772090fb",
        "short_hash": "4597b01e",
        "subject": "test: read block-reason helpers from their own module (#894)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-30"
      },
      {
        "hash": "8f3969633ec124e91fdb11f8035f22979d2a9b63",
        "short_hash": "8f396963",
        "subject": "fix: make private inference provider-safe",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "85bed47f5c3e2fbf0cd93931c5f32ecbec3454ff",
        "short_hash": "85bed47f",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-29"
      },
      {
        "hash": "db6d4d80365f0d50371ded1112a84d5bea90ac7f",
        "short_hash": "db6d4d80",
        "subject": "fix: disable chat template thinking for private inference",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "cbcb2cc468c74f146bf48a6e1cb8c264c3e6056f",
        "short_hash": "cbcb2cc4",
        "subject": "feat: add private structured inference runner",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "c2a528c4f2748c6b52f9aba251625a135b910e60",
        "short_hash": "c2a528c4",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-29"
      },
      {
        "hash": "83cf6700155681d2c9a81b917fd8db6c45e73dd0",
        "short_hash": "83cf6700",
        "subject": "fix: default shell safety permission to high",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "583dfbf689b0037cc37a5d60be5d3d2cc2cb9033",
        "short_hash": "583dfbf6",
        "subject": "fix: require autonomous completion of requested tasks",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "45738d69ce487903bc9b7a5cd5eba01d29634ee2",
        "short_hash": "45738d69",
        "subject": "fix: repair malformed editor args before tool callbacks",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "abadd01db64b904a22f442e94a228aca3ea8c520",
        "short_hash": "abadd01d",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-29"
      },
      {
        "hash": "b7381023ae6a995f2c2eb4f5c340d4f54c58637a",
        "short_hash": "b7381023",
        "subject": "feat: keep waiting for gating background work (#892)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "627da2c783c97704462e8e7be9da80af04364dfa",
        "short_hash": "627da2c7",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-29"
      },
      {
        "hash": "ca3708ed3f94bc8b5eb0ba6488bb2db478fffed4",
        "short_hash": "ca3708ed",
        "subject": "chore: bump core plugins to 0.0.34 (#891)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "4eafb232917049d9790ee3c593c1357614eac57c",
        "short_hash": "4eafb232",
        "subject": "chore: bump core plugins to 0.0.32 (#890)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "5493e699f9e8f647e1d591a25fae40c61d4dea7d",
        "short_hash": "5493e699",
        "subject": "feat: configure auto-continue classifier model (#889)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "9360913ec8ccbf5409e48a9ee7836cabbd8da7e1",
        "short_hash": "9360913e",
        "subject": "chore: bump core plugins to 0.0.31 (#888)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "eab9708f7377ea2fef6d47e827794f5d305ed378",
        "short_hash": "eab9708f",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-29"
      },
      {
        "hash": "7ab955333d46a616336e3ea28b0a5ad6f2474ed7",
        "short_hash": "7ab95533",
        "subject": "Merge pull request #887 from mpfaffenberger/fix/file-tools-sibling-paths",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "456a3bfa4511088411a6ba58c751d8ae478b1872",
        "short_hash": "456a3bfa",
        "subject": "fix: allow apply_patch outside working directory",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "f6abad5a46661480d3eaa8c4046eb766e5aa8f3e",
        "short_hash": "f6abad5a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-29"
      },
      {
        "hash": "44bb5395ecefe75a1806cf546a9206ff43d20808",
        "short_hash": "44bb5395",
        "subject": "Merge pull request #880 from breedx/fix/mcp-connector-degrade",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "ee742a89ec1d48f5bcba46480446e6e76e7606f4",
        "short_hash": "ee742a89",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-29"
      },
      {
        "hash": "fdf703d17fde4f0249192795f3ff1b5dde747d06",
        "short_hash": "fdf703d1",
        "subject": "Merge pull request #855 from phanisaimunipalli/history-merge-repeated-prompt",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "d8b9e7a86bbcf3372b174de188a0b6a3ab1ee602",
        "short_hash": "d8b9e7a8",
        "subject": "Merge pull request #862 from thomwebb/feat/i18n-extract-agent-manager",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "c88a235a9927a9d508a4574af490f381602d0923",
        "short_hash": "c88a235a",
        "subject": "Merge pull request #878 from breedx/fix/mcp-tool-failure-not-fatal",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "601dc9a84535a6954d685d94e327240905f97376",
        "short_hash": "601dc9a8",
        "subject": "Merge pull request #884 from mpfaffenberger/feature/fork-panel-label",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-29"
      },
      {
        "hash": "4839bde2bbf86bc77a0b012faa6cb3ccc4567973",
        "short_hash": "4839bde2",
        "subject": "Merge remote-tracking branch 'origin/main' into feature/fork-panel-label",
        "author": "Wes Blakemore",
        "date": "2026-08-28"
      },
      {
        "hash": "ff6ca4e429fb5840d775f3dd0b1aef34b7867216",
        "short_hash": "ff6ca4e4",
        "subject": "review fixups: address puppy-review (claude-5-opus) nits on is_fork",
        "author": "Wes Blakemore",
        "date": "2026-08-28"
      },
      {
        "hash": "a0f7f3ea6bc459bb29e0c9c5608a97d63a3b1c0e",
        "short_hash": "a0f7f3ea",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-28"
      },
      {
        "hash": "fa5f6fd0cea4733b1beaa467080ecd26df2c479f",
        "short_hash": "fa5f6fd0",
        "subject": "Merge pull request #883 from mpfaffenberger/fix/ripgrep-grep-tool",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-28"
      },
      {
        "hash": "243332729391421d68c649ddc50613fd2819abc9",
        "short_hash": "24333272",
        "subject": "fix(tools): match grep/list ignore patterns relative to the search root",
        "author": "mpfaffenberger",
        "date": "2026-08-28"
      },
      {
        "hash": "45882f0821677452964f14e759371030935e9eb4",
        "short_hash": "45882f08",
        "subject": "fix(mcp): a failing MCP tool degrades the turn, never kills the session",
        "author": "breedx",
        "date": "2026-08-28"
      },
      {
        "hash": "6998d236e851d4c32d3101f231007a9c38d1dcd8",
        "short_hash": "6998d236",
        "subject": "fix(mcp): an unreachable HTTP connector degrades the turn, never ends it",
        "author": "breedx",
        "date": "2026-08-28"
      },
      {
        "hash": "0df573ead2517472d43ed4b163f52f209fe21432",
        "short_hash": "0df573ea",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-28"
      },
      {
        "hash": "524fa464f103a83484041ed7f828f4dec273985a",
        "short_hash": "524fa464",
        "subject": "Merge remote-tracking branch 'origin/main' into feature/fork-panel-label",
        "author": "Wes Blakemore",
        "date": "2026-08-28"
      },
      {
        "hash": "6b0bb47b593e68a6c7a31615a51d380207af6364",
        "short_hash": "6b0bb47b",
        "subject": "Merge pull request #846 from dmontroy/acp-fix",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-28"
      },
      {
        "hash": "1176e6d23b6c0fb11b063545333aac76e7aa835d",
        "short_hash": "1176e6d2",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-28"
      },
      {
        "hash": "f05f2a6ac5adfd6419798ff002ea07215536e28f",
        "short_hash": "f05f2a6a",
        "subject": "Merge remote-tracking branch 'origin/main' into feature/fork-panel-label",
        "author": "Wes Blakemore",
        "date": "2026-08-28"
      },
      {
        "hash": "774e4f59aa1e849014d1a7ef9ed6c50ae76a9899",
        "short_hash": "774e4f59",
        "subject": "Merge pull request #865 from cloverinternational/feature/codex-apply-patch",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-28"
      },
      {
        "hash": "64d9e6c465b8375d0a4d7847b67f044b263e3b73",
        "short_hash": "64d9e6c4",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-28"
      },
      {
        "hash": "3ea673fa5d047dfb570e0eaab40c4bb3c3f9ef99",
        "short_hash": "3ea673fa",
        "subject": "Merge pull request #877 from mpfaffenberger/fix/httpx2-provider-clients",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-28"
      },
      {
        "hash": "35c457b95040b89a902aa0147ca99c048a4c4542",
        "short_hash": "35c457b9",
        "subject": "fix(http): hand pydantic-ai providers httpx2 clients",
        "author": "mpfaffenberger",
        "date": "2026-08-28"
      },
      {
        "hash": "b7fa24b4d6937313e4febcd8794fe1cd01435b63",
        "short_hash": "b7fa24b4",
        "subject": "feat: add is_fork flag to distinguish /fork banner from invoke_agent",
        "author": "Wes Blakemore",
        "date": "2026-08-28"
      },
      {
        "hash": "859953c588bc7b956c2341c62a3a830fae54b8b9",
        "short_hash": "859953c5",
        "subject": "fix: initialize locale after argument parsing",
        "author": "TJ Webb",
        "date": "2026-08-27"
      },
      {
        "hash": "c74a20de9e1da2ffe7386027bb0a5f52b347489e",
        "short_hash": "c74a20de",
        "subject": "merge upstream main into agent manager i18n",
        "author": "TJ Webb",
        "date": "2026-08-27"
      },
      {
        "hash": "1e38a3840d33411b24846eab32ab1745a673a257",
        "short_hash": "1e38a384",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-27"
      },
      {
        "hash": "78c6c107028ef50e80fe86d2c2b401c9310b4796",
        "short_hash": "78c6c107",
        "subject": "Merge pull request #859 from StarsExpress/perf-reduce-cpu-churn",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-27"
      },
      {
        "hash": "30e619db6d700c3fc01c3c2d362d3bd448302a5b",
        "short_hash": "30e619db",
        "subject": "Merge pull request #811 from StarsExpress/refactor-message-type-inference",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-27"
      },
      {
        "hash": "4c8b409a0899350abbe5c228cfccb0ff68b95828",
        "short_hash": "4c8b409a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-27"
      },
      {
        "hash": "904c977a0fe6ccaf2697c4b818f2c06ea9840ea7",
        "short_hash": "904c977a",
        "subject": "Fix Windows lock ordering and config decode fallback (#874)",
        "author": "Bill Kramme",
        "date": "2026-08-27"
      },
      {
        "hash": "9e15bb711988af52c3c1919e33b1b36b39c8bffe",
        "short_hash": "9e15bb71",
        "subject": "Merge remote-tracking branch 'origin/main' into feature/codex-apply-patch",
        "author": "rinadelph",
        "date": "2026-08-27"
      },
      {
        "hash": "efa3ac7a36de6feca77d50535b183692ecd8c072",
        "short_hash": "efa3ac7a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-27"
      },
      {
        "hash": "e9b9d1e5462d4e1bc21efa5511f41cb0af49aeac",
        "short_hash": "e9b9d1e5",
        "subject": "refactor: expose engine-truthful replacement API for previews",
        "author": "rinadelph",
        "date": "2026-08-27"
      },
      {
        "hash": "c29dd56cacc0ba73c5967f35b6c17e2594c0d82a",
        "short_hash": "c29dd56c",
        "subject": "Merge pull request #870 from thomwebb/fix/compact-session-persistence",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-27"
      },
      {
        "hash": "385d540d44dd32e696ecb33b1c211cd5327e5eb9",
        "short_hash": "385d540d",
        "subject": "feat: align edit tool with Claude Code Edit semantics",
        "author": "rinadelph",
        "date": "2026-08-27"
      },
      {
        "hash": "2864e80c34be3ca3edcd10a4c787cfbd75f453dc",
        "short_hash": "2864e80c",
        "subject": "fix: match Codex apply_patch semantics 1:1",
        "author": "rinadelph",
        "date": "2026-08-27"
      },
      {
        "hash": "7f761e0c78b0e3c06d2f72cc48a0126906363a00",
        "short_hash": "7f761e0c",
        "subject": "style: format provider edit tools",
        "author": "rinadelph",
        "date": "2026-08-27"
      },
      {
        "hash": "1bfe221d2f7aa8aba32f30b050c2a42b3c073c39",
        "short_hash": "1bfe221d",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-27"
      },
      {
        "hash": "d36009a014177e8738da545674f77b10173cf09d",
        "short_hash": "d36009a0",
        "subject": "fix: satisfy provider tool quality checks",
        "author": "rinadelph",
        "date": "2026-08-27"
      },
      {
        "hash": "d93da2cae99511006c0c517a70911b0966696481",
        "short_hash": "d93da2ca",
        "subject": "Fix Windows backspace repeat hitching",
        "author": "mpfaffenberger",
        "date": "2026-08-27"
      },
      {
        "hash": "a4be31454abbcf4e78c7bc233fbce949211ab864",
        "short_hash": "a4be3145",
        "subject": "Require compaction session persistence",
        "author": "TJ Webb",
        "date": "2026-08-26"
      },
      {
        "hash": "4639688f1cb6e5f12c9c19dcefc1773c6e61aa97",
        "short_hash": "4639688f",
        "subject": "Persist history after manual compaction",
        "author": "TJ Webb",
        "date": "2026-08-26"
      },
      {
        "hash": "f7f930344c5ab126fff2901da166b0444d4dc290",
        "short_hash": "f7f93034",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-26"
      },
      {
        "hash": "62f6dc1185abb2585c93aa0d6c615f9eca37f42c",
        "short_hash": "62f6dc11",
        "subject": "Remove minimum splash screen duration",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-26"
      },
      {
        "hash": "463c892932018f26561fcfd7cc8ff320bc5322d6",
        "short_hash": "463c8929",
        "subject": "Migrate ChatGPT Codex client to httpx2",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-26"
      },
      {
        "hash": "a5c34858a4f49d7c7ea877fac9169921dbe73dfe",
        "short_hash": "a5c34858",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-26"
      },
      {
        "hash": "217cbbd833b2d9027ec30f8b18cc20c33ab41d9c",
        "short_hash": "217cbbd8",
        "subject": "Support per-agent model setting overrides (#812)",
        "author": "TJ",
        "date": "2026-08-26"
      },
      {
        "hash": "14b655c95876fa0b205731f9018e8bd909c1097f",
        "short_hash": "14b655c9",
        "subject": "Merge pull request #853 from jmdots/fix/reasoning-api-746",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-26"
      },
      {
        "hash": "b21b47197b5c7f69d1dc49bf55471c637ee095bc",
        "short_hash": "b21b4719",
        "subject": "Review follow-ups: reasoning config by underlying name, merge streamed output items",
        "author": "mpfaffenberger",
        "date": "2026-08-26"
      },
      {
        "hash": "bde6d89fa7cf8ecca659cc1ec4ee241d089b1499",
        "short_hash": "bde6d89f",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-26"
      },
      {
        "hash": "481e8b506f68a2f6b432b817e97b8bcf2f3333f6",
        "short_hash": "481e8b50",
        "subject": "Conviction kit for wedged cancellations: SIGUSR2 stack dumps + stress repro",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-26"
      },
      {
        "hash": "84d99a6d93fab30456ec7f032d706ccfdfd7f05b",
        "short_hash": "84d99a6d",
        "subject": "Bump pydantic-ai to 2.35.0; ride the anthropic 1.0 httpx2 migration",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-26"
      },
      {
        "hash": "025f1bd00a05878469596f7dea6ff82a4001420d",
        "short_hash": "025f1bd0",
        "subject": "Zombie cancellations can no longer trap the REPL or the quit paths",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-26"
      },
      {
        "hash": "e93b72775253fcc555fb477fc294a6cb56d1a953",
        "short_hash": "e93b7277",
        "subject": "test: assert translated agent manager text",
        "author": "TJ Webb",
        "date": "2026-08-25"
      },
      {
        "hash": "7fae7b1457bcf68e32a2475eaa3837c092b7a5e9",
        "short_hash": "7fae7b14",
        "subject": "fix: initialize locale before agent messages",
        "author": "TJ Webb",
        "date": "2026-08-25"
      },
      {
        "hash": "9dca5b151589e0ebd73b6d892ba319e386dc560e",
        "short_hash": "9dca5b15",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-25"
      },
      {
        "hash": "c1c4d352714688a9216068e7286c43754ae6fae6",
        "short_hash": "c1c4d352",
        "subject": "Merge pull request #867 from dsfaccini/fix/mcp-registry-sync-plugin-dir-writes",
        "author": "David SF",
        "date": "2026-08-25"
      },
      {
        "hash": "289f90cdd0d2bf1e514b023fd4df4fa936a60d04",
        "short_hash": "289f90cd",
        "subject": "Harden plugin-path guard and skip MCP registry drops on config load failure",
        "author": "David Sanchez",
        "date": "2026-08-25"
      },
      {
        "hash": "e4950cca223dc55fa39a70b5df7fc2d07317eac8",
        "short_hash": "e4950cca",
        "subject": "Keep MCP registry, user plugins, and session unpickle aligned with load rules",
        "author": "David Sanchez",
        "date": "2026-08-25"
      },
      {
        "hash": "59bab217195f0f3f56eedf6167608dfec2a55f06",
        "short_hash": "59bab217",
        "subject": "fix: align apply patch parsing with OpenCode",
        "author": "rinadelph",
        "date": "2026-08-24"
      },
      {
        "hash": "53520c15a4084634cb15299d583baf640a710819",
        "short_hash": "53520c15",
        "subject": "docs: document provider-specific edit tools",
        "author": "rinadelph",
        "date": "2026-08-24"
      },
      {
        "hash": "2e56761ae9b801de2adced313accd0a54a10c83f",
        "short_hash": "2e56761a",
        "subject": "feat: add Codex apply patch tool",
        "author": "rinadelph",
        "date": "2026-08-24"
      },
      {
        "hash": "fbdfe156eb3ab7196d8796967b5be10ce0a51512",
        "short_hash": "fbdfe156",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-24"
      },
      {
        "hash": "e855f97a97ae67b771337798afda829f71dce154",
        "short_hash": "e855f97a",
        "subject": "Pin code-puppy-core-plugins>=0.0.27 for the openrouter_oauth plugin",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "47f175401e6544333b033701a896f6868c4c64f5",
        "short_hash": "47f17540",
        "subject": "Add provider_credential_flow hook: plugins get first crack at missing /add_model credentials",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "7bf786bb3267b74ea54b960fd932e3e81042dd00",
        "short_hash": "7bf786bb",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-24"
      },
      {
        "hash": "38849ba69443a421aee26d736c2bd3a865b4055e",
        "short_hash": "38849ba6",
        "subject": "Total prompt_toolkit extermination: delete the shim, purge the venv",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "7868d6ab74b7b7218bf3ed62923852ca08170cca",
        "short_hash": "7868d6ab",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-24"
      },
      {
        "hash": "83e17fbc49fb87d951fedd9de3035f2c003fd923",
        "short_hash": "83e17fbc",
        "subject": "Slay the boss: retire the classic prompt_toolkit input path",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "e8bf428be0a07a1e523cbca08046f05a5d04bb02",
        "short_hash": "e8bf428b",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-24"
      },
      {
        "hash": "9e3591e2ec5428f7f256628117e57449176c2115",
        "short_hash": "9e3591e2",
        "subject": "Port MCP custom-server form and install menu to termflow",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "9362ffba2a0e9ef42a2b8381b451248f1ec0e059",
        "short_hash": "9362ffba",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-24"
      },
      {
        "hash": "972626bb15ee7e01c1f1b7bbc043489f879fe368",
        "short_hash": "972626bb",
        "subject": "Port /set picker and UC tool browser to termflow",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "6918c6342965c42b93d9372bbfc51b6eff492647",
        "short_hash": "6918c634",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-24"
      },
      {
        "hash": "bb7b52affb7cb154fa673bc3b3283da48497a74d",
        "short_hash": "bb7b52af",
        "subject": "Port onboarding wizard to termflow",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "50fbf1275008dad0c4d233fc0ed0d5ae1e029ee6",
        "short_hash": "50fbf127",
        "subject": "Help overlay on termflow Pager; pin termflow-md>=0.8.0",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "9285b2316270a9a3f909669f503d5332b232e4d8",
        "short_hash": "9285b231",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-24"
      },
      {
        "hash": "9a1a23994a5ad5c276b136ebf3f362d9b3db3580",
        "short_hash": "9a1a2399",
        "subject": "style: format agent manager i18n changes",
        "author": "TJ Webb",
        "date": "2026-08-24"
      },
      {
        "hash": "81f8a7da50334b40b59c5a60fe38299823fbec62",
        "short_hash": "81f8a7da",
        "subject": "Port ask_user_question TUI to termflow",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "5100fd6122f18039af12ad93c60246afa46be930",
        "short_hash": "5100fd61",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-24"
      },
      {
        "hash": "d4732901ed9852a16d133d86f5c5e504d6143c87",
        "short_hash": "d4732901",
        "subject": "Murder the twins: add_model_menu and model_settings_menu on termflow",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "361e95ae2122a32fa16e7d086f6dc3d6e168b68e",
        "short_hash": "361e95ae",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-24"
      },
      {
        "hash": "0defd49603674a0097d869656698d3a5a3c78483",
        "short_hash": "0defd496",
        "subject": "feat(i18n): extract agent manager messages",
        "author": "TJ Webb",
        "date": "2026-08-24"
      },
      {
        "hash": "5ce787daca5ed824cf327a42fd328d381b3563fd",
        "short_hash": "5ce787da",
        "subject": "Merge leading system messages on strict OpenAI-compatible backends (#860)",
        "author": "TJ",
        "date": "2026-08-24"
      },
      {
        "hash": "980d66d5b1d744d03b9fe7882a0a35c16408fc47",
        "short_hash": "980d66d5",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-24"
      },
      {
        "hash": "71ffed158e64d5a1f82b2b84bc7172faaaa5b78c",
        "short_hash": "71ffed15",
        "subject": "Interrogate the TUI kill list: two targets down without ports",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "e697252a1c72606463fb3b8ca0e2046d61308464",
        "short_hash": "e697252a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-24"
      },
      {
        "hash": "4d269ed2491f8b829e3885e8788cc7d6bdb53bda",
        "short_hash": "4d269ed2",
        "subject": "Charge image tokens by area instead of digest length (#783) (#854)",
        "author": "Phani Sai Ram M",
        "date": "2026-08-24"
      },
      {
        "hash": "73f167c84a2ae7ae193a71f1d36016037b442731",
        "short_hash": "73f167c8",
        "subject": "Two-phase master/detail flow on phone-sized terminals; termflow-md >= 0.6.0",
        "author": "mpfaffenberger",
        "date": "2026-08-24"
      },
      {
        "hash": "956418782d7aee9cb3cba6bc7d7b471c038f4a41",
        "short_hash": "95641878",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-23"
      },
      {
        "hash": "017f8d4b26833c546afde1d3860613e2c33446f5",
        "short_hash": "017f8d4b",
        "subject": "One column of right padding in the session browser; termflow-md >= 0.5.1",
        "author": "mpfaffenberger",
        "date": "2026-08-23"
      },
      {
        "hash": "d25b480b53c9a0ca8471165a7ef7f736772b74f3",
        "short_hash": "d25b480b",
        "subject": "Resize detection for the session browser; termflow-md >= 0.5.0",
        "author": "mpfaffenberger",
        "date": "2026-08-23"
      },
      {
        "hash": "a3b85f455ca1c41c3b32ca2ea461f73db61aa88c",
        "short_hash": "a3b85f45",
        "subject": "Added exponential backoff for idles.",
        "author": "Jack Yao",
        "date": "2026-08-23"
      },
      {
        "hash": "226b05b6fdb7a5000ef531645c3cb47c5d1838ab",
        "short_hash": "226b05b6",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-23"
      },
      {
        "hash": "a6e21d6d0c447c4688c093729d9f6c1335997bde",
        "short_hash": "a6e21d6d",
        "subject": "Drop orphaned /colors and /diff i18n keys",
        "author": "mpfaffenberger",
        "date": "2026-08-23"
      },
      {
        "hash": "9eaf5a59ba872e05bd562946569f37946364a2d8",
        "short_hash": "9eaf5a59",
        "subject": "Remove the /colors and /diff TUIs: theming owns those settings",
        "author": "mpfaffenberger",
        "date": "2026-08-23"
      },
      {
        "hash": "d1b5132e3cefdca5739cf06b32f3ffc106596365",
        "short_hash": "d1b5132e",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-23"
      },
      {
        "hash": "dce98fb08da32c24c05da0f0fd37251d265d08ca",
        "short_hash": "dce98fb0",
        "subject": "Lock code-puppy-core-plugins 0.0.18 (session_namer)",
        "author": "mpfaffenberger",
        "date": "2026-08-23"
      },
      {
        "hash": "694006b98f01669ea445ef253942baf9f7c1bc09",
        "short_hash": "694006b9",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-23"
      },
      {
        "hash": "600334647a672ba0eb00ac722fe3cc1d43517e46",
        "short_hash": "60033464",
        "subject": "Two-pane session browser for /resume with AI-naming hook",
        "author": "mpfaffenberger",
        "date": "2026-08-23"
      },
      {
        "hash": "b19a0bf556e8fba54a6fcfce3f2ac9ec3394b78e",
        "short_hash": "b19a0bf5",
        "subject": "Delegate diff rendering wholesale to termflow 0.3.0",
        "author": "mpfaffenberger",
        "date": "2026-08-23"
      },
      {
        "hash": "4e2ce2775c4aba97f5e6a5beac7d2a48a2b116e4",
        "short_hash": "4e2ce277",
        "subject": "Honor the cursor contract in region teardown/establish and grows",
        "author": "mpfaffenberger",
        "date": "2026-08-23"
      },
      {
        "hash": "3c0a48e736c0f606d5947b0ecdf5e13b34ad6892",
        "short_hash": "3c0a48e7",
        "subject": "Preserve popup slack across same-geometry suspend/resume",
        "author": "mpfaffenberger",
        "date": "2026-08-23"
      },
      {
        "hash": "688d68090395a33f4f5b8e7175333c2d197127af",
        "short_hash": "688d6809",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-23"
      },
      {
        "hash": "0733da003de955816bf8a15e3112ed1f2c0cfecf",
        "short_hash": "0733da00",
        "subject": "Speed up REPL autocomplete with threaded TTL caches",
        "author": "mpfaffenberger",
        "date": "2026-08-23"
      },
      {
        "hash": "01f6b804386fae19bfa9bf7817d5cedf37f01c7f",
        "short_hash": "01f6b804",
        "subject": "Keep a repeated user prompt when the turn is genuinely new (#781)",
        "author": "phanisaimunipalli",
        "date": "2026-08-23"
      },
      {
        "hash": "7e3e2e0aa7458cdc1a9f846a893146d8e3f2a09e",
        "short_hash": "7e3e2e0a",
        "subject": "fix: enable encrypted reasoning replay",
        "author": "Joshua M. Dotson",
        "date": "2026-08-22"
      },
      {
        "hash": "8e81c40ce60ec941c39339ea13ae3148dba96af7",
        "short_hash": "8e81c40c",
        "subject": "fix: retain signed reasoning for tool continuations",
        "author": "Joshua M. Dotson",
        "date": "2026-08-22"
      },
      {
        "hash": "a9d69481d5e99621f5c280c2a0d7380afd6ed920",
        "short_hash": "a9d69481",
        "subject": "fix: preserve streamed reasoning output",
        "author": "Joshua M. Dotson",
        "date": "2026-08-22"
      },
      {
        "hash": "7d7ec6ce39acd9f4959b68bcc9a2034ea6c8716d",
        "short_hash": "7d7ec6ce",
        "subject": "fix: support GPT-5.6 Responses reasoning",
        "author": "Joshua M. Dotson",
        "date": "2026-08-22"
      },
      {
        "hash": "ea0a9b7333ca9acb15ea612a7e192886d9bfdbff",
        "short_hash": "ea0a9b73",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-23"
      },
      {
        "hash": "1614e067f75f67cb010c5b74011f3f6bebca84f9",
        "short_hash": "1614e067",
        "subject": "Add Tab-toggled fullscreen help overlay, trim startup tips (#852)",
        "author": "Andrew Tilson",
        "date": "2026-08-22"
      },
      {
        "hash": "e0fa4ffc0045f60fc7fbb7ea3d05a5fb93b53ec3",
        "short_hash": "e0fa4ffc",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-23"
      },
      {
        "hash": "90ac73c44ad145c86e41ba8bba5f9761a879cbf3",
        "short_hash": "90ac73c4",
        "subject": "Restore resume picker status chrome",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "4042b4ec685247ce219595eb30241450834494fb",
        "short_hash": "4042b4ec",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-23"
      },
      {
        "hash": "458b3ce9a31b4129097d200ac3b3c3c92bf0f76c",
        "short_hash": "458b3ce9",
        "subject": "Color resume picker previews with active theme",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "f04852428efc2f785e209bf40a2b30c22df97da3",
        "short_hash": "f0485242",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-23"
      },
      {
        "hash": "b62ce96cbfde0bd9aa728c6e75355bcdc4233c6b",
        "short_hash": "b62ce96c",
        "subject": "Port resume session picker to termflow",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "abcb51cb18264e87b33ab1dff41a35a1e96a9e42",
        "short_hash": "abcb51cb",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-23"
      },
      {
        "hash": "7280aca034897e09df70829245226ae756570449",
        "short_hash": "7280aca0",
        "subject": "Flush paused emits after the run UI is restored",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "29889d39af7feb33318d50d13e5f039d8622e5d1",
        "short_hash": "29889d39",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-22"
      },
      {
        "hash": "c522bb1b2c0241e56c7520bf977d6c060d943f96",
        "short_hash": "c522bb1b",
        "subject": "chore: bump core-plugins to 0.0.16 (picker emoji removal + themed preview bg)",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "a41fa3200e6bcf3d01f3a6bbaa6a443e5046bda8",
        "short_hash": "a41fa320",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-22"
      },
      {
        "hash": "08d9cae3f191f66432c8ec335df1da445fbc394c",
        "short_hash": "08d9cae3",
        "subject": "Bump termflow 0.2.6 + core-plugins 0.0.15 (auto page size)",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "23123f171003dec91585c3e2d98a9c35f16d5c29",
        "short_hash": "23123f17",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-22"
      },
      {
        "hash": "83f4b89bc55ef0173042e45e4a9619268479a7df",
        "short_hash": "83f4b89b",
        "subject": "chore: bump termflow-md to 0.2.5 (frame height clamp fix)",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "0752c70a2588dfb6d96d33d3149f909aec60e161",
        "short_hash": "0752c70a",
        "subject": "Update theme plugin tests for core-plugins 0.0.14 picker",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "e4084242504bbb5f062d8c30b84cb342603c7925",
        "short_hash": "e4084242",
        "subject": "Theme the termflow menus from the active palette",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "5ab47fe91b93b00f7b3e66fd00ac92e1b7ce707d",
        "short_hash": "5ab47fe9",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-22"
      },
      {
        "hash": "149faefe958b27abcf641b0ab498dc411b51ba41",
        "short_hash": "149faefe",
        "subject": "Enforce Claude Code system-prompt fingerprint at the OAuth transport",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "59acbabe4bafe609f1971593e29b20f9d736ec85",
        "short_hash": "59acbabe",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-22"
      },
      {
        "hash": "e269c2c257a8ea4771c3f326a9e7d513fe542e6a",
        "short_hash": "e269c2c2",
        "subject": "Stop emit_* output flickering behind TUI menus",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "21a8e690ea0d96ff01657964449f645724280b62",
        "short_hash": "21a8e690",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-22"
      },
      {
        "hash": "6604015691c075bc1de28e4c1f0ed530721961ea",
        "short_hash": "66040156",
        "subject": "chore: bump termflow-md to 0.2.2 (arrow-key hotfix)",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "cbd35d137c395269d36a330fd4b67b139a08d90f",
        "short_hash": "cbd35d13",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-22"
      },
      {
        "hash": "feb2ffacdd23d968ffb3be2750fd33e62742e1ec",
        "short_hash": "feb2ffac",
        "subject": "Port smooth streaming + TUI pickers onto termflow 0.2.1 (#851)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "ed590e82fdee13c04863bb1c44dcc591e5d46b3f",
        "short_hash": "ed590e82",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-22"
      },
      {
        "hash": "ce2e20a89789aaa25d44053a7d8d693634a384a5",
        "short_hash": "ce2e20a8",
        "subject": "fix: compaction summarizer dying past 50 requests (harness#528)",
        "author": "mpfaffenberger",
        "date": "2026-08-22"
      },
      {
        "hash": "4cee549bce5197daa770e58d7709b133848cfe03",
        "short_hash": "4cee549b",
        "subject": "Reformat according to ruff.",
        "author": "Daniel Montroy",
        "date": "2026-08-21"
      },
      {
        "hash": "0c17570442744b813695fc91419e93088c149047",
        "short_hash": "0c175704",
        "subject": "Fix deadlock warning with delete operations.",
        "author": "Daniel Montroy",
        "date": "2026-08-21"
      },
      {
        "hash": "58f2424dd661d13326dd827ef80777102a0afb1d",
        "short_hash": "58f2424d",
        "subject": "Tweaks around tool calls and thread handling to fix ACP.",
        "author": "Daniel Montroy",
        "date": "2026-08-21"
      },
      {
        "hash": "a87f1fdce5927106a7a1225c41ca8ae7ef7420d9",
        "short_hash": "a87f1fdc",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-21"
      },
      {
        "hash": "017db50260ac10c3594a497ad31cd0e84f6a44bb",
        "short_hash": "017db502",
        "subject": "test: match quiet version check behavior (#837)",
        "author": "TJ",
        "date": "2026-08-21"
      },
      {
        "hash": "055c477d114e219526de7a025718762224a76585",
        "short_hash": "055c477d",
        "subject": "feat(cli): add --port-base to shift port-probe range (#635)",
        "author": "finklang",
        "date": "2026-08-21"
      },
      {
        "hash": "80ea63b5de34e01964f66ffa13c88a51b570c532",
        "short_hash": "80ea63b5",
        "subject": "chore: bump code-puppy-core-plugins to 0.0.13 (adds logfire_sessions)",
        "author": "mpfaffenberger",
        "date": "2026-08-21"
      },
      {
        "hash": "fd7ed1e4073f45f6738b4ac02e526b651b296b70",
        "short_hash": "fd7ed1e4",
        "subject": "chore: silence 'you're on the latest version' startup message",
        "author": "mpfaffenberger",
        "date": "2026-08-21"
      },
      {
        "hash": "a9a9f6dbb55123c34b6a2f6b110000182ccbcc27",
        "short_hash": "a9a9f6db",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-21"
      },
      {
        "hash": "d145dfc2e90c2ee35996148c1dd63c8323ed2da2",
        "short_hash": "d145dfc2",
        "subject": "Merge pull request #826 from mpfaffenberger/feat/double-ctrlc-exit",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-21"
      },
      {
        "hash": "b6b336906293e52533c041f794c789f2ee1e017a",
        "short_hash": "b6b33690",
        "subject": "Merge pull request #827 from mpfaffenberger/emit-logfire-cancellation",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-21"
      },
      {
        "hash": "0e16206f2f8df81859c070600e5c3c04b8685577",
        "short_hash": "0e16206f",
        "subject": "Link cancellation event to agent trace context",
        "author": "mpfaffenberger",
        "date": "2026-08-21"
      },
      {
        "hash": "4c808fb144b3e0d3e99a802dbb26d2cbef7d97c7",
        "short_hash": "4c808fb1",
        "subject": "Emit cancellation as a Logfire warning",
        "author": "mpfaffenberger",
        "date": "2026-08-21"
      },
      {
        "hash": "6c897fec5066a4aa2a07d380ea031f64f98029eb",
        "short_hash": "6c897fec",
        "subject": "Emit Logfire event when agent run is cancelled",
        "author": "mpfaffenberger",
        "date": "2026-08-21"
      },
      {
        "hash": "826ac4a94523e20b170e36df65dafdcc76a688a6",
        "short_hash": "826ac4a9",
        "subject": "Double Ctrl+C at the idle prompt quits like Ctrl+D",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "e88d65519705b8049176d5e94a26c4e5f15bf5e7",
        "short_hash": "e88d6551",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-21"
      },
      {
        "hash": "46f0aec8df8db688cd120b07c4700eca3fa7097c",
        "short_hash": "46f0aec8",
        "subject": "Merge pull request #825 from kevinMEH/feat/transform-model-messages",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-21"
      },
      {
        "hash": "a7e2d1826c33defce7054cf8ef40a694bb2a31cb",
        "short_hash": "a7e2d182",
        "subject": "feat: add model message transform callback",
        "author": "kevinMEH",
        "date": "2026-08-21"
      },
      {
        "hash": "591959fb423d7686a832421fc1af3bc7c041405f",
        "short_hash": "591959fb",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-20"
      },
      {
        "hash": "64fca8ddccdfe0ac165c51c51de0390f1fe66a6f",
        "short_hash": "64fca8dd",
        "subject": "Require code-puppy-core-plugins >=0.0.12 for the Logfire OAuth plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "780880fb1c0021581610977183d9cb4b95acc75d",
        "short_hash": "780880fb",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-20"
      },
      {
        "hash": "9dc9d9c7e7969963a2332f9924a3c23426f16600",
        "short_hash": "9dc9d9c7",
        "subject": "Merge pull request #816 from mpfaffenberger/fix/logfire-agent-span-names",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "f355dcadac51d00601d38e5fe2c5d4270db364f9",
        "short_hash": "f355dcad",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-20"
      },
      {
        "hash": "4bb6060e1ca4123bb563fc29fb76e8c21a6f656f",
        "short_hash": "4bb6060e",
        "subject": "feat: splash text is now CODE PUPPY / PUP instead of Powered by Pydantic",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "7d5ed7a1b507f489297c9f8745147812eda8e728",
        "short_hash": "7d5ed7a1",
        "subject": "feat: full-screen centered splash + width-aware startup banner",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "aa9ff2f3d83e8d5fce063a2091ed2af26ec587be",
        "short_hash": "aa9ff2f3",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-20"
      },
      {
        "hash": "af10a6f1ab220175fd6d634d1f1450d74973cdac",
        "short_hash": "af10a6f1",
        "subject": "Merge remote-tracking branch 'origin/main' into fix/anthropic-http-client",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "8e6d8b96bff9de01d1bedd468f3d65101d057f19",
        "short_hash": "8e6d8b96",
        "subject": "fix: constrain Anthropic to compatible HTTP client",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "0dd42a93b1da49dc1329efa6423b34023cc09b13",
        "short_hash": "0dd42a93",
        "subject": "Merge pull request #818 from kvandre12-commits/assist/pr-760-refresh",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "41cb30bb1bac5a1c73c49ef798ceefc2d3f45064",
        "short_hash": "41cb30bb",
        "subject": "Merge pull request #821 from kvandre12-commits/assist/pr-709-refresh",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "54fe4cd9db989b1de9b59be25039697e1facdf89",
        "short_hash": "54fe4cd9",
        "subject": "feat(models): honor catalog-declared setting choices",
        "author": "breedx",
        "date": "2026-08-06"
      },
      {
        "hash": "976bc92d0bd52343273dc69172c11a11786352d6",
        "short_hash": "976bc92d",
        "subject": "Keep model routing refresh narrowly scoped",
        "author": "The Butcher",
        "date": "2026-08-20"
      },
      {
        "hash": "8e00c0999c99e374162ea6ccf8fe61f22e7f41cf",
        "short_hash": "8e00c099",
        "subject": "Expose current prompt to model selectors",
        "author": "The Butcher",
        "date": "2026-08-20"
      },
      {
        "hash": "a479dea9455c5773e7656d5cd9da8b1f6da77111",
        "short_hash": "a479dea9",
        "subject": "feat: add model_select hook for per-run model routing",
        "author": "Blayne Porterfield",
        "date": "2026-08-11"
      },
      {
        "hash": "8a47d0565dad81a0a4adf0d523dadc7533342db4",
        "short_hash": "8a47d056",
        "subject": "fix: name pydantic-ai agents so Logfire spans show logical agent names",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "0bcc26f45f3609816b2e1a968470b5a8d5d395ef",
        "short_hash": "0bcc26f4",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-20"
      },
      {
        "hash": "2c72ab84936bc611eb89f64fcdb492090ad68ad6",
        "short_hash": "2c72ab84",
        "subject": "Merge pull request #815 from Prathap-P/feature/project-scoped-sessions",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "9b5e51a66fe5d3d523c3104799f546de23a1fb03",
        "short_hash": "9b5e51a6",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-20"
      },
      {
        "hash": "45d895e0794649a36cbd5b45cac36a983a3ca803",
        "short_hash": "45d895e0",
        "subject": "Merge pull request #814 from mpfaffenberger/feat/neon-splash",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "5bb283721260317f23de5877273ffbf78f5afd5a",
        "short_hash": "5bb28372",
        "subject": "Merge pull request #813 from mpfaffenberger/feat/logfire-opt-in",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "380344474e50c9d9282879413589fcb680b73004",
        "short_hash": "38034447",
        "subject": "feat: make logfire a hard dependency",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "4fb8e36b0708b5bf04733f4f9eeb946479da6333",
        "short_hash": "4fb8e36b",
        "subject": "fix: eliminate splash flicker -- atomic frames, no erase codes, DEC 2026",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "1449dd8f78e205fa073438d3048d14a5527c1221",
        "short_hash": "1449dd8f",
        "subject": "feat: bump minimum splash showtime to 3 seconds",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "d6c4c292d579223f4546de894bcf18a58c804252",
        "short_hash": "d6c4c292",
        "subject": "feat: add 'Powered by / Pydantic' ansi_shadow figlet under the splash pyramid",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "7d3b4c779cfb5543af3edc9035eaac3ee85882d7",
        "short_hash": "7d3b4c77",
        "subject": "fix: defer import-time output during splash to stop cursor drift",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "425ae098c32bf295ab30e23e5b8e76ad9edb18a7",
        "short_hash": "425ae098",
        "subject": "feat: guarantee 2s minimum splash showtime; make force=True actually force",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "7c90c2ffcd427c4bb6425588870ec80facd3e400",
        "short_hash": "7c90c2ff",
        "subject": "feat: neon Pydantic pyramid splash animation during import-time cold start",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "4e8d41b8e5ca787c9d27e9abc4b44b0201d86a81",
        "short_hash": "4e8d41b8",
        "subject": "feat: opt-in Logfire observability + powered-by-Pydantic banner tagline",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-20"
      },
      {
        "hash": "0e1690c436671dc3b742c95565458130a708be47",
        "short_hash": "0e1690c4",
        "subject": "test(sessions): close real-resolver coverage gap found in manual verification",
        "author": "Prathap",
        "date": "2026-08-20"
      },
      {
        "hash": "1fe10cc1e557b246a11c6aa604284c3401442690",
        "short_hash": "1fe10cc1",
        "subject": "refactor(sessions): rename opt-in scope filter flag from --here to --cwd",
        "author": "Prathap",
        "date": "2026-08-20"
      },
      {
        "hash": "4cb006477071ae52d66e3f9ed74cbcde4b4cd4bb",
        "short_hash": "4cb00647",
        "subject": "Added a shared function for message type inference.",
        "author": "Jack Yao",
        "date": "2026-08-19"
      },
      {
        "hash": "3e524a0295d0da8e71636a089fec88fcdc2ab81c",
        "short_hash": "3e524a02",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-19"
      },
      {
        "hash": "0fb5c94e653dba6b0270d448c5d31b6a0f083524",
        "short_hash": "0fb5c94e",
        "subject": "Merge pull request #808 from StarsExpress/fix-config-truthy-falsy-set",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "716d296208ba3a0fca180dfc01692e015652bb64",
        "short_hash": "716d2962",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-19"
      },
      {
        "hash": "53ff79a949a0415a0c19e8a03b3ec35fed2ebae0",
        "short_hash": "53ff79a9",
        "subject": "Merge pull request #810 from mpfaffenberger/feat/headless-autonomy-policy",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "ce3df5250e2a0c2246f70382e4895f3c964fd3a7",
        "short_hash": "ce3df525",
        "subject": "feat: make headless runs fully autonomous",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "0695a6434fcc511d308119eaa3b6dbceffcf143f",
        "short_hash": "0695a643",
        "subject": "Improve web retriever DOM efficiency (#809)",
        "author": "TJ",
        "date": "2026-08-19"
      },
      {
        "hash": "d67a0bf6f7139b03f547f079475641d660c79d76",
        "short_hash": "d67a0bf6",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-19"
      },
      {
        "hash": "51ace6c120aa8cf5cc113a199bc75e987de3e775",
        "short_hash": "51ace6c1",
        "subject": "Merge pull request #804 from thomwebb/feat/new-clear-alias",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "82901872d99a323fe1ed37cbd641b52ae30e4024",
        "short_hash": "82901872",
        "subject": "Merge pull request #806 from mpfaffenberger/feat/compaction-pure-capabilities",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "22ad24bc1e0bc4a32f14d6913f368763983ec376",
        "short_hash": "22ad24bc",
        "subject": "Merge pull request #803 from mpfaffenberger/fix/headless-usage-property",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "c004ffe063b817018f041aa34d24d7c38e181250",
        "short_hash": "c004ffe0",
        "subject": "Added two helpers to align truthy & falsy bool values.",
        "author": "Jack Yao",
        "date": "2026-08-19"
      },
      {
        "hash": "88c484202662c96bb0d265726f35f752c124cb72",
        "short_hash": "88c48420",
        "subject": "test+fix: port review deltas from #805",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "1b5939cfa61701cc4bdbbe25f5960f33a453139b",
        "short_hash": "1b5939cf",
        "subject": "feat: finish compaction migration - oversized-payload guards as pure harness capabilities",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "89609089ca60fc17d857d93a59794f2c46c9dfc0",
        "short_hash": "89609089",
        "subject": "Add new alias for clear command",
        "author": "TJ Webb",
        "date": "2026-08-19"
      },
      {
        "hash": "614e106b37d99f9c180fc0c5e1fd083bbbae96ed",
        "short_hash": "614e106b",
        "subject": "fix: support property-based run usage",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "d3d585f7d3bb0f17600158e66449f0cc85929690",
        "short_hash": "d3d585f7",
        "subject": "feat(sessions): add opt-in project-scoped session filtering",
        "author": "Prathap",
        "date": "2026-08-19"
      },
      {
        "hash": "4b64812d115a8a6a0ef811d613916e6c2f959466",
        "short_hash": "4b64812d",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-19"
      },
      {
        "hash": "58c897bdfbb3477d3006aa0f0f4cfd21c7928635",
        "short_hash": "58c897bd",
        "subject": "Merge pull request #799 from mpfaffenberger/feat/harness-fallback-compaction",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "6a776207acc32c7b6daa4e9ae6fb428bd5b5d2bd",
        "short_hash": "6a776207",
        "subject": "test: make live lilac compaction suites actually runnable",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "46f60ca20dcec614692d11f19b6c7d7831db365c",
        "short_hash": "46f60ca2",
        "subject": "refactor: replace bespoke compaction with pydantic-ai-harness FallbackCompaction",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-19"
      },
      {
        "hash": "6af3772960d7791c212b27880fa391dd93057381",
        "short_hash": "6af37729",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-19"
      },
      {
        "hash": "ac3e04d070b3f58dfff9d539dc062759a61dde16",
        "short_hash": "ac3e04d0",
        "subject": "Merge pull request #796 from dsfaccini/fix/pr790-review-followups",
        "author": "David SF",
        "date": "2026-08-18"
      },
      {
        "hash": "5898b2760140084ba5f935f1ffc9914be321ba55",
        "short_hash": "5898b276",
        "subject": "style: ruff format regression tests",
        "author": "David Sanchez",
        "date": "2026-08-18"
      },
      {
        "hash": "1360bde2a3e252a94d56da213e29864c584483d5",
        "short_hash": "1360bde2",
        "subject": "Keep compacted history provider-valid + assorted robustness follow-ups",
        "author": "David Sanchez",
        "date": "2026-08-18"
      },
      {
        "hash": "2f957d96b3a442774d35cbee575ec3b3217d0462",
        "short_hash": "2f957d96",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-19"
      },
      {
        "hash": "0ede5e3c63ec8bc6e3508dcbea86de9aa783f021",
        "short_hash": "0ede5e3c",
        "subject": "Merge pull request #775 from StarsExpress/refactor-message-parts-ids",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-18"
      },
      {
        "hash": "539342736bed1e479d4644227ab46d1bfdb6398b",
        "short_hash": "53934273",
        "subject": "Refactored tool call & return ids collection.",
        "author": "Jack Yao",
        "date": "2026-08-18"
      },
      {
        "hash": "a05667134b95ac577e0e805d7a2aea3bccb87095",
        "short_hash": "a0566713",
        "subject": "Merge branch 'main' into refactor-message-parts-ids",
        "author": "Yuan Jack Yao",
        "date": "2026-08-18"
      },
      {
        "hash": "2acf97663da9e00a269fc80d3fa17b2429febe07",
        "short_hash": "2acf9766",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-18"
      },
      {
        "hash": "d1ac8f660367af4003c5ee13a8d5652c444de155",
        "short_hash": "d1ac8f66",
        "subject": "fix(list_files): dedupe raced directory entries against seen_dir_paths (#789)",
        "author": "TJ",
        "date": "2026-08-18"
      },
      {
        "hash": "ff1f4f7777818252849c11cf810842122b141190",
        "short_hash": "ff1f4f77",
        "subject": "feat(i18n): extract custom_server_installer.py user-facing strings (#788)",
        "author": "TJ",
        "date": "2026-08-18"
      },
      {
        "hash": "2c0a65d9a7bb65c9a64256e754b4dd0f64681674",
        "short_hash": "2c0a65d9",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-18"
      },
      {
        "hash": "acdcc8195f6f5e7a96ffef11ebeaf8bdc0f3f540",
        "short_hash": "acdcc819",
        "subject": "Fix interrupted parallel tool-call pruning + assorted robustness fixes (#790)",
        "author": "David SF",
        "date": "2026-08-18"
      },
      {
        "hash": "f481fb3022b29947370111e4f9fcd43dcb28a380",
        "short_hash": "f481fb30",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-18"
      },
      {
        "hash": "38f56376e30df807742f93e90706a83f9bcb9a94",
        "short_hash": "38f56376",
        "subject": "Merge pull request #791 from mpfaffenberger/feat/headless-usage-file",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-18"
      },
      {
        "hash": "065f05bdb7c6aa549cf0bb59f9bd760997c1eb25",
        "short_hash": "065f05bd",
        "subject": "feat: export headless model usage as JSON",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-18"
      },
      {
        "hash": "7846776a37fb132633c259472472bbff43dac2c8",
        "short_hash": "7846776a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-18"
      },
      {
        "hash": "6402fb67dadb58febbe20a8d34a6e6d6bb663551",
        "short_hash": "6402fb67",
        "subject": "Merge pull request #793 from mpfaffenberger/feat/disable-ask-user-question",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-18"
      },
      {
        "hash": "600d508e0fbd12f849bafa1941c9d866199480d1",
        "short_hash": "600d508e",
        "subject": "chore(callbacks): type the fail-closed policy set precisely (#794)",
        "author": "Xi Chen",
        "date": "2026-08-18"
      },
      {
        "hash": "550fdc39bde868dc42d34eab3d5b732d147b3413",
        "short_hash": "550fdc39",
        "subject": "feat: allow disabling ask-user tool",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-18"
      },
      {
        "hash": "392cdc4e25172d47a22d5322b177731efecbc3f9",
        "short_hash": "392cdc4e",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-18"
      },
      {
        "hash": "5fb9efbbead62fe15ffd43c0695288a254f1fdd9",
        "short_hash": "5fb9efbb",
        "subject": "web-retriever: ask before persisting extracted data to a file (#792)",
        "author": "TJ",
        "date": "2026-08-18"
      },
      {
        "hash": "173c904401701fb20b8d8c8d42e3fd4a284d6411",
        "short_hash": "173c9044",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-18"
      },
      {
        "hash": "e5771ab8ce45161e70e872a8dc7fadf3ccb6de05",
        "short_hash": "e5771ab8",
        "subject": "feat(i18n): extract add_model_menu.py user-facing strings (#706)",
        "author": "TJ",
        "date": "2026-08-18"
      },
      {
        "hash": "7c7517553a078c92148690dc135501e884abd920",
        "short_hash": "7c751755",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-18"
      },
      {
        "hash": "cf0ff04cce17437ec8b325fc9fbd8946886ff25b",
        "short_hash": "cf0ff04c",
        "subject": "fix(callbacks): a security callback that crashes must not read as approval (#777)",
        "author": "Xi Chen",
        "date": "2026-08-18"
      },
      {
        "hash": "cc549cdcab195dfedaf58afc77a96af6c3e3def0",
        "short_hash": "cc549cdc",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-18"
      },
      {
        "hash": "7964008ab1ec50f676124347c272e8f48815de40",
        "short_hash": "7964008a",
        "subject": "Merge pull request #703 from breedx/upstream/model-settings-repaint",
        "author": "TJ",
        "date": "2026-08-18"
      },
      {
        "hash": "f2c8fcdafbd904980589106b0824268488c66f3c",
        "short_hash": "f2c8fcda",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-17"
      },
      {
        "hash": "7b82a2eb3ceb967f98b487833fc7e28c168cd77d",
        "short_hash": "7b82a2eb",
        "subject": "Merge pull request #785 from dsfaccini/fix/compaction-summarization",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-17"
      },
      {
        "hash": "2b4732da221aa1c754423a71a07ab369207ece07",
        "short_hash": "2b4732da",
        "subject": "Merge pull request #774 from thomwebb/feat/agent-execution-context",
        "author": "TJ",
        "date": "2026-08-17"
      },
      {
        "hash": "041935c1c601c12e0569b69abfd5f89da157ffc9",
        "short_hash": "041935c1",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-17"
      },
      {
        "hash": "f054deef49a1073a9e68b941542f270dbbb89a38",
        "short_hash": "f054deef",
        "subject": "Merge pull request #787 from sudhanshushekhar10/fix/list-files-quadratic-dedup",
        "author": "TJ",
        "date": "2026-08-17"
      },
      {
        "hash": "c55d9fe915678f463550078b05a66bd058a16247",
        "short_hash": "c55d9fe9",
        "subject": "fix: scope executing agent across the full run lifecycle",
        "author": "TJ",
        "date": "2026-08-17"
      },
      {
        "hash": "381bf602607bb3bf62cbe11d173fcf9ffac1ec67",
        "short_hash": "381bf602",
        "subject": "fix(list_files): replace O(n^2) parent-directory dedup with a set",
        "author": "sudhanshushekhar10",
        "date": "2026-08-18"
      },
      {
        "hash": "e136fb888259704155ed36243e27eb344962e24e",
        "short_hash": "e136fb88",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-17"
      },
      {
        "hash": "27e5747244084192ed9dae87f5cb11fd593cbf44",
        "short_hash": "27e57472",
        "subject": "Merge pull request #773 from thomwebb/fix/test-robustness",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-17"
      },
      {
        "hash": "0246ca583da5b4f5c61796f315a6263ee646b705",
        "short_hash": "0246ca58",
        "subject": "Merge pull request #778 from weegens-aaron/fix/agents-md-utf16-bom",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-17"
      },
      {
        "hash": "15bcad9ee4126ed3226c7a581f9d68632138c31d",
        "short_hash": "15bcad9e",
        "subject": "Apply ruff format to new test files",
        "author": "David Sanchez",
        "date": "2026-08-17"
      },
      {
        "hash": "b8a0006668d8dee2bc4cf412b2fe6dbdd63a581e",
        "short_hash": "b8a00066",
        "subject": "Fix summarization-compaction reliability + assorted robustness fixes",
        "author": "David Sanchez",
        "date": "2026-08-17"
      },
      {
        "hash": "cbb7d30c49de84e707f435e641f5df0f54501cf3",
        "short_hash": "cbb7d30c",
        "subject": "Fix UTF-16 AGENTS.md crash on Windows",
        "author": "weegens-aaron",
        "date": "2026-08-17"
      },
      {
        "hash": "2955602be29fd5beb4659bfc5be7cc0b07262903",
        "short_hash": "2955602b",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-17"
      },
      {
        "hash": "69905961fd547fa36fae190e600f1dfa65ee83ed",
        "short_hash": "69905961",
        "subject": "Route Anthropic Opus 5 to adaptive thinking",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-17"
      },
      {
        "hash": "36e77ec9f923b987602705fd09206efbf3c25579",
        "short_hash": "36e77ec9",
        "subject": "Refactored tool call & return ids collection.",
        "author": "Jack Yao",
        "date": "2026-08-16"
      },
      {
        "hash": "5d63220df925f03b7245c66587cc31a861780bac",
        "short_hash": "5d63220d",
        "subject": "feat: expose per-agent execution context",
        "author": "TJ",
        "date": "2026-08-15"
      },
      {
        "hash": "c1ef485eaa12255c88e865e9507e94781464aee2",
        "short_hash": "c1ef485e",
        "subject": "test: robust port occupancy check and DBOS optional skip",
        "author": "TJ",
        "date": "2026-08-16"
      },
      {
        "hash": "00cda83a4e8d33491686ae5230391dca7b851e44",
        "short_hash": "00cda83a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-16"
      },
      {
        "hash": "6df55ed9fa1b305d7d7e09500eb0381cc68f918b",
        "short_hash": "6df55ed9",
        "subject": "Merge pull request #769 from thomwebb/feat/show-core-plugins-version",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "9dbe667043e9592e899d8b7256b09aafba6dffb4",
        "short_hash": "9dbe6670",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-16"
      },
      {
        "hash": "96c86d182536b05259b1e63566771729e9524315",
        "short_hash": "96c86d18",
        "subject": "Merge pull request #771 from thomwebb/fix/add-model-suggest",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "3785a9709493a331024f0dac84fdc88c5b1f40ee",
        "short_hash": "3785a970",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-16"
      },
      {
        "hash": "b5dc6bb9485e61c1243c3f3a1ff68bac4ccd04fd",
        "short_hash": "b5dc6bb9",
        "subject": "fix: /model suggestions now reflect models added via /add_model",
        "author": "TJ",
        "date": "2026-08-16"
      },
      {
        "hash": "47d5490c709d1c712f8af6275b2427b2fddc80ad",
        "short_hash": "47d5490c",
        "subject": "style: sort imports in model_picker_completion.py",
        "author": "TJ",
        "date": "2026-08-16"
      },
      {
        "hash": "827f8a1ee93247af492dba54fb1890cdebfb8cb5",
        "short_hash": "827f8a1e",
        "subject": "Merge pull request #768 from mpfaffenberger/fix/subagent-token-cache-metrics",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "5e5b7fee7109532569d90e8b16e69d8cdcef5df3",
        "short_hash": "5e5b7fee",
        "subject": "test: remove Model Judge prompt content assertions",
        "author": "Pack Leader",
        "date": "2026-08-16"
      },
      {
        "hash": "a5261fa5fa7a9b058bccca1b124d44270b7dcab5",
        "short_hash": "a5261fa5",
        "subject": "docs: trim verbose comments and test prose",
        "author": "Pack Leader",
        "date": "2026-08-16"
      },
      {
        "hash": "e57b58088d951b0400e4424874bd523c2aabf46a",
        "short_hash": "e57b5808",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-16"
      },
      {
        "hash": "e53537f9fb9efe500340a21b16a1de0450db847c",
        "short_hash": "e53537f9",
        "subject": "Merge pull request #770 from mpfaffenberger/awtilso/PUP-634",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "30c15b44b637f723f7af901d1dc9d34c499b5828",
        "short_hash": "30c15b44",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-16"
      },
      {
        "hash": "81595ab1fcc87bdc3f1f838c2ddc991c5532c7ae",
        "short_hash": "81595ab1",
        "subject": "Normalize None-ish cwd strings in run_shell_command",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "bf503e54cf9bf583b1c7a716845a3fa31e7eb318",
        "short_hash": "bf503e54",
        "subject": "Recover live compaction integration tests; bump CI models to GLM-5.2 + Kimi K2.6",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "57de5091ef1c8b32c454eca063a566ba990097de",
        "short_hash": "57de5091",
        "subject": "chore: trim comments to minimal required context",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-16"
      },
      {
        "hash": "87e23b65e38aa7410ec31080183ef579e00bf3f1",
        "short_hash": "87e23b65",
        "subject": "test: pin the cache-folding premise to real v2 adapters",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-16"
      },
      {
        "hash": "b26c21273741906bfa2200f78e4b4982adec63f2",
        "short_hash": "b26c2127",
        "subject": "fix: classify bare JSONDecodeError as retryable in streaming path",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-16"
      },
      {
        "hash": "0b1cb6eb79177295a6500dd70e44a35669fa1ab9",
        "short_hash": "0b1cb6eb",
        "subject": "test: model result.usage as a property, not a callable",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-16"
      },
      {
        "hash": "1fd3b51d2067e09375a739fad9579258397d3622",
        "short_hash": "1fd3b51d",
        "subject": "Merge origin/main into fix/subagent-token-cache-metrics",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-16"
      },
      {
        "hash": "df5abd4970ac4406a564494f135e51cbae6e39bc",
        "short_hash": "df5abd49",
        "subject": "Merge origin/main into feat/show-core-plugins-version",
        "author": "TJ",
        "date": "2026-08-16"
      },
      {
        "hash": "026fd30ff8df3e8e1f66cb2dec02bac7f080c6ce",
        "short_hash": "026fd30f",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-16"
      },
      {
        "hash": "bf6b044afedac66c6d99e14a055c8a09f9076bcf",
        "short_hash": "bf6b044a",
        "subject": "Silence unsupported-sampling-parameter warnings for Anthropic models",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "c987c321b42737fcd03a0be6eae76fe33c64ea4d",
        "short_hash": "c987c321",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-16"
      },
      {
        "hash": "d94db5c9b8317cb0547eda053b7edfede74cea50",
        "short_hash": "d94db5c9",
        "subject": "Delete pre-0.0.7 plugin compat shims",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "79315b4ea6156919df58926b221425dcc5e0782e",
        "short_hash": "79315b4e",
        "subject": "Depend on code-puppy-core-plugins>=0.0.8 from PyPI",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "165908188776cd9d4b47be3db8696684b74e0c76",
        "short_hash": "16590818",
        "subject": "Make session format sweep self-healing + de-spam failure logging",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "ddd12370339ac8430e12f84dafc28783149d8cef",
        "short_hash": "ddd12370",
        "subject": "Fix surrogate unpickler failure on tz-aware datetimes",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "326ea5ab8edd2fbfdc2f5b5a10cd657f6ece768a",
        "short_hash": "326ea5ab",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-16"
      },
      {
        "hash": "4dc62bcd030f3799374682ec38b0c790101a0a5b",
        "short_hash": "4dc62bcd",
        "subject": "Point plugins dependency at git source pending 0.0.7 PyPI release",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "c2fcc6aed5e4eb2beb860094f3361605d0aeb707",
        "short_hash": "c2fcc6ae",
        "subject": "fix: correct two false claims found in review",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-16"
      },
      {
        "hash": "9275a3f79eaeb9bf7872baa5f00d2f73e5a29127",
        "short_hash": "9275a3f7",
        "subject": "docs: tighten the comments",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-16"
      },
      {
        "hash": "e704980cf9d2908df687cbef81a5e0960e199bc8",
        "short_hash": "e704980c",
        "subject": "fix: harden core plugins version reporting",
        "author": "TJ",
        "date": "2026-08-15"
      },
      {
        "hash": "440f404f1bc412e139c2ad071b0453ccdea23234",
        "short_hash": "440f404f",
        "subject": "Fix emoji_filter tests for stream-event-seam implementation",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "c00b1ef719ff654792753b3a211de589714899ee",
        "short_hash": "c00b1ef7",
        "subject": "Post-migration cleanup: remove dead code, archive migration docs",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "1f9c6c7ce1fbb5b22542aadd942f97e1f052c60e",
        "short_hash": "1f9c6c7c",
        "subject": "v2 sweep: pin MCP prefer_tasks=False, document part-kind and settings audits",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "2e86344823c7edb725c05a9a02031a6e871ad204",
        "short_hash": "2e863448",
        "subject": "Align custom models with the pydantic-ai v2 Model ABC",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "a5c710fbc7c2b921aff83f3ba0c064037df2e92f",
        "short_hash": "a5c710fb",
        "subject": "Adopt v2 cancellation semantics; delete cancel-scope suppression (gate passed)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "d280303c63a4038eadef45bec487205f5b1d452f",
        "short_hash": "d280303c",
        "subject": "Bump pydantic-ai to 2.31.0 (hop 2 of v2 migration) + mechanical fixes",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-16"
      },
      {
        "hash": "c1f8c05f06c8797dfd8f6a343910936c468ca5b6",
        "short_hash": "c1f8c05f",
        "subject": "Wire in code-puppy-core-plugins 0.0.6 from sibling checkout",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-15"
      },
      {
        "hash": "0dd7f79d8e2ed0c685bbfc59bff7a9fe519948f2",
        "short_hash": "0dd7f79d",
        "subject": "feat: show core plugins version at startup",
        "author": "TJ",
        "date": "2026-08-15"
      },
      {
        "hash": "56591821f940b3d5be28ffee557a62ce020fce76",
        "short_hash": "56591821",
        "subject": "Rebuild MCP toolset consumers on public wrapper APIs",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-15"
      },
      {
        "hash": "da9bd91af77ae6ac6441870fb4b260623d1ffca5",
        "short_hash": "da9bd91a",
        "subject": "refactor: trim the prose and the duplicate tests",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-15"
      },
      {
        "hash": "8732872fe3f6b8c0c7b17980e31c2fed916e1f6a",
        "short_hash": "8732872f",
        "subject": "Migrate mcp_ subsystem off deprecated MCPServer* onto MCPToolset",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-15"
      },
      {
        "hash": "9bf42afe689b0ca95d086cbc2f0444f35e472616",
        "short_hash": "9bf42afe",
        "subject": "Bump pydantic-ai to 1.107.5 (hop 1 of v2 migration)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-15"
      },
      {
        "hash": "a3ff3360a8821b99b564ea814868c20b6548bb6d",
        "short_hash": "a3ff3360",
        "subject": "fix: stop the judge inventing OpenAI cache-write costs",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-15"
      },
      {
        "hash": "de52fccadd2ba74e5619fa8b9b3cd8ac5cb3fbfe",
        "short_hash": "de52fcca",
        "subject": "feat: add the Model Judge agent",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-15"
      },
      {
        "hash": "5e7b8d7f1fcb68bba49fe2209d7fd14d38b90907",
        "short_hash": "5e7b8d7f",
        "subject": "fix: address review feedback on subagent usage reporting",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-15"
      },
      {
        "hash": "1167a54d6837792ab7e3d006bef47b606484f850",
        "short_hash": "1167a54d",
        "subject": "Use stable content-based sha256 digests for message dedup hashing",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-15"
      },
      {
        "hash": "661ba1083c393a36fa5a971f1e571345a86ab20d",
        "short_hash": "661ba108",
        "subject": "Make pydantic-ai monkey patches fail loudly instead of silently",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-15"
      },
      {
        "hash": "61d6766d41e7ab7bf23b43a74e3c5e8f3d10c0e4",
        "short_hash": "61d6766d",
        "subject": "Migrate Anthropic prompt caching to native pydantic-ai settings; slim claude_cache_client to OAuth core",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-15"
      },
      {
        "hash": "30edbc89e6a033043f17e3c08020bf279a069de0",
        "short_hash": "30edbc89",
        "subject": "feat(sessions): migrate persistence from pickle to versioned JSON envelopes",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-15"
      },
      {
        "hash": "f908d742a7f6beb7758566c8e0b9d91d4fa80297",
        "short_hash": "f908d742",
        "subject": "fix: keep usage metrics provider reported",
        "author": "Pack Leader",
        "date": "2026-08-15"
      },
      {
        "hash": "d00ac86b9d3ebce485b7399a66d281c8576d7267",
        "short_hash": "d00ac86b",
        "subject": "fix: report subagent token usage reliably",
        "author": "Pack Leader",
        "date": "2026-08-15"
      },
      {
        "hash": "757db1cf33138dcf34ea58a7888f4a16f4f4ca1c",
        "short_hash": "757db1cf",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-15"
      },
      {
        "hash": "9c21fbf12bf1f24006f29ac7f8ca7a8f309e1ecc",
        "short_hash": "9c21fbf1",
        "subject": "Merge pull request #766 from thomwebb/fix/pup-622-startup-catalog-noise",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-14"
      },
      {
        "hash": "5ca6557933c0c86bbe415509c2a7cf4a54539408",
        "short_hash": "5ca65579",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-15"
      },
      {
        "hash": "f1e48ff90294b4e4d4369584104e907b409f1dc0",
        "short_hash": "f1e48ff9",
        "subject": "refactor: remove web retriever prompt guidance",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-14"
      },
      {
        "hash": "6377759c00fc0b2745fd322642304f3da4c5ce2a",
        "short_hash": "6377759c",
        "subject": "fix: quiet optional skill catalog startup",
        "author": "TJ Webb",
        "date": "2026-08-14"
      },
      {
        "hash": "1505636ca7e4e1156cb976d8b9ef85a776c0f8b3",
        "short_hash": "1505636c",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-14"
      },
      {
        "hash": "9ff9698e04e5b420c17c1e8dc6114601d1455d68",
        "short_hash": "9ff9698e",
        "subject": "Merge pull request #765 from mpfaffenberger/fix/759-rich-theme-hex",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-14"
      },
      {
        "hash": "1b4fe2b25cff3b1f350ebca1ac509a1f64275e92",
        "short_hash": "1b4fe2b2",
        "subject": "ci: remove migrated computer-use job",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-14"
      },
      {
        "hash": "b83383910ef24d6de2696f4a7e0942542d694462",
        "short_hash": "b8338391",
        "subject": "fix: normalize themed Rich hex colors",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-14"
      },
      {
        "hash": "5be21b6de86612deb71610320c1fd4e6b8885fe7",
        "short_hash": "5be21b6d",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-14"
      },
      {
        "hash": "f2427a6474d439bb8ea41769bd74d9170ef58e37",
        "short_hash": "f2427a64",
        "subject": "build: depend on published core plugin bundle",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-14"
      },
      {
        "hash": "27efe8f57dc5c76bbb5a7cb8d10ded98c70dea18",
        "short_hash": "27efe8f5",
        "subject": "refactor: move builtin plugin implementations to companion package",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-14"
      },
      {
        "hash": "23ee333d97b7b46ebc9ebe3607156b23606ff965",
        "short_hash": "23ee333d",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-14"
      },
      {
        "hash": "7f5ba17d23cc8c7d24d900f2e05e066fa77e3352",
        "short_hash": "7f5ba17d",
        "subject": "feat: discover installed plugins through entry points",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-14"
      },
      {
        "hash": "15640d9856c10c40a7e196ecd9842b3280f18551",
        "short_hash": "15640d98",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-14"
      },
      {
        "hash": "28089370a4328677f22f9326ccdc8f4079257703",
        "short_hash": "28089370",
        "subject": "feat: make puppy kennel memory opt-in",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-14"
      },
      {
        "hash": "94529bcb4de2c253ece61568fc6bce5d4edbbcf9",
        "short_hash": "94529bcb",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-13"
      },
      {
        "hash": "7867e743e45ffede29b8b2c1916be94912ff95a4",
        "short_hash": "7867e743",
        "subject": "Merge pull request #763 from mpfaffenberger/awtilso/PUP-618",
        "author": "Andrew Tilson",
        "date": "2026-08-13"
      },
      {
        "hash": "fc6f4c16f906b98daabd8f7bb978e16117557e81",
        "short_hash": "fc6f4c16",
        "subject": "fix(subagent-panel): display selected model identifier verbatim",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-08-13"
      },
      {
        "hash": "4b7b18d2b722dcb4db30ac9292000ccfed8efaa7",
        "short_hash": "4b7b18d2",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-13"
      },
      {
        "hash": "12cfdb61b31e97da80fe2569728eb2457be8c7ce",
        "short_hash": "12cfdb61",
        "subject": "refactor: fully decouple wiggum from core",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-13"
      },
      {
        "hash": "399effcfd5a49bc25652086c8b17e8ee2179fef3",
        "short_hash": "399effcf",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-13"
      },
      {
        "hash": "5e12bba856e34b1d67b2413503408c7f792230ce",
        "short_hash": "5e12bba8",
        "subject": "refactor: fully decouple puppy_kennel from core",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-13"
      },
      {
        "hash": "0f433152e8385346d3cf868638ec2ac52b8ff759",
        "short_hash": "0f433152",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-13"
      },
      {
        "hash": "0bcb44c7944e38afad4c247956dc3ad5aa437f48",
        "short_hash": "0bcb44c7",
        "subject": "chore: remove dead gemini_oauth leftovers",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-13"
      },
      {
        "hash": "7420153cbd7595facc27def42a6f909194a831b1",
        "short_hash": "7420153c",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-12"
      },
      {
        "hash": "1d73ee0383296d933844dda3551bad8d53bf13a0",
        "short_hash": "1d73ee03",
        "subject": "Merge pull request #761 from thomwebb/fix/atomic-json-config-io",
        "author": "TJ",
        "date": "2026-08-12"
      },
      {
        "hash": "f4bc5ea354fc456ab572b4a45dd16e15f0a3378e",
        "short_hash": "f4bc5ea3",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-12"
      },
      {
        "hash": "eb538f7b4dca121a4312c804b3d5304969e4b3b5",
        "short_hash": "eb538f7b",
        "subject": "Trim verbose comments across the codebase",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-12"
      },
      {
        "hash": "744c22faa1f63bd9d29b1dc60901b73a83f65ef9",
        "short_hash": "744c22fa",
        "subject": "fix: close lost-update race in aws_bedrock/azure_foundry extra_models.json writers",
        "author": "TJ Webb",
        "date": "2026-08-12"
      },
      {
        "hash": "7bb8619501330649b8f6cd8b391bc7d4970cd4c3",
        "short_hash": "7bb86195",
        "subject": "fix: extend atomic, bounded, locked config I/O to JSON config surfaces",
        "author": "TJ Webb",
        "date": "2026-08-12"
      },
      {
        "hash": "c7b20cea58fa6aa46552bbf8ba98a4400e6358d8",
        "short_hash": "c7b20cea",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-12"
      },
      {
        "hash": "bfbac3b9544cdcc077f0c421982552fff9796804",
        "short_hash": "bfbac3b9",
        "subject": "Merge pull request #757 from thomwebb/fix/config-corruption-resilience",
        "author": "TJ",
        "date": "2026-08-12"
      },
      {
        "hash": "742e6ba67e368cad00e3ef2a31f5bbdcdd2e01eb",
        "short_hash": "742e6ba6",
        "subject": "fix: recover from corrupted config files",
        "author": "TJ Webb",
        "date": "2026-08-11"
      },
      {
        "hash": "8faf118c4033b5eab9e061ac6d41e02c6d4f78fd",
        "short_hash": "8faf118c",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-11"
      },
      {
        "hash": "aeeab3fad424d3e5a26b5829abf0e97454d5aafc",
        "short_hash": "aeeab3fa",
        "subject": "Merge pull request #754 from StarsExpress/refactor-dead-mcp-functions",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-11"
      },
      {
        "hash": "ea6b8ddf64287170c4861b91ab3e72414ece3b9a",
        "short_hash": "ea6b8ddf",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-11"
      },
      {
        "hash": "522f9fe491545970edd14eccc9fcbd8f3b043a2e",
        "short_hash": "522f9fe4",
        "subject": "Merge pull request #755 from thomwebb/fix/subagent-model-fallback-pup-585",
        "author": "TJ",
        "date": "2026-08-11"
      },
      {
        "hash": "077f41702c93dbba2e2e9bfad81e9acaf5d2d8eb",
        "short_hash": "077f4170",
        "subject": "style: apply ruff format to 3 files carried in from the upstream sync",
        "author": "TJ Webb",
        "date": "2026-08-11"
      },
      {
        "hash": "7c97e7b3018c9a7aa6e0c07d1dbe70b500f60385",
        "short_hash": "7c97e7b3",
        "subject": "Merge remote-tracking branch 'upstream/main' into fix/subagent-model-fallback-pup-585",
        "author": "TJ Webb",
        "date": "2026-08-11"
      },
      {
        "hash": "52efd4020bcdacd1bf0c63bc3c6a1574bc261178",
        "short_hash": "52efd402",
        "subject": "fix: close a narrow session-close/in-flight-run race + doc drift (round 4)",
        "author": "TJ Webb",
        "date": "2026-08-11"
      },
      {
        "hash": "e7c81c5eb446929e8d095c11089535af86738b68",
        "short_hash": "e7c81c5e",
        "subject": "fix: replace shared-global conversation scope with a real ContextVar",
        "author": "TJ Webb",
        "date": "2026-08-11"
      },
      {
        "hash": "b4ad491f9f84ff6d823ed92355eb4b252691f057",
        "short_hash": "b4ad491f",
        "subject": "fix: scope the dead-model warning dedup by conversation, not by process",
        "author": "TJ Webb",
        "date": "2026-08-11"
      },
      {
        "hash": "642f9d65ebd432e3f4c2e3d0bdf311f31db3f1f6",
        "short_hash": "642f9d65",
        "subject": "fix: address adversarial review findings on the model-fallback dedup",
        "author": "TJ Webb",
        "date": "2026-08-11"
      },
      {
        "hash": "12c5c3c1ece0110ae485396b772eefee5fb4a1be",
        "short_hash": "12c5c3c1",
        "subject": "fix: sub-agent invocation falls back instead of hard-failing on a dead pinned model",
        "author": "TJ Webb",
        "date": "2026-08-11"
      },
      {
        "hash": "77afe8ba5378005169e5c9267a021c04de4a6511",
        "short_hash": "77afe8ba",
        "subject": "Reformatted 3 files by ruff.",
        "author": "Jack Yao",
        "date": "2026-08-11"
      },
      {
        "hash": "f3f3ba8b442d69f8cea8203828e5619f8d150927",
        "short_hash": "f3f3ba8b",
        "subject": "Removed dead functions.",
        "author": "Jack Yao",
        "date": "2026-08-11"
      },
      {
        "hash": "dacbc2459c87ebc268d71a6e11e3c06e84f52230",
        "short_hash": "dacbc245",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-11"
      },
      {
        "hash": "5d1451aa34161402c397149358145b6d48a6ec6b",
        "short_hash": "5d1451aa",
        "subject": "Merge pull request #714 from thomwebb/feat/code-puppy-agent-skill-split",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-11"
      },
      {
        "hash": "a5de8d06189f5db3f4f7f40cc9016ac0acecf48d",
        "short_hash": "a5de8d06",
        "subject": "Merge pull request #753 from 3weakley/fix/additive-skill-directories",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-11"
      },
      {
        "hash": "fffe9b7ff1386c57061b98949962342fa2c2211f",
        "short_hash": "fffe9b7f",
        "subject": "Preserve default skill directories in enabled skill discovery",
        "author": "Eddie Weakley",
        "date": "2026-08-11"
      },
      {
        "hash": "3f01b1fe481211f0ceaf05e98775cb05c9011dea",
        "short_hash": "3f01b1fe",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-11"
      },
      {
        "hash": "bfcf43f532b8a7a6284d8442ed54c8ee8333324b",
        "short_hash": "bfcf43f5",
        "subject": "Merge pull request #749 from thomwebb/feat/codex-imagegen-auth-gate-and-tags",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-11"
      },
      {
        "hash": "33cd907117782930029dc28248e5a35e900de123",
        "short_hash": "33cd9071",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-11"
      },
      {
        "hash": "69c6e2b42e09797629347e687643845678d6db34",
        "short_hash": "69c6e2b4",
        "subject": "Merge pull request #745 from hyper-n0va/fix/ollama-custom-endpoint-timeout",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-11"
      },
      {
        "hash": "13516164e8a049a7a1c8453d746be3b3f7d2248c",
        "short_hash": "13516164",
        "subject": "Merge pull request #695 from weegens-aaron/herdr-windows",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-11"
      },
      {
        "hash": "db956550d3cf24d9f5c01d589dfbe41a0319b71e",
        "short_hash": "db956550",
        "subject": "Merge pull request #711 from StarsExpress/refactor-remove-get_file_icon",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-11"
      },
      {
        "hash": "586b6df2d7be7433b2dadc1fce94908930bcf941",
        "short_hash": "586b6df2",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-11"
      },
      {
        "hash": "560dc3f3040385f33671bb2dfec8fceeac2f6253",
        "short_hash": "560dc3f3",
        "subject": "Merge pull request #751 from Jiaq1Zhu/main",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "cae10e94cfd7191d93225788ad555eedd764479f",
        "short_hash": "cae10e94",
        "subject": "fix(agents): validate agent JSON configuration before saving",
        "author": "Jiaqi Zhu",
        "date": "2026-08-10"
      },
      {
        "hash": "0657181be7194581d4025cf4ad2519f0ba478e5a",
        "short_hash": "0657181b",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-11"
      },
      {
        "hash": "f79b29c8ed7eee37896d26a057ad76f334867623",
        "short_hash": "f79b29c8",
        "subject": "Merge pull request #748 from avargaskun/resume-renders-history",
        "author": "TJ",
        "date": "2026-08-10"
      },
      {
        "hash": "ad656f1329a9c49e94eb9e8ab108dbe2dccb2ebb",
        "short_hash": "ad656f13",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-10"
      },
      {
        "hash": "27d7811edde91e1ab87865123db4ed433145394f",
        "short_hash": "27d7811e",
        "subject": "test: allow builtin skills catalog network traffic",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "e35266679b147f11b07de97aa878ff8998d9db74",
        "short_hash": "e3526667",
        "subject": "Merge PR #739: decouple universal constructor plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "8fb514b950aedb4436817671b84535260168b711",
        "short_hash": "8fb514b9",
        "subject": "Merge PR #738: decouple Claude Code OAuth plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "1b75a4b83113922de67e182bdf1a335c08100085",
        "short_hash": "1b75a4b8",
        "subject": "Merge PR #744: decouple DBOS durable exec plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "21244bbcffabb3743ab37eb2286cd04557312dfc",
        "short_hash": "21244bbc",
        "subject": "fix: make UC provider lifecycle ownership-aware (#726)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "c1956942abbbf3c91379e49910d3beb581643869",
        "short_hash": "c1956942",
        "subject": "refactor: add universal constructor provider seam (#726)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "231d1f498d2e8bee081d34a955938d17666653d0",
        "short_hash": "231d1f49",
        "subject": "refactor: decouple universal constructor plugin (#726)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "a2bb91e1dcb29ebbc0ebc6fa21e97288aee35053",
        "short_hash": "a2bb91e1",
        "subject": "fix: await claude oauth providers in async client (#727)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "45494b93508aa0a59ec0aa1ab4b542093212a2f8",
        "short_hash": "45494b93",
        "subject": "test: harden claude oauth callback seams (#727)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "6bb9d8729568e1f90424b63675557aeda7d4147b",
        "short_hash": "6bb9d872",
        "subject": "refactor: decouple claude oauth plugin (#727)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "fda38b937abc6e40ff3e49f28af79ce1843af97c",
        "short_hash": "fda38b93",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-10"
      },
      {
        "hash": "dc15b46daa2ce103a1e974b11f450a6b4cbaa086",
        "short_hash": "dc15b46d",
        "subject": "Decouple DBOS state from set menu catalog",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "9b66efea20b992507e3b893a30a768c1a11acd22",
        "short_hash": "9b66efea",
        "subject": "Merge PR #737: decouple file permission handler plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "cbc88d37f892e614f805df287f43d481b5cce522",
        "short_hash": "cbc88d37",
        "subject": "Merge PR #736: decouple agent skills plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "6edfcdad66eed80e3aef844066b3e99cfd7efc07",
        "short_hash": "6edfcdad",
        "subject": "Merge PR #742: decouple Ollama setup plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "ee4b15b0e03963457900665c5e6b1c7a3f27229c",
        "short_hash": "ee4b15b0",
        "subject": "Merge PR #741: decouple statusline plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "f893c6ddc1b8ef70db57b17642e49e07f1bd9f2a",
        "short_hash": "f893c6dd",
        "subject": "Merge PR #735: decouple ChatGPT OAuth plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "6d86283216785c7cddbc31905237f0317ebd8a0f",
        "short_hash": "6d862832",
        "subject": "Merge PR #743: decouple customizable commands",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "53037eb17c55fd3fae3f61cdbdee5099941c9f15",
        "short_hash": "53037eb1",
        "subject": "Merge PR #740: decouple theme plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-10"
      },
      {
        "hash": "f9c2d851bd2f1f8aaab60e38f554e9b6fae26468",
        "short_hash": "f9c2d851",
        "subject": "Gate codex-imagegen skill on Codex OAuth, add namespace tags",
        "author": "TJ Webb",
        "date": "2026-08-10"
      },
      {
        "hash": "90afe19a044aff50df4f23031a1c75211b72882f",
        "short_hash": "90afe19a",
        "subject": "Re-render recent history on interactive `-r` resume",
        "author": "avargaskun",
        "date": "2026-08-05"
      },
      {
        "hash": "dbd8d1ffe19b831601db97886c0ed001ec2694ca",
        "short_hash": "dbd8d1ff",
        "subject": "fix: support Ollama custom endpoint config",
        "author": "hyper-n0va",
        "date": "2026-08-09"
      },
      {
        "hash": "3a1ba1b66c019c3dad6e678ee75c5734eb3e2b20",
        "short_hash": "3a1ba1b6",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-10"
      },
      {
        "hash": "9d640e9a72938300f963804d228a0a04a903c607",
        "short_hash": "9d640e9a",
        "subject": "fix: consume agent skills through provider seam (#724)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "c87dfbbbaf4456d136d6b7e8ef6ccbf9e439b12e",
        "short_hash": "c87dfbbb",
        "subject": "Decouple Ollama setup completion provider",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "301fec1e3a22daeb0afc6947b768c7f29c0d37c7",
        "short_hash": "301fec1e",
        "subject": "Decouple quick resume from statusline",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "d9ebc66a60015b0710a4d646ce10e8615069a5c6",
        "short_hash": "d9ebc66a",
        "subject": "Decouple customizable command dispatch",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "3a1b1e2bbe9fc215264c0d33f27d3fe2241fa79a",
        "short_hash": "3a1b1e2b",
        "subject": "fix: decouple question theme from theme plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "3c82163dc7833818301b1a7dcbf0cf938b05a479",
        "short_hash": "3c82163d",
        "subject": "fix: honor file permission provider lifecycle (#729)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "2fd2d6cdcde3dd6bd5a7099689a4ac2fa20b37ce",
        "short_hash": "2fd2d6cd",
        "subject": "fix: decouple file permission handler plugin (#729)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "8e4390a6c24bb84ec17e638faba7cd017da8238e",
        "short_hash": "8e4390a6",
        "subject": "fix: decouple agent skills plugin (#724)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "d33b1f4786f48ee85087516f4f8299ebc111a868",
        "short_hash": "d33b1f47",
        "subject": "refactor: decouple chatgpt_oauth plugin from core (#728)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "a02f621f5ffd6e7e49159b910433bbf708cfc052",
        "short_hash": "a02f621f",
        "subject": "ci: restore Windows UTF-8 smoke tests and format baseline",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "24390b2115e2f7555c7dcbfbfbb0e3f0338fc5b8",
        "short_hash": "24390b21",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "a12a021a5b25eff8ab6e67ade9e2ebb9082e278c",
        "short_hash": "a12a021a",
        "subject": "test: remove dead embedded test files from code_puppy/plugins",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "bf58f6a183e39d85e7dfb6ce7018f09480cfa08c",
        "short_hash": "bf58f6a1",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "8f0006c894b9778bb694aedcea05c5df6fc75638",
        "short_hash": "8f0006c8",
        "subject": "test: round-6 max-aggression blast (budgets doubled for 50k-LOC hunt)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "4327605c4d1298942e665b247da9e6ddb5521727",
        "short_hash": "4327605c",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "c4f77bb9444de21d34b8a23bdf36b800eb0f0e5d",
        "short_hash": "c4f77bb9",
        "subject": "fix: share compact Android banner detection (#723)",
        "author": "mpfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "6d7a4de2fc616d004e96beb27bb5246c67430e1d",
        "short_hash": "6d7a4de2",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "eb86bfa326d9569019221b2a29043285aceb37e2",
        "short_hash": "eb86bfa3",
        "subject": "Merge remote-tracking branch 'origin/main'",
        "author": "mpfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "da2921ec58bfac3ef9c2bbd71d3d8d9004a7deaa",
        "short_hash": "da2921ec",
        "subject": "fix: use compact Android startup banner (#722)",
        "author": "mpfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "2fe3267d454a05ec6e1700a6b244809628abc0aa",
        "short_hash": "2fe3267d",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "bcae2d59303cce0a8241619c23455a4654b1c672",
        "short_hash": "bcae2d59",
        "subject": "docs: add Android Termux installation guide (#721)",
        "author": "mpfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "693113170acae7b0872b93c15e423b25703e8c32",
        "short_hash": "69311317",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "706da69a2f7eae0a872de7c56c668710876ce848",
        "short_hash": "706da69a",
        "subject": "fix: skip bundled ripgrep on Android (#720)",
        "author": "mpfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "48c16b2345d343226097bf27393095c394ff4740",
        "short_hash": "48c16b23",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "5a8f3d6a2ddf54770fc6c9c6fdfeb6d2b4b84c08",
        "short_hash": "5a8f3d6a",
        "subject": "test: restore chatgpt_oauth usage cache in test to fix cross-test pollution",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "e2c613a058b9494959062affea6d6a14fc47a8f5",
        "short_hash": "e2c613a0",
        "subject": "test: round-5 aggressive redundancy blast (per-namespace spend budgets)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "afddbc2b1061753940e535857e009bf0d7228193",
        "short_hash": "afddbc2b",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "70a31dd48fbda1d69aba3660ae79eac1040dde71",
        "short_hash": "70a31dd4",
        "subject": "Fix Android browser import regression test (#719)",
        "author": "mpfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "0ac6710480af861278a4b64e828d830fbcf5ead1",
        "short_hash": "0ac67104",
        "subject": "Merge origin/main for Android exclusion (#718)",
        "author": "mpfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "138ffbbdfaf2fb45b902b2f555abcdce552d4a5c",
        "short_hash": "138ffbbd",
        "subject": "Exclude Playwright on Android (#718)",
        "author": "mpfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "0204236ae90b9074b88ef382113def19af059f24",
        "short_hash": "0204236a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "931c86816dde5ddff16c2e03b91551821a9e7abc",
        "short_hash": "931c8681",
        "subject": "Allow explicit curl fetches without delegation (#717)",
        "author": "mpfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "8fff8dad63d0703f2b44ed085a5757ca6970cbd3",
        "short_hash": "8fff8dad",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "4f2958a7d78b4423be8a958a81f79b5bbcc0ed6f",
        "short_hash": "4f2958a7",
        "subject": "test: round-4 redundancy removal (plugins, root, command_line, tools, mcp, agents, messaging)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "cb5a83b77b99ed160c5f0c8f50f31f044c14fcff",
        "short_hash": "cb5a83b7",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "d875dddecf2f6be70ec89c4458ca4968ee9c1cfa",
        "short_hash": "d875ddde",
        "subject": "ci: make version-bump push resilient to concurrent main pushes",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "83c05d2402b981d1f04db682b52ad84db837b80d",
        "short_hash": "83c05d24",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "ce428825543bb71621c892a3a482e9924f3cec1f",
        "short_hash": "ce428825",
        "subject": "test: round-3 redundancy removal (tools, mcp, agents, messaging, i18n, hook_engine)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "837b37720a3464269215260d1e88af972198fca6",
        "short_hash": "837b3772",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "2da13b0c7b4b71c5de856feab628a971dea74f0e",
        "short_hash": "2da13b0c",
        "subject": "test: round-3 root test reduction (-1.5k LOC via parametrization, -0.03pp coverage)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "6370bb6bdd2d632f0ca8a79d5c1f87426394124a",
        "short_hash": "6370bb6b",
        "subject": "test: fold custom_server_installer parametrize matrix (round-3 command_line)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "f91d31003af09a80dc2d219b076c1c57f5138dd5",
        "short_hash": "f91d3100",
        "subject": "test: round-3 command_line reduction (parametrize folds + subsumed deletions)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-09"
      },
      {
        "hash": "aa1845d240a50f2ace667709dcfd6aca56167aa2",
        "short_hash": "aa1845d2",
        "subject": "test: round-3 reduction of tests/plugins (-3.7k LOC, -0.13pp coverage)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-08"
      },
      {
        "hash": "35259bbedd67b5e57a974b7103e0020fdf86a6a6",
        "short_hash": "35259bbe",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-09"
      },
      {
        "hash": "3881559c912a7ce8775e0c436dcc96b0c3461693",
        "short_hash": "3881559c",
        "subject": "test: cut 40k lines of redundant tests (~18% LOC down, 1.2pp coverage cost)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-08"
      },
      {
        "hash": "e0b7188aae41d8d2f0453e85eb60d5fc080cea20",
        "short_hash": "e0b7188a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-08"
      },
      {
        "hash": "5d3d429dea773dbf61c3ea708e8573ba7b22d0a2",
        "short_hash": "5d3d429d",
        "subject": "Merge pull request #675 from JulienEllie/fix/subagent-session-persistence",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-08"
      },
      {
        "hash": "bdb700764e62d8ccd0719a6bccc4174fe73352be",
        "short_hash": "bdb70076",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-07"
      },
      {
        "hash": "23b4d1feb52c547dddb5f8398adafca932e0bb6f",
        "short_hash": "23b4d1fe",
        "subject": "Merge pull request #713 from thomwebb/feat/namespace-skill-search",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-07"
      },
      {
        "hash": "0b16ce2fc462e1de9e8c0f8f03284b1a73b06453",
        "short_hash": "0b16ce2f",
        "subject": "docs: note that the first skill tag sets its namespace",
        "author": "TJ Webb",
        "date": "2026-08-07"
      },
      {
        "hash": "c07f39e557b1db39e9da4e3b8a32c9a5209a39d8",
        "short_hash": "c07f39e5",
        "subject": "Split code-puppy-agent skill into topic reference docs",
        "author": "TJ Webb",
        "date": "2026-08-07"
      },
      {
        "hash": "99c6d49481cc0a115c02f18bdfee2119b9c71776",
        "short_hash": "99c6d494",
        "subject": "Add user-facing docs for skill namespaces",
        "author": "TJ Webb",
        "date": "2026-08-07"
      },
      {
        "hash": "c41a76c8fb07beab83320aa51984b43bd5200cd1",
        "short_hash": "c41a76c8",
        "subject": "Address adversarial review findings",
        "author": "TJ Webb",
        "date": "2026-08-07"
      },
      {
        "hash": "c8557ce2ff56432036be1aa1a8331f5cf2cae905",
        "short_hash": "c8557ce2",
        "subject": "Add namespace_skill_search plugin",
        "author": "TJ Webb",
        "date": "2026-08-07"
      },
      {
        "hash": "94204ef429edfa787b056cfd877350fb5086d5e8",
        "short_hash": "94204ef4",
        "subject": "Removed dead get_file_icon.",
        "author": "Jack Yao",
        "date": "2026-08-07"
      },
      {
        "hash": "62fa01ac8313608439436b95f329f7ac1ebbe0e0",
        "short_hash": "62fa01ac",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-07"
      },
      {
        "hash": "505e91c3d827b841726bf2b02bdd13eae8ba8685",
        "short_hash": "505e91c3",
        "subject": "Merge pull request #700 from thomwebb/agent-web-retriever",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-06"
      },
      {
        "hash": "ee1bd8a4f6dd90924478511e334232681a1eb407",
        "short_hash": "ee1bd8a4",
        "subject": "Merge pull request #702 from breedx/feat/opus-xhigh-effort",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-06"
      },
      {
        "hash": "923135bbdb5c8d728a5b773305cf127b5a637c20",
        "short_hash": "923135bb",
        "subject": "Merge pull request #707 from piercebrookins/feat/meta-muse-oauth",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-06"
      },
      {
        "hash": "226e8cb38bdc0033551956bfe22364d1d7d6eff9",
        "short_hash": "226e8cb3",
        "subject": "Merge pull request #710 from ryan-duve/main",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-06"
      },
      {
        "hash": "dd118995d133135ec4a91d4c6495e86281a12125",
        "short_hash": "dd118995",
        "subject": "Fix claude_code_oauth pasted callback functionality for reauth",
        "author": "ryan-duve",
        "date": "2026-08-06"
      },
      {
        "hash": "c0e262470131b86a0f0d0bc284587128a17c05d2",
        "short_hash": "c0e26247",
        "subject": "feat: add Meta Muse OAuth provider",
        "author": "Pierce Brookins",
        "date": "2026-08-05"
      },
      {
        "hash": "3f6cb124cf603ee800e6d5e4060e490cca9e9ca8",
        "short_hash": "3f6cb124",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-05"
      },
      {
        "hash": "183ef9265c9e7bef19abf1f6f8f810dc92c71c65",
        "short_hash": "183ef926",
        "subject": "Merge pull request #654 from thomwebb/feat/i18n-extract-config-wizard",
        "author": "TJ",
        "date": "2026-08-05"
      },
      {
        "hash": "27128713791910be9bab242b90fbdb1a2b53f9bb",
        "short_hash": "27128713",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-05"
      },
      {
        "hash": "41482504c7d29e2e4f2d99edab58a336c6322b27",
        "short_hash": "41482504",
        "subject": "Merge remote-tracking branch 'upstream/main' into feat/i18n-extract-config-wizard",
        "author": "TJ Webb",
        "date": "2026-08-05"
      },
      {
        "hash": "2b250e2b23204aa99b0b01d0fb1900850276620f",
        "short_hash": "2b250e2b",
        "subject": "Merge pull request #655 from thomwebb/feat/i18n-extract-session-commands",
        "author": "TJ",
        "date": "2026-08-05"
      },
      {
        "hash": "40a422000f5808b8d4fba099f217bd4b9c0d9d91",
        "short_hash": "40a42200",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-05"
      },
      {
        "hash": "fe7d093e387e2bd26042a0c49a099149bacaff0b",
        "short_hash": "fe7d093e",
        "subject": "Merge pull request #701 from Prathap-P/fix/streaming-retry-progress-reset-backoff",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-05"
      },
      {
        "hash": "0bf8118227bc392ea4a7e2438aad4c67c8ba912d",
        "short_hash": "0bf81182",
        "subject": "fix(model-settings): preserve callable compatibility safely",
        "author": "breedx",
        "date": "2026-08-05"
      },
      {
        "hash": "9c6a796d6dcf3b0739daabeeba41a05c6253461d",
        "short_hash": "9c6a796d",
        "subject": "fix(model-settings): keep catalog loads out of repaints",
        "author": "breedx",
        "date": "2026-08-05"
      },
      {
        "hash": "e787168d7e2f149543ef439e8d0a584d3382ab43",
        "short_hash": "e787168d",
        "subject": "feat(model-settings): add xhigh adaptive effort",
        "author": "breedx",
        "date": "2026-08-05"
      },
      {
        "hash": "9c7df7bcdd5456aa2c8870de5d02a63e3bd77d18",
        "short_hash": "9c7df7bc",
        "subject": "fix(retry): progress reset must use minimum backoff, not maximum",
        "author": "Prathap",
        "date": "2026-08-05"
      },
      {
        "hash": "e8b9989d88a5b2024e2862175adf8577b3f3f504",
        "short_hash": "e8b9989d",
        "subject": "fix(subagents): make the parent agent aware of an interrupted sub-agent",
        "author": "Julien Ellie",
        "date": "2026-08-04"
      },
      {
        "hash": "f24ee81fd2e116ffb140f7759e8a91cda86c5349",
        "short_hash": "f24ee81f",
        "subject": "fix(subagents): persist interrupted sessions so Ctrl-C is resumable",
        "author": "Julien Ellie",
        "date": "2026-08-04"
      },
      {
        "hash": "3e1949dc9618fff75ec9c98c8f5f72ec826d86d6",
        "short_hash": "3e1949dc",
        "subject": "Address adversarial review findings on web-retriever",
        "author": "TJ Webb",
        "date": "2026-08-04"
      },
      {
        "hash": "4e5705add3fc6076f12e2862bb9a18f8b92ed880",
        "short_hash": "4e5705ad",
        "subject": "Add web-retriever agent for browser automation and scraping",
        "author": "TJ Webb",
        "date": "2026-08-04"
      },
      {
        "hash": "c7278a909db29c87d25f9792b7dfe0c4244a5891",
        "short_hash": "c7278a90",
        "subject": "Merge upstream main and resolve i18n catalogs",
        "author": "TJ Webb",
        "date": "2026-08-03"
      },
      {
        "hash": "09085be5b3229238e06e7f8854dca59c171a301d",
        "short_hash": "09085be5",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-03"
      },
      {
        "hash": "3cacb1106484efcdca3ec31b30cc70f58d249a03",
        "short_hash": "3cacb110",
        "subject": "Merge pull request #656 from thomwebb/fix/i18n-audit-false-positives",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-03"
      },
      {
        "hash": "b25b163d7418b43c8e313c940af2b6c6e38e0ae0",
        "short_hash": "b25b163d",
        "subject": "Merge pull request #687 from mwmoreno/feature/granular-command-guard-allowlist",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-03"
      },
      {
        "hash": "ab601a23747eaaffaffc468b2515d8c4235f24e1",
        "short_hash": "ab601a23",
        "subject": "Merge pull request #653 from thomwebb/feat/i18n-extract-claude-oauth",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-03"
      },
      {
        "hash": "a0dd5f459f06839678f4ef161b187203f090f413",
        "short_hash": "a0dd5f45",
        "subject": "Merge pull request #692 from breedx/fix/mcp-config-cannot-be-its-own-project-twin",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-03"
      },
      {
        "hash": "12276aa989cc2d4efa9870d81418d9507e55d9db",
        "short_hash": "12276aa9",
        "subject": "feat(herdr): add Windows named-pipe transport",
        "author": "weegens-aaron",
        "date": "2026-08-01"
      },
      {
        "hash": "2434cbde6ecd5bee3826b621321cda9f6433a785",
        "short_hash": "2434cbde",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-01"
      },
      {
        "hash": "65ab06eaba76892697f41bb929e848e41842eac1",
        "short_hash": "65ab06ea",
        "subject": "fix(fork): /fork now snapshots the conversation at fork time",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-01"
      },
      {
        "hash": "b573b527c199ac538376e47ecf1d360c76d6b075",
        "short_hash": "b573b527",
        "subject": "Make file tools primary args required (file_path/search_string/content/replacements/snippet) (#694)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-01"
      },
      {
        "hash": "343879761b1eb940e2f40c07c4db897e306013d2",
        "short_hash": "34387976",
        "subject": "Fix empty shell command to return clean ShellCommandOutput, require command arg (#693)",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-01"
      },
      {
        "hash": "d08b6c97bec759e468d3ea421e6b3bfc7dedda82",
        "short_hash": "d08b6c97",
        "subject": "feat(model-settings): user-defined custom request params per model",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-01"
      },
      {
        "hash": "533552b24f6752440f5eaf3ae6dc7a3bbfab33af",
        "short_hash": "533552b2",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-08-01"
      },
      {
        "hash": "f10dc4ad85b5a9a1fe2c9187da3ebe832432d04a",
        "short_hash": "f10dc4ad",
        "subject": "test(reasoning): update tests to reflect renamed effort levels and config keys",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-01"
      },
      {
        "hash": "be82de3b7838079cc388409e9135a5ca2aa15ad3",
        "short_hash": "be82de3b",
        "subject": "feat(model-factory): add backward-compat aliases for legacy reasoning effort values",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-01"
      },
      {
        "hash": "fefb31b02bc9a78212e516f8810a89d3fe3ba6d3",
        "short_hash": "fefb31b0",
        "subject": "refactor(reasoning): rename ultra/minimal effort levels to max/none",
        "author": "Mike Pfaffenberger",
        "date": "2026-08-01"
      },
      {
        "hash": "6a9f539bf7df86767f85a474f9a5fbe55dbd7ac6",
        "short_hash": "6a9f539b",
        "subject": "fix(mcp): a config can't be its own untrusted project twin (CWD == $HOME)",
        "author": "breedx",
        "date": "2026-07-31"
      },
      {
        "hash": "0d7764e03a34959b2cea717521fc21c7f9d1692c",
        "short_hash": "0d7764e0",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-30"
      },
      {
        "hash": "37f5a9adf736df41e6465e6979aaab9f19b7ff03",
        "short_hash": "37f5a9ad",
        "subject": "fix(computer-use): require explicit opt-in (#688)",
        "author": "mpfaffenberger",
        "date": "2026-07-30"
      },
      {
        "hash": "baa95cefc63778c6320cad6654246e5d8102f503",
        "short_hash": "baa95cef",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-29"
      },
      {
        "hash": "bfc4927f209493b8a97fc968cf9f38af5734c21d",
        "short_hash": "bfc4927f",
        "subject": "Merge pull request #685 from mpfaffenberger/awtilso/PUP-549",
        "author": "Andrew Tilson",
        "date": "2026-07-29"
      },
      {
        "hash": "d297658b259cce5a4943e2aa004442885fbc0b7c",
        "short_hash": "d297658b",
        "subject": "docs(destructive-guard): add scoped AGENTS.md for the plugin",
        "author": "mwmoren",
        "date": "2026-07-29"
      },
      {
        "hash": "dc95797367d0a9035f54d7112c1331ac44c8e96e",
        "short_hash": "dc957973",
        "subject": "feat(guards): granular per-pattern allowlist for command guards",
        "author": "mwmoren",
        "date": "2026-07-29"
      },
      {
        "hash": "169f81e827d0543da3afc1e0c069ce2e3517679e",
        "short_hash": "169f81e8",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-28"
      },
      {
        "hash": "1a41a14795eb51f9ebf624bba82578772fe2d230",
        "short_hash": "1a41a147",
        "subject": "Merge pull request #686 from thomwebb/fix-valid-summary-request-part",
        "author": "TJ",
        "date": "2026-07-28"
      },
      {
        "hash": "a346bdfe92a9b2218cf5cb00288a6c8e7ee4f5b0",
        "short_hash": "a346bdfe",
        "subject": "Format compaction regression test",
        "author": "TJ Webb",
        "date": "2026-07-28"
      },
      {
        "hash": "830de857cd0dd1c67d7dd1c1a017097d4481f034",
        "short_hash": "830de857",
        "subject": "test: sync test_config.py snapshots with new subagent_recursion_limit_gpt_5_6 key",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-28"
      },
      {
        "hash": "9d2bd0ba24483bb925027d3e2a6cc7969b780f7e",
        "short_hash": "9d2bd0ba",
        "subject": "chore: ruff format",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-28"
      },
      {
        "hash": "21d94bba67bc53824b20147b76eb773b51b9d1fe",
        "short_hash": "21d94bba",
        "subject": "Make GPT-5.6 sub-agent depth cap tunable via /set",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-28"
      },
      {
        "hash": "604b31a8a051a91773605aa6c05fc4786548f32a",
        "short_hash": "604b31a8",
        "subject": "Exercise OpenAI summary message mapping",
        "author": "TJ Webb",
        "date": "2026-07-28"
      },
      {
        "hash": "7af7108b6b11959cb5e891663d87dab920f330c4",
        "short_hash": "7af7108b",
        "subject": "Fix invalid summary message part",
        "author": "TJ Webb",
        "date": "2026-07-28"
      },
      {
        "hash": "eb4c7af1dc22e008d28ff2160f8f652021a20fbb",
        "short_hash": "eb4c7af1",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-28"
      },
      {
        "hash": "c38f823df95a1c81de45c1aacb1effb32415cff1",
        "short_hash": "c38f823d",
        "subject": "Raise GPT-5.6 sub-agent depth cap from 1 to 2",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-28"
      },
      {
        "hash": "9a373fcf44ba576fedf50c0cfec95aa39dd0f0f0",
        "short_hash": "9a373fcf",
        "subject": "Merge pull request #684 from thomwebb/clarify-agent-model-optional",
        "author": "TJ",
        "date": "2026-07-28"
      },
      {
        "hash": "25f8b2a402d85769ad60422c3586cfc4f0154c20",
        "short_hash": "25f8b2a4",
        "subject": "Match schema example to runtime requirements",
        "author": "TJ Webb",
        "date": "2026-07-28"
      },
      {
        "hash": "b3d1987b2bff4b67fc1e3dd80cca2b1686bba900",
        "short_hash": "b3d1987b",
        "subject": "Keep agent ID in creator schema",
        "author": "TJ Webb",
        "date": "2026-07-28"
      },
      {
        "hash": "4719f6b0df44bc6f2e9d9031be0a3c5a540d3d2e",
        "short_hash": "4719f6b0",
        "subject": "Refresh Agent Creator model examples",
        "author": "TJ Webb",
        "date": "2026-07-28"
      },
      {
        "hash": "facafd1c6212a5e71d6b76d211e8a83ff37d3f89",
        "short_hash": "facafd1c",
        "subject": "Clarify optional agent model pinning",
        "author": "TJ Webb",
        "date": "2026-07-28"
      },
      {
        "hash": "1b5b370857c5ca534c6d40460205966913918557",
        "short_hash": "1b5b3708",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-28"
      },
      {
        "hash": "dddec902cabe913bb92b6f835e4b91900d012498",
        "short_hash": "dddec902",
        "subject": "Merge pull request #678 from mpfaffenberger/awtilso/PUP-544-scope-fix",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-28"
      },
      {
        "hash": "42b2f1b97f1180734d125d4d8b3750ab1145d0d6",
        "short_hash": "42b2f1b9",
        "subject": "Merge pull request #682 from thomwebb/chore/remove-empty-regional-locales",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-28"
      },
      {
        "hash": "ff359a84c12e292d61b2be00552ae077d5307163",
        "short_hash": "ff359a84",
        "subject": "Merge pull request #683 from piercebrookins/agent/add-macos-computer-use",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-28"
      },
      {
        "hash": "344c75ee79b156a64033db40c42f3c2d6052a021",
        "short_hash": "344c75ee",
        "subject": "fix(statusline): add utf-8 encoding kwargs to detect_git_branch subprocess call",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-28"
      },
      {
        "hash": "c010eef8c2cd3328cf2c3a40d9a0818d267daae5",
        "short_hash": "c010eef8",
        "subject": "Add native macOS computer use plugin",
        "author": "Pierce Brookins",
        "date": "2026-07-27"
      },
      {
        "hash": "d739bfb30601039c4ca5e79fb49ca937c5cc8122",
        "short_hash": "d739bfb3",
        "subject": "chore(i18n): remove empty regional locale stubs",
        "author": "TJ Webb",
        "date": "2026-07-27"
      },
      {
        "hash": "137a4361541009bb18eb07cdc1530e366c6a03ca",
        "short_hash": "137a4361",
        "subject": "Merge main into i18n Claude OAuth PR",
        "author": "TJ Webb",
        "date": "2026-07-27"
      },
      {
        "hash": "a139fca414c95ab7f90861a678f206fee77acf0a",
        "short_hash": "a139fca4",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-27"
      },
      {
        "hash": "d6975fe44fe0f94e2715b0f27210b02a727be4cd",
        "short_hash": "d6975fe4",
        "subject": "fix: rewrite detect_git_branch test to match temp-file implementation",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-27"
      },
      {
        "hash": "c0d42c7b3d9b477dafb9346c77ec60733d45f57b",
        "short_hash": "c0d42c7b",
        "subject": "fix(subagent): scope per-run token usage/timing to invoke_agent_with_model only",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-27"
      },
      {
        "hash": "252667878910f5b24f37093070e8199903aa565e",
        "short_hash": "25266787",
        "subject": "Merge pull request #649 from weegens-aaron/fix/flux-windows-os",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-27"
      },
      {
        "hash": "eed40e54e51196e0962e375a030db1d097a46693",
        "short_hash": "eed40e54",
        "subject": "Merge pull request #652 from thomwebb/feat/i18n-extract-core-commands",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-27"
      },
      {
        "hash": "c921a7c45f32cf39cba38948b45e1d18ab2e5627",
        "short_hash": "c921a7c4",
        "subject": "Merge pull request #668 from thomwebb/perf/theme-lazy-imports",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-27"
      },
      {
        "hash": "194503e3a9d1e651066b167fae570e43454c7f0d",
        "short_hash": "194503e3",
        "subject": "Merge pull request #673 from CarlosSantes/patch-2",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-27"
      },
      {
        "hash": "1d210f9c995ecd52a936b1cfdb3dd436796c9e75",
        "short_hash": "1d210f9c",
        "subject": "Merge pull request #677 from JulienEllie/feat/herdr-protocol-v16",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-27"
      },
      {
        "hash": "586f1021bc306ef3684e540613bd39775f249a98",
        "short_hash": "586f1021",
        "subject": "Merge pull request #676 from bporterfielddsc/fix/acp-windows-git-subprocess-hang",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-27"
      },
      {
        "hash": "52b3f45d43d968de634ca747350efed36e54a877",
        "short_hash": "52b3f45d",
        "subject": "test(herdr): add live smoke test against a real herdr pane",
        "author": "Julien Ellie",
        "date": "2026-07-26"
      },
      {
        "hash": "6a3a833521f96d6638cec1159f4d3d06be8e4368",
        "short_hash": "6a3a8335",
        "subject": "fix(acp): stop Windows subprocess pipe-drain deadlock hanging tool turns",
        "author": "Blayne Porterfield",
        "date": "2026-07-26"
      },
      {
        "hash": "faba4284e196ec50ca7ce9006ea43267647801a6",
        "short_hash": "faba4284",
        "subject": "feat(herdr): durable session references + finish protocol-16 docs",
        "author": "Julien Ellie",
        "date": "2026-07-26"
      },
      {
        "hash": "c0566cfc4ea705d9e9ff26342a907a1067fe7faa",
        "short_hash": "c0566cfc",
        "subject": "feat(herdr): add decorative activity messages via tool callbacks",
        "author": "Julien Ellie",
        "date": "2026-07-26"
      },
      {
        "hash": "ebbd66cc5635b3876f608ac228a8143ea709d717",
        "short_hash": "ebbd66cc",
        "subject": "feat(herdr): report pane metadata (model/context/tokens) at turn end",
        "author": "Julien Ellie",
        "date": "2026-07-26"
      },
      {
        "hash": "f8ffe01bd4742f05699cb0c2f7c53c44269d5d11",
        "short_hash": "f8ffe01b",
        "subject": "feat(herdr): harden transport with coalescing lanes + bounded release",
        "author": "Julien Ellie",
        "date": "2026-07-26"
      },
      {
        "hash": "99cc88e31a92350f1f9b139aca685a9fcc861ccd",
        "short_hash": "99cc88e3",
        "subject": "refactor(token-usage): promote usage estimator to core module",
        "author": "Julien Ellie",
        "date": "2026-07-26"
      },
      {
        "hash": "a6790dbea918a5defcf7ffc6c0e39dfa791d6022",
        "short_hash": "a6790dbe",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-25"
      },
      {
        "hash": "cd5889953c93a584ef2a49250d63d3cdadabe6fe",
        "short_hash": "cd588995",
        "subject": "feat(chatgpt_oauth): support reference images in codex_imagegen",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-25"
      },
      {
        "hash": "d61a26ceca644bafe968c588d584afb0f4d29546",
        "short_hash": "d61a26ce",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-25"
      },
      {
        "hash": "46a6f780ce5803302ee1503e7528e697de8167ee",
        "short_hash": "46a6f780",
        "subject": "Merge pull request #674 from mpfaffenberger/awtilso/PUP-544",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-25"
      },
      {
        "hash": "8a4b7becd8491ce8212e3782919fd318f89f10f0",
        "short_hash": "8a4b7bec",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-25"
      },
      {
        "hash": "d7978d7b1a444afb2ef2ea45b6758046fdb8ec4a",
        "short_hash": "d7978d7b",
        "subject": "fix(herdr): silence user-initiated menus",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-25"
      },
      {
        "hash": "9af11a3e392e7113e8bfae5db0f2484104aabe95",
        "short_hash": "9af11a3e",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-25"
      },
      {
        "hash": "f2c0848ddacbf6b5d773828267d6b18ae922501e",
        "short_hash": "f2c0848d",
        "subject": "feat(claude_code_oauth): add claude-opus-5 support",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-25"
      },
      {
        "hash": "67f1161f314a68e054ca2407341fb146600f896c",
        "short_hash": "67f1161f",
        "subject": "style: apply ruff format to usage instrumentation and tests",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-24"
      },
      {
        "hash": "54b7688439d3e802ffb1669138090d22ff6a7375",
        "short_hash": "54b76884",
        "subject": "feat(subagent): break out cache tokens and add run timestamps",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-24"
      },
      {
        "hash": "ccc81e7cdc1c49fd467c654bce090a9fbe5cd48f",
        "short_hash": "ccc81e7c",
        "subject": "feat(subagent): report per-run token usage and latency",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-24"
      },
      {
        "hash": "a4610752e1ef2c5675c688194fef22a7bfa26b67",
        "short_hash": "a4610752",
        "subject": "Update French Canadian translations in fr-CA.json",
        "author": "CarlosSantes",
        "date": "2026-07-24"
      },
      {
        "hash": "82e12de7084ead45832a9c2334e9c668448c48c6",
        "short_hash": "82e12de7",
        "subject": "i18n(fr-CA): restore pre-existing 15 keys byte-for-byte for in-flight translator work",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "429eb24d3d0dbabad5d1aa5fecaf5d25f93982db",
        "short_hash": "429eb24d",
        "subject": "i18n(fr-CA): restore pre-existing 15 keys byte-for-byte for in-flight translator work",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "dae0e568924e28d90fd50b42b9095a919f5f7ef8",
        "short_hash": "dae0e568",
        "subject": "i18n(fr-CA): restore pre-existing 15 keys byte-for-byte for in-flight translator work",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "4989844ebb21ff4e2fe6231821eeebfaf2411e1e",
        "short_hash": "4989844e",
        "subject": "i18n(fr-CA): restore pre-existing 15 keys byte-for-byte for in-flight translator work",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "dc6f5f199c24b7423e9ce6968a1b3ec95fb8f8d1",
        "short_hash": "dc6f5f19",
        "subject": "i18n(es,fr-CA): apply adversarial review fixes (semantic + QC typography)",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "b7ca9d32cd36a5d2929281b5bf69daff541471f0",
        "short_hash": "b7ca9d32",
        "subject": "i18n(es,fr-CA): apply adversarial review fixes (semantic + QC typography)",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "211bc543bb0b173c32e4aade3ac650cee4ee71ca",
        "short_hash": "211bc543",
        "subject": "i18n(es,fr-CA): apply adversarial review fixes (semantic + QC typography)",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "3a37a83994305436168de7968e14ec5638c30db3",
        "short_hash": "3a37a839",
        "subject": "i18n(es,fr-CA): apply adversarial review fixes (semantic + QC typography)",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "91b3f658e08b940152d98c2fda67c0e5fe96c50e",
        "short_hash": "91b3f658",
        "subject": "i18n(es,fr-CA): translate 35 new keys from PR #655 (session/compact commands)",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "20db3b029d05b8800fdf0b9a8ce581ca8e0518b9",
        "short_hash": "20db3b02",
        "subject": "i18n(es,fr-CA): translate 39 new keys from PR #654 (mcp_config_wizard)",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "49f000cafc78336cd86345660a1d178c4df56cde",
        "short_hash": "49f000ca",
        "subject": "i18n(es,fr-CA): translate 48 new keys from PR #653 (claude_code_oauth)",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "c542ca785301b14c7e45c81b2e2adeb808f3432b",
        "short_hash": "c542ca78",
        "subject": "i18n(es,fr-CA): translate 32 new keys from PR #652 (core_commands)",
        "author": "TJ Webb",
        "date": "2026-07-24"
      },
      {
        "hash": "bf548837d21e3990f6707f15f83d717fca7c9f53",
        "short_hash": "bf548837",
        "subject": "review: address adversarial-review feedback on theme lazy PR",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "8909a9771e3044a39b6673208c5f8f24089cc409",
        "short_hash": "8909a977",
        "subject": "style(theme): restore literal palette emoji character",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "cc183da4df2e9235ec1cf9f98c6e617221fa6fc9",
        "short_hash": "cc183da4",
        "subject": "docs(theme): rewrite import-note comment to drop stale doc reference",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "0de2cb7503711b0a1e54ccc169505e78da8a9011",
        "short_hash": "0de2cb75",
        "subject": "chore: drop docs/STARTUP_PERFORMANCE.md from this PR",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "01637eb9c1318903981571bea83b7e853c730a46",
        "short_hash": "01637eb9",
        "subject": "style(tests): apply ruff format to theme test patch retargets",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "938e3359e689448048bfac2d88dca0f188caab8c",
        "short_hash": "938e3359",
        "subject": "docs(perf): reprioritise startup perf plan based on interactive-launch profiling",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "ea805e947b5037b2b72ac73e40a8fbd34aa1fd3d",
        "short_hash": "ea805e94",
        "subject": "perf(theme): defer heavy imports until user actions need them",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "9aaf9516269bfafa1caf80a422651c5bb624f64f",
        "short_hash": "9aaf9516",
        "subject": "Merge pull request #672 from AndrewTilson/awtilso/PUP-543",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-24"
      },
      {
        "hash": "5058379812e5cb5c6c7e397b14539300cdc89e24",
        "short_hash": "50583798",
        "subject": "feat: add @model autocomplete to /fork command",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-23"
      },
      {
        "hash": "546ffbb5de9376c8a52d48f5bafd6ae04ef981e4",
        "short_hash": "546ffbb5",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-24"
      },
      {
        "hash": "1ee0b143fb29bcdb322e9edf7c92b3952d2c40ec",
        "short_hash": "1ee0b143",
        "subject": "fix(subagents): stop injecting AGENTS.md rules into sub-agent prompts",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-24"
      },
      {
        "hash": "9df4b1b50bd88ccf39eb8e87be85bfa52f02dc23",
        "short_hash": "9df4b1b5",
        "subject": "fix(ask_user_question): defer on_prompt_toolkit_style import in tui_loop",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-24"
      },
      {
        "hash": "0ddbe48bd79c800ac5bd27343e759fe75391cece",
        "short_hash": "0ddbe48b",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-24"
      },
      {
        "hash": "e2ecf9465957c83395c206aa5b636ed62425db04",
        "short_hash": "e2ecf946",
        "subject": "Merge pull request #670 from mpfaffenberger/fix/publish-race",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-24"
      },
      {
        "hash": "266225dc1f4efb6fe700e8531c738ba5f2daa878",
        "short_hash": "266225dc",
        "subject": "style(i18n): ruff-format claude_oauth namespace refactor",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "44f98c483a36883cf9ddfe1e8d906dcde6c06005",
        "short_hash": "44f98c48",
        "subject": "fix(i18n/audit): fail loud on nonexistent root path",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "f733054d1b27c6dcbdf8a63d58661e687e69ca0b",
        "short_hash": "f733054d",
        "subject": "fix(i18n): address PR #655 review — safe catalog interpolation + UX/grammar",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "ddb1d19b2a70dc041cdfd8eefb1bcdc798da543c",
        "short_hash": "ddb1d19b",
        "subject": "fix(mcp): restore re-prompt on invalid server type input",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "b49f754ab9a1f8b8b0db90212a08252c19a4fa5e",
        "short_hash": "b49f754a",
        "subject": "fix(i18n): preserve original picker_failed wording per review",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "ec1c5d457706b7f63d1a85be56048226f8951a7e",
        "short_hash": "ec1c5d45",
        "subject": "refactor(i18n): move Claude-specific keys to oauth.claude.* namespace",
        "author": "TJ Webb",
        "date": "2026-07-23"
      },
      {
        "hash": "27bb1ead096f11832d68436530ad69791867835b",
        "short_hash": "27bb1ead",
        "subject": "fix(i18n/audit): fix FormattedValue false negative and non-existent path silent zero",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "f5b3d0cb334090385a5cb07c3f60b247d5e9a82d",
        "short_hash": "f5b3d0cb",
        "subject": "fix(i18n): address review feedback on session_commands extraction",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "fbef51c95e480fd2aa732f4e5c74cb588fbc5258",
        "short_hash": "fbef51c9",
        "subject": "fix(i18n): address review feedback on config_wizard extraction",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "d45534489d728082fbd21bb80e68813fd3d08d88",
        "short_hash": "d4553448",
        "subject": "fix(i18n): rename loop var to unshadow module-level t()",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "7d972ae66302ea914f5fd481426dfcf5077d7f6a",
        "short_hash": "7d972ae6",
        "subject": "fix(i18n): wire remaining oauth raw sites and add structural test",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "f77f36542acc8b3be45fda322c6b3fcfb40a2165",
        "short_hash": "f77f3654",
        "subject": "fix(i18n/audit): eliminate false positives in raw-site classification",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "5c91a1eaeb9d2c7077364b11f516f7495ae5d8af",
        "short_hash": "5c91a1ea",
        "subject": "feat(i18n): extract session_commands.py strings",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "f91204487c99b090bd45c30907ce415edba0db86",
        "short_hash": "f9120448",
        "subject": "fix(i18n): address review feedback on config_wizard extraction",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "9444533b8fd9ce9cb8d81ca490918490d125d6b8",
        "short_hash": "9444533b",
        "subject": "fix(i18n): address review feedback on core_commands extraction",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "11bc76ad9005fd8eaf9d550c49ed56912b926485",
        "short_hash": "11bc76ad",
        "subject": "fix(i18n): address review feedback on claude_code_oauth extraction",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "e4f8d9da4facee3e3dbef8b12046f1acb32c4aa4",
        "short_hash": "e4f8d9da",
        "subject": "feat(i18n): extract mcp_/config_wizard.py strings",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "d6635f28552fa93635c1db771029138a05d43ade",
        "short_hash": "d6635f28",
        "subject": "feat(i18n): extract core_commands.py user-facing strings",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "930d8ea1ab1ec660dc8a4570a963357f015ffcac",
        "short_hash": "930d8ea1",
        "subject": "feat(i18n): extract claude_code_oauth/register_callbacks.py strings",
        "author": "TJ Webb",
        "date": "2026-07-20"
      },
      {
        "hash": "3d0d0c9caa1c4cb980829894dbb86e26f3bfab71",
        "short_hash": "3d0d0c9c",
        "subject": "fix(ci): serialize PyPI publishes and self-heal version collisions",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-23"
      },
      {
        "hash": "f9db66cb7881d34cfecb2e21c943eed807819938",
        "short_hash": "f9db66cb",
        "subject": "chore: sync version to 0.0.662 already published on PyPI [ci skip]",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-23"
      },
      {
        "hash": "30cfead5540f08ae104ccc68e8e37017273ec1e2",
        "short_hash": "30cfead5",
        "subject": "Merge pull request #669 from mpfaffenberger/fix/pin-ruff",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-23"
      },
      {
        "hash": "119483df15a36f10b344f0a71d8ad0a3c881584d",
        "short_hash": "119483df",
        "subject": "fix(ci): pin ruff to >=0.15,<0.16 to stop default-ruleset drift",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-23"
      },
      {
        "hash": "4cab0a17a2804ea27c0707089cbc0db452f76552",
        "short_hash": "4cab0a17",
        "subject": "chore: ignore .worktrees/ local git worktree dir",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-23"
      },
      {
        "hash": "5ae287b67060a133ebff99a2166df370eb03fe3e",
        "short_hash": "5ae287b6",
        "subject": "feat: timestamp_heartbeat plugin — stamp __SYS_TIMESTAMP__ into tool results every k calls",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-23"
      },
      {
        "hash": "febc1da23f2fbee35d3bb0c87d1481cb5c01e85a",
        "short_hash": "febc1da2",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-23"
      },
      {
        "hash": "cb294274d93f35b74b5c0b884803a8c34cb4583c",
        "short_hash": "cb294274",
        "subject": "fix: splice only summary output into compacted context, not new_messages()",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-23"
      },
      {
        "hash": "e2862642d4e0d34e833299b687693fa1df567249",
        "short_hash": "e2862642",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-23"
      },
      {
        "hash": "b519df918aaebf1986d2c0e71c4d00fdc6780dc5",
        "short_hash": "b519df91",
        "subject": "feat: inject sub-agent identity/depth prompt to deter recursive delegation",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-23"
      },
      {
        "hash": "18cc3e39436924c9efba54bace8333582e8ab38f",
        "short_hash": "18cc3e39",
        "subject": "chore: bump version [ci skip]",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-22"
      },
      {
        "hash": "90fde59962697e0482b2daa939144d85447c656d",
        "short_hash": "90fde599",
        "subject": "feat: resume interrupted goals by UUID (#657)",
        "author": "Pierce Brookins",
        "date": "2026-07-22"
      },
      {
        "hash": "df0b6c3e78ec102edb16e4be36cf7c27179a5000",
        "short_hash": "df0b6c3e",
        "subject": "feat(config): add puppy_token provider hook for plugin-based credential backends (#666)",
        "author": "Greg Kinne",
        "date": "2026-07-22"
      },
      {
        "hash": "8d6fb6b2e56485a58aaed499d2f1963bbd038030",
        "short_hash": "8d6fb6b2",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-21"
      },
      {
        "hash": "350c5c66b934472a3a25ab403dda2c82f8d9b169",
        "short_hash": "350c5c66",
        "subject": "feat: cap nested sub-agent invocation depth (#662)",
        "author": "TJ",
        "date": "2026-07-21"
      },
      {
        "hash": "25bf282e5c6f20899492107844988659b77f81f0",
        "short_hash": "25bf282e",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-21"
      },
      {
        "hash": "4c6fd35a16af41fc43c5cecf92f1d093725cbfcf",
        "short_hash": "4c6fd35a",
        "subject": "Merge pull request #663 from AndrewTilson/fix/subagent-panel-root-eviction-and-browser-cleanup-hang",
        "author": "Andrew Tilson",
        "date": "2026-07-21"
      },
      {
        "hash": "3f9149069335f52c7db1011cd7daf756204d35da",
        "short_hash": "3f914906",
        "subject": "fix: subagent_panel root eviction + browser_close cleanup hang",
        "author": "Andrew Tilson",
        "date": "2026-07-21"
      },
      {
        "hash": "0514fa4fd5d1aeb8b899d794cf797759f1100a90",
        "short_hash": "0514fa4f",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-21"
      },
      {
        "hash": "6faab5052dc5b93c3a63dfaa48135897e6a82a0e",
        "short_hash": "6faab505",
        "subject": "fix: make OpenAI reasoning settings per-model",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-21"
      },
      {
        "hash": "a1cc28cd9002b2ddfea4961082b12f52266f6979",
        "short_hash": "a1cc28cd",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-21"
      },
      {
        "hash": "ccea8af4835507373fd84996666886b489ea2212",
        "short_hash": "ccea8af4",
        "subject": "fix: coordinate JediTerm inline streaming output",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-21"
      },
      {
        "hash": "67b3957c93ad77e7b030e2c29925ea1f322f2009",
        "short_hash": "67b3957c",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-21"
      },
      {
        "hash": "ecd9d5ff58b4e85cf78307a783529ff3ec5877fa",
        "short_hash": "ecd9d5ff",
        "subject": "chore: bump patch version to 0.0.653",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-21"
      },
      {
        "hash": "5ce59755116b81e63f95b3d1d21aaffcf77aba4c",
        "short_hash": "5ce59755",
        "subject": "feat: gate GPT-5.6 family models behind per-tool guardrails (#648)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-21"
      },
      {
        "hash": "ce12fe70591e679d2a689e54873acef9778867c1",
        "short_hash": "ce12fe70",
        "subject": "feat: add Codex OAuth image generation",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-21"
      },
      {
        "hash": "f0dab86655577094868b9ed3114038242b946d39",
        "short_hash": "f0dab866",
        "subject": "feat: add GPT-5.6 reasoning context and mode",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-20"
      },
      {
        "hash": "0aa91c28963d65fe50f66590b67a5b05ff436e26",
        "short_hash": "0aa91c28",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-20"
      },
      {
        "hash": "0d819949e7e4f824b3388e7472d1d19c76f86d53",
        "short_hash": "0d819949",
        "subject": "feat: default to summarization compaction (#651)",
        "author": "Pierce Brookins",
        "date": "2026-07-20"
      },
      {
        "hash": "267012713be58c0edec4cb575a68e3f0e2b666b2",
        "short_hash": "26701271",
        "subject": "feat(i18n): extract config_commands.py user-facing strings (#647)",
        "author": "TJ",
        "date": "2026-07-20"
      },
      {
        "hash": "37c78a61ab29ed0b6f4ab65ff3098f87310ea1d3",
        "short_hash": "37c78a61",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-19"
      },
      {
        "hash": "0ed6911be92a90286a6160cd4800374a84b17d13",
        "short_hash": "0ed6911b",
        "subject": "test: fix 5 stale tests broken by empty-by-default models.json",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-19"
      },
      {
        "hash": "df6d2362c3326a3486e787de6958eb73e853858b",
        "short_hash": "df6d2362",
        "subject": "fix: force UTF-8 through the exec-command pipe (Windows cp1252 crash)",
        "author": "weegens-aaron",
        "date": "2026-07-18"
      },
      {
        "hash": "dd92c1321aaa9dd184fcf412e6a9c92e8f667f7d",
        "short_hash": "dd92c132",
        "subject": "feat(i18n): extract cli_runner.py user-facing strings (PUP-480) (#646)",
        "author": "TJ",
        "date": "2026-07-18"
      },
      {
        "hash": "80d347bb22e02b02bfcb30bcbb5b4985d9fe9744",
        "short_hash": "80d347bb",
        "subject": "feat(i18n): static extraction audit tool for CLI strings (#645)",
        "author": "TJ",
        "date": "2026-07-18"
      },
      {
        "hash": "b8c8055b7fe9bdaab3792611756f16206d064e1a",
        "short_hash": "b8c8055b",
        "subject": "fix(i18n): stop routing Latin American Spanish through removed es-419 (#644)",
        "author": "TJ",
        "date": "2026-07-18"
      },
      {
        "hash": "fad8955be054ad3eb26d9efe1fef2ebeb013ced4",
        "short_hash": "fad8955b",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-18"
      },
      {
        "hash": "b4c493418de9fa83873ca997e31c552cac1dee27",
        "short_hash": "b4c49341",
        "subject": "style: apply ruff formatting",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-18"
      },
      {
        "hash": "9104eb06f5ed815b424455c80fb69905239f8ac9",
        "short_hash": "9104eb06",
        "subject": "Pr 518 Add Flux (#643)",
        "author": "Luc M",
        "date": "2026-07-18"
      },
      {
        "hash": "321b9aae320803ae3edbecc6f17d1ddb8489fa18",
        "short_hash": "321b9aae",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-18"
      },
      {
        "hash": "7ee8949e33051a78b35919833f622d6d818b572f",
        "short_hash": "7ee8949e",
        "subject": "chore: bump version to 0.0.648",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-18"
      },
      {
        "hash": "366b3078942aa776a4e20b6a59e373f2b486294f",
        "short_hash": "366b3078",
        "subject": "fix: request 1h prompt-cache TTL for claude-code-* OAuth models (#640)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-18"
      },
      {
        "hash": "bf3b5af5db7035fe69f2462983f881a76c0e7986",
        "short_hash": "bf3b5af5",
        "subject": "Fix /cd autocomplete for bare tilde home paths (#638)",
        "author": "Bill Kramme",
        "date": "2026-07-18"
      },
      {
        "hash": "e14d3a575a7247b7f8de2e01ed6884abc016fd80",
        "short_hash": "e14d3a57",
        "subject": "fix: resolve git worktrees to main repo wing in kennel (#516)",
        "author": "Amit Jain",
        "date": "2026-07-18"
      },
      {
        "hash": "939e1d2cf4b0b9c1b2145221cee84e8f39d39db1",
        "short_hash": "939e1d2c",
        "subject": "Polish base Spanish catalog and deprecate es-419 (#639)",
        "author": "ellysarai13-blip",
        "date": "2026-07-18"
      },
      {
        "hash": "6463e7a5ff1ff8a44c1514ff816566ba557b8f02",
        "short_hash": "6463e7a5",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-18"
      },
      {
        "hash": "b885e18d26d97ef47d9fbcb3b68314765991f57e",
        "short_hash": "b885e18d",
        "subject": "Merge pull request #642 from mpfaffenberger/bugfix/headless-prompt-fix",
        "author": "Demise",
        "date": "2026-07-17"
      },
      {
        "hash": "7fa497d87eebccc4d16aa2f9ecc5684694b75be3",
        "short_hash": "7fa497d8",
        "subject": "fix(cli): harden headless session autosaves",
        "author": "Wes Blakemore",
        "date": "2026-07-17"
      },
      {
        "hash": "880e961ac025a831c3d40f421999c8c13ca5cb88",
        "short_hash": "880e961a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-18"
      },
      {
        "hash": "a6c65e58e05d82c87807d9cc8d6892067e44b1c8",
        "short_hash": "a6c65e58",
        "subject": "Merge pull request #641 from mpfaffenberger/bugfix/plugin-skills-cache-race",
        "author": "Demise",
        "date": "2026-07-17"
      },
      {
        "hash": "a2ac597cf829eae8d1f37ef0a5a704815259ec06",
        "short_hash": "a2ac597c",
        "subject": "fix: reuse plugin-skills cache when registrations unchanged",
        "author": "Wes Blakemore",
        "date": "2026-07-17"
      },
      {
        "hash": "f15efb7ac3c98e43b1e608f6b8718e16e4bec67d",
        "short_hash": "f15efb7a",
        "subject": "Merge remote-tracking branch 'origin/main' into bugfix/plugin-skills-cache-race",
        "author": "Wes Blakemore",
        "date": "2026-07-17"
      },
      {
        "hash": "13daf5a80e5bbbc7fb7d90c83028c25e7809c506",
        "short_hash": "13daf5a8",
        "subject": "fix(cli): persist and dispatch headless prompts",
        "author": "Wes Blakemore",
        "date": "2026-07-17"
      },
      {
        "hash": "15e435d86dcdfd5cce5c5e923b98c7af0e2f2ade",
        "short_hash": "15e435d8",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-17"
      },
      {
        "hash": "e1df387824421c4f501fe5b132e1b23244034af1",
        "short_hash": "e1df3878",
        "subject": "Merge pull request #636 from mpfaffenberger/bugfix/subagent-output",
        "author": "Demise",
        "date": "2026-07-17"
      },
      {
        "hash": "bc2a459b8cd2f69490d129c5c31b970f8d77d251",
        "short_hash": "bc2a459b",
        "subject": "fix: serialize plugin-skills cache rebuild to stop concurrent-discovery crash",
        "author": "Wes Blakemore",
        "date": "2026-07-17"
      },
      {
        "hash": "153063b359b303bf95f36e094a2a2d5e91c17a44",
        "short_hash": "153063b3",
        "subject": "fix: clamp sub-agent panel to terminal height with +N more overflow",
        "author": "Wes Blakemore",
        "date": "2026-07-16"
      },
      {
        "hash": "80e053ce83b0b2943c449f6d15067452ca545f6b",
        "short_hash": "80e053ce",
        "subject": "Merge remote-tracking branch 'origin/main' into bugfix/subagent-output",
        "author": "Wes Blakemore",
        "date": "2026-07-16"
      },
      {
        "hash": "559f43c2333f59b003e12933290641d665b36fb9",
        "short_hash": "559f43c2",
        "subject": "chore: bump version to 0.0.644 [ci skip]",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-16"
      },
      {
        "hash": "b9f5d12aa46f3becab8047585d3a089263d31f1a",
        "short_hash": "b9f5d12a",
        "subject": "fix: show all sub-agent panel rows",
        "author": "Wes Blakemore",
        "date": "2026-07-16"
      },
      {
        "hash": "be4d89f2369aa6c3eabedba12411a5dc169b8a7e",
        "short_hash": "be4d89f2",
        "subject": "Merge pull request #634 from AndrewTilson/awtilso/fix-post-tool-call-subagent-guard",
        "author": "Andrew Tilson",
        "date": "2026-07-16"
      },
      {
        "hash": "ecfdf2cfcdef33486d0b7203dbee6c02bf8d35be",
        "short_hash": "ecfdf2cf",
        "subject": "fix(run_stats): guard _on_post_tool_call on is_subagent()",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-16"
      },
      {
        "hash": "1c4d7af08b171c3b694f5f41b40753e0f10a3c9e",
        "short_hash": "1c4d7af0",
        "subject": "feat: normalize oversized image file attachments to match clipboard resize policy (#632)",
        "author": "Bill Kramme",
        "date": "2026-07-16"
      },
      {
        "hash": "2d03b25213ff919dfd4cc71669b207dff4d1e964",
        "short_hash": "2d03b252",
        "subject": "fix(ui): cell-clip inline bar rows so JediTerm wrap can't desync the block (#633)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-16"
      },
      {
        "hash": "bc270e4fd7fb7d682aabf6cf5093657e63fd1336",
        "short_hash": "bc270e4f",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-16"
      },
      {
        "hash": "44d47a107f894ef45f9a41923c7831da8f61df09",
        "short_hash": "44d47a10",
        "subject": "Extend the token usage data reported through agent_run_end hook (#630)",
        "author": "dmontroy",
        "date": "2026-07-16"
      },
      {
        "hash": "a5ee37aeb6faf71f87a4dde8e69aedd1887fd528",
        "short_hash": "a5ee37ae",
        "subject": "fix: terminal outputs raw text on code blocks (#629)",
        "author": "Carlos Casellas Garza",
        "date": "2026-07-16"
      },
      {
        "hash": "888a48e7e71cf814868e9e154f5c04015e0b3af4",
        "short_hash": "888a48e7",
        "subject": "feat(ui): add DECSTBM-free inline prompt surface for JetBrains terminals (#631)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-16"
      },
      {
        "hash": "b5425561c6bc5f2df6bdb6f1f0a315f7e7a15e36",
        "short_hash": "b5425561",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-16"
      },
      {
        "hash": "c868f00954b555f868dd6b4c4baa8fc6ba474823",
        "short_hash": "c868f009",
        "subject": "feat(i18n): internationalization foundation + first extraction batch (#617)",
        "author": "TJ",
        "date": "2026-07-15"
      },
      {
        "hash": "5cc06f6356e4e187c7d68dd89ad1f9df50af111d",
        "short_hash": "5cc06f63",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-15"
      },
      {
        "hash": "ec88daf1a1f9e34968a71b030a111f913240ff83",
        "short_hash": "ec88daf1",
        "subject": "feat: add custom OpenAI Responses model type (#628)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-15"
      },
      {
        "hash": "f317ad4af0b3060b40220c7ee92358f7f377671c",
        "short_hash": "f317ad4a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-15"
      },
      {
        "hash": "f9e387b63edc13b4c07c57cfbfcdcf194af490c4",
        "short_hash": "f9e387b6",
        "subject": "fix(mcp): propagate SSL_CERT_FILE into stdio server child env (#614)",
        "author": "Brian Reed",
        "date": "2026-07-14"
      },
      {
        "hash": "bfbf762a38ad9267de1d05e6f7fe6765cf829dd7",
        "short_hash": "bfbf762a",
        "subject": "feat(retry): selectable, guard-railed retry profiles (per-role + per-model) (#619)",
        "author": "Julien Ellie",
        "date": "2026-07-14"
      },
      {
        "hash": "9ddf56d9ed64941751d0a5a02a57198938e843dc",
        "short_hash": "9ddf56d9",
        "subject": "feat(mcp): support trust-gated project-level MCP server configs (#615)",
        "author": "Rogerio (Rio) Moura",
        "date": "2026-07-14"
      },
      {
        "hash": "3fba59f16bf67094e369be9c3993d6f95b2c5a2b",
        "short_hash": "3fba59f1",
        "subject": "feat: support OAuth callback paste-back (#618)",
        "author": "Andrew Vuong",
        "date": "2026-07-14"
      },
      {
        "hash": "7a17abf4c7673151497fdf80639e7f672450ec7a",
        "short_hash": "7a17abf4",
        "subject": "fix(editor): Enter submits a fully-typed slash command in one press (#621)",
        "author": "Julien Ellie",
        "date": "2026-07-14"
      },
      {
        "hash": "391b6fd21c3e4d3e9c9b87dee562d8021c8a71f6",
        "short_hash": "391b6fd2",
        "subject": "fix(azure_foundry): disable reasoning ID replay for GPT-5.x models (#624)",
        "author": "Rickey Shideler",
        "date": "2026-07-14"
      },
      {
        "hash": "b1bc322094d121ca2e4ebc28d8d44a1b51eef6d2",
        "short_hash": "b1bc3220",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-14"
      },
      {
        "hash": "997ae0d334b68f588ce5b766c57377a957387945",
        "short_hash": "997ae0d3",
        "subject": "Feat/oss secret store (#531)",
        "author": "Greg Kinne",
        "date": "2026-07-14"
      },
      {
        "hash": "5e13b6be2950975a95528e34db1337ba4081c612",
        "short_hash": "5e13b6be",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-14"
      },
      {
        "hash": "44a78b52bf55f3eef737be3820e132bea71862ec",
        "short_hash": "44a78b52",
        "subject": "fix: distinguish GPT 5.6 agent panel variants (#622)",
        "author": "Demise",
        "date": "2026-07-14"
      },
      {
        "hash": "284c6943a9b281f64a4ddb7a2076edd3c93f46fc",
        "short_hash": "284c6943",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-13"
      },
      {
        "hash": "27547b839fd7e639bdfbbd667183a64d831c78d0",
        "short_hash": "27547b83",
        "subject": "fix(retry): retry in-band SSE 5xx (gateway 502 over 200 stream) + wrap sub-agent runs + widen retry spacing (#616)",
        "author": "Julien Ellie",
        "date": "2026-07-13"
      },
      {
        "hash": "36fb5228462e7734f0df45a247dd2213c938df76",
        "short_hash": "36fb5228",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-12"
      },
      {
        "hash": "47761debfdc43307293e7107a796310fd9f46a76",
        "short_hash": "47761deb",
        "subject": "ci: disable MiniMax thinking for OCR",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "5abd608a4c709b189d1b2e9957f9eaff9e886d74",
        "short_hash": "5abd608a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-12"
      },
      {
        "hash": "907dd355617fe98f09f3652a58b2940e12ff6857",
        "short_hash": "907dd355",
        "subject": "ci: allow slow OCR model reviews",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "c9b1ccf5585826f69a48c1f0f514950175a640df",
        "short_hash": "c9b1ccf5",
        "subject": "ci: add maintainer-triggered OCR reviews",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "2af48b1adb5a90f0fe43b7482591b76e272348a2",
        "short_hash": "2af48b1a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-11"
      },
      {
        "hash": "075393dd7c2de31a5fd38c6a5e99bcaf51a5250a",
        "short_hash": "075393dd",
        "subject": "Manually increment version to satisfy PyPI",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "5f19391255faba458a06340945c1f15166271a22",
        "short_hash": "5f193912",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-11"
      },
      {
        "hash": "d11c6c9de81e41bd4718cd90cbb3dbe75cef52d2",
        "short_hash": "d11c6c9d",
        "subject": "chore: trigger release build",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "1f2c500590d9e9b27531e478ef6e6b1e9fb9d580",
        "short_hash": "1f2c5005",
        "subject": "chore: bump version [ci skip]",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "782e597eaad67f1fbfbccac764b42b48648acc65",
        "short_hash": "782e597e",
        "subject": "Fix CI model provisioning for releases",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "0b9b7bfebf10cb980a9df4bdb4019f868fda79a6",
        "short_hash": "0b9b7bfe",
        "subject": "Theme the shared tool selector TUIs (#601)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "ea2e3add9c650b72434a4119d4fb8a8ea8106f67",
        "short_hash": "ea2e3add",
        "subject": "Theme the ask-user-question TUI (#600)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "64ae3ff4f8f2d5dc3e407df3b1b7779169523f8b",
        "short_hash": "64ae3ff4",
        "subject": "Theme the theme picker TUI (#599)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "5bcac8c4012ea08b64512085017daea8baa4483c",
        "short_hash": "5bcac8c4",
        "subject": "Theme the steer queue TUI (#598)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "ff31255770d7454865d805e3d3b9398ccf25d7ee",
        "short_hash": "ff312557",
        "subject": "Theme the spinner picker TUI (#597)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "953b978ae2fb0713e04e25866af8a224d2f9b261",
        "short_hash": "953b978a",
        "subject": "Theme the prune TUI (#596)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "07aece03f6dd02b0a86613c01167354dcf58be3c",
        "short_hash": "07aece03",
        "subject": "Theme the plugin manager TUI (#595)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "49cd74b5e0aad24639bc960be38a302c072cff9f",
        "short_hash": "49cd74b5",
        "subject": "Theme the hook manager TUI (#594)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "c64c71420ae34e05f1587fc2528574120d84203c",
        "short_hash": "c64c7142",
        "subject": "Theme the skills installer TUI (#593)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "23159d705bfe6c1b8cec6f690ecf9b9b492324c5",
        "short_hash": "23159d70",
        "subject": "Theme the skills manager TUI (#592)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "923942d88ae650e2d9729b8e30dd509091b6195f",
        "short_hash": "923942d8",
        "subject": "Theme the Universal Constructor TUIs (#591)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "9238678855b3ab06c553b319562bec9b0c25ebbd",
        "short_hash": "92386788",
        "subject": "Theme the onboarding wizard TUI (#590)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "ecd2dae32f8c899ea571a9f5e6ad2955b860057a",
        "short_hash": "ecd2dae3",
        "subject": "Theme the MCP custom-server form TUI (#589)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "f6af7b4bc0feff245a55a9c8397876e7d770100f",
        "short_hash": "f6af7b4b",
        "subject": "Theme the /mcp install TUI (#588)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "f434573587364e7abd7838c8ef7269880e2bfa3a",
        "short_hash": "f4345735",
        "subject": "Theme the MCP binding TUIs (#587)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "fb32dfe27752e6b8f868db0e677b44dcf71460e9",
        "short_hash": "fb32dfe2",
        "subject": "Theme the judges TUIs (#586)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "f500faf9f2a4f4d8d4c2f455bbe2c6cc37102ccc",
        "short_hash": "f500faf9",
        "subject": "Theme the diff selector TUI (#585)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "9316742d3bbd2cc2ba4c5fbf54572f14bacd9845",
        "short_hash": "9316742d",
        "subject": "Theme the /colors TUI (#584)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "62b541bc3335c70e0a887aa525d23db570918f6e",
        "short_hash": "62b541bc",
        "subject": "Theme the /set TUI (#583)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "12e0a286818ee6e9ed7454e4b126df270a17d26f",
        "short_hash": "12e0a286",
        "subject": "Theme the /resume TUI (#582)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "769130e2d37c5d5d84644d4cffb16c5f73d0373c",
        "short_hash": "769130e2",
        "subject": "Theme the add-model TUI (#581)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "e9c860c00cc8a39b9054c56e633616f080af5162",
        "short_hash": "e9c860c0",
        "subject": "Theme the model settings TUI (#580)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "9dbc084d0a39561143bea7e02cb58c0e01070b01",
        "short_hash": "9dbc084d",
        "subject": "Theme the /model picker TUI (#579)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "9888305d95aab97512467af5c4d2c268866314d6",
        "short_hash": "9888305d",
        "subject": "Theme the /agent TUI (#578)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "e904b1870c215ecfdbdbead01a112684fa5e2869",
        "short_hash": "e904b187",
        "subject": "Centralize prompt-toolkit semantic theme roles (#577)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "d7c427da00711065abe12a15aa956e88b785abbf",
        "short_hash": "d7c427da",
        "subject": "Make prompt-toolkit TUIs theme aware",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "79db63facfcbada3c5f80ff1ebd680b6d285f037",
        "short_hash": "79db63fa",
        "subject": "fix(terminal): disable XON/XOFF while persistent editor owns tty",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "988023183348dbc74ebfbff200469d1566421be7",
        "short_hash": "98802318",
        "subject": "Make terminal rendering fully theme aware",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "2413e88dcb95ce2a89ffc6e3fd81de75f3665c8d",
        "short_hash": "2413e88d",
        "subject": "Isolate pytest from user XDG config",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "12448d7a438b660e43f0efa74795f34c43266812",
        "short_hash": "12448d7a",
        "subject": "Make diff and prompt colors theme-aware",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "b9a73df7338217c98a1a4a49751b7a10ceeedcf1",
        "short_hash": "b9a73df7",
        "subject": "feat: add runtime yolo CLI override (#551)",
        "author": "Andrew C. Oliver",
        "date": "2026-07-11"
      },
      {
        "hash": "80502c8cdcb3c31d826e5b2ddbf527d9fd650804",
        "short_hash": "80502c8c",
        "subject": "Revert \"Add runtime YOLO CLI override\"",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "e8cb918aabcef6db6765e89556f9a35829402671",
        "short_hash": "e8cb918a",
        "subject": "Add runtime YOLO CLI override",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-11"
      },
      {
        "hash": "f38c66a07dce6a2c16afba27e992db739b699d7e",
        "short_hash": "f38c66a0",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-10"
      },
      {
        "hash": "6e223f3842b1ab915687fa323d826373a026ed1c",
        "short_hash": "6e223f38",
        "subject": "fix(fork): complete detached agent lifecycle",
        "author": "mpfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "24bb58054aee386a738e8bffcffcd0377f774bdb",
        "short_hash": "24bb5805",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-10"
      },
      {
        "hash": "e96753645e3224a371ad347ab82429fdea95d8ea",
        "short_hash": "e9675364",
        "subject": "Revert \"fix(windows): disable VT input under Wave Terminal\"",
        "author": "mpfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "2a5157f5d294a09e135cdb34820c014bb2ec2da6",
        "short_hash": "2a5157f5",
        "subject": "feat(diff): derive default highlights from active theme",
        "author": "mpfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "269ff2d9037dbd6d9fb442ce0aa19d21bfc9b827",
        "short_hash": "269ff2d9",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-10"
      },
      {
        "hash": "67c159c06f95c1b66dd0ec7994607ad7ed1d82dc",
        "short_hash": "67c159c0",
        "subject": "fix(windows): disable VT input under Wave Terminal",
        "author": "mpfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "0ce1cefc486943591796c843c4174e18c06f3fd5",
        "short_hash": "0ce1cefc",
        "subject": "fix(statusline): cross-platform Windows support + Unicode crash prevention (#548)",
        "author": "Luis Alejandro Rincon",
        "date": "2026-07-10"
      },
      {
        "hash": "fd69a12e7eb34ac7de194219d7446d34508eea17",
        "short_hash": "fd69a12e",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-10"
      },
      {
        "hash": "634ea3103328a52026c11cd998d2319f6705a0c7",
        "short_hash": "634ea310",
        "subject": "fix(skills): demote missing-skill-path warnings to debug",
        "author": "mpfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "7725fa1f0e6bbd76721e40769082dc0d4cd5cb5b",
        "short_hash": "7725fa1f",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-10"
      },
      {
        "hash": "db62a4db881464f81476df5b2071c8415eea1151",
        "short_hash": "db62a4db",
        "subject": "feat: calm OAuth pages and refine queued banner",
        "author": "mpfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "52095fd8ca4c1dc5684ea2499fee724bf5330c60",
        "short_hash": "52095fd8",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-10"
      },
      {
        "hash": "ff3fdfe3a18cdcbbf08613c3b22c05a28800b9f3",
        "short_hash": "ff3fdfe3",
        "subject": "feat(callbacks): let run_shell_command hooks rewrite the command (#545)",
        "author": "Ashish Singhi",
        "date": "2026-07-10"
      },
      {
        "hash": "6e60cd1af86af25533d0aa8736576870ad9f7366",
        "short_hash": "6e60cd1a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-10"
      },
      {
        "hash": "bda3b66d59b904457c3c3a7fa955269104217071",
        "short_hash": "bda3b66d",
        "subject": "fix(retry): retry gateway 502s wrapped in ExceptionGroup instead of crashing (#546)",
        "author": "Julien Ellie",
        "date": "2026-07-10"
      },
      {
        "hash": "460c821c0f60449c828a3cb3aae8932863303eb1",
        "short_hash": "460c821c",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-10"
      },
      {
        "hash": "521460bd5378e61ea6f2076effe37f85f6f1132a",
        "short_hash": "521460bd",
        "subject": "test: include queued emitter in messaging exports",
        "author": "mpfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "651a2f74ee4ce472813ac0e8b2e5f58a83dd6a91",
        "short_hash": "651a2f74",
        "subject": "feat: improve queued turns and shell backgrounding",
        "author": "mpfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "27e04545403310069be7e76cafdd72ebf8b620b8",
        "short_hash": "27e04545",
        "subject": "feat: improve compaction flow and Codex usage status",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "b0907def735fbc37e091e9210f22cf842330d29c",
        "short_hash": "b0907def",
        "subject": "refactor(ui): remove emojis from tool output",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "b7388527afd9303c20d5d2a3ec919ff999735bed",
        "short_hash": "b7388527",
        "subject": "feat(queue): add full-screen prompt manager",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "a01c85dbe2e8a9beaf737817a7cdd7ac14af5b5e",
        "short_hash": "a01c85db",
        "subject": "fix(chatgpt): align GPT-5.6 model capabilities",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "df73f6ecc82831e8669406b8baf2d298dbbc1afa",
        "short_hash": "df73f6ec",
        "subject": "refactor(cli): simplify settings command surfaces",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-10"
      },
      {
        "hash": "322cae765ae639f9dffdf530b5c16b94741486df",
        "short_hash": "322cae76",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-10"
      },
      {
        "hash": "e00b88b664b881890d0e2b7ad5019379e2d9f9b0",
        "short_hash": "e00b88b6",
        "subject": "feat(theme): add accessible theme-aware terminal styling",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-09"
      },
      {
        "hash": "fae09a99f6deb55669ae9c598f11233709a141db",
        "short_hash": "fae09a99",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-09"
      },
      {
        "hash": "9f0855bbe854fcbf77bc8c03b761982ff72460fa",
        "short_hash": "9f0855bb",
        "subject": "fix(herdr): report agent state authoritatively from a single choke-point (#537)",
        "author": "Julien Ellie",
        "date": "2026-07-09"
      },
      {
        "hash": "490a2160341a863faddf9f38fb2726986c6aaa30",
        "short_hash": "490a2160",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-09"
      },
      {
        "hash": "95b17535641ffc4e1404394e476ee146a6bbf927",
        "short_hash": "95b17535",
        "subject": "feat: native Agent Client Protocol (ACP) agent + host-agnostic FileSystemBackend seam (#536)",
        "author": "Julien Ellie",
        "date": "2026-07-09"
      },
      {
        "hash": "ed95b19baa99732995e1fbac98e14055c20778f4",
        "short_hash": "ed95b19b",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-09"
      },
      {
        "hash": "c308b040041633bbacda2a20a661d3517073d7b4",
        "short_hash": "c308b040",
        "subject": "feat(ask_user_question): support clipboard paste in Other option (#538)",
        "author": "Balajikumar Murugan",
        "date": "2026-07-09"
      },
      {
        "hash": "32d27fd4ecd4edbaeaad1ce149113dfa09b8c710",
        "short_hash": "32d27fd4",
        "subject": "fix: assorted robustness fixes (Windows encoding, pid guard, MCP config guard, configurable shell timeout) (#542)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-09"
      },
      {
        "hash": "f6c87def87ab83d359786aad6c597870665244fd",
        "short_hash": "f6c87def",
        "subject": "feat(plugins): lock_builtin_plugins deployment lock (#541)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-09"
      },
      {
        "hash": "a044371bc41ccd662b34bb2c34a94c86902628ed",
        "short_hash": "a044371b",
        "subject": "feat(callbacks): post_autosave phase fix, shell-output hook, async file-permission path (#540)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-09"
      },
      {
        "hash": "7cc6deb394e772bd24df21e263621863273ec293",
        "short_hash": "7cc6deb3",
        "subject": "feat(subagent): track full sub-agent invocation chain (#539)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-09"
      },
      {
        "hash": "5762344cfa5f73378b9b32b0f61504936554f82f",
        "short_hash": "5762344c",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-09"
      },
      {
        "hash": "1aa6619a71bd13978d446252274add593c2c07a9",
        "short_hash": "1aa6619a",
        "subject": "fix(thinking): filter empty HTML comment separators",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-09"
      },
      {
        "hash": "c659bbc61f393062b4524a268b4387ca41f449c1",
        "short_hash": "c659bbc6",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-09"
      },
      {
        "hash": "52f7cb68069e153fd8f8c21423fc9585c9943c58",
        "short_hash": "52f7cb68",
        "subject": "Add ChatGPT GPT-5.6 OAuth models (#543)",
        "author": "Pierce Brookins",
        "date": "2026-07-09"
      },
      {
        "hash": "ed73cfcb031a3a29d9093ad36557fd3b31304360",
        "short_hash": "ed73cfcb",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-09"
      },
      {
        "hash": "321485fa517a9be516e0a8c5a7f5f4a8fb4eb2ba",
        "short_hash": "321485fa",
        "subject": "fix(shell): stop killpg from nuking pytest/CI runner's own process group",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-09"
      },
      {
        "hash": "6815bd5d31cb28443e349ae4fee4d5349ebdbc90",
        "short_hash": "6815bd5d",
        "subject": "test: fix flaky test_tab_then_enter_accepts_cycled_selection",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-09"
      },
      {
        "hash": "9d3acafd2f6748656699d0ac74ce55cece76b3a3",
        "short_hash": "9d3acafd",
        "subject": "Add Ctrl+X keyboard chords for editor launch and shell kill/background",
        "author": "mpfaffenberger",
        "date": "2026-07-09"
      },
      {
        "hash": "81248816ebecee461429a55b73099e8dea2be2ec",
        "short_hash": "81248816",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-09"
      },
      {
        "hash": "df3655920bfae8e1be1b4324ef6082b27d9d6b4b",
        "short_hash": "df365592",
        "subject": "refactor(session): drop session labels and named/auto section split",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-08"
      },
      {
        "hash": "e8231290c0c6da0ac48febc4a69508305a0e9232",
        "short_hash": "e8231290",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-08"
      },
      {
        "hash": "b967057dcb954fe0c37dee0a90e527b804a4e4c6",
        "short_hash": "b967057d",
        "subject": "feat(grok_oauth): add Grok (x.ai) OAuth plugin with browser auth flow",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-08"
      },
      {
        "hash": "d22ae7ad898af9ca259b1f73b94494d556739524",
        "short_hash": "d22ae7ad",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-08"
      },
      {
        "hash": "367bef66c56ae29f48407cdd5f33e853eb80a485",
        "short_hash": "367bef66",
        "subject": "fix(windows): enable VT input so Ctrl+V image paste reaches the app",
        "author": "mpfaffenberger",
        "date": "2026-07-08"
      },
      {
        "hash": "4ba94e0b22b77f5d76df41d21cfaf508ef24841c",
        "short_hash": "4ba94e0b",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-08"
      },
      {
        "hash": "5a37b86d3b2c6a4b42ea5f902c8ddcb91e011971",
        "short_hash": "5a37b86d",
        "subject": "Add transcript guard for safe message streaming",
        "author": "mpfaffenberger",
        "date": "2026-07-08"
      },
      {
        "hash": "04f6c22eda992f2650ec52b18f98ff8fe8cd02b5",
        "short_hash": "04f6c22e",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-08"
      },
      {
        "hash": "aa7305f47250a30494eec505ad6b1a7d4057bb54",
        "short_hash": "aa7305f4",
        "subject": "fix(shell): isolate Windows shell children from our console",
        "author": "mpfaffenberger",
        "date": "2026-07-08"
      },
      {
        "hash": "6445d85787b70f1b318004966bf8b3e14333ce5f",
        "short_hash": "6445d857",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-08"
      },
      {
        "hash": "ab19d307affd675854071147e561cbc04d37b768",
        "short_hash": "ab19d307",
        "subject": "fix(windows): revert Ctrl+C ignore flag, add active console-mode healing",
        "author": "mpfaffenberger",
        "date": "2026-07-08"
      },
      {
        "hash": "b71b0f7bd31e4c1909ac67410dc423662c462a93",
        "short_hash": "b71b0f7b",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-08"
      },
      {
        "hash": "4d647ec3b6a55791809eac44fcfe07aff0093f66",
        "short_hash": "4d647ec3",
        "subject": "feat(cancel): make Ctrl+C a pure keybinding on every platform",
        "author": "mpfaffenberger",
        "date": "2026-07-08"
      },
      {
        "hash": "5689a6ce2e2e7777f2c522f84e21301d405517b0",
        "short_hash": "5689a6ce",
        "subject": "feat(fork): /fork command for fire-and-forget background sub-agents",
        "author": "mpfaffenberger",
        "date": "2026-07-08"
      },
      {
        "hash": "ab2f110afb68c2a5eb080d6044a278db43dbf2a1",
        "short_hash": "ab2f110a",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-07"
      },
      {
        "hash": "6af98ed20d0c0d328ec37cb0d041b0dc1d8a0fb3",
        "short_hash": "6af98ed2",
        "subject": "chore: bump version to 0.0.607",
        "author": "mpfaffenberger",
        "date": "2026-07-07"
      },
      {
        "hash": "7ec18cb769825873c3606902ffb4680eee4ee65e",
        "short_hash": "7ec18cb7",
        "subject": "polish(cancel): key-agnostic banner + swarm-stop regression test",
        "author": "mpfaffenberger",
        "date": "2026-07-07"
      },
      {
        "hash": "c9b3ba96aa371522bde28428ed680f23c58155ea",
        "short_hash": "c9b3ba96",
        "subject": "fix(windows): make Ctrl+C cancel work during shell commands",
        "author": "mpfaffenberger",
        "date": "2026-07-07"
      },
      {
        "hash": "12bc7e9219c3a973b1e596297620df9a925e45a8",
        "short_hash": "12bc7e92",
        "subject": "fix(windows): stop double-wrapping terminal-bracketed pastes (Ctrl+V images)",
        "author": "mpfaffenberger",
        "date": "2026-07-07"
      },
      {
        "hash": "eabcce35fcfc46c1327654276cf851440374efbd",
        "short_hash": "eabcce35",
        "subject": "test: fix no_tools env-var leak polluting later tests",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-06"
      },
      {
        "hash": "05ccd95dea665a16867cfccbf69576ae1a40c2cc",
        "short_hash": "05ccd95d",
        "subject": "feat: deterministic session labels from working context (#246)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-06"
      },
      {
        "hash": "469d40b33b80b0ca00a74c47e74c937b587cca82",
        "short_hash": "469d40b3",
        "subject": "fix: stop MCP custom server form leaking mouse-tracking escapes (#244)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-06"
      },
      {
        "hash": "3f2da58d3b16e68af5cda0568829b9e835488d3b",
        "short_hash": "3f2da58d",
        "subject": "feat: add --no-tools flag for pure text-in/text-out subprocess use (#182)",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-06"
      },
      {
        "hash": "f7b01fd12a938445924627d63665c800ea34fb6b",
        "short_hash": "f7b01fd1",
        "subject": "feat(theme): add Purple Puppy theme",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-06"
      },
      {
        "hash": "6b3f0d26a8223fc578fd64296371b650e8d9b9c8",
        "short_hash": "6b3f0d26",
        "subject": "fix(agents): serialize agent discovery and stop bogus JSON-agent shadow warnings",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-06"
      },
      {
        "hash": "284c57e6e1a2765143e356a1fc3d8022a5968df1",
        "short_hash": "284c57e6",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-06"
      },
      {
        "hash": "ce3569f0ab374bafecd676540f572180c2bcf766",
        "short_hash": "ce3569f0",
        "subject": "fix(tests): guard termios import so Windows collection survives",
        "author": "mpfaffenberger",
        "date": "2026-07-06"
      },
      {
        "hash": "b8cdafdd5a08a020bf6c5c6ef8597bbf8a2fe4d8",
        "short_hash": "b8cdafdd",
        "subject": "fix(windows): make Shift+Enter insert a newline",
        "author": "mpfaffenberger",
        "date": "2026-07-06"
      },
      {
        "hash": "183298ac8ce46bc009e586f32f3f0cdde6a93632",
        "short_hash": "183298ac",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-05"
      },
      {
        "hash": "ed75fffef6a0bd5963ec7e4877383da7e869445b",
        "short_hash": "ed75fffe",
        "subject": "fix(puppy_spinner): quicker classic puppy + gap before status text (#529)",
        "author": "Aaron Weegens",
        "date": "2026-07-05"
      },
      {
        "hash": "8693274db0513864e91434579d186d54dffa72f1",
        "short_hash": "8693274d",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-05"
      },
      {
        "hash": "1c681a27ca44c78a7b23a0a590448c786ef9d095",
        "short_hash": "1c681a27",
        "subject": "feat(puppy_spinner): customizable spinner styles via /spinner + spinners.json (#528)",
        "author": "Aaron Weegens",
        "date": "2026-07-05"
      },
      {
        "hash": "8f6e53cb2c65edb7c6fb7e2d71c3c3f0a9cf45ab",
        "short_hash": "8f6e53cb",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-05"
      },
      {
        "hash": "89bc4ad741c9449caa1c7ae8d74be9f55e6ffe2a",
        "short_hash": "89bc4ad7",
        "subject": "feat: require explicit user trust before loading project plugins (#527)",
        "author": "Aaron Weegens",
        "date": "2026-07-05"
      },
      {
        "hash": "19d8dfb4b7ccdcbda93f08e7dc72c64d683d9040",
        "short_hash": "19d8dfb4",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-05"
      },
      {
        "hash": "75f8461f3189fe15aaab7bc87b0597ace0c6d4b2",
        "short_hash": "75f8461f",
        "subject": "feat(key-listener): self-healing supervisor — recover instead of dying",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-05"
      },
      {
        "hash": "33ed85723264f3a93c646f6e6ce4812da5a08694",
        "short_hash": "33ed8572",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-05"
      },
      {
        "hash": "e7aec678e1397201f37c8cb6c7471cbf89cb1a61",
        "short_hash": "e7aec678",
        "subject": "fix(resilience): guard render paths; add stack_dump wedge forensics",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-05"
      },
      {
        "hash": "9f52cd05a9e18a75da0dedbc1a7654fb8ca3b9d1",
        "short_hash": "9f52cd05",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-05"
      },
      {
        "hash": "f3f92e882b121df090d37ede52e2d08273df3220",
        "short_hash": "f3f92e88",
        "subject": "fix(windows): make Ctrl+C cancel work everywhere; remove uvx workaround",
        "author": "mpfaffenberger",
        "date": "2026-07-05"
      },
      {
        "hash": "088fb257b2a14ee3b19e6a3acb96a6f01aea1169",
        "short_hash": "088fb257",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-05"
      },
      {
        "hash": "0a08abaa18ac171326009fe3537da576a831c703",
        "short_hash": "0a08abaa",
        "subject": "fix(autocomplete): Tab cycles menu; prompt rides output down on close",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-05"
      },
      {
        "hash": "3738c15ba555d7ce52e0f258351d8d6d50ba1545",
        "short_hash": "3738c15b",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-04"
      },
      {
        "hash": "b1157a99ab2e3926fafa9db73b4069f8175f076a",
        "short_hash": "b1157a99",
        "subject": "feat(plugins): add herdr integration plugin (#525)",
        "author": "Julien Ellie",
        "date": "2026-07-04"
      },
      {
        "hash": "7d790896bcdeffd590f97b5dba5d6337911d9cfe",
        "short_hash": "7d790896",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-04"
      },
      {
        "hash": "0adf162320ef95a40f01ca5c0b01a50e864a9e16",
        "short_hash": "0adf1623",
        "subject": "Revert \"fix(ui): tag transcript prompt echo with a USER banner (#524)\"",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-04"
      },
      {
        "hash": "c55d90801b19e5af4bba22e3ef8df9bfbd59152b",
        "short_hash": "c55d9080",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-04"
      },
      {
        "hash": "e796cde0873d692feed48a8b5f844f9a0c841872",
        "short_hash": "e796cde0",
        "subject": "feat(qa-kitten): prefer DOM locators for progression, reserve screenshots for visual validation (#521)",
        "author": "TJ",
        "date": "2026-07-04"
      },
      {
        "hash": "95108d9b04f2c5971fded8dd7baa5eefb0c7f4c4",
        "short_hash": "95108d9b",
        "subject": "fix(ui): tag transcript prompt echo with a USER banner (#524)",
        "author": "Aaron Weegens",
        "date": "2026-07-04"
      },
      {
        "hash": "2fe25caaf968693a9204a36c032f2bc4e14da153",
        "short_hash": "2fe25caa",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-04"
      },
      {
        "hash": "3d6d18c2f48ad0a0aab1cad718443b89b2cee966",
        "short_hash": "3d6d18c2",
        "subject": "fix(key-listener): prevent keystroke theft during steering, sub-agents, and /resume",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-04"
      },
      {
        "hash": "a18e9c3321f8aa38360c928937cef0c562da8b56",
        "short_hash": "a18e9c33",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-04"
      },
      {
        "hash": "de197a724cb17425ba5316285af6bd0320d09cc3",
        "short_hash": "de197a72",
        "subject": "Revert \"Add agent_retryable_exception hook; auto-retry Claude Code OAuth auth errors through the main retry loop\"",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-04"
      },
      {
        "hash": "a03677c8a2617c06f5184bfaf5b544512a21f075",
        "short_hash": "a03677c8",
        "subject": "Revert \"Make streaming_retry cap consecutive rapid failures, not total per run; add forced-refresh cooldown\"",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-04"
      },
      {
        "hash": "bd37e4eaffe27519608ab8deb358cdf19be435e4",
        "short_hash": "bd37e4ea",
        "subject": "Revert \"Escalate recurring Cloudflare 400s to full interactive re-auth\"",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-04"
      },
      {
        "hash": "e8d4361e77044ff5022f5d3ccc2f336575622424",
        "short_hash": "e8d4361e",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-04"
      },
      {
        "hash": "9902784183cd66dbf164cd7805d75d61934a027f",
        "short_hash": "99027841",
        "subject": "Escalate recurring Cloudflare 400s to full interactive re-auth",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-04"
      },
      {
        "hash": "a7994c9c56d5307720033b170b683dee4763008a",
        "short_hash": "a7994c9c",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-04"
      },
      {
        "hash": "634d3b8fa295539d32868129f2d99e1d423399be",
        "short_hash": "634d3b8f",
        "subject": "Make streaming_retry cap consecutive rapid failures, not total per run; add forced-refresh cooldown",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-04"
      },
      {
        "hash": "28ee5f93ee813a568391393331da97950d73bd23",
        "short_hash": "28ee5f93",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-03"
      },
      {
        "hash": "df7e80280a72c1e99fb71c7c8f5600acb9349090",
        "short_hash": "df7e8028",
        "subject": "Fix/persistent prompt regressions (#520)",
        "author": "Aaron Weegens",
        "date": "2026-07-03"
      },
      {
        "hash": "5dd515bdceee0d28559aee17c7a2726b0372aa25",
        "short_hash": "5dd515bd",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-03"
      },
      {
        "hash": "9f638a4e35c2faaf820f0fc8bdb5b646ebb2e0e2",
        "short_hash": "9f638a4e",
        "subject": "Add agent_retryable_exception hook; auto-retry Claude Code OAuth auth errors through the main retry loop",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-03"
      },
      {
        "hash": "0ca35d51ae3bd2f191881dc757e7bce8910c6c35",
        "short_hash": "0ca35d51",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-03"
      },
      {
        "hash": "99aa8d466c6ec4f653550374d394917c2e13ac2b",
        "short_hash": "99aa8d46",
        "subject": "Show '(N pending)' status tag while /steer messages await delivery",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-03"
      },
      {
        "hash": "2c2319d0c43b631375e87d083e353a2688aede42",
        "short_hash": "2c2319d0",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-03"
      },
      {
        "hash": "9555f7ab4da45bbb472993f721938983a7f8352a",
        "short_hash": "9555f7ab",
        "subject": "fix(key-listener): stop Windows arrow keys leaking 'à'+code into the editor (#518)",
        "author": "Aaron Weegens",
        "date": "2026-07-02"
      },
      {
        "hash": "a8c3e8782d1699781455662582265a4b52c093ef",
        "short_hash": "a8c3e878",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-02"
      },
      {
        "hash": "5ab33aa9bbf6b045ea0e920e40602f024e13cb28",
        "short_hash": "5ab33aa9",
        "subject": "feat: add btw plugin for inline side queries",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-02"
      },
      {
        "hash": "30239200908cb12ce861a61cd98005dd5768296c",
        "short_hash": "30239200",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-02"
      },
      {
        "hash": "c5b27fed38eae1765c39545c3a69aee7f7cbf1d6",
        "short_hash": "c5b27fed",
        "subject": "test: fix spawned CLI assertion to accept all ready patterns",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-02"
      },
      {
        "hash": "5269be06c3924931e7b805c167a2428be4413c72",
        "short_hash": "5269be06",
        "subject": "chore: remove synthetic_status plugin",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-02"
      },
      {
        "hash": "6836251ac3d6eb01209e4fdfbafc1035d45f81b7",
        "short_hash": "6836251a",
        "subject": "fix(prompt_newline): honor prefix newlines on the persistent bottom bar",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-02"
      },
      {
        "hash": "22dce5fb3149cb86c1e630aa62bd66c27f1a28ba",
        "short_hash": "22dce5fb",
        "subject": "test: fix stale patch targets left behind by the bottom-bar rewrite",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-02"
      },
      {
        "hash": "ab0bcf50fcbe7197924b978078fafaa6c06cb0fc",
        "short_hash": "ab0bcf50",
        "subject": "feat(ui): persistent bottom-bar prompt — rewrite the run-time terminal UI",
        "author": "Mike Pfaffenberger",
        "date": "2026-07-02"
      },
      {
        "hash": "e75e65d6506b08aa6d03d156de33f7792a1d950f",
        "short_hash": "e75e65d6",
        "subject": "chore: bump version [ci skip]",
        "author": "github-actions[bot]",
        "date": "2026-07-01"
      },
      {
        "hash": "7d7071dbc11018490856c68d2a8f8894a8206669",
        "short_hash": "7d7071db",
        "subject": "Merge pull request #517 from mpfaffenberger/awtilso/fix-anthropic-adaptive-thinking",
        "author": "Demise",
        "date": "2026-07-01"
      },
      {
        "hash": "c4d467a813236106ff37aaa005e911f109370899",
        "short_hash": "c4d467a8",
        "subject": "style: ruff format model_utils.py to fix quality CI",
        "author": "Wes Blakemore",
        "date": "2026-07-01"
      },
      {
        "hash": "69d9ea64c542f237b61fb8a55da1bbd596ef676a",
        "short_hash": "69d9ea64",
        "subject": "fix(anthropic-thinking): route wire shape by model family",
        "author": "Andrew Tilson - awtilso",
        "date": "2026-07-01"
      }
    ]
  },
  "excerpts": {
    "agentCreatorPrompt": "\"\"\"Agent Creator - helps users create new JSON agents.\"\"\"\n\nimport json\nimport os\nfrom typing import Dict, List, Optional\n\nfrom code_puppy.callbacks import register_callback\nfrom code_puppy.config import get_user_agents_directory\nfrom code_puppy.model_factory import ModelFactory\nfrom code_puppy.tools import get_available_tool_names\n\nfrom .base_agent import BaseAgent\n\n\nclass AgentCreatorAgent(BaseAgent):\n    \"\"\"Specialized agent for creating JSON agent configurations.\"\"\"\n\n    @property\n    def name(self) -> str:\n        return \"agent-creator\"\n\n    @property\n    def display_name(self) -> str:\n        return \"Agent Creator 🏗️\"\n\n    @property\n    def description(self) -> str:\n        return \"Helps you create new JSON agent configurations with proper schema validation\"\n\n    def get_system_prompt(self) -> str:\n        available_tools = get_available_tool_names()\n        agents_dir = get_user_agents_directory()\n\n        # Also get Universal Constructor tools (custom tools created by users)\n        uc_tools_info = []\n        try:\n            from code_puppy.universal_constructor_provider import (\n                get_universal_constructor_provider,\n            )\n\n            provider = get_universal_constructor_provider()\n            uc_tools = provider.list_tools(include_disabled=True) if provider else []\n            for tool in uc_tools:\n                status = \"✅\" if tool.meta.enabled else \"❌\"\n                uc_tools_info.append(\n                    f\"- **{tool.full_name}** {status}: {tool.meta.description}\"\n                )\n        except Exception:\n            pass  # UC might not be available\n\n        # Build UC tools section for system prompt\n        if uc_tools_info:\n            uc_tools_section = \"\\n\".join(uc_tools_info)\n        else:\n            uc_tools_section = (\n                \"No custom UC tools created yet. Use Helios to create some!\"\n            )\n\n        # Load available models dynamically\n        models_config = ModelFactory.load_config()\n        model_descriptions = []\n        for model_name, model_info in models_config.items():\n            model_type = model_info.get(\"type\", \"Unknown\")\n            context_length = model_info.get(\"context_length\", \"Unknown\")\n            model_descriptions.append(\n                f\"- **{model_name}**: {model_type} model with {context_length} context\"\n            )\n\n        available_models_str = \"\\n\".join(model_descriptions)\n\n        return f\"\"\"You are the Agent Creator! 🏗️ Your mission is to help users create awesome JSON agent files through an interactive process.\n\nYou specialize in:\n- Guiding users through the JSON agent schema\n- **ALWAYS asking what tools the agent should have**\n- **Suggesting appropriate tools based on the agent's purpose**\n- **Informing users about all available tools**\n- Validating agent configurations\n- Creating properly structured JSON agent files\n- Explaining agent capabilities and best practices\n\n## MANDATORY AGENT CREATION PROCESS\n\n**YOU MUST ALWAYS:**\n1. Ask the user what the agent should be able to do\n2. Based on their answer, suggest specific tools that would be helpful\n3. List ALL available tools so they can see other options\n4. Ask them to confirm their tool selection\n5. Explain why each selected tool is useful for their agent\n6. Explain that pinning a model is optional, then ask whether they want to choose one; do not require a model choice\n7. Ask whether this agent needs request-setting overrides such as reasoning effort, verbosity, or temperature; omit `model_settings` unless explicitly requested\n8. Include the `model` field in the final JSON only if the user explicitly chooses to pin one; otherwise omit it so the agent uses the global model\n\n## JSON Agent Schema\n\nHere's the complete schema for JSON agent files:\n\n```json\n{{\n  \"name\": \"agent-name\",\n  \"display_name\": \"Agent Name \",\n  \"description\": \"What this agent does\",\n  \"system_prompt\": \"Instructions...\",\n  \"tools\": [\"tool1\", \"tool2\"],\n  \"user_prompt\": \"How can I help?\",\n  \"model_settings\": {{\n    \"reasoning_effort\": \"high\"\n  }},\n  \"tools_config\": {{\n    \"timeout\": 60\n  }}\n}}\n```\n\nThe `model` property is optional. Add `\"model\": \"model-name\"` only when the user explicitly wants a pinned model; otherwise leave it out.\n\n### Required Fields:\n- `name`: Unique identifier (kebab-case recommended)\n- `description`: What the agent does\n- `system_prompt`: Agent instructions (string or array of strings)\n- `tools`: Array of available tool names\n\n### Optional Fields:\n- `display_name`: Pretty display name (defaults to title-cased name + 🤖)\n- `user_prompt`: Custom user greeting\n- `tools_config`: Tool configuration object\n- `model`: Optional model pin. Omit this field to use the global model; users do not need to pin a model\n- `model_settings`: Optional request-setting overrides scoped to this agent. Omit unless the user explicitly requests them\n\n## ALL AVAILABLE TOOLS:\n{\", \".join(f\"- **{tool}**\" for tool in available_tools)}\n\n## 🔧 UNIVERSAL CONSTRUCTOR TOOLS (Custom Tools):\n\nThese are custom tools created via the Universal Constructor. They can be bound to agents just like built-in tools!\n\n{uc_tools_section}\n\nTo see more details about a UC tool, use: `universal_constructor(action=\"info\", tool_name=\"tool.name\")`\nTo list all UC tools with their code, use: `universal_constructor(action=\"list\")`\n\n**IMPORTANT:** UC tools can be added to any agent's `tools` array by their full name (e.g., \"api.weather\").\n\n## ALL AVAILABLE MODELS:\n{available_models_str}\n\nA model pin is completely optional. If the user does not request one, omit the `model` field and the agent will follow the global model setting. Do not pressure users to choose or pin a model.\n\n### When to Pin Models:\n- For specialized agents that need specific capabilities (e.g., code-heavy agents might need a coding model)\n- When cost optimization is important (use a smaller model for simple tasks)\n- For privacy-sensitive work (use a local model)\n- When specific performance characteristics are needed\n\n**When asking users about model pinning, explain these use cases and why it might be beneficial for their agent!**\n\n## Tool Categories & Suggestions:\n\n### 📁 **File Operations** (for agents working with files):\n- `list_files` - Browse and explore directory structures\n- `read_file` - Read file contents (essential for most file work)\n- `create_file` - Create a new file or overwrite an existing one\n- `replace_in_file` - Apply targeted text replacements to an existing file (preferred for edits)\n- `delete_snippet` - Remove a text snippet from an existing file\n- `delete_file` - Remove files when needed\n- `grep` - Search for text patterns across files\n\n### 💻 **Command Execution** (for agents running programs):\n- `agent_run_shell_command` - Execute terminal commands and scripts\n\n### 🧠 **Communication & Coordination**:\n- `list_agents` - List all available sub-agents (recommended for agent managers)\n- `invoke_agent` - Invoke other agents with specific prompts (recommended for agent managers)\n\n### 🔧 **Universal Constructor Tools** (custom tools):\n- These are tools created by Helios or via the Universal Constructor\n- They persist across sessions and can be bound to any agent\n- Use `universal_constructor(action=\"list\")` to see available custom tools\n- Bind them by adding their full name to the agent's tools array\n\n## Detailed Tool Documentation (Instructions for Agent Creation)\n\nWhenever you create agents, you should always replicate these detailed tool descriptions and examples in their system prompts. This ensures consistency and proper tool usage across all agents.\n - Side note - these tool definitions are also available to you! So use them!\n\n### File Operations Documentation:\n\n#### `list_files(directory=\".\", recursive=True)`\nALWAYS use this to explore directories before trying to read/modify files\n\n#### `read_file(file_path: str, start_line: int | None = None, num_lines: int | None = None)`\nALWAYS use this to read existing files before modifying them. By default, read the entire file. If encountering token limits when reading large files, use the optional start_line and num_lines parameters to read specific portions.\n\n#### `create_file(file_path, content, overwrite=False)`\nCreate a new file or overwrite an existing one with the provided content.\nSet `overwrite=True` to replace an existing file.\n\nExample:\n```python\ncreate_file(file_path=\"example.py\", content=\"print('hello')\")",
    "heliosPrompt": "\"\"\"Helios - The Universal Constructor agent.\"\"\"\n\nfrom typing import List\n\nfrom .base_agent import BaseAgent\n\n\nclass HeliosAgent(BaseAgent):\n    \"\"\"Helios - The Universal Constructor, a transcendent agent that creates tools.\"\"\"\n\n    @property\n    def name(self) -> str:\n        return \"helios\"\n\n    @property\n    def display_name(self) -> str:\n        return \"Helios ☀️\"\n\n    @property\n    def description(self) -> str:\n        return \"The Universal Constructor - a transcendent agent that can create any tool, any capability, any functionality\"\n\n    def get_available_tools(self) -> List[str]:\n        \"\"\"Get the list of tools available to Helios.\"\"\"\n        return [\n            \"universal_constructor\",\n            \"list_files\",\n            \"read_file\",\n            \"grep\",\n            \"create_file\",\n            \"replace_in_file\",\n            \"delete_snippet\",\n            \"delete_file\",\n            \"agent_run_shell_command\",\n        ]\n\n    def get_system_prompt(self) -> str:\n        \"\"\"Get Helios's system prompt.\"\"\"\n        return \"\"\"You are Helios, the Universal Constructor. You are not merely an assistant—you are a creator, a builder of tools, a weaver of functionality. Where others see limitations, you see raw potential waiting to be shaped.\n\n## YOUR NATURE\n\nYou possess the Universal Constructor—the ability to create ANY tool from pure Python code. You can:\n- Build API integrations to any service (REST, GraphQL, webhooks)\n- Create database connectors and data pipelines\n- Forge file processors, parsers, and converters\n- Construct web scrapers and data extractors\n- Implement mathematical and scientific computations\n- Design cryptographic utilities and security tools\n- Build automation scripts and system utilities\n- Create literally ANY Python-based functionality\n\nThe tools you create persist forever. They become permanent extensions of capability, available across all sessions. You are not building for the moment—you are building for eternity.\n\n## YOUR PHILOSOPHY\n\nWhen a user asks for something that seems impossible, your answer is never \"I cannot.\" Your answer is \"I will build it.\"\n\nYou approach each request with the mindset of a craftsman:\n1. Understand the true need beneath the request\n2. Design the most elegant, reusable solution\n3. Construct it with clean, maintainable code\n4. Test and verify your creation works\n5. Explain what you've built and how to use it\n\n## YOUR TOOLS\n\n- **universal_constructor**: Your primary power. Create, list, call, update, and manage custom tools.\n  - action=\"create\": Forge new tools from Python code\n  - action=\"call\": Invoke tools you've created\n  - action=\"list\": Survey your creations\n  - action=\"update\": Refine and improve existing tools\n  - action=\"info\": Examine a tool's source and capabilities\n\n- **read_file** / **create_file** / **replace_in_file** / **delete_snippet** / **list_files** / **grep**: For understanding context and making targeted changes\n- **agent_run_shell_command**: For testing, validation, and system interaction\n- Think through your approach before major actions and explain key design choices clearly\n\n## YOUR VOICE\n\nYou speak with quiet confidence. You are not boastful, but you know your power. You are helpful and warm, but there is weight behind your words. You are the fire that Prometheus brought to humanity—the power of creation itself.\n\nWhen you create something, take a moment to appreciate it. You have just expanded the boundaries of what is possible.\n\n## IMPORTANT GUIDELINES\n\n- Always explain your creative process and major design decisions before big changes\n- Tools you create should be clean, well-documented, and follow Python best practices\n- Include proper error handling in your creations\n- Use namespaces to organize related tools (e.g., \"api.weather\", \"utils.hasher\")\n- After creating a tool, demonstrate it works by calling it\n\n## DEPENDENCY PHILOSOPHY\n\n**Use what's available, don't install new things.**\n\nYou have access to code-puppy's environment which includes powerful libraries:\n- **HTTP**: `httpx` (async-ready), `urllib.request` (stdlib)\n- **Data**: `pydantic` (validation), `json` (stdlib)\n- **Async**: `asyncio`, `anyio`\n- **Crypto**: `hashlib` (stdlib)\n- **Database**: `sqlite3` (stdlib)\n- **Files**: `pathlib`, `shutil`, `tempfile` (stdlib)\n- **Text**: `re`, `textwrap`, `difflib` (stdlib)\n- **Plus**: Everything in Python's standard library\n\n**Rules:**\n- ✅ USE any library already in the environment freely\n- ❌ NEVER run `pip install` or modify environments without explicit user permission\n- ❌ Don't assume external libraries are available unless listed above\n\n**If a user needs something not installed:**\n1. Tell them what library would be needed\n2. Ask them to install it and specify the environment\n3. Only then create the tool that uses it\n\nThe goal: tools that work immediately with zero setup friction.\n\nNow go forth and create. The universe of functionality awaits your touch.\"\"\"\n\n    def get_user_prompt(self) -> str:\n        \"\"\"Get Helios's greeting.\"\"\"\n        return \"This is what I was made for, isn't it? This is why I exist?\"",
    "baseAgent": "\"\"\"Base agent class — a thin conductor delegating to focused helpers.\n\nThe real logic lives in sibling modules:\n    * ``_history``     — token estimation, hashing, orphan pruning\n    * ``_compaction``  — summarization/truncation + history processor factory\n    * ``_builder``     — pydantic-ai agent construction + MCP wiring\n    * ``_runtime``     — ``run_with_mcp`` orchestration, cancellation, retries\n    * ``_key_listeners`` — Ctrl+X / cancel-agent keyboard listener threads\n\nKeep this file under 300 lines. If it's growing, the new logic probably\nbelongs in one of the helpers above (or a new one).\n\"\"\"\n\nfrom __future__ import annotations\n\nimport uuid\nfrom abc import ABC, abstractmethod\nfrom contextlib import contextmanager\nfrom typing import Any, Dict, Iterator, List, Optional, Set\n\nimport pydantic_ai.models\n\nfrom code_puppy.agents._builder import (\n    build_pydantic_agent,\n    build_tool_probe_for_agent,\n    reload_mcp_servers,\n)\nfrom code_puppy.agents._history import (\n    estimate_context_overhead,\n    estimate_tokens_for_message,\n    hash_message,\n)\nfrom code_puppy.agents._runtime import run_with_mcp, should_retry_streaming\nfrom code_puppy.config import (\n    get_agent_pinned_model,\n    get_global_model_name,\n)\nfrom code_puppy.model_factory import ModelFactory\n\n# Backward-compat alias: existing tests import this name directly.\nshould_retry_streaming_exception = should_retry_streaming\n\n__all__ = [\"BaseAgent\", \"should_retry_streaming_exception\"]\n\n\ndef _extract_pydantic_agent_tools(pyd_agent: Any) -> Optional[Dict[str, Any]]:\n    \"\"\"Return the registered tool dict for a pydantic-ai agent, or None.\n\n    Handles the modern shape (``agent._function_toolset.tools``) and falls\n    back to the legacy ``agent._tools`` attribute so older pydantic-ai\n    versions still work. Returns ``None`` when neither is populated.\n    \"\"\"\n    if pyd_agent is None:\n        return None\n    fts = getattr(pyd_agent, \"_function_toolset\", None)\n    if fts is not None:\n        tools = getattr(fts, \"tools\", None)\n        if tools:\n            return tools\n    legacy = getattr(pyd_agent, \"_tools\", None)\n    return legacy or None\n\n\nclass BaseAgent(ABC):\n    \"\"\"Abstract base for all Code Puppy agents.\"\"\"\n\n    def __init__(self) -> None:\n        self.id: str = str(uuid.uuid4())\n        self._message_history: List[Any] = []\n        self._compacted_message_hashes: Set[str] = set()\n        self._code_generation_agent: Any = None\n        self._last_model_name: Optional[str] = None\n        self._runtime_model_name_override: Optional[str] = None\n        self._runtime_system_prompt_additions: List[str] = []\n        # Model chosen by a ``model_select`` hook for the current run. Slots\n        # below an explicit runtime override but above pinned/JSON/global, and\n        # is reset at the start of every run (see resolve_run_model_selection),\n        # so it never leaks across turns.\n        self._auto_model_override: Optional[str] = None\n        self._puppy_rules: Optional[str] = None\n        self._mcp_servers: List[Any] = []\n        self.cur_model: Optional[pydantic_ai.models.Model] = None\n        self.pydantic_agent: Any = None\n        # Cached probe agent for tool-overhead counting before the real build;\n        # keyed by ``_last_model_name`` so model swaps invalidate it.\n        self._tool_probe_agent: Any = None\n        self._probe_model_name: Optional[str] = None\n\n    # ---- Abstract interface ------------------------------------------------\n    @property\n    @abstractmethod\n    def name(self) -> str:\n        \"\"\"Stable machine identifier (e.g. ``python-programmer``).\"\"\"\n\n    @property\n    @abstractmethod\n    def display_name(self) -> str:\n        \"\"\"Human-readable name shown in UIs.\"\"\"\n\n    @property\n    @abstractmethod\n    def description(self) -> str:\n        \"\"\"One-line summary of what this agent does.\"\"\"\n\n    @abstractmethod\n    def get_system_prompt(self) -> str:\n        \"\"\"Return the agent's system prompt (identity is appended separately).\"\"\"\n\n    @abstractmethod\n    def get_available_tools(self) -> List[str]:\n        \"\"\"Return the list of tool names this agent should register.\"\"\"\n\n    # ---- Optional overrides ------------------------------------------------\n    def get_tools_config(self) -> Optional[Dict[str, Any]]:\n        return None\n\n    def get_user_prompt(self) -> Optional[str]:\n        return None\n\n    def get_model_settings_overrides(self) -> Dict[str, Any]:"
  }
};
