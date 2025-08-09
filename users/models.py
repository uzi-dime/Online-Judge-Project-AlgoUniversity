from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    # Profile Information
    bio = models.TextField(blank=True)
    avatar = models.URLField(max_length=500, blank=True, validators=[URLValidator()])
    institution = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Social Links
    github_profile = models.URLField(max_length=200, blank=True)
    linkedin_profile = models.URLField(max_length=200, blank=True)
    website = models.URLField(max_length=200, blank=True)
    
    # Programming Skills
    preferred_languages = models.JSONField(default=list, blank=True, help_text=_('List of preferred programming languages'))
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('BEGINNER', 'Beginner'),
            ('INTERMEDIATE', 'Intermediate'),
            ('ADVANCED', 'Advanced'),
            ('EXPERT', 'Expert')
        ],
        default='BEGINNER'
    )
    
    # Statistics
    problems_solved = models.PositiveIntegerField(default=0)
    total_submissions = models.PositiveIntegerField(default=0)
    successful_submissions = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=1200)  # Initial ELO rating
    contests_participated = models.PositiveIntegerField(default=0)
    
    # Signup Token
    signup_token = models.CharField(
        max_length=500,
        editable=True,
        unique=True,
        default='',
        null=True,
        blank=True,
        help_text=_('Signup token')
    )    
    # Preferences
    theme_preference = models.CharField(
        max_length=10,
        choices=[
            ('LIGHT', 'Light'),
            ('DARK', 'Dark'),
            ('SYSTEM', 'System')
        ],
        default='SYSTEM'
    )
    email_notifications = models.BooleanField(default=True)
    
    # Timestamps already included from AbstractUser:
    # date_joined
    # last_login
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def __str__(self):
        return self.username
        
    def get_success_rate(self):
        if self.total_submissions == 0:
            return 0
        return (self.successful_submissions / self.total_submissions) * 100
        
    def update_rating(self, new_rating):
        self.rating = new_rating
        self.save(update_fields=['rating'])
        
    def add_badge(self, badge_name):
        current_badges = self.badges
        if badge_name not in current_badges:
            current_badges.append(badge_name)
            self.badges = current_badges
            self.save(update_fields=['badges'])
            
    def increment_problems_solved(self):
        self.problems_solved += 1
        self.save(update_fields=['problems_solved'])
