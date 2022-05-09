from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

# Kevin Configuration models
################################################################
class RequestStatusChoice(models.Model):
    choice = models.CharField(max_length=300)

    def __str__(self):
        return self.choice


class RequesterStatusChoice(models.Model):
    choice = models.CharField(max_length=300)

    def __str__(self):
        return self.choice
class MaintainerStatusChoice(models.Model):
    choice = models.CharField(max_length=300)

    def __str__(self):
        return self.choice
class AuditorStatusChoice(models.Model):
    choice = models.CharField(max_length=300)

    def __str__(self):
        return self.choice
class EventStatusChoice(models.Model):
    choice = models.CharField(max_length=300)

    def __str__(self):
        return self.choice
class EventDurationChoice(models.Model):
    choice = models.CharField(max_length=300)

    def __str__(self):
        return self.choice
class EventTypeChoice(models.Model):
    choice = models.CharField(max_length=300)

    def __str__(self):
        return self.choice
class HardDriveStatusChoice(models.Model):
    choice = models.CharField(max_length=300)

    def __str__(self):
        return self.choice
class HardDriveClassificationChoice(models.Model):
    choice = models.CharField(max_length=300)

    def __str__(self):
        return self.choice
class HardDriveBootTestStatusChoice(models.Model):
    choice = models.CharField(max_length=300)

    def __str__(self):
        return self.choice
class HardDriveSizeChoice(models.Model):
    choice = models.CharField(max_length=300)

    def __str__(self):
        return self.choice
################################################################

# Kevin
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg')
    first_name = models.CharField(max_length=100)  # required
    last_name = models.CharField(max_length=100)  # required
    email = models.EmailField(max_length=254)  # required
    direct_supervisor_email = models.EmailField(max_length=254)  # required
    branch_chief_email = models.EmailField(max_length=254)  # required
    requester_status = models.ForeignKey(RequesterStatusChoice, blank=True, null=True, on_delete=models.SET_NULL)  # required
    maintainer_status = models.ForeignKey(MaintainerStatusChoice, blank=True, null=True, on_delete=models.SET_NULL)  # required
    auditor_status = models.ForeignKey(AuditorStatusChoice, blank=True, null=True, on_delete=models.SET_NULL)  # required

    def __str__(self):
        full_name = (str(self.first_name), str(self.last_name),str(self.id))
        return " ".join(full_name)


# Denise
class HardDrive(models.Model):
    # Denise
    creation_date = models.DateField(auto_now_add=True)  # required
    serial_number = models.CharField(max_length=100, unique=True)  # required
    manufacturer = models.CharField(max_length=100)  # required
    model_number = models.CharField(max_length=100)  # required
    type = models.CharField(max_length=50)  # required
    connection_port = models.CharField(max_length=50)  # required
    size = models.ForeignKey(HardDriveSizeChoice, blank=True, null=True, on_delete=models.SET_NULL)  # required
    classification = models.ForeignKey(HardDriveClassificationChoice, blank=True, null=True, on_delete=models.SET_NULL)  # required
    boot_test_status = models.ForeignKey(HardDriveBootTestStatusChoice, blank=True, null=True, on_delete=models.SET_NULL)  # required
    status = models.ForeignKey(HardDriveStatusChoice, blank=True, null=True, on_delete=models.SET_NULL)  # required
    classification_change_justification = models.TextField(blank=True, null=True)
    image_version_ID = models.CharField(max_length=10, blank=True, null=True)
    boot_test_expiration_date = models.DateField(blank=True, null=True)
    hard_drive_status_change_justification = models.TextField(blank=True, null=True)
    date_issued = models.DateField(blank=True, null=True)
    expected_return_date = models.DateField(blank=True, null=True)
    hard_drive_return_date_justification = models.TextField(blank=True, null=True)
    actual_return_date = models.DateField(blank=True, null=True)
    date_modified = models.DateField(auto_now=True)  # required

    def __str__(self):  # uncomment to see default name in /admin
        details = (str(self.serial_number), str(self.status))
        return " ".join(details)


# Miriam
class Event(models.Model):
    # Denise
    name = models.CharField(max_length=100, unique=True)  # required
    description = models.TextField()  #
    location = models.CharField(max_length=254)
    lead = models.CharField(max_length=254, blank=True, null=True)
    participants = models.TextField(max_length=500)
    type = models.ForeignKey(EventTypeChoice, blank=True, null=True, on_delete=models.SET_NULL)  # required
    duration = models.ForeignKey(EventDurationChoice, blank=True, null=True, on_delete=models.SET_NULL)  # required
    status = models.ForeignKey(EventStatusChoice, blank=True, null=True, on_delete=models.SET_NULL)  # required
    start_date = models.DateField(max_length=254, null=True)  # required
    end_date = models.DateField(max_length=254, null=True)  # required

    def __str__(self):  # uncomment to see default name in /admin
        # details = (str(self.lead), str(self.name), str(self.status))
        # return " ".join(details)
        return str(self.name)


# Jacob and Bryant


class Request(models.Model):
    # user is tied to a one unique user account
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # a user can submit a request for another requester that is not themselves
    requester = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    event = models.OneToOneField(Event, null=True, on_delete=models.CASCADE)
    hard_drive = models.ManyToManyField(HardDrive)
    status = models.ForeignKey(RequestStatusChoice, blank=True, null=True, on_delete=models.SET_NULL)  # required
    request_number = models.CharField(max_length=22)  # MMDDYYYY/requesterfirstinitial_requesterlastinitial/devcomHHMMSS
    creation_date = models.DateField(auto_now_add=True)  # required
    date_of_last_modification = models.DateField(auto_now=True)  # required
    pickup_date = models.DateField(max_length=254, blank=False, null=True)  # required
    number_of_classified_hard_drives_needed = models.PositiveIntegerField(default=0)  # required
    number_of_unclassified_hard_drives_needed = models.PositiveIntegerField(default=0)  # required
    comment = models.TextField(blank=True, null=True)

    def __str__(self):  # uncomment to see default name in /admin
        details = (str(self.requester), str(self.request_number), str(self.status))
        return " ".join(details)


#Laura
class Log(models.Model):
    # (blank=False, null=False) means that it is required
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    timestamp = models.DateField()
    action_performed = models.CharField(max_length=254)

    def __str__(self):  # uncomment to see default name in /admin
        details = (str(self.user), str(self.timestamp), str(self.action_performed))
        return " ".join(details)


#Denise
class Amendment(models.Model):
    #Denise
    amendment_Status = (
        #(Actual Value, human-readable name)
        ("Created","Created"),
        ("Approved","Approved"),
        ("Denied","Denied"),
    )

    # (blank=False, null=False) means that it is required
    user = models.CharField(max_length=100, blank=False, null=False)
    amendment_submission_date = models.DateField()
    amendment_decison_date = models.DateField(max_length=254, null=True)
    # amendment_description = models.FileField(upload_to=None, max_length=100)# double check & required
    # amendment_description1 = models.CharField(max_length=100, blank=True, null=True)
    amendment_description = models.TextField() # double check
    # decision_date = models.DateField(max_length=254, blank=False, null=True) 
    status = amendment_Status 
    comment = models.TextField() # double check

    def __str__(self):  # uncomment to see default name in /admin
        details = (str(self.amendment_submission_date), str(self.status))
        return " ".join(details)
