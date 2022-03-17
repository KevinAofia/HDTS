from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Denise
class HardDrive(models.Model):
    # Denise
    hard_drive_status_choices = (
        ("Assigned", "Assigned"),
        ("Available", "Available"),
        ("End of Life", "End of Life"),
        ("Master Clone", "Master Clone"),
        ("Pending Wipe", "Pending Wipe"),
        ("Destroyed", "Destroyed"),
        ("Lost", "Lost"),
        ("Overdue", "Overdue"),
        ("Picked Up", "Picked Up"),
        ("Returned", "Returned"),
        ("Pending Change", "Pending Change"),
    )
    # Denise
    justifications_choices = [
        ("Text", "Text"),
        ("File Attachment", "File Attachment"),
    ]
    # Denise
    classification_choices = (
        ("Unclassified", "Unclassified"),
        ("Classified", "Classified"),
    )
    # Denise
    boot_test_status_choices = (
        ("Pass", "Pass"),
        ("Fail", "Fail"),
    )
    size_choices = (
        ("16GB", "16GB"),
        ("32GB", "32GB"),
        ("64GB", "64GB"),
        ("128GB", "128GB"),
        ("256GB", "256GB"),
        ("500GB", "500GB"),
        ("1TB", "1TB"),
        ("1.5TB", "1.5TB"),
        ("2TB", "2TB"),
        ("4TB", "4TB"),
        ("6TB", "6TB"),
        ("8TB", "8TB"),
        ("12TB", "12TB"),
        ("Other", "Other"),
    )
    creation_date = models.DateField(auto_now_add=False, blank=False, null=False)  # required
    serial_number = models.CharField(max_length=100, blank=False, null=False)  # required
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    model_number = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50, blank=False, null=False)  # required
    connection_port = models.CharField(max_length=50, blank=False, null=False)  # required
    size = models.CharField(max_length=50, choices=size_choices, blank=False, null=False)  # required
    classification = models.CharField(max_length=50, choices=classification_choices)  # required
    classification_change_justification = models.CharField(max_length=50, choices=justifications_choices,
                                                           default='Text')
    image_version_ID = models.CharField(max_length=50, blank=False, null=False)  # required
    boot_test_status = models.CharField(max_length=50, choices=boot_test_status_choices, default='Pass')
    boot_test_expiration_date = models.DateField(auto_now_add=False, blank=True, null=True)
    status = models.CharField(max_length=50, choices=hard_drive_status_choices, default='Available')
    hard_drive_status_change_justification = models.CharField(max_length=50, choices=justifications_choices,
                                                              default='Text')
    date_issued = models.DateField(auto_now_add=False, blank=False, null=False)  # required
    expected_return_date = models.DateField(auto_now_add=False, blank=False, null=False)  # required
    hard_drive_return_date_justification = models.CharField(max_length=50, choices=justifications_choices,
                                                            default='Text')
    actual_return_date = models.DateField(auto_now_add=False, blank=False, null=False)  # required
    date_modified = models.DateField(auto_now=False, blank=False, null=False)  # required

    def __str__(self):  # uncomment to see default name in /admin
        details = (str(self.serial_number), str(self.status))
        return " ".join(details)


# Denise
class Requester(models.Model):
    # at the moment we can delete the relationship with other models for testing purposes
    # a user can be one requester, a requester can be one user
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # Denise
    requester_status_choices = (
        ("Good Standing", "Good Standing"),
        ("Delinquent", "Delinquent"),
        ("Disabled", "Disabled"),
        ("Archived", "Archived"),
    )
    first_name = models.CharField(max_length=100)  # required
    last_name = models.CharField(max_length=100)  # required
    email = models.EmailField(max_length=254,null=True)  # required
    username = models.CharField(max_length=50)  # required
    password = models.CharField(max_length=50)  # required
    direct_supervisor_email = models.EmailField(max_length=254,null=True)  # required
    branch_chief_email = models.EmailField(max_length=254,null=True)  # required
    requester_status = models.CharField(max_length=50, choices=requester_status_choices,
                                        default=requester_status_choices[0][0])  # required
    def __str__(self):
        full_name = (str(self.first_name), str(self.last_name))
        return " ".join(full_name)


# Denise
class Maintainer(models.Model):
    # at the moment we can delete the relationship with other models for testing purposes
    # a user can be one maintainer, a maintainer can be one user
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    # Denise
    maintainer_status_choices = (
        ("Active", "Active"),
        ("Disabled", "Disabled"),
        ("Archived", "Archived"),
    )
    first_name = models.CharField(max_length=100)  # required
    last_name = models.CharField(max_length=100)  # required
    email = models.EmailField(max_length=254)  # required
    username = models.CharField(max_length=50)  # required
    password = models.CharField(max_length=50)  # required
    maintainer_status = models.CharField(max_length=50, choices=maintainer_status_choices,
                                         default=maintainer_status_choices[0][0])  # required

    def __str__(self):  # uncomment to see default name in /admin
        full_name = (str(self.first_name), str(self.last_name))
        return " ".join(full_name)


# Denise
class Auditor(models.Model):
    # at the moment we can delete the relationship with other models for testing purposes
    # a user can be one auditor, a auditor can be one user
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    # Denise
    auditor_status_choices = (
        ("Authorized", "Authorized"),
        ("Unauthorized", "Unauthorized"),
        ("Archived", "Archived"),
    )
    first_name = models.CharField(max_length=100)  # required
    last_name = models.CharField(max_length=100)  # required
    email = models.EmailField(max_length=254)  # required
    username = models.CharField(max_length=50)  # required
    password = models.CharField(max_length=50)  # required
    auditor_status = models.CharField(max_length=50, choices=auditor_status_choices,
                                      default=auditor_status_choices[0][0])  # required

    def __str__(self):  # uncomment to see default name in /admin
        full_name = (str(self.first_name), str(self.last_name))
        return " ".join(full_name)


# Miriam
class Event(models.Model):
    # Denise
    status_choices = (
        ("Pending Request Approval", "Pending Request Approval"),
        ("Upcoming", "Upcoming"),
        ("Ongoing", "Ongoing"),
        ("Past", "Past"),
        ("Cancelled", "Cancelled"),
    )
    lead_choices = (
        ("none ", "none"),
    )
    duration_choices = (
        ("10 days", "10 days"),
        ("20 days", "20 days"),
        ("30 days", "30 days"),
        ("40 days", "40 days"),
        ("50 days", "50 days"),
        ("60 days", "60 days"),
    )
    type_choices = (
        ("CVPA", "CVPA"),
        ("VoF", "VoF"),
        ("CVI", "CVI"),
        ("PMR", "PMR"),
        ("Cyber Resilience", "Cyber Resilience"),
        ("Individual Project", "Individual Project"),
        ("Research Project", "Research Project"),
        ("System Acceptance", "System Acceptance"),
        ("Other", "Other"),
    )
    name = models.CharField(max_length=254)  # required
    description = models.CharField(max_length=254)  # could be file attachment
    location = models.CharField(max_length=254)
    lead = models.CharField(max_length=254, choices=lead_choices)
    participants = models.CharField(max_length=254)
    type = models.CharField(max_length=254, choices=type_choices)  # required IT IS STILL PENDING
    duration = models.CharField(max_length=254, choices=duration_choices)  # required
    status = models.CharField(max_length=254, choices=status_choices)  # required
    start_date = models.DateField(max_length=254)  # required
    end_date = models.DateField(max_length=254)  # required

    def __str__(self):  # uncomment to see default name in /admin
        details = (str(self.name), str(self.lead))
        return " ".join(details)


# Jacob and Bryant
class Request(models.Model):
    # request will stay in system if Requester is deleting for the moment
    requester = models.ForeignKey(Requester, null=True, on_delete=models.SET_NULL)
    # Denise
    status_choices = (
        ("Pending Approval", "Pending Approval"),
        ("Under Review", "Under Review"),
        ("Approved", "Approved"),
        ("Denied", "Denied"),
        ("Cancelled", "Cancelled"),
        ("Completed", "Completed"),
    )
    receipt_number = models.CharField(max_length=50, blank=False, null=False)  # required
    status = models.CharField(max_length=50, choices=status_choices, blank=False, null=False)  # required
    creation_date = models.DateField(max_length=254)  # required
    data_of_last_modification = models.DateField(max_length=254)  # required
    need_hard_drives_by_date = models.DateField(max_length=254)  # required
    number_of_classified_hard_drives_needed = models.PositiveIntegerField(default=0)  # required
    number_of_unclassified_hardDrives_needed = models.PositiveIntegerField(default=0)  # required
    comment = models.CharField(max_length=1000)

    def __str__(self):  # uncomment to see default name in /admin
        details = (str(self.receipt_number), str(self.status))
        return " ".join(details)
