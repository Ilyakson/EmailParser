from django.db import models


class Account(models.Model):
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=10, default="New")

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.login


class IncomingMessage(models.Model):
    email = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="incoming_messages"
    )
    subject = models.CharField(max_length=255, null=True, blank=True)
    sender = models.CharField(max_length=255, null=True, blank=True)
    recipient = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    media_file = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Incoming Message"
        verbose_name_plural = "Incoming Messages"

    def __str__(self):
        return self.sender


class OutgoingMessage(models.Model):
    email = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="outgoing_messages"
    )
    subject = models.CharField(max_length=255, null=True, blank=True)
    sender = models.CharField(max_length=255, null=True, blank=True)
    recipient = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    media_file = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Outgoing Message"
        verbose_name_plural = "Outgoing Messages"

    def __str__(self):
        return self.subject
