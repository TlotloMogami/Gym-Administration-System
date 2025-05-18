from django.db import models

class Trainer(models.Model):
    FITNESS_PROGRAM_CHOICES = [
        ('Yoga', 'Yoga'),
        ('Zumba', 'Zumba'),
        ('Pilates', 'Pilates'),
        ('Weight Training', 'Weight Training'),
        ('CrossFit', 'CrossFit'),
    ]
    
    name = models.CharField(max_length=100)
    fitness_programs = models.CharField(
        max_length=255,
        default='Yoga',
        help_text="Comma-separated list of programs this trainer can lead"
    )
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    hired_date = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def get_programs_list(self):
        return [p.strip() for p in self.fitness_programs.split(',')]
    
    def __str__(self):
        return self.name

class Member(models.Model):
    FITNESS_PROGRAM_CHOICES = Trainer.FITNESS_PROGRAM_CHOICES  # Reuse the same choices
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    MEMBERSHIP_CHOICES = [('Basic', 'Basic'), ('Premium', 'Premium')]
    STATUS_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive')]
    
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    fitness_program = models.CharField(
        max_length=20, 
        choices=FITNESS_PROGRAM_CHOICES, 
        default='Yoga'
    )
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Inactive')
    joined = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    assigned_trainer = models.ForeignKey(
        Trainer, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'status': 'Active'}
    )

    def __str__(self):
        return self.name

class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    subscription_type = models.CharField(max_length=10)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Payment #{self.id} for {self.member.name}"

class Venue(models.Model):
    ROOM_CHOICES = [
        ('Room 101', 'Room 101'),
        ('Room 102', 'Room 102'),
        ('Room 201', 'Room 201'),
        ('Room 202', 'Room 202'),
        ('Main Hall', 'Main Hall'),
    ]

    name = models.CharField(max_length=100, choices=ROOM_CHOICES, unique=True)

    def capacity(self):
        capacities = {
            'Room 101': 40,
            'Room 102': 30,
            'Room 201': 50,
            'Room 202': 35,
            'Main Hall': 100,
        }
        return capacities.get(self.name, 0)

    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity()})"

class ScheduledClass(models.Model):
    fitness_program = models.CharField(
        max_length=50,
        choices=Trainer.FITNESS_PROGRAM_CHOICES
    )
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        limit_choices_to={'status': 'Active'}
    )
    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.fitness_program} - {self.trainer.name} on {self.date} at {self.time} in {self.venue.name}"
