from django.db import models


# Create your models here.

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
class HardDrive(models.Model):
    creationDate = models.DateField(auto_now_add=False, blank=False, null=False)  # required
    serialNumber = models.CharField(max_length=100, blank=False, null=False)  # required
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    modelNumber = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50, blank=False, null=False)  # required
    connectionPort = models.CharField(max_length=50, blank=False, null=False)  # required
    size = models.CharField(max_length=50, blank=False, null=False)  # required
    classification = models.CharField(max_length=50, choices=classification_choices,
                                      default='unclassified')  # required & default = unclassified
    classificationChangeJustification = models.CharField(max_length=50, choices=justifications_choices, default='Text')
    imageVersionID = models.CharField(max_length=50, blank=False, null=False)  # required & format = NNNN
    bootTestStatus = models.CharField(max_length=50, choices=boot_test_status_choices, default='Pass')
    bootTestExpirationDate = models.DateField(auto_now_add=False, blank=True, null=True)
    status = models.CharField(max_length=50, choices=hard_drive_status_choices, default='Available')
    hardDriveStatusChangeJustification = models.CharField(max_length=50, choices=justifications_choices, default='Text')
    dateIssued = models.DateField(auto_now_add=False, blank=False, null=False)  # required
    expectedReturnDate = models.DateField(auto_now_add=False, blank=False, null=False,
                                          default='needs to be Generate')  # need to do the calculation & required
    hardDriveReturnDateJustification = models.CharField(max_length=50, choices=justifications_choices, default='Text')
    actualReturnDate = models.DateField(auto_now_add=False, blank=False, null=False)  # required
    dateModified = models.DateField(auto_now=False, blank=False, null=False)  # required
