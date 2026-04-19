from django.core.validators import RegexValidator
from django.db import models
from cloudinary.models import CloudinaryField

class Team(models.Model):
    team_name = models.CharField(max_length=100, unique=True)
    team_size = models.IntegerField()
    payment_proof = models.URLField(max_length=500, blank=True, null=True)
    utr_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name

class TeamMember(models.Model):
    TSHIRT_SIZES = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL'),
    ]

    phone_regex = RegexValidator(
        regex=r'^[6-9]\d{9}$',
        message="Phone number must be exactly 10 digits and start with 6-9."
    )
    
    college_code_regex = RegexValidator(
        regex=r'^[A-Z0-9]+$',
        message="College code must contain only capital letters and numbers."
    )
    
    team = models.ForeignKey(Team, related_name='members', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20)
    college_code = models.CharField(validators=[college_code_regex], max_length=20)
    college_name = models.CharField(max_length=200)
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    email = models.EmailField()
    tshirt_size = models.CharField(max_length=5, choices=TSHIRT_SIZES)

    def __str__(self):
        return f"{self.name} ({self.team.team_name})"
