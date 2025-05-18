from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from .models import Member,Trainer, Venue
from django.views.decorators.csrf import csrf_exempt, csrf_protect  
import json
from collections import OrderedDict
from .models import ScheduledClass
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods


# Authentication Views
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            return render(request, 'loginPage.html', {'error': 'Invalid username or password.'})

    return render(request, 'loginPage.html')

# Dashboard Views
@login_required
def dashboard(request):
    return render(request, 'base.html', {'page_title': 'Dashboard'})

# Member Management Views
@login_required
def members(request):
    members = Member.objects.all()
    return render(request, 'members.html', {
        'members': members,
        'page_title': 'Members'
    })

@login_required
def add_member(request):
    if request.method == 'POST':
        data = request.POST
        member = Member.objects.create(
            name=data.get('name'),
            gender=data.get('gender'),
            dob=data.get('dob'),
            membership_type=data.get('membership_type', 'Basic'),
            status='Inactive',  # Force inactive status for new members
            joined=data.get('joined'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address')
        )
        return JsonResponse({'success': True, 'member_id': member.id})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@login_required
@csrf_exempt  # Temporarily add this for testing, remove in production
def edit_member(request, member_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            member = Member.objects.get(id=member_id)
            
            # Update member fields
            member.name = data.get('name', member.name)
            member.gender = data.get('gender', member.gender)
            member.dob = data.get('dob', member.dob)
            member.membership_type = data.get('membership_type', member.membership_type)
            member.status = data.get('status', member.status)
            member.joined = data.get('joined', member.joined)
            member.email = data.get('email', member.email)
            member.phone = data.get('phone', member.phone)
            member.address = data.get('address', member.address)
            member.fitness_program = data.get('fitness_program', member.fitness_program)
            
            member.save()
            
            return JsonResponse({'success': True, 'message': 'Member updated successfully'})
        except Member.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Member not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

# Payment Views
@login_required
def payments(request):
    return render(request, 'payments.html', {'page_title': 'Payments'})

# Class Scheduling Views
@login_required
def class_scheduling(request):
    venues = Venue.objects.all()
    trainers = Trainer.objects.all()
    scheduled_classes = ScheduledClass.objects.select_related("venue", "trainer")

    # Count members per program (adjust if your model differs)
    members_count_map = (
        ScheduledClass.objects
        .values('fitness_program')
        .annotate(count=Count('id'))  # Replace with actual Member-Class relationship if exists
    )
    # Convert to dict: {'yoga': 3, 'zumba': 2, ...}
    members_dict = {entry['fitness_program']: entry['count'] for entry in members_count_map}

    return render(request, 'class_scheduling.html', {
        'venues': venues,
        'trainers': trainers,
        'scheduled_classes': scheduled_classes,
        'members_count_map': members_dict,
        'page_title': 'Schedule a Class'
    })

# Report Views
@login_required
def reports(request):
    """Render the reports dashboard template"""
    return render(request, 'reports.html', {'page_title': 'Reports'})

@login_required
def reports_api(request):
    """API endpoint for chart data"""

    # Chart 1: Count members per membership type
    membership_data = Member.objects.values('membership_type').annotate(count=Count('id'))
    count_map = {'Basic': 0, 'Premium': 0}
    for entry in membership_data:
        m_type = entry['membership_type']
        if m_type in count_map:
            count_map[m_type] = entry['count']

    # Chart 2: Count members per fitness program
    program_data = Member.objects.values('fitness_program').annotate(count=Count('id'))

    # Optional: ensure consistent order (for matching colors, etc.)
    program_order = ['Yoga', 'Zumba', 'Pilates', 'Weight Training', 'CrossFit']
    program_count_map = OrderedDict((prog, 0) for prog in program_order)
    for entry in program_data:
        prog = entry['fitness_program']
        if prog in program_count_map:
            program_count_map[prog] = entry['count']

    return JsonResponse({
        # Chart 1
        'labels': ['Basic', 'Premium'],
        'data': [count_map['Basic'], count_map['Premium']],

        # Chart 2
        'class_labels': list(program_count_map.keys()),
        'class_data': list(program_count_map.values()),
    })

@login_required
@csrf_exempt
def delete_member(request, member_id):
    if request.method == 'POST':
        try:
            member = Member.objects.get(pk=member_id)
            member.delete()
            return JsonResponse({'success': True})
        except Member.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Member not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
# Display all trainers
def trainers(request):
    trainer_list = Trainer.objects.all()
    return render(request, 'trainers.html', {
        'trainers': trainer_list,
        'page_title': 'Trainers'
    })

# Add new trainer
def add_trainer(request):
    if request.method == 'POST':
        # Let Django handle the ID automatically
        Trainer.objects.create(
            name=request.POST['name'],
            fitness_programs=request.POST['fitness_program'],
            status=request.POST['status'],
            hired_date=request.POST['hired_date'],
            email=request.POST['email'],
            phone=request.POST['phone']
        )
        messages.success(request, 'Trainer added successfully.')
        return redirect('trainers')


@login_required
@csrf_exempt  # Remove if you implement CSRF tokens properly in frontend
def edit_trainer(request, id):
    trainer = get_object_or_404(Trainer, pk=id)

    if request.method == 'POST':
        data = request.POST

        trainer.name = data.get('name', trainer.name)
        trainer.fitness_programs = data.get('fitness_program', trainer.fitness_programs)
        trainer.status = data.get('status', trainer.status)
        trainer.hired_date = data.get('hired_date', trainer.hired_date)
        trainer.email = data.get('email', trainer.email)
        trainer.phone = data.get('phone', trainer.phone)

        try:
            trainer.save()
            return redirect('trainer_list')  # ✅ Make sure this is the correct URL name
        except Exception as e:
            # Optionally pass error to the template
            return render(request, 'trainers.html', {
                'error': f"Error saving trainer: {e}",
                'trainers': Trainer.objects.all()
            })

    # fallback
    return redirect('trainer_list')

# Delete trainer
def delete_trainer(request, id):
    trainer = get_object_or_404(Trainer, pk=id)
    if request.method == 'POST':
        trainer.delete()
        messages.success(request, 'Trainer deleted successfully.')
        return redirect('trainers')

@login_required
@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            member_id = data.get('memberId')
            
            try:
                member = Member.objects.get(id=member_id)
                
                # Validate payment amount
                amount = float(data.get('amount', 0))
                if amount <= 0:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid payment amount'
                    }, status=400)
                
                # Validate subscription type
                subscription_type = data.get('subscriptionType')
                if subscription_type not in dict(Member.MEMBERSHIP_CHOICES).keys():
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid subscription type'
                    }, status=400)
                
                # Update member status and membership type
                member.status = 'Active'
                member.membership_type = subscription_type
                member.save()
                
                # Here you would typically:
                # 1. Create a Payment record
                # 2. Send email confirmation
                # 3. Log the transaction
                
                return JsonResponse({
                    'success': True,
                    'message': 'Payment processed and member activated',
                    'new_status': member.status,
                    'membership_type': member.membership_type
                })
                
            except Member.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Member not found'
                }, status=404)
                
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid amount format'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=400)


def scheduled_classes_view(request):
    scheduled_classes = ScheduledClass.objects.select_related('venue', 'trainer').all()
    
    # Count members per fitness program
    counts = Member.objects.values('fitness_program').annotate(count=Count('id'))
    members_count_map = {item['fitness_program']: item['count'] for item in counts}
    
    return render(request, 'scheduled_classes.html', {
        'scheduled_classes': scheduled_classes,
        'members_count_map': members_count_map,
    })

@login_required
@require_GET
def get_trainers_by_category(request):
    category = request.GET.get('category', '')
    if category:
        trainers = Trainer.objects.filter(fitness_programs__iexact=category).values('id', 'name')
        return JsonResponse(list(trainers), safe=False)
    return JsonResponse([], safe=False)

@login_required
@csrf_exempt
def schedule_class(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            trainer_id = data.get('trainer')
            fitness_program = data.get('category')
            date = data.get('date')
            time = data.get('time')
            duration = data.get('duration')
            venue_id = data.get('location')  # This is actually the venue ID

            # Ensure all required fields are provided
            if not all([trainer_id, fitness_program, date, time, duration, venue_id]):
                return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)

            # Get venue by ID
            venue = Venue.objects.get(id=venue_id)

            # Create ScheduledClass
            ScheduledClass.objects.create(
                trainer_id=trainer_id,
                venue=venue,
                fitness_program=fitness_program,
                date=date,
                time=time,
                duration=duration
            )

            return JsonResponse({'success': True, 'message': 'Class scheduled successfully'})
        except Venue.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Selected venue does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

from django.views.decorators.http import require_http_methods

from django.views.decorators.http import require_POST

@login_required
@require_POST
def delete_class(request, class_id):
    try:
        scheduled_class = ScheduledClass.objects.get(pk=class_id)
        scheduled_class.delete()
        return JsonResponse({'success': True, 'message': 'Class deleted successfully.'})
    except ScheduledClass.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Class not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
