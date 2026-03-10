"""
VentureLens AI - Analysis Forms
"""

from django import forms


class StartupIdeaForm(forms.Form):
    """Form for submitting a startup idea for analysis."""

    startup_idea = forms.CharField(
        label='Your Startup Idea',
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': (
                'Describe your startup idea in detail...\n\n'
                'Example: "An AI-powered platform that helps small restaurants '
                'reduce food waste by predicting demand using machine learning '
                'and connecting surplus food with local food banks."'
            ),
            'class': 'idea-textarea',
            'maxlength': 2000,
        }),
        min_length=50,
        max_length=2000,
        error_messages={
            'min_length': 'Please describe your idea in at least 50 characters.',
            'max_length': 'Please keep your description under 2000 characters.',
            'required': 'Please enter your startup idea.',
        }
    )

    def clean_startup_idea(self):
        idea = self.cleaned_data['startup_idea'].strip()
        # Basic quality check
        if len(idea.split()) < 8:
            raise forms.ValidationError(
                "Please provide a more detailed description (at least 8 words)."
            )
        return idea
