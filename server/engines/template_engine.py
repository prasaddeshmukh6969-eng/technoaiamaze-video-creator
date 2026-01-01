"""
Template Engine for Pre-made Video Templates
Renders template variables and manages template library
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path

class TemplateEngine:
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.templates_cache = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load all JSON templates from templates directory"""
        if not self.templates_dir.exists():
            return
        
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                    template_id = template_data.get('id')
                    if template_id:
                        self.templates_cache[template_id] = template_data
            except Exception as e:
                print(f"Error loading template {template_file}: {e}")
    
    def get_template(self, template_id: str) -> Optional[Dict]:
        """Get template by ID"""
        return self.templates_cache.get(template_id)
    
    def list_templates(self, category: Optional[str] = None) -> List[Dict]:
        """List all available templates, optionally filtered by category"""
        templates = list(self.templates_cache.values())
        if category:
            templates = [t for t in templates if t.get('category') == category]
        return templates
    
    def render_script(self, template_id: str, variables: Dict[str, str]) -> str:
        """
        Render template script with provided variables
        
        Args:
            template_id: ID of template to use
            variables: Dictionary of {variable_key: value}
        
        Returns:
            Rendered script with variables replaced
        """
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        script_template = template.get('script_template', '')
        
        # Replace all variables
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            script_template = script_template.replace(placeholder, str(value))
        
        return script_template
    
    def validate_variables(self, template_id: str, variables: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Validate that all required variables are provided
        
        Returns:
            Dictionary with 'missing' and 'invalid' lists
        """
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        required_vars = [
            var['key'] for var in template.get('variables', [])
            if var.get('required', False)
        ]
        
        missing = [var for var in required_vars if var not in variables]
        
        return {
            'missing': missing,
            'invalid': []
        }
