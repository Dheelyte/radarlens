from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='chat_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='chat_receiver', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sender.name} & {self.receiver.name}'

    def last_message(self):
        messages = Message.objects.filter(chat=self)
        if messages:
            last_message = messages.last()
        return last_message

    def last_message_seen(self):
        messages = Message.objects.filter(chat=self)
        if messages:
            last_message = messages.last()
            return last_message.seen

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, related_name='message_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='message_receiver', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.id
