# 代码生成时间: 2025-10-16 21:18:17
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotData


# Define the Chatbot model to store conversation data
class ChatbotConversation(models.Model):
    user_input = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation {self.id}'


# Initialize the chatbot
chatbot = ChatBot('DjangoChatbot',
                   trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
                   storage_adapter='django_storage',
                   logic_adapters=[{'import_path': 'chatterbot.logic.BestMatch'}],
                   database='default')

# Train the chatbot with the ChatterBotCorpus
ChatbotData().train(chatbot)


# Define the view to handle chatbot conversation
class ChatbotView(View):
    """
    A view to handle chatbot conversation.
    It accepts user input and returns the bot's response.
    """
    def post(self, request, *args, **kwargs):
        try:
            user_input = request.POST.get('user_input', '')
            # Save the conversation to the database
            conversation = ChatbotConversation(user_input=user_input)
            conversation.save()
            
            # Generate the bot's response
            response = chatbot.get_response(user_input)
            # Save the bot's response to the database
            conversation.bot_response = str(response)
            conversation.save()
            
            # Return the bot's response as JSON
            return JsonResponse({'response': str(response)})
        except Exception as e:
            # Return an error message as JSON in case of exception
            return JsonResponse({'error': str(e)})


# Define the URL pattern for the chatbot view
urlpatterns = [
    path('chatbot/', ChatbotView.as_view(), name='chatbot'),
]
