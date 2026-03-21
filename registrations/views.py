from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from .models import Team, TeamMember
import cloudinary.uploader

def home(request):
    return render(request, 'registrations/home.html')

def register(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                team_name = request.POST.get('team_name')
                team_size = int(request.POST.get('team_size'))
                payment_proof = request.FILES.get('payment_proof')
                utr_id = request.POST.get('utr_id')

                # Case-insensitive team name check
                if Team.objects.filter(team_name__iexact=team_name).exists():
                    messages.error(request, f"Team name '{team_name}' already exists! Please choose another one.")
                    return redirect('register')

                # Upload to Cloudinary manually to get the secure URL
                upload_result = cloudinary.uploader.upload(payment_proof)
                payment_proof_url = upload_result.get('secure_url')

                team = Team.objects.create(
                    team_name=team_name,
                    team_size=team_size,
                    payment_proof=payment_proof_url,
                    utr_id=utr_id
                )

                import re
                phone_pattern = re.compile(r'^[6-9]\d{9}$')
                college_code_pattern = re.compile(r'^[A-Z]+$')

                for i in range(1, team_size + 1):
                    phone_number = request.POST.get(f'member_phone_{i}')
                    college_code = request.POST.get(f'member_cc_{i}')

                    if not phone_pattern.match(phone_number):
                        messages.error(request, f"Invalid phone number for Member {i}. Must be 10 digits starting with 6-9.")
                        return redirect('register')
                    
                    if not college_code_pattern.match(college_code):
                        messages.error(request, f"Invalid college code for Member {i}. Must contain only capital letters.")
                        return redirect('register')

                    TeamMember.objects.create(
                        team=team,
                        name=request.POST.get(f'member_name_{i}'),
                        roll_no=request.POST.get(f'member_roll_{i}'),
                        college_code=request.POST.get(f'member_cc_{i}'),
                        college_name=request.POST.get(f'member_college_{i}'),
                        phone_number=phone_number,
                        email=request.POST.get(f'member_email_{i}'),
                        tshirt_size=request.POST.get(f'member_tshirt_{i}')
                    )
                
                messages.success(request, f"Registration successful for team {team_name}!")
                return redirect('success')
        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")
            return render(request, 'registrations/register.html')

    return render(request, 'registrations/register.html')

def success(request):
    return render(request, 'registrations/success.html')
