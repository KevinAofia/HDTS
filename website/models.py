from django.db import models


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
    creationDate = models.DateField(auto_now_add=False, blank=False, null=False)  # required
    serialNumber = models.CharField(max_length=100, blank=False, null=False)  # required
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    modelNumber = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=50, blank=False, null=False)  # required
    connectionPort = models.CharField(max_length=50, blank=False, null=False)  # required
    size = models.CharField(max_length=50, choices=size_choices, blank=False, null=False)  # required
    classification = models.CharField(max_length=50, choices=classification_choices)  # required
    classificationChangeJustification = models.CharField(max_length=50, choices=justifications_choices, default='Text')
    imageVersionID = models.CharField(max_length=50, blank=False, null=False)  # required
    bootTestStatus = models.CharField(max_length=50, choices=boot_test_status_choices, default='Pass')
    bootTestExpirationDate = models.DateField(auto_now_add=False, blank=True, null=True)
    status = models.CharField(max_length=50, choices=hard_drive_status_choices, default='Available')
    hardDriveStatusChangeJustification = models.CharField(max_length=50, choices=justifications_choices, default='Text')
    dateIssued = models.DateField(auto_now_add=False, blank=False, null=False)  # required
    expectedReturnDate = models.DateField(auto_now_add=False, blank=False, null=False)  # required
    hardDriveReturnDateJustification = models.CharField(max_length=50, choices=justifications_choices, default='Text')
    actualReturnDate = models.DateField(auto_now_add=False, blank=False, null=False)  # required
    dateModified = models.DateField(auto_now=False, blank=False, null=False)  # required

    def __str__(self):  # uncomment to see default name in /admin
        details = (str(self.serialNumber), str(self.status))
        return " ".join(details)


# Denise
class Requester(models.Model):
    # Denise
    requester_status_choices = (
        ("Good Standing", "Good Standing"),
        ("Delinquent", "Delinquent"),
        ("Disabled", "Disabled"),
        ("Archived", "Archived"),
    )
    firstName = models.CharField(max_length=100)  # required
    lastName = models.CharField(max_length=100)  # required
    email = models.EmailField(max_length=254)  # required
    username = models.CharField(max_length=50)  # required
    password = models.CharField(max_length=50)  # required
    directSupervisorEmail = models.EmailField(max_length=254)  # required
    branchChiefEmail = models.EmailField(max_length=254)  # required
    requesterStatus = requester_status_choices  # required

    def __str__(self):  # uncomment to see default name in /admin
        full_name = (str(self.firstName), str(self.lastName))
        return " ".join(full_name)


# Denise
class Maintainer(models.Model):
    # Denise
    maintainer_status_choices = (
        ("Active", "Active"),
        ("Disabled", "Disabled"),
        ("Archived", "Archived"),
    )
    firstName = models.CharField(max_length=100)  # required
    lastName = models.CharField(max_length=100)  # required
    email = models.EmailField(max_length=254)  # required
    username = models.CharField(max_length=50)  # required
    password = models.CharField(max_length=50)  # required
    maintainerStatus = maintainer_status_choices  # required

    def __str__(self):  # uncomment to see default name in /admin
        full_name = (str(self.firstName), str(self.lastName))
        return " ".join(full_name)


# Denise
class Auditor(models.Model):
    # Denise
    auditor_status_choices = (
        ("authorized", "authorized"),
        ("unauthorized", "unauthorized"),
        ("Archived", "Archived"),
    )
    firstName = models.CharField(max_length=100)  # required
    lastName = models.CharField(max_length=100)  # required
    email = models.EmailField(max_length=254)  # required
    username = models.CharField(max_length=50)  # required
    password = models.CharField(max_length=50)  # required
    auditorStatus = auditor_status_choices  # required

    def __str__(self):  # uncomment to see default name in /admin
        full_name = (str(self.firstName), str(self.lastName))
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
    startDate = models.DateField(max_length=254)  # required
    endDate = models.DateField(max_length=254)  # required

    def __str__(self):  # uncomment to see default name in /admin
        details = (str(self.name), str(self.status))
        return " ".join(details)


# Jacob and Bryant
class Request(models.Model):
    receiptNumber = models.CharField(max_length=50, blank=False, null=False)  # required
    status = models.CharField(max_length=50, blank=False, null=False)  # required
    creationDate = models.CharField(max_length=50, blank=False, null=False)  # required
    dataOfLastModification = models.CharField(max_length=50, blank=False, null=False)  # required
    needHardDrivesByDate = models.CharField(max_length=50, blank=False, null=False)  # required
    numberOfClassifiedHardDrivesNeeded = models.CharField(max_length=50, blank=False, null=False)  # required
    numberOfUnclassifiedHardDrivesNeeded = models.CharField(max_length=50, blank=False, null=False)  # required
    comment = models.CharField(max_length=1000)

    def __str__(self):  # uncomment to see default name in /admin
        details = (str(self.receiptNumber), str(self.status))
        return " ".join(details)
