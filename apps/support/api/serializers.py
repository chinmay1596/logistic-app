from rest_framework import serializers
from apps.support.models import Ticket, Chat, Documents


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Documents
        fields = ['files']


class TicketSerializer(serializers.ModelSerializer):
    files = serializers.ListField(required=False, write_only=True, child=serializers.FileField(
        allow_empty_file=False, use_url=False))

    class Meta:
        model = Ticket
        fields = ['id', 'customer', 'title', 'type_of_issue',
                  'description', 'generated_by', 'files']

    def create(self, validated_data):
        ticket = Ticket.objects.create(customer=validated_data['customer'], title=validated_data['title'], type_of_issue=validated_data[
                                       'type_of_issue'], description=validated_data['description'], generated_by=validated_data['generated_by'])

        if validated_data.get('files') != None:
            files_data = validated_data.pop('files')
            for file_data in files_data:
                doc = Documents.objects.create(files=file_data)
                ticket.documents.add(doc)

        return ticket


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['sender', 'receiver', 'message', 'file_upload']


class TicketDetailSerializer(serializers.ModelSerializer):
    chat_messages = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['customer', 'title', 'type_of_issue', 'description',
                  'generated_by', 'chat_messages', 'documents']

    def get_chat_messages(self, obj):
        chats = Chat.objects.filter(ticket=obj)
        message = ChatSerializer(chats, many=True).data
        return message
