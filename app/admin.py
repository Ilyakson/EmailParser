from django.contrib import admin
from .models import Account, IncomingMessage, OutgoingMessage


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["login", "status"]


@admin.register(IncomingMessage)
class IncomingMessageAdmin(admin.ModelAdmin):
    list_display = ["email", "subject", "sender", "recipient", "text", "media_file"]


@admin.register(OutgoingMessage)
class OutgoingMessageAdmin(admin.ModelAdmin):
    list_display = ["email", "subject", "sender", "recipient", "text", "media_file"]
