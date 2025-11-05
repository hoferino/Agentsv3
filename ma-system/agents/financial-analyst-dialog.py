"""
Financial Analyst Dialog System

Provides interactive, menu-driven workflows for financial analysis
instead of single-prompt execution. Enables iterative refinement,
devil's advocate challenges, and guided analysis.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import os
import yaml
from pathlib import Path


class InteractionMode(Enum):
    """Overall interaction mode"""
    ONE_SHOT = "one_shot"  # Traditional: single prompt, full execution
    DIALOG = "dialog"      # New: interactive, menu-driven
    HYBRID = "hybrid"      # Mix: one-shot with option to refine


class DialogMode(Enum):
    """Different dialog modes for financial analysis"""
    MAIN_MENU = "main_menu"
    DOCUMENT_ANALYSIS = "document_analysis"
    EXCEL_REFINEMENT = "excel_refinement"
    DEVILS_ADVOCATE = "devils_advocate"
    SENSITIVITY_ANALYSIS = "sensitivity_analysis"
    ASSUMPTION_REVIEW = "assumption_review"


@dataclass
class DialogState:
    """Tracks current state of the dialog session"""
    interaction_mode: InteractionMode
    current_mode: DialogMode
    deal_name: str
    analysis_completed: Dict[str, bool]
    current_valuation_version: Optional[str]
    pending_questions: List[str]
    challenges_addressed: List[str]
    session_history: List[Dict]
    user_preference: Optional[InteractionMode] = None  # User's saved preference


class FinancialAnalystDialog:
    """
    Interactive dialog system for financial analysis.

    Instead of "analyze everything", this provides:
    - Step-by-step guided workflows
    - Menu-driven choices
    - Iterative refinement
    - Challenge mode to test assumptions
    """

    def __init__(self, deal_name: str, interaction_mode: InteractionMode = None):
        self.deal_name = deal_name

        # Load user preference from knowledge base if not specified
        if interaction_mode is None:
            interaction_mode = self._load_user_preference()

        self.state = DialogState(
            interaction_mode=interaction_mode,
            current_mode=DialogMode.MAIN_MENU,
            deal_name=deal_name,
            analysis_completed={
                'documents_analyzed': False,
                'valuation_created': False,
                'qoe_completed': False,
                'sensitivity_done': False,
                'challenged': False
            },
            current_valuation_version=None,
            pending_questions=[],
            challenges_addressed=[],
            session_history=[],
            user_preference=interaction_mode
        )

        self.menu_options = self._load_menu_configuration()

    def _get_preferences_path(self) -> Path:
        """Get path to user preferences file"""
        # Determine knowledge base path relative to this file
        current_dir = Path(__file__).parent
        kb_path = current_dir.parent / "knowledge-base" / "user-preferences.yaml"
        return kb_path

    def _get_menu_config_path(self) -> Path:
        """Get path to shared menu configuration."""
        return Path(__file__).with_name("financial-analyst-menu.yaml")

    def _load_menu_configuration(self) -> List[Dict]:
        """Load central menu configuration shared across prompts."""
        try:
            menu_path = self._get_menu_config_path()
            with open(menu_path, "r") as f:
                data = yaml.safe_load(f) or {}
                options = data.get("options", [])
                normalized: List[Dict] = []
                for option in options:
                    normalized.append(
                        {
                            "id": option.get("id"),
                            "label": option.get("label"),
                            "description": option.get("description"),
                            "workflow": option.get("workflow"),
                            "action": option.get("action"),
                            "status_key": option.get("status_key"),
                            "highlight": bool(option.get("highlight", False)),
                        }
                    )
                return normalized
        except FileNotFoundError:
            print("Menu configuration file missing; falling back to defaults.")
        except Exception as exc:
            print(f"Unable to load menu configuration: {exc}")
        return []

    def _load_user_preference(self) -> InteractionMode:
        """Load user's preferred interaction mode from knowledge base"""
        try:
            prefs_path = self._get_preferences_path()
            if prefs_path.exists():
                with open(prefs_path, 'r') as f:
                    prefs = yaml.safe_load(f)
                    mode_str = prefs.get('financial_analyst_mode', 'hybrid')
                    # Convert string to enum
                    mode_map = {
                        'one_shot': InteractionMode.ONE_SHOT,
                        'dialog': InteractionMode.DIALOG,
                        'hybrid': InteractionMode.HYBRID
                    }
                    return mode_map.get(mode_str, InteractionMode.HYBRID)
        except Exception as e:
            print(f"Could not load preferences: {e}")

        # Default to hybrid mode
        return InteractionMode.HYBRID

    def _save_user_preference(self, mode: InteractionMode):
        """Save user's preferred interaction mode"""
        try:
            prefs_path = self._get_preferences_path()

            # Load existing preferences
            prefs = {}
            if prefs_path.exists():
                with open(prefs_path, 'r') as f:
                    prefs = yaml.safe_load(f) or {}

            # Update mode
            prefs['financial_analyst_mode'] = mode.value
            prefs['last_updated'] = str(Path(__file__).stat().st_mtime)

            # Save
            prefs_path.parent.mkdir(parents=True, exist_ok=True)
            with open(prefs_path, 'w') as f:
                yaml.dump(prefs, f, default_flow_style=False)

            self.state.user_preference = mode
        except Exception as e:
            print(f"Could not save preferences: {e}")

    def show_mode_selection(self) -> Dict:
        """
        Present mode selection interface to user.
        Only shown on first interaction or when user switches modes.
        """
        return {
            "title": "Financial Analyst - Choose Your Workflow",
            "subtitle": f"Deal: {self.deal_name}",
            "description": (
                "How would you like to work with the Financial Analyst? "
                "You can change this anytime."
            ),
            "modes": [
                {
                    "id": "one_shot",
                    "name": "One-Shot Mode",
                    "icon": "⚡",
                    "description": "Give me a task, I'll complete it fully and present results",
                    "best_for": [
                        "Quick analysis when you trust standard assumptions",
                        "When you have limited time",
                        "Initial draft that you'll refine later"
                    ],
                    "example": "You: 'Analyze documents and build valuation'\nMe: [Completes everything, presents final model]"
                },
                {
                    "id": "dialog",
                    "name": "Dialog Mode",
                    "icon": "💬",
                    "description": "Interactive menu-driven workflow with your input at every step",
                    "best_for": [
                        "When you want to understand and control assumptions",
                        "Learning financial analysis",
                        "High-stakes valuations requiring careful thought"
                    ],
                    "example": "You: 'Build valuation'\nMe: 'What methodologies? Do you have projections? Let's discuss assumptions...'"
                },
                {
                    "id": "hybrid",
                    "name": "Hybrid Mode",
                    "icon": "🔄",
                    "description": "I'll do one-shot analysis, then offer dialog options to refine",
                    "best_for": [
                        "Balance of speed and control",
                        "Get initial results fast, then iterate",
                        "Most versatile approach"
                    ],
                    "example": "You: 'Build valuation'\nMe: [Creates v1.0] 'Done! Want to: refine assumptions / run devil's advocate / add sensitivity?'"
                }
            ],
            "default_recommendation": "hybrid",
            "can_change_later": True
        }

    def switch_mode(self, new_mode: InteractionMode) -> str:
        """Switch interaction mode"""
        old_mode = self.state.interaction_mode
        self.state.interaction_mode = new_mode
        self._save_user_preference(new_mode)

        return f"Switched from {old_mode.value} to {new_mode.value} mode. This preference will be saved."

    def show_main_menu(self) -> Dict:
        """
        Build main menu from shared configuration and dialog state.
        """
        options: List[Dict] = []

        for option in self.menu_options:
            status_text = "Ready"

            status_key = option.get("status_key")
            if status_key:
                if status_key == "valuation_created" and self.state.current_valuation_version:
                    status_text = f"Latest: v{self.state.current_valuation_version}"
                elif self.state.analysis_completed.get(status_key):
                    status_text = "Completed ✓"

            if option["id"] == "devils_advocate":
                status_text = (
                    "Ready" if self.state.analysis_completed.get("valuation_created") else "Available after valuation"
                )
            if option["id"] == "refine_excel":
                status_text = (
                    f"Latest: v{self.state.current_valuation_version}"
                    if self.state.current_valuation_version
                    else "Available after valuation"
                )
            if option["id"] == "sensitivity":
                status_text = (
                    "Ready" if self.state.analysis_completed.get("valuation_created") else "Available after valuation"
                )
            if option["id"] == "review_export":
                ready_outputs = [
                    self.state.analysis_completed.get("valuation_created"),
                    self.state.analysis_completed.get("qoe_completed"),
                    self.state.analysis_completed.get("sensitivity_done"),
                ]
                status_text = "Ready" if any(ready_outputs) else "Available after core analyses"
            if option["id"] == "ask_questions":
                status_text = "Always available"
            if option["id"] == "change_mode":
                status_text = f"Current: {self.state.interaction_mode.value}"

            options.append(
                {
                    "id": option["id"],
                    "label": option["label"],
                    "description": option["description"],
                    "status": status_text,
                    "workflow": option.get("workflow"),
                    "action": option.get("action"),
                    "highlight": option.get("highlight", False),
                }
            )

        return {
            "title": "Financial Analyst - Main Menu",
            "subtitle": f"Deal: {self.deal_name}",
            "options": options,
        }

    def handle_analyze_documents(self) -> Dict:
        """
        Document analysis workflow with user choices.
        """
        workflow = {
            "mode": "document_analysis",
            "title": "Financial Document Analysis",
            "steps": []
        }

        # Step 1: Confirm document scope
        workflow["steps"].append({
            "step": 1,
            "type": "user_choice",
            "question": "How many financial documents have you uploaded?",
            "options": [
                {"id": "few", "label": "1-10 documents", "description": "Standard analysis workflow"},
                {"id": "many", "label": "20-100 documents", "description": "Large-scale batched processing"},
                {"id": "massive", "label": "100+ documents", "description": "Enterprise-scale parallel extraction"}
            ],
            "next": "choose_focus"
        })

        # Step 2: Choose analysis focus
        workflow["steps"].append({
            "step": 2,
            "id": "choose_focus",
            "type": "multi_choice",
            "question": "What should I focus on? (Select all that apply)",
            "options": [
                {"id": "historical", "label": "Historical financials", "description": "P&L, Balance Sheet, Cash Flow"},
                {"id": "projections", "label": "Management projections", "description": "Future forecasts and budgets"},
                {"id": "tax", "label": "Tax returns", "description": "Tax filings and reconciliation"},
                {"id": "contracts", "label": "Key contracts", "description": "Customer/supplier agreements"},
                {"id": "everything", "label": "Everything", "description": "Comprehensive analysis"}
            ],
            "next": "extraction_detail"
        })

        # Step 3: Level of detail
        workflow["steps"].append({
            "step": 3,
            "id": "extraction_detail",
            "type": "user_choice",
            "question": "How detailed should the extraction be?",
            "options": [
                {"id": "quick", "label": "Quick overview", "description": "Key metrics only (30 min)"},
                {"id": "standard", "label": "Standard analysis", "description": "Full financial extraction (2-4 hours)"},
                {"id": "deep", "label": "Deep dive", "description": "Line-by-line with anomalies (4-8 hours)"}
            ],
            "next": "execute_analysis"
        })

        return workflow

    def handle_excel_refinement(self) -> Dict:
        """
        Interactive Excel model refinement dialog.
        """
        refinement = {
            "mode": "excel_refinement",
            "title": f"Refine Valuation Model (Current: v{self.state.current_valuation_version})",
            "current_model": f"{self.deal_name}_Valuation_Model_v{self.state.current_valuation_version}.xlsx",
            "dialog_options": []
        }

        # Offer specific refinement areas
        refinement["dialog_options"] = [
            {
                "id": "review_assumptions",
                "label": "Review Key Assumptions",
                "description": "Walk through WACC, growth rates, margins - I'll ask clarifying questions"
            },
            {
                "id": "test_scenarios",
                "label": "Test 'What-If' Scenarios",
                "description": "Change key drivers and see impact on valuation"
            },
            {
                "id": "add_analysis",
                "label": "Add New Analysis",
                "description": "Working capital deep-dive, customer concentration, etc."
            },
            {
                "id": "improve_structure",
                "label": "Improve Model Structure",
                "description": "Better formatting, error checks, input/output separation"
            },
            {
                "id": "data_validation",
                "label": "Data Quality Review",
                "description": "Check for inconsistencies, unusual trends, missing data"
            },
            {
                "id": "explain_sections",
                "label": "Explain Model Sections",
                "description": "I'll walk through any complex formulas or calculations"
            }
        ]

        refinement["prompt"] = (
            "I'll work with you interactively to refine the model. "
            "Choose a focus area, and I'll ask questions and make improvements based on your feedback."
        )

        return refinement

    def handle_devils_advocate(self) -> Dict:
        """
        Devil's advocate challenge mode.
        """
        challenge = {
            "mode": "devils_advocate",
            "title": "Devil's Advocate - Challenge Your Assumptions",
            "description": (
                "I'll challenge the valuation from multiple angles. "
                "This helps identify weaknesses before buyers or investors do."
            ),
            "challenge_areas": []
        }

        # Generate challenges based on current analysis
        challenge["challenge_areas"] = [
            {
                "category": "Revenue Assumptions",
                "challenges": [
                    "What if revenue growth is half your projection?",
                    "What if a major customer leaves?",
                    "Are you overstating market size or share?"
                ]
            },
            {
                "category": "Cost Structure",
                "challenges": [
                    "Have you accounted for margin compression as you scale?",
                    "What if key supplier prices increase 20%?",
                    "Are there hidden fixed costs that emerge at higher volumes?"
                ]
            },
            {
                "category": "Working Capital",
                "challenges": [
                    "Is working capital really sustainable at these levels?",
                    "What if payment terms worsen?",
                    "Have you stress-tested inventory assumptions?"
                ]
            },
            {
                "category": "Discount Rate (WACC)",
                "challenges": [
                    "Is your WACC too low given company-specific risks?",
                    "What if beta is higher for this industry?",
                    "Have you adequately priced in execution risk?"
                ]
            },
            {
                "category": "Terminal Value",
                "challenges": [
                    "Is perpetual growth rate too optimistic?",
                    "What if the business model becomes obsolete?",
                    "Are you assuming too high an exit multiple?"
                ]
            },
            {
                "category": "EBITDA Adjustments",
                "challenges": [
                    "Are your add-backs truly non-recurring?",
                    "What if buyer doesn't accept these normalizations?",
                    "Have you been too aggressive with adjustments?"
                ]
            }
        ]

        challenge["workflow"] = {
            "step_1": "Choose which areas to challenge",
            "step_2": "For each area, I'll present specific challenges",
            "step_3": "You respond with your reasoning",
            "step_4": "I provide counter-arguments or alternative views",
            "step_5": "We refine assumptions or document the risks",
            "step_6": "Update valuation model with adjusted scenarios"
        }

        challenge["options"] = [
            {
                "id": "challenge_all",
                "label": "Challenge Everything",
                "description": "Full adversarial review of all assumptions"
            },
            {
                "id": "challenge_select",
                "label": "Focus on Specific Areas",
                "description": "Choose which categories to challenge"
            },
            {
                "id": "buyer_perspective",
                "label": "Take Buyer Perspective",
                "description": "Challenge from a specific buyer type (PE, Strategic, etc.)"
            }
        ]

        return challenge

    def handle_sensitivity_analysis(self) -> Dict:
        """
        Interactive sensitivity analysis workflow.
        """
        sensitivity = {
            "mode": "sensitivity_analysis",
            "title": "Sensitivity & Scenario Analysis",
            "description": "Test how changes in key assumptions impact valuation"
        }

        # Present sensitivity options
        sensitivity["analysis_types"] = [
            {
                "id": "one_way",
                "label": "One-Way Sensitivity",
                "description": "Vary one assumption at a time",
                "variables": [
                    "Revenue growth rate",
                    "EBITDA margin",
                    "WACC",
                    "Terminal growth rate",
                    "Exit multiple"
                ]
            },
            {
                "id": "two_way",
                "label": "Two-Way Sensitivity Tables",
                "description": "Vary two assumptions simultaneously",
                "examples": [
                    "Revenue growth × EBITDA margin",
                    "WACC × Terminal growth",
                    "Exit multiple × EBITDA"
                ]
            },
            {
                "id": "scenarios",
                "label": "Scenario Analysis",
                "description": "Pre-defined scenarios with multiple assumptions",
                "scenarios": [
                    {
                        "name": "Base Case",
                        "description": "Most likely scenario"
                    },
                    {
                        "name": "Upside",
                        "description": "Optimistic but achievable"
                    },
                    {
                        "name": "Downside",
                        "description": "Conservative assumptions"
                    },
                    {
                        "name": "Stress Test",
                        "description": "What if multiple things go wrong?"
                    }
                ]
            },
            {
                "id": "monte_carlo",
                "label": "Monte Carlo Simulation",
                "description": "Probabilistic analysis with distributions",
                "note": "Requires defining probability distributions for key variables"
            }
        ]

        sensitivity["user_prompt"] = (
            "Which analysis would be most valuable? "
            "I'll create interactive tables and charts you can explore."
        )

        return sensitivity

    def get_dialog_prompt(self, mode: DialogMode) -> str:
        """
        Generate the appropriate dialog prompt based on mode.
        """
        prompts = {
            DialogMode.MAIN_MENU: self._format_main_menu(),
            DialogMode.DOCUMENT_ANALYSIS: self._format_document_analysis(),
            DialogMode.EXCEL_REFINEMENT: self._format_excel_refinement(),
            DialogMode.DEVILS_ADVOCATE: self._format_devils_advocate(),
            DialogMode.SENSITIVITY_ANALYSIS: self._format_sensitivity_analysis()
        }

        return prompts.get(mode, "")

    def _format_mode_selection(self) -> str:
        """Format mode selection interface"""
        selection = self.show_mode_selection()

        prompt = f"# {selection['title']}\n\n"
        prompt += f"**{selection['subtitle']}**\n\n"
        prompt += f"{selection['description']}\n\n"

        for i, mode in enumerate(selection['modes'], 1):
            is_recommended = mode['id'] == selection['default_recommendation']
            rec_tag = " **[RECOMMENDED]**" if is_recommended else ""
            prompt += f"{i}. {mode['icon']} **{mode['name']}**{rec_tag}\n"
            prompt += f"   {mode['description']}\n\n"
            prompt += f"   **Best for:**\n"
            for use_case in mode['best_for']:
                prompt += f"   - {use_case}\n"
            prompt += f"\n   **Example:**\n"
            prompt += f"   {mode['example']}\n\n"
            prompt += "   " + "-"*60 + "\n\n"

        prompt += "\n**Note:** You can change modes anytime by selecting 'Change Mode' from the main menu.\n"
        prompt += "\nWhich mode would you like to use? (1-3)"

        return prompt

    def _format_main_menu(self) -> str:
        """Format main menu as user-friendly prompt"""
        menu = self.show_main_menu()

        prompt = f"# {menu['title']}\n\n"
        prompt += f"**{menu['subtitle']}**\n\n"

        # Show current mode indicator
        mode_icons = {
            InteractionMode.ONE_SHOT: "⚡",
            InteractionMode.DIALOG: "💬",
            InteractionMode.HYBRID: "🔄"
        }
        mode_icon = mode_icons.get(self.state.interaction_mode, "")
        prompt += f"**Mode:** {mode_icon} {self.state.interaction_mode.value.replace('_', ' ').title()}\n\n"

        prompt += "What would you like to do?\n\n"

        for i, option in enumerate(menu['options'], 1):
            status_icon = "✓" if "✓" in option['status'] else "○"
            highlight = " **[RECOMMENDED]**" if option.get('highlight') else ""
            prompt += f"{i}. **{option['label']}** {status_icon}{highlight}\n"
            prompt += f"   {option['description']}\n"
            prompt += f"   Status: {option['status']}\n\n"

        return prompt

    def _format_document_analysis(self) -> str:
        """Format document analysis workflow"""
        workflow = self.handle_analyze_documents()
        return f"# {workflow['title']}\n\n[Interactive workflow - details omitted for brevity]"

    def _format_excel_refinement(self) -> str:
        """Format Excel refinement dialog"""
        refinement = self.handle_excel_refinement()

        prompt = f"# {refinement['title']}\n\n"
        prompt += f"Current Model: `{refinement['current_model']}`\n\n"
        prompt += f"{refinement['prompt']}\n\n"
        prompt += "**Refinement Options:**\n\n"

        for i, option in enumerate(refinement['dialog_options'], 1):
            prompt += f"{i}. **{option['label']}**\n"
            prompt += f"   {option['description']}\n\n"

        return prompt

    def _format_devils_advocate(self) -> str:
        """Format devil's advocate mode"""
        challenge = self.handle_devils_advocate()

        prompt = f"# {challenge['title']}\n\n"
        prompt += f"{challenge['description']}\n\n"
        prompt += "**Challenge Areas:**\n\n"

        for area in challenge['challenge_areas']:
            prompt += f"### {area['category']}\n"
            for ch in area['challenges']:
                prompt += f"- {ch}\n"
            prompt += "\n"

        prompt += "\n**How would you like to proceed?**\n\n"
        for i, option in enumerate(challenge['options'], 1):
            prompt += f"{i}. {option['label']}: {option['description']}\n"

        return prompt

    def _format_sensitivity_analysis(self) -> str:
        """Format sensitivity analysis options"""
        sensitivity = self.handle_sensitivity_analysis()

        prompt = f"# {sensitivity['title']}\n\n"
        prompt += f"{sensitivity['description']}\n\n"

        for analysis in sensitivity['analysis_types']:
            prompt += f"### {analysis['label']}\n"
            prompt += f"{analysis['description']}\n\n"

        return prompt


def example_usage():
    """Example of how the dialog system works"""

    # Initialize dialog for a deal
    dialog = FinancialAnalystDialog(deal_name="Project_Munich")

    # Show main menu
    print(dialog._format_main_menu())
    print("\n" + "="*60 + "\n")

    # Simulate completing document analysis
    dialog.state.analysis_completed['documents_analyzed'] = True
    dialog.state.current_valuation_version = "1.0"

    # Show updated menu
    print(dialog._format_main_menu())
    print("\n" + "="*60 + "\n")

    # Show devil's advocate mode
    print(dialog._format_devils_advocate())


if __name__ == "__main__":
    example_usage()
