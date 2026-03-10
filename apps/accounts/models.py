"""
VentureLens AI - Accounts Models
Custom User model with profile data.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Extended User model.
    Always use this instead of Django's default User.
    """
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    avatar_initial = models.CharField(max_length=2, blank=True)

    # Plan / subscription
    class Plan(models.TextChoices):
        FREE = 'free', 'Free'
        PRO = 'pro', 'Pro'

    plan = models.CharField(max_length=10, choices=Plan.choices, default=Plan.FREE)

    # Usage tracking
    analyses_today = models.IntegerField(default=0)
    last_analysis_date = models.DateField(null=True, blank=True)
    total_analyses = models.IntegerField(default=0)

    # Preferences
    language = models.CharField(
        max_length=5,
        default='en',
        choices=[('en', 'English'), ('id', 'Indonesia')],
    )

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Use email as login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Auto-generate avatar initial from name or email
        if self.full_name:
            self.avatar_initial = self.full_name[0].upper()
        elif self.email:
            self.avatar_initial = self.email[0].upper()
        super().save(*args, **kwargs)

    @property
    def display_name(self):
        return self.full_name or self.email.split('@')[0]

    def can_analyze(self, max_per_day: int) -> bool:
        """Check if user can run another analysis today."""
        today = timezone.now().date()
        if self.last_analysis_date != today:
            # Reset counter for new day
            self.analyses_today = 0
            self.last_analysis_date = today
            self.save(update_fields=['analyses_today', 'last_analysis_date'])
        return self.analyses_today < max_per_day

    def increment_analysis_count(self):
        """Call after a successful analysis."""
        today = timezone.now().date()
        if self.last_analysis_date != today:
            self.analyses_today = 1
        else:
            self.analyses_today += 1
        self.last_analysis_date = today
        self.total_analyses += 1
        self.save(update_fields=['analyses_today', 'last_analysis_date', 'total_analyses'])

    @property
    def daily_limit(self):
        return 50 if self.plan == self.Plan.PRO else 10
